"""
Lexical Utilities
-----------------

Various utilities for working with lexical aspects of ontologies plus mappings

"""
import logging
import re
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.metamodelcore import URIorCURIE
from sssom.constants import LICENSE, MAPPING_SET_ID
from sssom.context import get_default_metadata
from sssom.sssom_document import MappingSetDocument
from sssom.typehints import Metadata
from sssom.util import MappingSetDataFrame, to_mapping_set_dataframe
from sssom_schema import Mapping, MappingSet

from oaklib.datamodels.lexical_index import (
    LexicalGrouping,
    LexicalIndex,
    LexicalTransformation,
    LexicalTransformationPipeline,
    RelationshipToTerm,
    TransformationType,
)
from oaklib.datamodels.mapping_rules_datamodel import (
    MappingRuleCollection,
    Precondition,
)
from oaklib.datamodels.vocabulary import (
    SEMAPV,
    SKOS_BROAD_MATCH,
    SKOS_CLOSE_MATCH,
    SKOS_EXACT_MATCH,
    SKOS_NARROW_MATCH,
)
from oaklib.interfaces import BasicOntologyInterface
from oaklib.types import PRED_CURIE
from oaklib.utilities.basic_utils import pairs_as_dict


def add_labels_from_uris(oi: BasicOntologyInterface):
    """
    Adds a label based on the CURIE or URI for entities that lack labels

    :param oi: An ontology interface for making label lookups.
    """
    logging.info("Adding labels from URIs")
    curies = list(oi.entities())
    for curie in curies:
        if not oi.label(curie):
            if "#" in curie:
                sep = "#"
            elif curie.startswith("http") or curie.startswith("<http"):
                sep = "/"
            else:
                sep = ":"
            label = curie.split(sep)[-1]
            if curie.startswith("<http"):
                label = label.replace(">", "")
            label = " ".join(label.split("_"))
            # print(f'{curie} ==> {label} // {type(oi)}')
            oi.set_label(curie, label)
            # print(oi.get_label_by_curie(curie))


def create_lexical_index(
    oi: BasicOntologyInterface, pipelines: List[LexicalTransformationPipeline] = None
) -> LexicalIndex:
    """
    Generates a LexicalIndex keyed by normalized terms

    If the pipelines parameter is not specified, then default pipelines will be applied
    (currently CaseNormalization and WhitespaceNormalization)

    :param oi: An ontology interface for making label lookups.
    :param pipelines: list of transformation pipelines to apply
    :return: An index over an ontology keyed by lexical unit.
    """
    if pipelines is None:
        step1 = LexicalTransformation(TransformationType.CaseNormalization)
        step2 = LexicalTransformation(TransformationType.WhitespaceNormalization)
        pipelines = [LexicalTransformationPipeline(name="default", transformations=[step1, step2])]
    ix = LexicalIndex(pipelines={p.name: p for p in pipelines})
    for curie in oi.entities():
        logging.debug(f"Indexing {curie}")
        if not URIorCURIE.is_valid(curie):
            logging.warning(f"Skipping {curie} as it is not a valid CURIE")
            continue
        alias_map = oi.entity_alias_map(curie)
        mapping_map = pairs_as_dict(oi.simple_mappings_by_curie(curie))
        for pred, terms in {**alias_map, **mapping_map}.items():
            for term in terms:
                if not term:
                    logging.debug(f"No term for {curie}.{pred} (expected for aggregator interface)")
                    continue
                for pipeline in pipelines:
                    term2 = term
                    for tr in pipeline.transformations:
                        term2 = apply_transformation(term2, tr)
                    rel = RelationshipToTerm(
                        predicate=pred, element=curie, element_term=term, pipeline=pipeline.name
                    )
                    if term2 not in ix.groupings:
                        ix.groupings[term2] = LexicalGrouping(term=term2)
                    ix.groupings[term2].relationships.append(rel)
    return ix


def save_lexical_index(lexical_index: LexicalIndex, path: str):
    """
    Saves a YAML using standard mapping of datanodel to YAML

    :param lexical_index:
    :param path:
    :return:
    """
    yaml_dumper.dump(lexical_index, to_file=path)


