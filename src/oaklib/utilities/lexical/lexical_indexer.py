"""
Lexical Utilities
-----------------

Various utilities for working with lexical aspects of ontologies plus mappings

"""
import logging
import re
from collections import defaultdict
from typing import List, Dict, Optional, Tuple

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
from oaklib.interfaces import BasicOntologyInterface
from oaklib.types import PRED_CURIE
from oaklib.datamodels.lexical_index import LexicalIndex, LexicalTransformation, TransformationType, RelationshipToTerm, \
    LexicalGrouping, LexicalTransformationPipeline
from oaklib.datamodels.mapping_rules_datamodel import Precondition, MappingRuleCollection
from oaklib.datamodels.vocabulary import SKOS_EXACT_MATCH, SKOS_BROAD_MATCH, SKOS_NARROW_MATCH, \
    SKOS_CLOSE_MATCH
from oaklib.utilities.basic_utils import pairs_as_dict
from sssom import Mapping
from sssom.sssom_document import MappingSetDocument
from sssom.util import MappingSetDataFrame, to_mapping_set_dataframe
from sssom.sssom_datamodel import MatchTypeEnum, MappingSet

def add_labels_from_uris(oi: BasicOntologyInterface):
    """
    Adds a label based on the CURIE or URI for entities that lack labels

    :param oi:
    :return:
    """
    for curie in oi.all_entity_curies():
        if not oi.get_label_by_curie(curie):
            if '#' in curie:
                sep = '#'
            elif curie.startswith('http'):
                sep = '/'
            else:
                sep = ':'
            label = curie.split(sep)[-1]
            oi.set_label_for_curie(curie, label)


