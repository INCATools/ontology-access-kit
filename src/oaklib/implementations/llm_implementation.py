"""A text annotator based on LLM."""
import json
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator, List

from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.interfaces import TextAnnotatorInterface
from oaklib.interfaces.text_annotator_interface import TEXT

if TYPE_CHECKING:
    import llm

__all__ = [
    "LLMImplementation",
]


@dataclass
class LLMImplementation(TextAnnotatorInterface):
    """Perform named entity normalization on LLM."""

    grounder: TextAnnotatorInterface = None
    """A wrapped annotator used to ground NEs.
    """

    model_id: str = None
    """The ID of the LLM model to use. E.g gpt-4"""

    model: "llm.Model" = None
    """The LLM model to use."""

    default_model_id: str = "gpt-3.5-turbo"

    allow_direct_grounding: bool = False
    """The point of this implementation is to perform NER and delegate to a grounded."""

    max_recursion_depth: int = 0

    def __post_init__(self):
        slug = self.resource.slug
        if not slug:
            logging.warning("LLM implementation requires a slug for grounding")
        else:
            slug = slug.replace("llm:", "")
            logging.info(f"LLM implementation will use grounder: {slug}")
            from oaklib import get_adapter

            self.grounder = get_adapter(slug)
        if self.model_id is not None:
            self.model = llm.get_model(self.model_id)

    def annotate_text(
        self, text: TEXT, configuration: TextAnnotationConfiguration = None
    ) -> Iterator[TextAnnotation]:
        if not configuration:
            raise NotImplementedError("Missing text annotation configuration")
        if configuration.matches_whole_text:
            if not self.allow_direct_grounding:
                raise NotImplementedError("LLM does not support whole-text matching")
            else:
                logging.info("Delegating directly to grounder, bypassing LLM")
                yield from self.grounder.annotate_text(text, configuration)
        else:
            yield from self._llm_annotate(text, configuration)

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
            matches = list(self.grounder.annotate_text(term, grounder_configuration))
            if not matches:
                aliases = self._suggest_aliases(
                    term, model, configuration.categories, configuration
                )
                for alias in aliases:
                    matches = list(self.grounder.annotate_text(alias, grounder_configuration))
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
