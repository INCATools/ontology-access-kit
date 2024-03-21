import logging
import re
from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    TextIO,
    Tuple,
    Union,
)

from kgcl_schema.datamodel import kgcl
from pydantic import BaseModel

from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    HAS_DEFINITION_CURIE,
    IAO_ALTERNATIVE_LABEL,
    IDENTIFIER_PREDICATE,
    RDF_TYPE,
    RDFS_LABEL,
)
from oaklib.implementations.tabular.tabular_implementation import TabularImplementation
from oaklib.interfaces import TextAnnotatorInterface
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    DEFINITION,
    LANGUAGE_TAG,
    METADATA_MAP,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.dumper_interface import DumperInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.merge_interface import MergeInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.obolegacy_interface import OboLegacyInterface
from oaklib.interfaces.owl_interface import OwlInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.summary_statistics_interface import SummaryStatisticsInterface
from oaklib.interfaces.taxon_constraint_interface import TaxonConstraintInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.kgcl_utilities import tidy_change_object

ROBOT_CV_ID = "ID"
ROBOT_CV_LABEL = "LABEL"
ROBOT_CV_DEFINITION = "A definition"
ROBOT_CV_ALTERNATIVE_LABEL = "A alternative term"
ROBOT_CV_TYPE = "TYPE"
ROBOT_CV_C_PCT = "C %"
ROBOT_CV_SUBCLASS = "SC %"

ALIASES = {
    "A rdfs:label": ROBOT_CV_LABEL,
    "A IAO:0000115": ROBOT_CV_DEFINITION,
}

URI_MAP = {
    ROBOT_CV_ID: IDENTIFIER_PREDICATE,
    ROBOT_CV_LABEL: RDFS_LABEL,
    ROBOT_CV_DEFINITION: HAS_DEFINITION_CURIE,
    ROBOT_CV_TYPE: RDF_TYPE,
    ROBOT_CV_ALTERNATIVE_LABEL: IAO_ALTERNATIVE_LABEL,
}

SPEC_COL = str

SPLIT_TOKEN = " SPLIT="  # noqa S105


class TemplateString(BaseModel):
    """
    A robot template string

    https://robot.obolibrary.org/template
    """

    value: str
    """the verbatim value"""

    predicate: Optional[str] = None
    """E.g. ID, LABEL, SC"""

    argument: Optional[str] = None

    split_delimiter: Optional[str] = None

    def parse(self):
        """
        Parse the template string
        """
        v = self.value
        if SPLIT_TOKEN in v:
            v, self.split_delimiter = v.split(SPLIT_TOKEN, 1)
        if " " in v:
            # e.g. "A alternative term"
            # the A should be interpreted as a predicate
            # the rest as an argument
            self.predicate, self.argument = v.split(" ", 1)
        else:
            self.predicate = v
            self.argument = None


def template_slice(
    template: Dict[str, str], rows: List[Dict[str, Any]], spec_cols: Optional[List[SPEC_COL]] = None
) -> List[Dict[str, Any]]:
    """
    Slice the columns of the tabular file.

    >>> template = {"id": "ID", "name": "LABEL", "definition": "A DEFINITION"}
    >>> rows = [ {"id": "X:1", "name": "foo"}, {"id": "X:2", "name": "bar", "definition": "A bar"} ]
    >>> spec_cols = ["LABEL"]
    >>> template_slice(template, rows, spec_cols)
    [{'LABEL': 'foo'}, {'LABEL': 'bar'}]


    Multiple columns:

    >>> template_slice(template, rows, ["ID", "LABEL"])
    [{'ID': 'X:1', 'LABEL': 'foo'}, {'ID': 'X:2', 'LABEL': 'bar'}]

    There is more than one way to specify a template mapping; this is equivalent

    >>> template = {"id": "ID", "name": "A rdfs:label", "definition": "A DEFINITION"}

    It is still necessary to query by the canonical form; the results will be identical

    >>> template_slice(template, rows, spec_cols)
    [{'LABEL': 'foo'}, {'LABEL': 'bar'}]

    >>> template = {"id": "ID", "name": "A rdfs:label SPLIT=|", "definition": "A DEFINITION"}
    >>> template_slice(template, rows, spec_cols)
    [{'LABEL': ['foo']}, {'LABEL': ['bar']}]

    :param self:
    :param spec_cols:
    :param template:
    :param rows:
    :return:
    """
    split_aliases = {}
    canonical_to_local_map = {}
    split_by_col = {}
    for k, v in template.items():
        norm_v = v
        if SPLIT_TOKEN in v:
            truncated, sep = v.split(SPLIT_TOKEN, 1)
            split_aliases[truncated] = v
            split_by_col[k] = sep
            norm_v = truncated
        if norm_v in ALIASES:
            norm_v = ALIASES[norm_v]
        canonical_to_local_map[norm_v] = v
    spec2col = {spec: col for col, spec in template.items()}
    if spec_cols is None:
        spec_cols = [ALIASES.get(spec, spec) for spec in spec2col.keys()]
    else:
        if any(spec in ALIASES for spec in spec_cols):
            raise ValueError(f"Alias in spec_cols: {spec_cols}")

    def lookup_value_in_row(row: Dict[str, Any], spec: str) -> Optional[Any]:
        norm_spec = canonical_to_local_map.get(spec, spec)
        spec = spec2col.get(norm_spec, norm_spec)
        if spec:
            rv = row.get(spec, None)
            if rv is not None and spec in split_by_col:
                sep_token = split_by_col[spec]
                rv = rv.split(sep_token)
            return rv
        else:
            return None

    return [{spec: lookup_value_in_row(row, spec) for spec in spec_cols} for row in rows]


