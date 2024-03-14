import csv
import logging
from abc import ABC
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, Iterable, Iterator, Optional

from oaklib.datamodels.lexical_index import LexicalIndex
from oaklib.datamodels.mapping_rules_datamodel import MappingRuleCollection
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty
from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.interfaces import SearchInterface
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

__all__ = [
    "TEXT",
    "nen_annotation",
    "TextAnnotatorInterface",
]

from oaklib.utilities.lexical.lexical_indexer import create_or_load_lexical_index

TEXT = str


def nen_annotation(text: str, object_id: CURIE, object_label: str) -> TextAnnotation:
    """Return an annotation appropriate for a grounding."""
    return TextAnnotation(
        subject_start=1,
        subject_end=len(text),
        subject_label=text,
        object_id=object_id,
        object_label=object_label,
        matches_whole_text=True,
    )


class TextAnnotatorInterface(BasicOntologyInterface, ABC):
    """
    Finds occurrences of ontology terms in text.

    This interface defines methods for providing Concept Recognition (CR) (grounding)
    on texts.

    For example, given a text:

        "the mitochondrion of hippocampal neurons"

    An annotator might recognize the concepts "mitochondrion" and "hippocampus neuron"
    from GO and CL respectively.

    Different adapters may choose to implement this differently. The default implementation is
    to build a simple textual index from an ontology, using all labels and synonyms, and to perform
    simple string matching.

    Adapters that talk to a remote endpoint may leverage more advanced strategies, and may obviate
    the need for a local indexing step. For example, the :ref:`bioportal_implementation` will use
    the OntoPortal annotate endpoint which is pre-indexed over all >1000 ontologies in bioportal.

    All return payloads conform to the `TextAnnotation` data model:

     - `<https://w3id.org/oak/text-annotator>`_

    Additional plugins may be available to provide more advanced functionality:

    - `OAK SciSpacy plugin <https://pypi.org/project/oakx-spacy/>`_ - provides a Spacy pipeline component
    - `OAK OGER plugin <https://pypi.org/project/oakx-oger/>`_ - provides a OGER pipeline component

    For more advanced extraction use cases, see:

    - `OntoGPT <https://github.com/monarch-initiative/ontogpt>`_ - LLM-based NER and schema extraction
    """

    lexical_index: Optional[LexicalIndex] = None
    """If present, some implementations may choose to use this"""

    cache_directory: Optional[str] = None
    """If present, some implementations may choose to cache any ontology indexes here.
    These may be used in subsequent invocations, it is up to the user to manage this cache."""

    rule_collection: Optional[MappingRuleCollection] = None
    """
    Mapping rules to apply to the results of the annotation, including synonymizer rules.
    """

    def annotate_text(
        self,
        text: TEXT,
        configuration: Optional[TextAnnotationConfiguration] = None,
    ) -> Iterable[TextAnnotation]:
        """
        Annotate a piece of text.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> for annotation in adapter.annotate_text("The nucleus is a organelle with a membrane"):
        ...     print(annotation.object_id, annotation.object_label, annotation.subject_start, annotation.subject_end)
        GO:0005634 nucleus 5 11
        GO:0016020 membrane 35 42
        GO:0043226 organelle 18 26

        :param text: Text to be annotated.
        :param configuration: Text annotation configuration.
        :yield: A generator function that yields annotated results.
        """
        if not configuration:
            configuration = TextAnnotationConfiguration()

        if isinstance(text, str) and configuration.token_exclusion_list:
            text = " ".join(
                [term for term in text.split() if term not in configuration.token_exclusion_list]
            )
        elif isinstance(text, tuple) and configuration.token_exclusion_list:
            filtered_text = tuple()
            # text is a tuple of string(s)
            for token in text:
                filtered_text = filtered_text + tuple(
                    term for term in token.split() if term not in configuration.token_exclusion_list
                )
            text = " ".join(filtered_text)
        else:
            logging.info("No token exclusion list provided. Proceeding ...")

        if configuration.matches_whole_text:
            if self.rule_collection:
                logging.warning("Synonymizer rules not applied for whole text matching")
            if isinstance(self, SearchInterface):
                search_config = SearchConfiguration(force_case_insensitive=True)
                for object_id in self.basic_search(text, config=search_config):
                    label = self.label(object_id)
                    yield nen_annotation(text=text, object_id=object_id, object_label=label)
                search_config.properties = [SearchProperty(SearchProperty.ALIAS)]
                logging.debug(f"Config, including synonyms: {search_config}")
                for object_id in self.basic_search(text, config=search_config):
                    label = self.label(object_id)
                    yield nen_annotation(text=text, object_id=object_id, object_label=label)
            else:
                raise NotImplementedError(
                    f"{self.__class__.__name__} can't be used to match partial text"
                )
        else:
            if self.cache_directory:
                index_name = f"{self.resource.scheme}-{self.resource.slug}-index.yaml"
                index_path = str(Path(self.cache_directory) / index_name)
                logging.info(f"Caching to {index_path}")
            else:
                index_path = None
            if not self.lexical_index:
                logging.info("Indexing ontology...")
                self.lexical_index = create_or_load_lexical_index(
                    index_path, self, mapping_rule_collection=self.rule_collection
                )
            logging.info("Performing naive search using lexical index")
            li = self.lexical_index
            text_lower = text.lower()
            for k, grouping in li.groupings.items():
                if k in text_lower:
                    ix = text_lower.index(k)
                    # TODO: make configurable. Exclude mid-word matches
                    if ix > 0 and text_lower[ix - 1].isalpha():
                        continue
                    # end = ix + len(k)
                    # if end < len(text_lower) and text_lower[end].isalpha():
                    #    continue
                    for r in grouping.relationships:
                        ann = TextAnnotation(
                            subject_start=ix + 1,
                            subject_end=ix + len(k),
                            predicate_id=r.predicate,
                            object_id=r.element,
                            object_label=r.element_term,
                            match_string=text[ix : ix + len(k)],
                            matches_whole_text=(ix == 0 and len(k) == len(text)),
                        )
                        yield ann

    def annotate_file(
        self,
        text_file: TextIOWrapper,
        configuration: TextAnnotationConfiguration = None,
    ) -> Iterator[TextAnnotation]:
        """
        Annotate text in a file.

        :param text_file: Text file that is iterated line-by-line.
        :param configuration: Text annotation configuration, defaults to None.
        :yield: Annotation of each line.
        """
        for line in text_file.readlines():
            line = line.strip()
            annotation = self.annotate_text(line, configuration)
            yield from annotation

    def annotate_tabular_file(
        self,
        text_file: TextIOWrapper,
        delimiter: Optional[str] = None,
        configuration: TextAnnotationConfiguration = None,
        match_column: str = None,
        result_column: str = "matched_id",
        result_label_column: str = "matched_label",
        match_multiple=False,
        include_unmatched=True,
    ) -> Iterator[Dict[str, str]]:
        """
        Annotate text in a file.

        :param text_file: Text file that is iterated line-by-line.
        :param configuration: Text annotation configuration, defaults to None.
        :yield: Annotation of each line.
        """
        if not configuration:
            configuration = TextAnnotationConfiguration()
        if not match_column:
            raise ValueError("Must provide a match column")
        if not delimiter:
            if text_file.name.endswith(".tsv"):
                delimiter = "\t"
            elif text_file.name.endswith(".csv"):
                delimiter = ","
            else:
                raise ValueError("Must provide a delimiter")
        reader = csv.DictReader(text_file, delimiter=delimiter)
        for row in reader:
            if match_column not in row:
                raise ValueError(f"Missing match column {match_column} in {row}")
            text = row[match_column]
            has_result = False
            for ann in self.annotate_text(text, configuration):
                row[result_column] = ann.object_id
                row[result_label_column] = ann.object_label
                has_result = True
                yield row
                if not match_multiple:
                    break
            if not has_result and include_unmatched:
                row[result_column] = ""
                row[result_label_column] = ""
                yield row
