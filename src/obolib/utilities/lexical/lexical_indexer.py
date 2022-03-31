"""
Lexical Utilities
-----------------

Various utilities for working with lexical aspects of ontologies plus mappings

"""
import logging
import re
from collections import defaultdict
from typing import List

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
from obolib.interfaces import BasicOntologyInterface
from obolib.vocabulary.lexical_index import LexicalIndex, LexicalTransformation, TransformationType, RelationshipToTerm, \
    LexicalGrouping, LexicalTransformationPipeline
from obolib.vocabulary.vocabulary import SKOS_EXACT_MATCH
from sssom import Mapping
from sssom.sssom_document import MappingSetDocument
from sssom.util import MappingSetDataFrame, to_mapping_set_dataframe
from sssom.sssom_datamodel import MatchTypeEnum, MappingSet


def create_lexical_index(oi: BasicOntologyInterface,
                         pipelines: List[LexicalTransformationPipeline] = None) -> LexicalIndex:
    """

    :param oi:
    :param pipelines:
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
        mapping_map = oi.get_mappings_by_curie(curie)
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
    return yaml_loader.load(path, target_class=LexicalIndex, source=path)

def lexical_index_to_sssom(oi: BasicOntologyInterface, lexical_index: LexicalIndex, id='default') -> MappingSetDataFrame:
    """
    Transform a lexical index to an SSSOM MappingSetDataFrame by finding all pairs for any given index term

        TODO: Add rules

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
                            mappings.append(create_mapping(oi, term, r1, r2))

        #for r1 in grouping.relationships:
        #    for r2 in grouping.relationships:
        #        if r1.element < r2.element:
        #            mappings.append(create_mapping(oi, term, r1, r2))
    logging.info('Done creating SSSOM mappings')
    mset = MappingSet(mapping_set_id=id, mappings=mappings, license='CC-0')
    #doc = MappingSetDocument(prefix_map=oi.get_prefix_map(), mapping_set=mset)
    doc = MappingSetDocument(prefix_map={}, mapping_set=mset)
    return to_mapping_set_dataframe(doc)


def create_mapping(oi: BasicOntologyInterface, term: str, r1: RelationshipToTerm, r2: RelationshipToTerm) -> Mapping:
    m = Mapping(subject_id=r1.element,
                subject_label=oi.get_label_by_curie(r1.element),
                object_id=r2.element,
                object_label=oi.get_label_by_curie(r2.element),
                predicate_id=SKOS_EXACT_MATCH,
                match_string=term,
                subject_match_field=r1.predicate,
                object_match_field=r2.predicate,
                match_type=MatchTypeEnum.Lexical,
                mapping_tool='obolib'
                )
    return m

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
