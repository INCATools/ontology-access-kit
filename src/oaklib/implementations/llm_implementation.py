"""An OAK implementation that wraps Large Language Models."""

import base64
import json
import logging
import re
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Iterable, Iterator, List, Optional, Tuple

from sssom_schema import Mapping
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

from oaklib import BasicOntologyInterface
from oaklib.datamodels.class_enrichment import ClassEnrichmentResult
from oaklib.datamodels.item_list import ItemList
from oaklib.datamodels.obograph import DefinitionPropertyValue
from oaklib.datamodels.similarity import TermPairwiseSimilarity
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
from oaklib.interfaces.class_enrichment_calculation_interface import (
    ClassEnrichmentCalculationInterface,
)
from oaklib.interfaces.ontology_generator_interface import OntologyGenerationInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.text_annotator_interface import TEXT
from oaklib.types import CURIE, PRED_CURIE

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

ENRICHMENT_SYSTEM_PROMPT = """
I will provide you with a list of {{subject_category}} identifiers/names.
Your job is to test for over-representation of {{object_category}} associations
of that set.

Return results as a valid JSON list with the following structure:

{{"terms": ["<TERM-NAME1>", "<TERM-NAME2>, ...],
  "description": "<NARRATIVE DESCRIPTION>"}}

Always return JSON in this structure. Only use the two keys "terms" and "description".
"terms" is always a list of term names (not IDs). "description" is a narrative description
of the commonalities in the input list. Do not escape JSON keys. No verbiage before
or after the JSON object.
"""


def _prefix(curie: CURIE) -> str:
    return curie.split(":")[0].lower()


def is_rate_limit_error(exception):
    # List of fully qualified names of RateLimitError exceptions from various libraries
    rate_limit_errors = [
        "openai.error.RateLimitError",
        "anthropic.error.RateLimitError",
        # Add more as needed
    ]
    exception_full_name = f"{exception.__class__.__module__}.{exception.__class__.__name__}"
    logger.warning(f"Exception_full_name: {exception_full_name}")
    logger.warning(f"Exception: {exception}")
    return exception_full_name in rate_limit_errors


@retry(
    retry=retry_if_exception(is_rate_limit_error),
    wait=wait_random_exponential(multiplier=1, max=40),
    stop=stop_after_attempt(3),
)
def query_model(model, *args, **kwargs):
    logger.debug(f"Querying model with args={args} and kwargs={kwargs}")
    return model.prompt(*args, **kwargs)


def query_model_to_json(model, *args, **kwargs):
    response = query_model(model, *args, **kwargs)
    text = json.loads(response.text())
    logger.debug(f"Response: {text}")
    return text


