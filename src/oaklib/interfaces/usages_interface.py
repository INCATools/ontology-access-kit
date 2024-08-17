import logging
from abc import ABC
from enum import Enum
from typing import Iterable, List, Optional

from pydantic import BaseModel

from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import MappingProviderInterface, OboGraphInterface
from oaklib.interfaces.association_provider_interface import AssociationProviderInterface
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

logger = logging.getLogger(__name__)


class UsageContext(str, Enum):
    """
    The context of a usage
    """

    RELATIONSHIP_SUBJECT = "relationship_subject"
    RELATIONSHIP_OBJECT = "relationship_object"
    RELATIONSHIP_PREDICATE = "relationship_predicate"
    LOGICAL_DEFINITION_GENUS = "logical_definition_genus"
    LOGICAL_DEFINITION_PREDICATE = "logical_definition_predicate"
    LOGICAL_DEFINITION_FILLER = "logical_definition_filler"
    ASSOCIATION_SUBJECT = "association_subject"
    ASSOCIATION_PREDICATE = "association_predicate"
    ASSOCIATION_OBJECT = "association_object"
    MAPPING_SUBJECT = "mapping_subject"
    MAPPING_OBJECT = "mapping_object"
    MULTIPLE = "multiple"


class Usage(BaseModel):
    """
    Represents a usage of a term
    """

    used_id: str
    used_by_id: str
    predicate: Optional[str] = None
    source: str
    dataset: Optional[str] = None
    context: UsageContext
    axiom: Optional[str] = None
    description: Optional[str] = None


class UsagesInterface(BasicOntologyInterface, ABC):
    """
    Allows querying for usages of terms
    """

    def usages(
        self,
        curies: List[CURIE],
        used_by: Optional[List[CURIE]] = None,
        used_by_prefixes: Optional[List[str]] = None,
        include_unused: bool = False,
        **kwargs,
    ) -> Iterable[Usage]:
        """
        Get usages of a term

        :param curies:
        :param used_by:
        :param used_by_prefixes:
        :param include_unused:
        :param kwargs:
        :return:
        """
        logger.info(f"Getting usages for {curies}, prefixes={used_by_prefixes}")

        used_curies = set()
        if used_by or used_by_prefixes:
            for usage in self.usages(curies, **kwargs):
                ok = True
                if used_by:
                    if usage.used_by_id not in used_by:
                        ok = False
                if used_by_prefixes:
                    if not any(usage.used_by_id.startswith(p) for p in used_by_prefixes):
                        ok = False
                if not ok:
                    logger.debug(f"Skipping {usage} as not in used_by")
                if ok:
                    yield usage
                    used_curies.add(usage.used_id)
            return

        def _source_id():
            return self.implementation_name

        logger.info(f"Checking relationships subjects for {len(curies)} curies")
        for s, p, o in self.relationships(curies):
            yield Usage(
                used_id=s,
                used_by_id=o,
                predicate=p,
                source=_source_id(),
                context=UsageContext.RELATIONSHIP_SUBJECT,
            )
            used_curies.add(s)
        logger.info(f"Checking relationships objects for {len(curies)} curies")
        for s, p, o in self.relationships(objects=curies):
            yield Usage(
                used_id=o,
                used_by_id=s,
                predicate=p,
                source=_source_id(),
                context=UsageContext.RELATIONSHIP_OBJECT,
            )
            used_curies.add(o)
        logger.info(f"Checking relationships predicates for {len(curies)} curies")
        for _s, p, o in self.relationships(predicates=curies):
            # TODO: used_by is a relationship
            yield Usage(
                used_id=p,
                used_by_id=o,
                predicate=p,
                source=_source_id(),
                context=UsageContext.RELATIONSHIP_PREDICATE,
            )
            used_curies.add(p)
        logger.info(f"Checking logical definitions for {len(curies)} curies")
        if isinstance(self, OboGraphInterface):
            for ldef in self.logical_definitions(objects=curies):
                for genus in ldef.genusIds:
                    if genus in curies:
                        yield Usage(
                            used_id=ldef.definedClassId,
                            used_by_id=genus,
                            predicate=IS_A,
                            source=_source_id(),
                            context=UsageContext.LOGICAL_DEFINITION_GENUS,
                        )
                        used_curies.add(ldef.definedClassId)
                for r in ldef.restrictions:
                    if r.propertyId in curies:
                        yield Usage(
                            used_id=ldef.definedClassId,
                            used_by_id=r.fillerId,
                            predicate=r.propertyId,
                            source=_source_id(),
                            context=UsageContext.LOGICAL_DEFINITION_PREDICATE,
                        )
                        used_curies.add(ldef.definedClassId)
                    if r.fillerId in curies:
                        yield Usage(
                            used_id=ldef.definedClassId,
                            used_by_id=r.fillerId,
                            predicate=r.propertyId,
                            source=_source_id(),
                            context=UsageContext.LOGICAL_DEFINITION_FILLER,
                        )
                        used_curies.add(ldef.definedClassId)
        logger.info(f"Checking associations for {len(curies)} curies")
        if isinstance(self, AssociationProviderInterface):
            for a in self.associations(objects=curies, object_closure_predicates=[]):
                yield Usage(
                    used_id=a.subject,
                    used_by_id=a.object,
                    predicate=a.predicate,
                    source=_source_id(),
                    context=UsageContext.ASSOCIATION_OBJECT,
                )
                used_curies.add(a.subject)
        logger.info(f"Checking mappings for {len(curies)} curies")
        if isinstance(self, MappingProviderInterface):
            for m in self.sssom_mappings(curies):
                if m.subject_id in curies:
                    yield Usage(
                        used_id=m.subject_id,
                        used_by_id=m.object_id,
                        predicate=m.predicate_id,
                        source=_source_id(),
                        context=UsageContext.MAPPING_SUBJECT,
                    )
                    used_curies.add(m.subject_id)
                elif m.object_id in curies:
                    yield Usage(
                        used_id=m.object_id,
                        used_by_id=m.subject_id,
                        predicate=m.predicate_id,
                        source=_source_id(),
                        context=UsageContext.MAPPING_OBJECT,
                    )
                    used_curies.add(m.object_id)
                else:
                    raise AssertionError(f"Mapping {m} not in curies {curies}")
        if include_unused:
            for c in curies:
                if c not in used_curies:
                    yield Usage(
                        used_id=c,
                        used_by_id="None",
                        source=_source_id(),
                        context=UsageContext.MULTIPLE,
                    )