def create_lexical_index(oi: BasicOntologyInterface,
                         pipelines: List[LexicalTransformationPipeline] = None) -> LexicalIndex:
    """
    Generates a LexicalIndex keyed by normalized terms

    If the pipelines parameter is not specified, then default pipelines will be applied
    (currently CaseNormalization and WhitespaceNormalization)

    :param oi:
    :param pipelines: list of transformation pipelines to apply
    :return:
    """
    if pipelines is None:
        step1 = LexicalTransformation(TransformationType.CaseNormalization)
        step2 = LexicalTransformation(TransformationType.WhitespaceNormalization)
        pipelines = [LexicalTransformationPipeline(name='default',
                                                   transformations=[step1, step2])]
    ix = LexicalIndex(pipelines={p.name: p for p in pipelines})
    for curie in oi.all_entity_curies():
        alias_map = oi.alias_map_by_curie(curie)
        mapping_map = pairs_as_dict(oi.get_simple_mappings_by_curie(curie))
        for pred, terms in {**alias_map, **mapping_map}.items():
            for term in terms:
                if not term:
                    logging.warning(f'No term for {curie}.{pred}')
                    continue
                for pipeline in pipelines:
                    term2 = term
                    for tr in pipeline.transformations:
                        term2 = apply_transformation(term, tr)
                    rel = RelationshipToTerm(predicate=pred, element=curie, element_term=term, pipeline=pipeline.name)
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

    :param path:
    :return:
    """
    return yaml_loader.load(path, target_class=LexicalIndex)

def lexical_index_to_sssom(oi: BasicOntologyInterface, lexical_index: LexicalIndex, id='default',
                           ruleset: MappingRuleCollection = None) -> MappingSetDataFrame:
    """
    Transform a lexical index to an SSSOM MappingSetDataFrame by finding all pairs for any given index term

    :param oi:
    :param lexical_index:
    :param id:
    :return:
    """
    mappings = []
    logging.info('Converting lexical index to SSSOM')
    for term, grouping in lexical_index.groupings.items():
        elements = set([r.element for r in grouping.relationships])
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

        #for r1 in grouping.relationships:
        #    for r2 in grouping.relationships:
        #        if r1.element < r2.element:
        #            mappings.append(create_mapping(oi, term, r1, r2))
    logging.info('Done creating SSSOM mappings')
    mset = MappingSet(mapping_set_id=id, mappings=mappings, license='CC-0')
    #doc = MappingSetDocument(prefix_map=oi.get_prefix_map(), mapping_set=mset)
    doc = MappingSetDocument(prefix_map={}, mapping_set=mset)
    return to_mapping_set_dataframe(doc)


def create_mapping(term: str, r1: RelationshipToTerm, r2: RelationshipToTerm,
                   pred: PRED_CURIE = SKOS_CLOSE_MATCH, confidence: float = None) -> Mapping:
    return Mapping(subject_id=r1.element,
                   object_id=r2.element,
                   predicate_id=pred,
                   confidence=confidence,
                   match_string=term,
                   subject_match_field=[r1.predicate],
                   object_match_field=[r2.predicate],
                   match_type=MatchTypeEnum.Lexical,
                   mapping_tool='oaklib'
                   )

def inferred_mapping(oi: BasicOntologyInterface, term: str, r1: RelationshipToTerm, r2: RelationshipToTerm,
                     ruleset: MappingRuleCollection = None) -> Mapping:
    m1 = create_mapping(term, r1, r2)
    m2 = create_mapping(term, r2, r1)
    weightmap: Dict[PRED_CURIE, float] = {}
    best: Tuple[float, Mapping, PRED_CURIE] = None, m1, m1.predicate_id
    if ruleset is not None:
        rules = ruleset.rules
    else:
        rules = []
    for rule in rules:
        inverted = False
        if precondition_holds(rule.preconditions, m1):
            m = m1
        elif not rule.oneway and precondition_holds(rule.preconditions, m2):
            m = m2
            inverted = True
        else:
            m = None
        if m:
            weight = 0.0
            if rule.postconditions.predicate_id:
                m.predicate_id = rule.postconditions.predicate_id
            if rule.postconditions.weight:
                weight = rule.postconditions.weight
            if inverted:
                inv_pred = invert_mapping_predicate(m.predicate_id)
                if inv_pred:
                    m.predicate_id = inv_pred
                else:
                    m = None
            if m:
                if m.predicate_id not in weightmap:
                    weightmap[m.predicate_id] = weight
                else:
                    weightmap[m.predicate_id] += weight
                weight = weightmap[m.predicate_id]
                if best[0] is None or weight > best[0]:
                    best = weight, m, m.predicate_id
                    #print(f' ** BEST {best} ==> {m}')
    best_weight, best_mapping, _ = best
    if best_weight is not None:
        best_mapping.confidence = inverse_logit(best_weight)
    best_mapping.subject_label = oi.get_label_by_curie(best_mapping.subject_id)
    best_mapping.object_label = oi.get_label_by_curie(best_mapping.object_id)
    return best_mapping

def inverse_logit(weight: float) -> float:
    """
    Inverse logit

    https://upload.wikimedia.org/wikipedia/commons/5/57/Logit.png

    :param weight:
    :return: probability between 0 and 1
    """
    return 1/(1+2**(-weight))

def invert_mapping_predicate(pred: PRED_CURIE) -> Optional[PRED_CURIE]:
    if pred == SKOS_EXACT_MATCH or pred == SKOS_CLOSE_MATCH:
        return pred
    if pred == SKOS_BROAD_MATCH:
        return SKOS_NARROW_MATCH
    return None

def precondition_holds(precondition: Precondition, mapping: Mapping) -> bool:
    for k in ['subject_match_field', 'object_match_field']:
        k_one_of = f'{k}_one_of'
        expected_values = getattr(precondition, k_one_of, [])
        actual_values = getattr(mapping, k, [])
        #print(f'CHECKING {actual_values} << {expected_values}')
        if expected_values and not any(v for v in actual_values if v in expected_values ):
            #print('** NO MATCH')
            return False
        #print(f'**** MTCH {k}')
    return True

def apply_transformation(term: str, transformation: LexicalTransformation) -> str:
    """
    Apply an individual transformation on a term

    :param term:
    :param transformation:
    :return:
    """
    typ = str(transformation.type)
    if typ == TransformationType.CaseNormalization.text:
        return term.lower()
    elif typ == TransformationType.WhitespaceNormalization.text:
        return re.sub(" {2,}", " ", term.strip())
    else:
        raise NotImplementedError(f'Transformation Type {typ} {type(typ)} not implemented {TransformationType.CaseNormalization.text}')

    
def save_mapping_rules(mapping_rules: MappingRuleCollection, path: str):
    """
    Saves a YAML using standard mapping of datanodel to YAML

    :param mapping_rules:
    :param path:
    :return:
    """
    yaml_dumper.dump(mapping_rules, to_file=path)

def load_mapping_rules(path: str) -> MappingRuleCollection:
    """
    Loads from a YAML file

    :param path:
    :return:
    """
    return yaml_loader.load(path, target_class=MappingRuleCollection)