@dataclass
class LLMImplementation(
    OboGraphInterface,
    ClassEnrichmentCalculationInterface,
    TextAnnotatorInterface,
    SearchInterface,
    MappingProviderInterface,
    OntologyGenerationInterface,
    SemanticSimilarityInterface,
    ValidatorInterface,
):
    """
    An Ontology Interface that wraps Large Language Models (LLM).

    This is a wrapper interface, it needs to wrap an existing adapter; e.g.

    >>> adapter = get_adapter("llm:sqlite:obo:cl")

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

    throttle_time: float = 0.0

    requires_associations = False

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
            if "claude" in self.model_id or "openrouter" in self.model_id:
                # TODO: claude API seems to have its own rate limiting
                # TODO: openrouter just seems very flaky
                # but it is too conservative
                self.throttle_time = 10

    def entities(self, **kwargs) -> Iterator[CURIE]:
        """Return all entities in the ontology."""
        yield from self.wrapped_adapter.entities(**kwargs)

    def basic_search(self, *args, **kwargs) -> Iterator[CURIE]:
        if not isinstance(self.wrapped_adapter, SearchInterface):
            raise NotImplementedError(
                "LLM can only perform basic search on a wrapped adapter that supports it"
            )
        yield from self.wrapped_adapter.basic_search(*args, **kwargs)

    def label(self, *args, **kwargs) -> Optional[str]:
        return self.wrapped_adapter.label(*args, **kwargs)

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
        """
        Suggest definitions for the given curies.

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
            time.sleep(self.throttle_time)
            response = query_model(model, main_prompt, system=system_prompt).text()
            # response = model.prompt(main_prompt, system=system_prompt).text()
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
                logger.info(f"New Prompt: {main_prompt + extra}")
                response = query_model(model, main_prompt + extra, system=system_prompt).text()
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

    def enriched_classes(
        self,
        subjects: Optional[Iterable[CURIE]] = None,
        item_list: Optional[ItemList] = None,
        predicates: Iterable[CURIE] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        background: Iterable[CURIE] = None,
        hypotheses: Iterable[CURIE] = None,
        cutoff=0.05,
        autolabel=False,
        filter_redundant=False,
        sort_by: str = None,
        direction="greater",
    ) -> Iterator[ClassEnrichmentResult]:
        """
        Test for over-representation of classes in a set of entities.

        Implements TALISMAN approach.

        :param subjects:
        :param item_list:
        :param predicates:
        :param object_closure_predicates:
        :param background:
        :param hypotheses:
        :param cutoff:
        :param autolabel:
        :param filter_redundant:
        :param sort_by:
        :param direction:
        :return:
        """
        model = self.get_model()

        if not subjects:
            if not item_list:
                raise ValueError("Either subjects or item_list must be provided")
            if not item_list.itemListElements:
                raise ValueError("item_list must not be empty")
            subjects = item_list.itemListElements
        subjects = list(subjects)
        sample_size = len(subjects)
        logging.info(f"Calculating sample_counts for {sample_size} subjects")
        if not sample_size:
            raise ValueError("No subjects provided")
        object_category = "Gene"
        subject_category = "Function"
        system_prompt = ENRICHMENT_SYSTEM_PROMPT.format(
            subject_category=subject_category, object_category=object_category
        )
        prompt = "; ".join(subjects)
        result = query_model_to_json(model, system=system_prompt, prompt=prompt)
        logger.info(f"Result: {result}")
        wrapped = self.wrapped_adapter
        if isinstance(wrapped, TextAnnotatorInterface):
            annotator = wrapped
        else:
            annotator = self
        for term in result["terms"]:
            anns = list(
                annotator.annotate_text(term, TextAnnotationConfiguration(matches_whole_text=True))
            )
            for ann in anns:
                yield ClassEnrichmentResult(
                    class_id=ann.object_id,
                    class_label=term,
                )
            if not anns:
                yield ClassEnrichmentResult(
                    class_id="_:AUTO",
                    class_label=term,
                )

    def _term2ids(
        self, term: str, annotator: Optional[TextAnnotatorInterface] = None
    ) -> List[CURIE]:
        """Convert a term to an ID."""
        if annotator is None:
            if isinstance(self.wrapped_adapter, TextAnnotatorInterface):
                annotator = self.wrapped_adapter
            else:
                annotator = self
        anns = annotator.annotate_text(term, TextAnnotationConfiguration(matches_whole_text=True))
        ids = [ann.object_id for ann in anns]
        if ids:
            return ids
        else:
            e = base64.b64encode(term.encode("utf-8")).decode("utf-8")
            return [f"_:{e}"]

    def _term2id(self, term: str, annotator: Optional[TextAnnotatorInterface] = None) -> CURIE:
        return self._term2ids(term, annotator)[0]

    def pairwise_similarity(
        self,
        subject: CURIE,
        object: CURIE,
        **kwargs,
    ) -> Optional[TermPairwiseSimilarity]:
        # Current implementation is naive and the MRCA returned is usually not in ontology
        logger.debug(f"Querying {subject} vs {object}")
        subject_label = self.label(subject)
        object_label = self.label(object)
        if not subject_label:
            subject_label = subject
        if not object_label:
            object_label = object
        sp = (
            "given two terms, estimate the most recent common subsumer/ancestor "
            "as well as how similar the terms are (0..1.0). "
            "return results as a JSON object with the following structure:\n\n"
            '{"score": 0.95, "ancestor": "<term-name>"}'
            "\nAlways return valid JSON. Only use the two keys 'score' and 'ancestor'. "
            "the value of score is a float between 0 and 1.0.\n"
            "the value of ancestor is a term label with the most recent common subsumer/ancestor."
        )
        p = f'TERMS: {subject} "{subject_label}" vs {object} "{object_label}"'
        obj = query_model_to_json(self.model, system=sp, prompt=p)
        anc = obj["ancestor"]
        logger.info(f"Most recent common subsumer: {anc}")
        sim = TermPairwiseSimilarity(
            subject_id=subject,
            object_id=object,
            subject_label=subject_label,
            object_label=object_label,
            jaccard_similarity=obj["score"],
            ancestor_id=self._term2id(anc),
            ancestor_label=anc,
        )
        logger.info(f"Pairwise similarity: {sim}")
        return sim