def load_lexical_index(path: str) -> LexicalIndex:
    """
    Loads from a YAML file

    :param path: Lexical index in the form of a YAML file.
    :return: An index over an ontology keyed by lexical unit.
    """
    return yaml_loader.load(path, target_class=LexicalIndex)


def lexical_index_to_sssom(
    oi: BasicOntologyInterface,
    lexical_index: LexicalIndex,
    ruleset: MappingRuleCollection = None,
    meta: Metadata = None,
) -> MappingSetDataFrame:
    """
    Transform a lexical index to an SSSOM MappingSetDataFrame by finding all pairs for any given index term.

    :param oi: An ontology interface for making label lookups.
    :param lexical_index: An index over an ontology keyed by lexical unit.
    :param meta: Metadata object that contains the curie_map and metadata for the SSSOM maaping.
    :return: SSSOM MappingSetDataFrame object.
    """
    mappings = []
    logging.info("Converting lexical index to SSSOM")
    for term, grouping in lexical_index.groupings.items():
        # elements = set([r.element for r in grouping.relationships])
        elementmap = defaultdict(list)
        for r in grouping.relationships:
            elementmap[r.element].append(r)
        if len(elementmap.keys()) < 2:
            continue
        for e1 in elementmap:
            for e2 in elementmap:
                if e1 < e2:
                    for r1 in elementmap[e1]:
                        for r2 in elementmap[e2]:
                            mappings.append(inferred_mapping(oi, term, r1, r2, ruleset=ruleset))

        # for r1 in grouping.relationships:
        #    for r2 in grouping.relationships:
        #        if r1.element < r2.element:
        #            mappings.append(create_mapping(oi, term, r1, r2))
    logging.info("Done creating SSSOM mappings")

    if meta is None:
        meta = get_default_metadata()

    mapping_set_id = meta.metadata[MAPPING_SET_ID]
    license = meta.metadata[LICENSE]

    mset = MappingSet(mapping_set_id=mapping_set_id, mappings=mappings, license=license)
    # doc = MappingSetDocument(prefix_map=oi.prefix_map(), mapping_set=mset)
    doc = MappingSetDocument(prefix_map=meta.prefix_map, mapping_set=mset)
    msdf = to_mapping_set_dataframe(doc)
    # TODO uncomment below.
    # TODO Right now it erases the entire msdf.df in the absence of CURIEs in map.
    # msdf.clean_prefix_map()
    return msdf


def create_mapping(
    term: str,
    r1: RelationshipToTerm,
    r2: RelationshipToTerm,
    pred: PRED_CURIE = SKOS_CLOSE_MATCH,
    confidence: float = None,
) -> Mapping:
    """Create mappings between a pair of entities.

    :param term: Match string
    :param r1: Term relationship 1
    :param r2: Term relationship 2
    :param pred: Predicate, defaults to SKOS_CLOSE_MATCH
    :param confidence: Confidence score., defaults to None
    :return: Mapping object.
    """
    return Mapping(
        subject_id=r1.element,
        object_id=r2.element,
        predicate_id=pred,
        confidence=confidence,
        match_string=term,
        subject_match_field=[r1.predicate],
        object_match_field=[r2.predicate],
        mapping_justification=SEMAPV.LexicalMatching.value,
        mapping_tool="oaklib",
    )


