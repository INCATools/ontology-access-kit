"""An OAK implementation that wraps Large Language Models."""

import json
import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Iterable, Iterator, List, Optional, Tuple

from sssom_schema import Mapping

from oaklib import BasicOntologyInterface
from oaklib.datamodels.obograph import DefinitionPropertyValue
from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.datamodels.validation_datamodel import (
    MappingValidationResult,
    ValidationConfiguration,
)
from oaklib.datamodels.vocabulary import HAS_DBXREF, SKOS_EXACT_MATCH
from oaklib.interfaces import (
    MappingProviderInterface,
    OboGraphInterface,
    SearchInterface,
    TextAnnotatorInterface,
    ValidatorInterface,
)
from oaklib.interfaces.ontology_generator_interface import OntologyGenerationInterface
from oaklib.interfaces.text_annotator_interface import TEXT
from oaklib.types import CURIE

if TYPE_CHECKING:
    import llm

__all__ = [
    "LLMImplementation",
]

logger = logging.getLogger(__name__)

MAPPING_VALIDATION_SYSTEM_PROMPT = """
Your job is to validate ontology mappings. I will provide
you with two entities (SUBJECT and OBJECT) and their proposed
relationship (PREDICATE).
Use your judgment to evaluate the scientific accuracy of the
mapping. Make use of the PREDICATE. For exact mappings, the
concepts should be identical, and you should note any subtle errors.
You may also suggest modifications to SUBJECT or OBJECT in order to
make the mapping more accurate. For close mappings you can be more lenient,
but the concepts should still be related. For example, a mapping between
a "digit" (in the sense of a finger) and a "digit" (in the sense of a number)
would always be wrong.
{prompt_info}

Return a JSON object with the following structure:

{{"problem": true | false,
 "confidence": "high" | "medium" | "low",
 "comment": "Your comment here",
 "subject_modifications": "<any modifications to the SUBJECT",
 "object_modifications": "<any modifications to the OBJECT",
 "predicate_modifications": "<any modifications to the PREDICATE"
}}

Always return valid JSON, and no more. Do not include additional verbiage before or
after the JSON object. Do not escape JSON keys.
"""


def _prefix(curie: CURIE) -> str:
    return curie.split(":")[0].lower()


