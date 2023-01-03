"""OboGraph to FHIR Converter

Resources
- Updates issue: https://github.com/INCATools/ontology-access-kit/issues/369
- Conversion examples: https://drive.google.com/drive/folders/1lwGQ63_fedfWlGlRemq8OeZhZsvIXN01
"""
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

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
from oaklib.types import CURIE
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
    """Converts from OboGraph to FHIR.

    - An ontology is mapped to a FHIR `CodeSystem <https://build.fhir.org/codesystem.html>`_.
    - Each node in the OboGraph is converted to a _FHIR Concept_.
    - Each CURIE/URI in the OboGraph is treated as a CURIE when it becomes a code (e.g. "HP:0000001")

         - TODO: make this configurable

    - Each edge in the OboGraph is converted to a _FHIR ConceptProperty_ if the `include_all_predicates` param is True.
      Otherwise, will only convert edges if the predicate is in the `DIRECT_PREDICATE_MAP`.
    - Each synonym in the OboGraph is converted to a _FHIR ConceptDesignation_.

        - The synonym predicate is mapped to a _FHIR Coding_, using the `SCOPE_MAP`.

    # TODO: These currently unresolvable
        from oaklib.utilities.obograph_utils import load_obograph
        from oaklib.utilities.curie_converter import CurieConverter
    To use:

        >>> from oaklib.converters.obo_graph_to_fhir_converter import OboGraphToFHIRConverter
        >>> from oaklib.datamodels.obograph import GraphDocument
        >>> from oaklib.utilities.obograph_utils import load_obograph
        >>> from oaklib.utilities.curie_converter import CurieConverter
        >>> from linkml_runtime.dumpers import json_dumper
        >>> converter = OboGraphToFHIRConverter(curie_converter=CurieConverter())
        >>> graph = load_obograph("hp.obo.json")
        >>> code_system = converter.dump(graph)
        >>> print(json_dumper.dumps(code_system))

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
        include_all_predicates: bool = True,
        **kwargs,
    ) -> None:
        """
        Dump an OBO Graph Document to a FHIR CodeSystem.

        By default, only IS_A predicates are converted to ConceptProperties. To override this,
        specify ``include_all_predicates=True``.

        :param source:
        :param target:
        :param include_all_predicates: include the maximal amount of predicates
        """
        cs = self.convert(source, include_all_predicates=include_all_predicates, **kwargs)
        json_str = json_dumper.dumps(cs)
        if target is None:
            print(json_str)
        else:
            with open(target, "w", encoding="UTF-8") as f:
                f.write(json_str)

    def convert(
        self,
        source: GraphDocument,
        target: CodeSystem = None,
        include_all_predicates: bool = True,
        **kwargs,
    ) -> CodeSystem:
        """
        Convert an OBO Graph Document to a FHIR CodingSystem

        :param source:
        :param target: if None, one will be created
        :param include_all_predicates: include the maximal amount of predicates
        :return:
        """
        if target is None:
            target = CodeSystem()
        target.resourceType = CodeSystem.__name__
        for g in source.graphs:
            self._convert_graph(g, target=target, include_all_predicates=include_all_predicates)
        return target

    def code(self, uri: CURIE) -> str:
        """Convert a code"""
        if not self.curie_converter:
            return uri
        curie = self.curie_converter.compress(uri)
        if curie is None:
            return uri
        else:
            return curie

    def _convert_graph(
        self, source: Graph, target: CodeSystem, include_all_predicates: bool = True
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
            )
        # CodeSystem.property
        # todo's
        #  i. code: mostly URIs, which don't conform to [^\s]+(\s[^\s]+)* (https://hl7.org/fhir/datatypes.html#code)
        #  ii. description: can get, but tedious; downloading and caching and looking up in source ontologies
        #  iii. type: ideally Coding (https://build.fhir.org/datatypes.html#Coding). The property value is a code
        #  defined in an external code system. This may be used for translations, but is not the intent.
        #  https://hl7.org/fhir/codesystem-concept-property-type.htm
        target.property = [
            CodeSystemProperty(code=x, uri=x, type="code") for x in self.predicates_to_export
        ]
        return target

    def _convert_node(
        self,
        source: Node,
        index: Dict[CURIE, List[Edge]],
        target: CodeSystem,
        include_all_predicates: bool = True,
    ) -> Concept:
        """Converts a node to a FHIR Concept. Also collects predicates to be included in CodeSystem.property."""
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