def template_modify(
    curie: CURIE, template: Dict[str, str], rows: List[Dict[str, Any]], update_map: Dict[str, Any]
) -> bool:
    """
    Modify a template value

    >>> template = {"id": "ID", "name": "LABEL", "definition": "A DEFINITION"}
    >>> rows = [ {"id": "X:1", "name": "foo"}, {"id": "X:2", "name": "bar", "definition": "A bar"} ]
    >>> template_modify("X:2", template, rows, {"LABEL": "baz"})
    True
    >>> template_slice(template, rows)
    [{'ID': 'X:1', 'LABEL': 'foo', 'A DEFINITION': None}, {'ID': 'X:2', 'LABEL': 'baz', 'A DEFINITION': 'A bar'}]

    :param self:
    :param spec_cols:
    :param template:
    :param rows:
    :return:
    """
    rev_aliases = {v: k for k, v in ALIASES.items()}
    spec2col = {spec: col for col, spec in template.items()}

    def lookup_value_in_row(row: Dict[str, Any], spec: str):
        if spec in spec2col:
            return row.get(spec2col[spec], None)
        if spec in rev_aliases:
            col = spec2col.get(rev_aliases[spec], None)
            if col:
                return row.get(col, None)
        return None

    for row in rows:
        this_curie = lookup_value_in_row(row, ROBOT_CV_ID)
        if this_curie == curie:
            for spec, value in update_map.items():
                col = spec2col.get(spec, None)
                if not col:
                    col = spec2col.get(rev_aliases[spec], None)
                if not col:
                    raise ValueError(f"Unknown spec: {spec}")
                row[col] = value
            return True
    return False


def template_slice_as_map(
    template: Dict[str, str], rows: List[Dict[str, Any]], spec_cols: Optional[List[SPEC_COL]] = None
) -> Dict[CURIE, Dict[str, Any]]:
    """
    Slice the columns of the tabular file as a map.

    >>> template = {"id": "ID", "name": "LABEL", "definition": "A DEFINITION"}
    >>> rows = [ {"id": "X:1", "name": "foo"}, {"id": "X:2", "name": "bar", "definition": "A bar"} ]
    >>> spec_cols = ["LABEL"]
    >>> template_slice_as_map(template, rows, spec_cols)
    {'X:1': {'ID': 'X:1', 'LABEL': 'foo'}, 'X:2': {'ID': 'X:2', 'LABEL': 'bar'}}

    :param template:
    :param rows:
    :param spec_cols:
    :return:
    """
    m = {}
    # if spec_cols is None:
    #    spec_cols = list(template.values())
    if spec_cols is not None and ROBOT_CV_ID not in spec_cols:
        spec_cols = [ROBOT_CV_ID] + spec_cols
    for row in template_slice(template, rows, spec_cols):
        curie = row[ROBOT_CV_ID]
        if curie in m:
            raise ValueError(f"Duplicate curie: {curie}: {row} plus {m[curie]}")
        m[curie] = row
    return m