@dataclass
class LLMImplementation(
    OboGraphInterface,
    TextAnnotatorInterface,
    SearchInterface,
    MappingProviderInterface,
    OntologyGenerationInterface,
    ValidatorInterface,
):
    """
    An Ontology Interface that wraps Large Language Models (LLM).

    This is a wrapper interface, it needs to wrap an existing adapter; e.g.

    >>> adaoter = get_adapter("llm:sqlite:obo:cl")

    """

    wrapped_adapter: TextAnnotatorInterface = None
    """A wrapped annotator used to ground NEs.
    """

    model_id: str = None
    """The ID of the LLM model to use. E.g gpt-4"""

    model: "llm.Model" = None
    """The LLM model to use."""

    default_model_id: str = "gpt-4-turbo"

    allow_direct_grounding: bool = False
    """The point of this implementation is to perform NER and delegate to a grounded."""

    max_recursion_depth: int = 0

    def __post_init__(self):
        slug = self.resource.slug
        if not slug:
            logging.warning("LLM implementation requires a slug for grounding")
        else:
            slug = slug.replace("llm:", "")
            # check for a slug that starts with curly braces {...}:<rest>
            # the part in the curly braces is the model_id
            matches = re.match(r"^\{(\S+)\}:(.*)$", slug)
            if matches:
                logger.info(f"Looks like a model_id is specified in {slug}")
                # extract the model id
                self.model_id = matches.group(1)
                slug = matches.group(2)
                logger.info(f"LLM implementation will use model: {self.model_id} // slug={slug}")
            logging.info(f"LLM implementation will use grounder: {slug}")
            from oaklib import get_adapter

            self.wrapped_adapter = get_adapter(slug)
        if self.model_id is not None:
            import llm

            self.model = llm.get_model(self.model_id)

    def entities(self, **kwargs) -> Iterator[CURIE]:
        """Return all entities in the ontology."""
        yield from self.wrapped_adapter.entities(**kwargs)

    def basic_search(self, *args, **kwargs) -> Iterator[CURIE]:
        if not isinstance(self.wrapped_adapter, SearchInterface):
            raise NotImplementedError(
                "LLM can only perform basic search on a wrapped adapter that supports it"
            )
        yield from self.wrapped_adapter.basic_search(*args, **kwargs)

    def descendants(
        self,
        *args,
        **kwargs,
    ) -> Iterable[CURIE]:
        if not isinstance(self.wrapped_adapter, OboGraphInterface):
            raise NotImplementedError(
                "LLM can only perform descendants search on a wrapped adapter that supports it"
            )
        yield from self.wrapped_adapter.descendants(*args, **kwargs)

    def sssom_mappings(self, *args, **kwargs) -> Iterable[Mapping]:
        if not isinstance(self.wrapped_adapter, MappingProviderInterface):
            raise NotImplementedError(
                "LLM can only provide mappings on a wrapped adapter that supports it"
            )
        yield from self.wrapped_adapter.sssom_mappings(*args, **kwargs)

    def annotate_text(
        self, text: TEXT, configuration: TextAnnotationConfiguration = None
    ) -> Iterator[TextAnnotation]:
        """
        Implement the TextAnnotatorInterface using an LLM.

        :param text:
        :param configuration:
        :return:
        """
        if not configuration:
            raise NotImplementedError("Missing text annotation configuration")
        if configuration.matches_whole_text:
            if not self.allow_direct_grounding:
                raise NotImplementedError("LLM does not support whole-text matching")
            else:
                logging.info("Delegating directly to grounder, bypassing LLM")
                yield from self.wrapped_adapter.annotate_text(text, configuration)
        else:
            yield from self._llm_annotate(text, configuration)

    def get_model(self):
        model = self.model
        if not self.model:
            # model_id = self.configuration.model or self.model_id
            model_id = self.model_id
            if not model_id:
                model_id = self.default_model_id
            import llm

            model = llm.get_model(model_id)
        return model

    def _llm_annotate(
        self,
        text: str,
        configuration: TextAnnotationConfiguration = None,
        depth=0,
    ) -> Iterator[TextAnnotation]:
        system_prompt = self._system_prompt(configuration)
        model = self.model
        if not self.model:
            model_id = configuration.model or self.model_id
            if not model_id:
                model_id = self.default_model_id
            import llm

            model = llm.get_model(model_id)
        response = model.prompt(text, system=system_prompt)
        logging.info(f"LLM response: {response}")
        terms = json.loads(response.text())

        grounder_configuration = TextAnnotationConfiguration(matches_whole_text=True)
        while terms:
            term_obj = terms.pop(0)
            term = term_obj["term"]
            category = term_obj["category"]
            ann = TextAnnotation(subject_label=term, object_categories=[category])
            matches = list(self.wrapped_adapter.annotate_text(term, grounder_configuration))
            if not matches:
                aliases = self._suggest_aliases(
                    term, model, configuration.categories, configuration
                )
                for alias in aliases:
                    matches = list(
                        self.wrapped_adapter.annotate_text(alias, grounder_configuration)
                    )
                    if matches:
                        break
                logging.info(f"Aliases={aliases}; matches={matches}")
                if not matches:
                    if " " in term and depth < self.max_recursion_depth:
                        logging.info(f"Recursing on {term}")
                        anns = list(self._llm_annotate(term, configuration, depth + 1))
                        logging.info(f"Results from recursion: on {term} => {anns}")
                        if any(ann.object_id for ann in anns):
                            for ann in anns:
                                # TODO: offset
                                ann.start = None
                                ann.end = None
                                yield ann
                            continue
            if matches:
                ann.object_id = matches[0].object_id
                ann.object_label = matches[0].object_label
            else:
                logging.info(f"LLM failed to ground {term} or its aliases")
            if term in text:
                ann.start = text.index(term)
                ann.end = ann.start + len(term)
            yield ann

    def _system_prompt(self, configuration: TextAnnotationConfiguration = None) -> str:
        categories = configuration.categories
        prompt = "Perform named entity recognition on the text, returning a list of terms. "
        prompt += "Terms can be compound containing multiple words. "
        prompt += (
            "Use noun phrases or terms representing entire concepts rather than multiple words. "
        )
        if configuration.sources:
            prompt += (
                f"Include terms that might be found in the following: {configuration.sources}. "
            )
        if categories:
            prompt += f"Include only terms that are of type {categories}. "
        prompt += """Return results as a JSON list:
                     [{"term:" "term1", "category": "category1"}, ... ]"""
        return prompt

    def _suggest_aliases(
        self,
        term: str,
        model: "llm.Model" = None,
        categories: List = None,
        configuration: TextAnnotationConfiguration = None,
    ) -> List[str]:
        logging.info(f"LLM aliasing term: {term}")
        prompt = "List exact synonyms for this term. "
        prompt += "Normalize the string to a form found in an ontology. "
        if configuration.sources:
            prompt += f"Valid ontologies: {configuration.sources}. "
        if categories:
            prompt += f"Valid categories: {categories}. "
        prompt += "You can split compound concepts into multiple terms."
        prompt += "Return as a semi-colon separate list of terms. "
        response = model.prompt(term, system=prompt).text()
        logging.info(f"LLM aliases[{term}] => {response}")
        return [x.strip() for x in response.split(";")]

    def generate_definitions(
        self, curies: List[CURIE], style_hints="", **kwargs
    ) -> Iterator[Tuple[CURIE, DefinitionPropertyValue]]:
        """Suggest definitions for the given curies.

        Wraps the LLM to suggest definitions for the given curies.

        To use on the command line:

        .. code-block:: bash

           runoak --stacktrace -i llm:sqlite:obo:uberon \
             generate-definitions finger toe --style-hints "write definitions in formal genus-differentia form"

        """
        wrapped_adapter = self.wrapped_adapter
        model = self.get_model()
        if not isinstance(wrapped_adapter, OboGraphInterface):
            raise NotImplementedError("LLM can only suggest definitions for OBO graphs")
        if style_hints is None:
            style_hints = ""
        for curie in curies:
            node = wrapped_adapter.node(curie)
            info = f"id: {curie}\n"
            info += f"label: {node.lbl}\n"
            system_prompt = "Provide a textual definition for the given term."
            system_prompt += style_hints
            response = model.prompt(info, system=system_prompt).text()
            yield curie, DefinitionPropertyValue(val=response)

    def validate_mappings(
        self,
        entities: Iterable[CURIE] = None,
        adapters: Dict[str, BasicOntologyInterface] = None,
        configuration: ValidationConfiguration = None,
    ) -> Iterable[MappingValidationResult]:
        """
        Validate mappings for a set of entities using an LLM.

        :param entities:
        :return:
        """
        model = self.get_model()
        if not isinstance(self, MappingProviderInterface):
            raise ValueError(f"Cannot validate mappings on {self}")
        mappings = list(self.sssom_mappings(entities))
        descriptions = {}
        from oaklib.utilities.mapping.mapping_validation import lookup_mapping_adapter

        def _get_description(entity: CURIE) -> Optional[str]:
            if entity not in descriptions:
                adapter = lookup_mapping_adapter(entity, adapters)
                if not adapter:
                    return None
                lbl = adapter.label(entity)
                defn = adapter.definition(entity)
                desc = f"Name: {lbl}\nDefinition: {defn}\nRelationships:"
                for _, p, o in adapter.relationships(entity):
                    ol = adapter.label(o)
                    pl = adapter.label(p)
                    if not pl:
                        pl = p
                    if ol:
                        desc += f"\n  {pl} => {ol} [{o}]"
                descriptions[entity] = desc
            return descriptions[entity]

        for m in mappings:
            sd = _get_description(m.subject_id)
            if not sd:
                continue
            od = _get_description(m.object_id)
            if not od:
                continue
            pred = m.predicate_id
            if pred == HAS_DBXREF:
                pred = SKOS_EXACT_MATCH

            prompt_info = configuration.prompt_info if configuration else ""
            system_prompt = MAPPING_VALIDATION_SYSTEM_PROMPT.format(prompt_info=prompt_info)
            main_prompt = (
                f"# PREDICATE: {pred}\n"
                f"# SUBJECT:\n{sd}\n"
                f"# OBJECT:\n{od}\n"
                f"JSON RESPONSE:"
            )
            logger.debug(f"System: {system_prompt}")
            logger.info(f"Prompt: {main_prompt}")
            response = model.prompt(main_prompt, system=system_prompt).text()
            logger.info(f"Response: {response}")
            try:
                obj = json.loads(response)
            except json.JSONDecodeError as e:
                logger.info(f"Failed to parse JSON: {response}")
                extra = "Please return VALID JSON ONLY."
                extra += f"You provided: {response}"
                extra += f"This resulted in: {e}\n"
                extra += "Please try again, WITH VALID JSON."
                extra += "Do not apologize or give more verbiage, JUST JSON."
                response = model.prompt(main_prompt + extra, system=system_prompt).text()
                try:
                    obj = json.loads(response)
                except json.JSONDecodeError as e:
                    logger.error(
                        "Failed to parse JSON for 2nd time:\n"
                        f"You provided: {response}\n"
                        f"This resulted in: {e}\n"
                    )
                    # TODO: strict mode
                    obj = {"confidence": "none", "comment": "Failed to parse JSON"}
            cmap = {
                "high": 1.0,
                "medium": 0.5,
                "low": 0.1,
                "none": 0.0,
            }
            mods = (
                str(obj.get("subject_modifications", ""))
                + "; "
                + str(obj.get("object_modifications", ""))
            )
            yield MappingValidationResult(
                subject_id=m.subject_id,
                subject_info=sd,
                object_id=m.object_id,
                object_info=od,
                predicate_id=m.predicate_id,
                problem=obj.get("problem", None),
                confidence=cmap.get(obj.get("confidence", None), 0.5),
                info=obj.get("comment", None),
                suggested_predicate=obj.get("predicate_modifications", None),
                suggested_modifications=mods,
            )
