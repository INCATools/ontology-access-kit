"""
OboGraph to FHIR Converter

Resources
- Updates issue: https://github.com/INCATools/ontology-access-kit/issues/369
- Conversion examples: https://drive.google.com/drive/folders/1lwGQ63_fedfWlGlRemq8OeZhZsvIXN01
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Union

import rdflib
from linkml_runtime.dumpers import json_dumper

from oaklib.converters.data_model_converter import DataModelConverter
from oaklib.datamodels.fhir import (
    CodeSystem,
    CodeSystemProperty,
    Coding,
    Concept,
    ConceptDesignation,
    ConceptProperty,
)
from oaklib.datamodels.obograph import Edge, Graph, GraphDocument, Node
from oaklib.datamodels.vocabulary import (
    HAS_BROAD_SYNONYM,
    HAS_EXACT_SYNONYM,
    HAS_NARROW_SYNONYM,
    HAS_RELATED_SYNONYM,
)
from oaklib.types import CURIE, URI
from oaklib.utilities.obograph_utils import index_graph_edges_by_subject

TRIPLE = Tuple[rdflib.URIRef, rdflib.URIRef, Any]

DIRECT_PREDICATE_MAP = {
    "is_a": "parent",
}

SCOPE_MAP = {
    "hasBroadSynonym": HAS_BROAD_SYNONYM,
    "hasExactSynonym": HAS_EXACT_SYNONYM,
    "hasNarrowSynonym": HAS_NARROW_SYNONYM,
    "hasRelatedSynonym": HAS_RELATED_SYNONYM,
}

SCOPE_DISPLAY = {
    "hasBroadSynonym": "has broad synonym",
    "hasExactSynonym": "has exact synonym",
    "hasNarrowSynonym": "has narrow synonym",
    "hasRelatedSynonym": "has related synonym",
}


@dataclass
class OboGraphToFHIRConverter(DataModelConverter):
    """
    Converts from OboGraph to FHIR.

    - An ontology is mapped to a FHIR `CodeSystem <https://build.fhir.org/codesystem.html>`_.
    - Each node in the OboGraph is converted to a _FHIR Concept_.
    - Each CURIE/URI in the OboGraph is treated as a CURIE when it becomes a packages (e.g. "HP:0000001")

    - Each edge in the OboGraph is converted to a _FHIR ConceptProperty_ if the `include_all_predicates` param is
      True. Otherwise, will only convert edges if the predicate is in the `DIRECT_PREDICATE_MAP`.
    - Each synonym in the OboGraph is converted to a _FHIR ConceptDesignation_.

        - The synonym predicate is mapped to a _FHIR Coding_, using the `SCOPE_MAP`.

    To run on the command line:

        runoak  --prefix my_prefix=my_expansion -i obograph:my-ont.json dump -O fhirjson -o my-ont.fhir.json

    Here the input is an OboGraph JSON file. You can also specify:

     - OWL as sqlite
     - OBO Format

    """

    def dump(
        self,
        source: GraphDocument,
        target: str = None,
        **kwargs,
    ) -> None:
        """
        Dump an OBO Graph Document to a FHIR CodeSystem.

        :param source: Source serialization.
        :param target: Target serialization.
        :param kwargs: Additional keyword arguments passed to :ref:`convert`.
        """
        cs = self.convert(
            source,
            **kwargs,
        )
        json_str = json_dumper.dumps(cs, inject_type=False)
        if target is None:
            print(json_str)
        else:
            with open(target, "w", encoding="UTF-8") as f:
                f.write(json_str)

    # todo: id/url: any way to try to ascertain ID or URL if not passed? and warn if not determined?
    def convert(
        self,
        source: GraphDocument,
        target: CodeSystem = None,
        code_system_id: str = None,
        code_system_url: str = None,
        include_all_predicates: bool = True,
        native_uri_stems: List[str] = None,
        use_curies_native_concepts: bool = False,
        use_curies_foreign_concepts: bool = True,
        predicate_period_replacement: bool = False,
        **kwargs,
    ) -> CodeSystem:
        """
        Convert an OBO Graph Document to a FHIR CodingSystem

        To use:

        >>> from oaklib.converters.obo_graph_to_fhir_converter import OboGraphToFHIRConverter
        >>> from oaklib.datamodels.obograph import GraphDocument
        >>> from linkml_runtime.dumpers import json_dumper
        >>> from linkml_runtime.loaders import json_loader
        >>> converter = OboGraphToFHIRConverter()
        >>> graph = json_loader.load("tests/input/hp_test.json", target_class=GraphDocument)
        >>> code_system = converter.convert(graph)
        >>> print(json_dumper.dumps(code_system))
        <BLANKLINE>
        ...
         "concept": [
            {
            "code": "HP:0012639",
            "display": "Abnormal nervous system morphology",
            "definition": "A structural anomaly of the nervous system.",
            "designation": [
         ...

        :param code_system_id: The packages system ID to use for identification on the server uploaded to.
                               See: https://hl7.org/fhir/resource-definitions.html#Resource.id
        :param code_system_url: Canonical URL for the packages system.
                                See: https://hl7.org/fhir/codesystem-definitions.html#CodeSystem.url
        :param native_uri_stems: A list of URI stems that will be used to determine whether a
                                 concept is native to the CodeSystem. (not implemented)
                                 For example, for OMIM, the following URI stems are native:
                                 https://omim.org/entry/, https://omim.org/phenotypicSeries/PS
        :param include_all_predicates: Include the maximal amount of predicates.
                                       Changes the default behavior from only
                                       exporting: IS_A (rdfs:subClassOf)
        :param use_curies_native_concepts: FHIR conventionally uses codes for references to
                                           concepts that are native to a given CodeSystem. With this option,
                                           references will be CURIEs instead. (not implemented)
        :param use_curies_foreign_concepts: Typical FHIR CodeSystems do not contain any
                                            concepts that are not native to that CodeSystem. In cases where they
                                            do appear, this converter defaults to URIs
                                            for references, unless this flag is present, in which case the converter
                                            will attempt to construct CURIEs. (not implemented)
        :param predicate_period_replacement: Predicates URIs populated into `CodeSystem.concept.property.packages`
                                             and `CodeSystem.concept.property.packages`, but the HAPI FHIR server
                                             has a bug in which periods '.' cause errors. If this flag is present,
                                             periods will be replaced with underscores '_'.
        :return: FHIR CodeSystem object
        """
        if target is None:
            target = CodeSystem()
        target.resourceType = CodeSystem.__name__
        for g in source.graphs:
            self._convert_graph(
                g,
                target=target,
                include_all_predicates=include_all_predicates,
                native_uri_stems=native_uri_stems,
                use_curies_native_concepts=use_curies_native_concepts,
                use_curies_foreign_concepts=use_curies_foreign_concepts,
                predicate_period_replacement=predicate_period_replacement,
            )
        target.id = code_system_id
        if not code_system_id:
            del target.id
        if code_system_id:
            target.url = code_system_url
        return target

    def code(self, uri: CURIE) -> str:
        """
        Convert a packages.

        This is a wrapper onto curie_converter.compress

        :param uri: URI or CURIE to convert
        :return: CURIE
        """
        if not self.curie_converter:
            return uri
        return self.curie_converter.compress(uri, passthrough=True)

    def _convert_graph(
        self,
        source: Graph,
        target: CodeSystem,
        include_all_predicates: bool = True,
        native_uri_stems: List[str] = None,
        use_curies_native_concepts: bool = False,
        use_curies_foreign_concepts: bool = True,
        predicate_period_replacement: bool = False,
    ) -> CodeSystem:
        target.id = source.id
        edges_by_subject = index_graph_edges_by_subject(source)
        logging.info(f"Converting graph to obo: {source.id}, nodes={len(source.nodes)}")
        self.predicates_to_export = set()
        # CodeSystem.concept
        for n in source.nodes:
            logging.debug(f"Converting node {n.id}")
            self._convert_node(
                n,
                index=edges_by_subject,
                target=target,
                include_all_predicates=include_all_predicates,
                native_uri_stems=native_uri_stems,
                use_curies_native_concepts=use_curies_native_concepts,
                use_curies_foreign_concepts=use_curies_foreign_concepts,
                predicate_period_replacement=predicate_period_replacement,
            )
        # CodeSystem.property
        # todo's
        #  i. packages: mostly URIs, which don't conform to [^\s]+(\s[^\s]+)* (https://hl7.org/fhir/datatypes.html#code)
        #  ii. description: can get, but tedious; downloading and caching and looking up in source ontologies
        #  iii. type: ideally Coding (https://build.fhir.org/datatypes.html#Coding). The property value is a packages
        #  defined in an external packages system. This may be used for translations, but is not the intent.
        #  https://hl7.org/fhir/codesystem-concept-property-type.htm
        target.property = [
            CodeSystemProperty(code=x, uri=x, type="packages") for x in self.predicates_to_export
        ]
        return target

    def _convert_node(
        self,
        source: Node,
        index: Dict[Union[URI, CURIE], List[Edge]],
        target: CodeSystem,
        include_all_predicates: bool = True,
        native_uri_stems: List[str] = None,
        use_curies_native_concepts: bool = False,
        use_curies_foreign_concepts: bool = True,
        predicate_period_replacement: bool = False,
    ) -> Concept:
        """Converts a node to a FHIR Concept. Also collects predicates to be included in CodeSystem.property."""
        # TODO: Use new flags
        #  self.uri(source.id)  # <--- self.uri does not exist
        #  self.packages is actually a curie. change to self.curie and add a self.packages func?
        _id = self.code(source.id)
        logging.debug(f"Converting node {_id} from {source}")
        concept = Concept(code=_id, display=source.lbl)
        target.concept.append(concept)
        if source.meta:
            self._convert_meta(source, concept)
        for e in index.get(source.id, []):
            obj = self.code(e.obj)
            logging.debug(
                f"Converting edge {e.pred} {e.obj} // include_all={include_all_predicates}"
            )
            if include_all_predicates or e.pred in DIRECT_PREDICATE_MAP:
                pred: str = DIRECT_PREDICATE_MAP.get(e.pred, e.pred)
                if predicate_period_replacement:
                    pred = pred.replace(".", "_")
                concept.property.append(ConceptProperty(code=pred, valueCode=obj))
                self.predicates_to_export.add(pred)
            else:
                logging.debug(f"Skipping edge {e}")
        return concept

    def _convert_meta(self, source: Node, concept: Concept):
        meta = source.meta
        if meta.definition:
            concept.definition = meta.definition.val
        for synonym in meta.synonyms:
            synonym_pred_code = self.code(synonym.pred)
            concept.designation.append(
                ConceptDesignation(
                    # language=synonym.lang,
                    use=Coding(
                        system="oio",
                        code=synonym_pred_code,
                        display=SCOPE_DISPLAY.get(synonym.pred),
                    ),
                    value=synonym.val,
                )
            )