@dataclass
class RobotTemplateImplementation(
    TabularImplementation,
    ValidatorInterface,
    DifferInterface,
    RdfInterface,
    OboGraphInterface,
    OboLegacyInterface,
    SearchInterface,
    MappingProviderInterface,
    PatcherInterface,
    SummaryStatisticsInterface,
    SemanticSimilarityInterface,
    TaxonConstraintInterface,
    TextAnnotatorInterface,
    DumperInterface,
    MergeInterface,
    OwlInterface,
):
    """
    Simple ROBOT-template backed implementation.

    .. note::

        Highly incomplete!
    """

    _curie2label_map: Optional[Dict[CURIE, str]] = None
    _label2curie_map: Optional[Dict[str, CURIE]] = None
    _row_by_curie: Optional[Dict[CURIE, Tuple[str, Dict[str, Any]]]] = None

    @property
    def curie2label_map(self) -> Dict[CURIE, str]:
        """
        Return a map from curie to label.

        :return:
        """
        if self._curie2label_map is None:
            m = self._slice_as_map([ROBOT_CV_ID, ROBOT_CV_LABEL])
            self._curie2label_map = {
                curie: row.get(ROBOT_CV_LABEL, None) for curie, row in m.items()
            }
        return self._curie2label_map

    @property
    def label2curie_map(self) -> Dict[str, CURIE]:
        """
        Return a map from label to curie.

        :return:
        """
        if self._label2curie_map is None:
            self._label2curie_map = {label: curie for curie, label in self.curie2label_map.items()}
        return self._label2curie_map

    def _slice(self, cols: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Slice the columns of the tabular file.

        :param cols:
        :return:
        """
        for tf in self.tabfile_map.values():
            data = tf.rows
            tmpl = data[0]
            rows = data[1:]
            return template_slice(tmpl, rows, cols)

    def _modify(self, curie: CURIE, update_map: Dict[str, Any]) -> bool:
        """
        Modify a template value

        :param curie:
        :param update_map:
        :return:
        """
        for tf in self.tabfile_map.values():
            data = tf.rows
            tmpl = data[0]
            rows = data[1:]
            success = template_modify(curie, tmpl, rows, update_map)
            if success:
                self._clear_cache()
                return True
        return False

    def _clear_cache(self):
        self._label2curie_map = None
        self._curie2label_map = None
        self._row_by_curie = None

    def _slice_as_map(self, cols: Optional[List[str]] = None) -> Dict[CURIE, Dict[str, Any]]:
        """
        Slice the columns of the tabular file as a map

        :param cols:
        :return:
        """
        m = {}
        for tf in self.tabfile_map.values():
            data = tf.rows
            if len(data) == 0:
                continue
            tmpl = data[0]
            all_rows = data[1:]
            for curie, rows in template_slice_as_map(tmpl, all_rows, cols).items():
                if curie in m:
                    raise ValueError(f"Duplicate curie: {curie}: {rows} plus {m[curie]}")
                m[curie] = rows
        return m

    @property
    def row_by_curie(self) -> Tuple[str, Dict[str, Any]]:
        """
        Return the row for the curie.

        :param curie:
        :return:
        """
        if self._row_by_curie is None:
            self._row_by_curie = {}
            for tf in self.tabfile_map.values():
                data = tf.rows
                tmpl = data[0]
                all_rows = data[1:]
                for curie, row in template_slice_as_map(tmpl, all_rows).items():
                    self._row_by_curie[curie] = (tf.name, row)
        return self._row_by_curie

    def entities(self, filter_obsoletes=True, owl_type=None, **kwargs) -> Iterable[CURIE]:
        """
        Return the entities in the ontology.

        :param filter_obsoletes:
        :param owl_type:
        :param kwargs:
        :return:
        """
        yield from self._slice_as_map([ROBOT_CV_ID]).keys()

    def labels(
        self,
        curies: Iterable[CURIE],
        allow_none=True,
        lang: LANGUAGE_TAG = None,
        **kwargs,
    ) -> Iterable[Tuple[CURIE, str]]:
        """
        Return the labels for the entities.

        :param curies:
        :param allow_none:
        :param lang:
        :param kwargs:
        :return:
        """
        m = self.curie2label_map
        for curie in curies:
            if curie in m:
                yield curie, m[curie]
            elif allow_none:
                yield curie, None

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        """
        Return the label for the entity.

        :param curie:
        :param lang:
        :return:
        """
        return self.curie2label_map.get(curie, None)

    def curies_by_label(self, label: str, **kwargs) -> List[CURIE]:
        """
        Return the curies for the label.

        :param label:
        :param kwargs:
        :return:
        """
        curie = self.label2curie_map.get(label, None)
        if curie:
            return [curie]
        return []

    def definitions(
        self,
        curies: Iterable[CURIE],
        include_metadata=False,
        include_missing=False,
        lang: Optional[LANGUAGE_TAG] = None,
    ) -> Iterator[DEFINITION]:
        """
        Return the definitions for the entities.

        :param curies:
        :param include_metadata:
        :param include_missing:
        :param lang:
        :return:
        """
        m = self._slice_as_map([ROBOT_CV_ID, ROBOT_CV_DEFINITION])
        for curie in curies:
            if curie in m:
                yield curie, m[curie].get(ROBOT_CV_DEFINITION, None), None
            elif include_missing:
                yield curie, None, None

    def definition(
        self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None, **kwargs
    ) -> Optional[str]:
        """
        Return the definition for the entity.

        :param curie:
        :param lang:
        :param kwargs:
        :return:
        """
        defns = list(self.definitions([curie], lang=lang))
        if len(defns) == 0:
            return None
        return defns[0][1]

    def entity_metadata_map(self, curie: CURIE, **kwargs) -> METADATA_MAP:
        """
        Return the metadata for the entity.

        :param curie:
        :param kwargs:
        :return:
        """
        name, row = self.row_by_curie[curie]
        metadata = {"source": name}
        for k, v in row.items():
            p = URI_MAP.get(k, None)
            if not p:
                if k.startswith("A "):
                    p = k[2:]
            if not p:
                # URL-encode k using urllib.parse.quote_plus
                p = f"_:{k}"
            metadata[p] = v
        return metadata

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        """
        Return the aliases for the entity.

        :param curie:
        :return:
        """
        # This hardcodes use of IAO as label vocabulary
        m = self._slice_as_map([ROBOT_CV_ID, ROBOT_CV_ALTERNATIVE_LABEL])
        if curie in m:
            alts = m[curie].get(ROBOT_CV_ALTERNATIVE_LABEL, [])
            if not isinstance(alts, list):
                alts = [alts]
            return {IAO_ALTERNATIVE_LABEL: alts}

    def basic_search(
        self, search_term: str, config: Optional[SearchConfiguration] = None
    ) -> Iterable[CURIE]:
        if config is None:
            config = SearchConfiguration()
        matches = []
        # TODO: DRY
        if config.syntax == SearchTermSyntax(SearchTermSyntax.STARTS_WITH):
            mfunc = lambda label: str(label).startswith(search_term)
        elif config.syntax == SearchTermSyntax(SearchTermSyntax.REGULAR_EXPRESSION):
            prog = re.compile(search_term)
            mfunc = lambda label: prog.search(label)
        elif config.is_partial:
            mfunc = lambda label: search_term in str(label)
        else:
            mfunc = lambda label: label == search_term
        search_all = SearchProperty(SearchProperty.ANYTHING) in config.properties
        logging.info(f"SEARCH={search_term}")
        for t in self.entities(filter_obsoletes=False):
            lbl = self.label(t)
            logging.debug(f"T={t} // {config}")
            if (
                search_all
                or SearchProperty(SearchProperty.LABEL)
                or config.properties not in config.properties
            ):
                if lbl and mfunc(lbl):
                    matches.append(t)
                    logging.info(f"Name match to {t}")
                    continue
            if search_all or SearchProperty(SearchProperty.IDENTIFIER) in config.properties:
                if mfunc(t):
                    matches.append(t)
                    logging.info(f"identifier match to {t}")
                    continue
        for m in matches:
            yield m

    def dump(self, path: Union[str, TextIO] = None, syntax: str = None, **kwargs):
        if syntax is None:
            syntax = "robottemplate"
        if syntax != "robottemplate":
            raise NotImplementedError(f"Syntax {syntax} not supported")
        super().dump(path, syntax, **kwargs)

    def set_label(self, curie: CURIE, label: str, lang: Optional[LANGUAGE_TAG] = None) -> bool:
        if lang:
            raise NotImplementedError("Language tags not supported")
        return self._modify(curie, {ROBOT_CV_LABEL: label})

    def set_definition(
        self,
        curie: CURIE,
        value: str,
        lang: Optional[LANGUAGE_TAG] = None,
        sources: Optional[List] = None,
    ) -> bool:
        if lang:
            raise NotImplementedError("Language tags not supported")
        return self._modify(curie, {ROBOT_CV_DEFINITION: value})

    def apply_patch(
        self,
        patch: kgcl.Change,
        activity: kgcl.Activity = None,
        metadata: Mapping[PRED_CURIE, Any] = None,
        configuration: kgcl.Configuration = None,
    ) -> kgcl.Change:
        tidy_change_object(patch)
        logging.debug(f"Applying {patch}")
        modified_entities = []
        if isinstance(patch, kgcl.NodeRename):
            # self.set_label(patch.about_node, _clean(patch.new_value))
            self.set_label(patch.about_node, patch.new_value)
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.NewTextDefinition):
            # self.set_label(patch.about_node, _clean(patch.new_value))
            self.set_definition(patch.about_node, patch.new_value)
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.NodeCreation):
            raise NotImplementedError("NodeCreation not supported - don't know which template")
        else:
            raise NotImplementedError(f"Patch type {type(patch)} not supported")