def inferred_mapping(
    oi: BasicOntologyInterface,
    term: str,
    r1: RelationshipToTerm,
    r2: RelationshipToTerm,
    ruleset: MappingRuleCollection = None,
) -> Mapping:
    """
    Create a mapping from a pair of relationships, applying rules to filter or assign confidence

    :param oi: An ontology interface for making label lookups.
    :param term: Match string
    :param r1: Term relationship 1
    :param r2: Term relationship 2
    :param ruleset: Rules of matching.
    :return: Mapping object.
    """
    # create two mappings, one in each direction
    m1 = create_mapping(term, r1, r2)
    m2 = create_mapping(term, r2, r1)
    # confidence in a particular predicate (eg sameAs)
    weightmap: Dict[PRED_CURIE, float] = defaultdict(float)
    best: Tuple[Optional[float], Mapping, PRED_CURIE] = None, m1, m1.predicate_id
    if ruleset is not None:
        rules = ruleset.rules
    else:
        rules = []
    for rule in rules:
        inverted = False
        # determine if preconditions hold for the mapping or its inverse
        if precondition_holds(rule.preconditions, m1):
            m = m1
        elif not rule.oneway and precondition_holds(rule.preconditions, m2):
            m = m2
            inverted = True
        else:
            m = None
        if m:
            # preconditions hold: assign weight
            # weight is a float, with 0 indicating 0.5 probability,
            # higher is increased confidence, lower is decreased confidence
            weight = 0.0
            if rule.postconditions.predicate_id:
                m.predicate_id = rule.postconditions.predicate_id
            if rule.postconditions.weight:
                weight = rule.postconditions.weight
            if inverted:
                # TODO: consider moving this logic up
                inv_pred = invert_mapping_predicate(m.predicate_id)
                if inv_pred:
                    m.predicate_id = inv_pred
                else:
                    # cannot invert this mapping; ignore it
                    m = None
            if m:
                weightmap[m.predicate_id] += weight
                weight = weightmap[m.predicate_id]
                if best[0] is None or weight > best[0]:
                    best = weight, m, m.predicate_id
    best_weight, best_mapping, _ = best
    if best_weight is not None:
        best_mapping.confidence = inverse_logit(best_weight)
    best_mapping.subject_label = oi.label(best_mapping.subject_id)
    best_mapping.object_label = oi.label(best_mapping.object_id)
    return best_mapping


def inverse_logit(weight: float) -> float:
    """
    Inverse logit

    https://upload.wikimedia.org/wikipedia/commons/5/57/Logit.png

    :param weight: Weight for calculating confidence.
    :return: probability between 0 and 1
    """
    return 1 / (1 + 2 ** (-weight))


def invert_mapping_predicate(pred: PRED_CURIE) -> Optional[PRED_CURIE]:
    """Return the opposite of predicate passed.

    :param pred: Predicate.
    :return: Opposite of the predicate.
    """
    if pred == SKOS_EXACT_MATCH or pred == SKOS_CLOSE_MATCH:
        return pred
    if pred == SKOS_BROAD_MATCH:
        return SKOS_NARROW_MATCH
    return None


def precondition_holds(precondition: Precondition, mapping: Mapping) -> bool:
    for k in ["subject_match_field", "object_match_field"]:
        k_one_of = f"{k}_one_of"
        expected_values = getattr(precondition, k_one_of, [])
        actual_values = getattr(mapping, k, [])
        # print(f'CHECKING {actual_values} << {expected_values}')
        if expected_values and not any(v for v in actual_values if v in expected_values):
            # print('** NO MATCH')
            return False
        # print(f'**** MTCH {k}')
    return True


def apply_transformation(term: str, transformation: LexicalTransformation) -> str:
    """
    Apply an individual transformation on a term

    :param term:
    :param transformation:
    :return:
    """
    typ = str(transformation.type)
    logging.debug(f"Applying: {transformation}")
    if typ == TransformationType.CaseNormalization.text:
        return term.lower()
    elif typ == TransformationType.WhitespaceNormalization.text:
        return re.sub(" {2,}", " ", term.strip())
    else:
        raise NotImplementedError(
            f"Transformation Type {typ} {type(typ)} not implemented {TransformationType.CaseNormalization.text}"
        )


def save_mapping_rules(mapping_rules: MappingRuleCollection, path: str):
    """
    Saves a YAML using standard mapping of datanodel to YAML

    :param mapping_rules: YAML file that contains rules for mapping.
    :param path: Path where the YAML file is saved
    """
    yaml_dumper.dump(mapping_rules, to_file=path)


def load_mapping_rules(path: str) -> MappingRuleCollection:
    """
    Loads from a YAML file that contains rules for mapping.

    :param path:  Path where the YAML file is located.
    :return: Rules for mapping
    """
    return yaml_loader.load(path, target_class=MappingRuleCollection)
