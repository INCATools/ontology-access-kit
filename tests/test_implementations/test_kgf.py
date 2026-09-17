"""Tests for the KGF adapter.

The tests that talk to `<https://apps.okn.us/kgf>`_ are skipped when the service
cannot be reached, so the suite still runs offline.
"""

import unittest

import requests

from oaklib import get_adapter
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import HAS_EXACT_SYNONYM, IS_A, LABEL_PREDICATE
from oaklib.implementations.kgf.kgf_implementation import (
    DEFAULT_KGF_BASE_URL,
    KGFImplementation,
    _is_blank,
    _literal_term,
)
from oaklib.interfaces import OboGraphInterface, SearchInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.resource import OntologyResource
from tests import CELLULAR_COMPONENT, NUCLEUS

#: A KGF bundle of the OBO ontologies, used for the ontology-shaped tests.
UBERGRAPH = "ubergraph"
#: One of the smallest bundles on the public service; used where a whole-graph scan is needed.
PHASES = "phaseskg"

BNODE_IRI = (
    "urn:fdc:frink-okn.github.io:20260818:kgf:bnode:v1:sha256:"
    "72c3e0dfbde80d34c6c8192cbb032fcae474043358bcbb6f13bf7c333bd7d29d:sh-1"
)


def _service_is_up() -> bool:
    try:
        return requests.get(DEFAULT_KGF_BASE_URL, timeout=10).ok
    except requests.RequestException:
        return False


SERVICE_IS_UP = _service_is_up()
requires_service = unittest.skipUnless(SERVICE_IS_UP, f"{DEFAULT_KGF_BASE_URL} is unreachable")


class TestKGFSelector(unittest.TestCase):
    """Tests selector parsing, which needs no network access."""

    def test_bare_dataset(self):
        adapter = KGFImplementation(OntologyResource(slug=UBERGRAPH))
        self.assertEqual(UBERGRAPH, adapter.dataset)
        self.assertIsNone(adapter.version)
        self.assertEqual(f"{DEFAULT_KGF_BASE_URL}/{UBERGRAPH}", adapter._dataset_url)

    def test_pinned_version(self):
        adapter = KGFImplementation(OntologyResource(slug=f"{UBERGRAPH}@v0.0.2"))
        self.assertEqual(UBERGRAPH, adapter.dataset)
        self.assertEqual("v0.0.2", adapter.version)
        self.assertEqual(f"{DEFAULT_KGF_BASE_URL}/{UBERGRAPH}/v/v0.0.2", adapter.endpoint_url)

    def test_full_url(self):
        adapter = KGFImplementation(OntologyResource(slug="https://example.org/kgf/mykg@v1.2.3"))
        self.assertEqual("mykg", adapter.dataset)
        self.assertEqual("v1.2.3", adapter.version)
        self.assertEqual("https://example.org/kgf/mykg/v/v1.2.3", adapter.endpoint_url)

    def test_dataset_is_required(self):
        with self.assertRaises(ValueError):
            KGFImplementation(OntologyResource())


class TestKGFTermSyntax(unittest.TestCase):
    """Tests the N-Triples-style term syntax KGF expects, and blank node detection."""

    def test_literal_term(self):
        self.assertEqual('"nucleus"', _literal_term("nucleus"))
        self.assertEqual('"nucleus"@en', _literal_term("nucleus", lang="en"))
        self.assertEqual(
            '"true"^^<http://www.w3.org/2001/XMLSchema#boolean>',
            _literal_term("true", datatype="http://www.w3.org/2001/XMLSchema#boolean"),
        )

    def test_literal_term_escaping(self):
        self.assertEqual(r'"a \"b\" c"', _literal_term('a "b" c'))
        self.assertEqual(r'"a\\b"', _literal_term("a\\b"))
        self.assertEqual(r'"a\nb"', _literal_term("a\nb"))

    def test_is_blank(self):
        self.assertTrue(_is_blank({"type": "bnode", "value": "_:b0"}))
        self.assertTrue(_is_blank({"type": "iri", "value": BNODE_IRI}))
        self.assertFalse(
            _is_blank({"type": "iri", "value": "http://purl.obolibrary.org/obo/GO_0005634"})
        )
        self.assertFalse(_is_blank({"type": "literal", "value": "nucleus"}))


@requires_service
class TestKGFImplementation(unittest.TestCase):
    """Tests :class:`KGFImplementation` against the public FRINK/Proto-OKN service."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.adapter = get_adapter(f"kgf:{UBERGRAPH}")

    def test_interfaces(self):
        self.assertIsInstance(self.adapter, OboGraphInterface)
        self.assertIsInstance(self.adapter, SearchInterface)
        self.assertIsInstance(self.adapter, MappingProviderInterface)

    def test_resolves_current_version(self):
        self.assertTrue(self.adapter.current_version().startswith("v"))
        self.assertIn(
            self.adapter.current_version(), list(self.adapter.ontology_versions(UBERGRAPH))
        )

    def test_ontology_metadata(self):
        metadata = self.adapter.ontology_metadata_map(UBERGRAPH)
        self.assertEqual(["Ubergraph"], metadata["title"])
        self.assertGreater(metadata["count_triples"][0], 0)

    def test_prefix_map_includes_bundle_prefixes(self):
        prefix_map = self.adapter.prefix_map()
        # declared by the bundle manifest rather than by OAK
        self.assertIn("reasoner", prefix_map)
        # OBO prefixes must keep OAK's expansions so that terms compress to GO:nnn
        self.assertEqual("http://purl.obolibrary.org/obo/GO_", prefix_map["GO"])

    def test_label(self):
        self.assertEqual("nucleus", self.adapter.label(NUCLEUS))

    def test_labels_are_batched(self):
        labels = dict(self.adapter.labels([NUCLEUS, CELLULAR_COMPONENT, "GO:9999999"]))
        self.assertEqual("nucleus", labels[NUCLEUS])
        self.assertEqual("cellular_component", labels[CELLULAR_COMPONENT])
        self.assertIsNone(labels["GO:9999999"])

    def test_labels_allow_none_false(self):
        labels = dict(self.adapter.labels(["GO:9999999"], allow_none=False))
        self.assertEqual({}, labels)

    def test_curies_by_label(self):
        self.assertIn(NUCLEUS, self.adapter.curies_by_label("nucleus"))

    def test_definition(self):
        definition = self.adapter.definition(NUCLEUS)
        self.assertIsNotNone(definition)
        self.assertIn("organelle", definition)

    def test_aliases(self):
        alias_map = self.adapter.entity_alias_map(NUCLEUS)
        self.assertEqual(["nucleus"], alias_map[LABEL_PREDICATE])
        self.assertIn("cell nucleus", alias_map[HAS_EXACT_SYNONYM])

    def test_metadata_map(self):
        metadata = self.adapter.entity_metadata_map(NUCLEUS)
        self.assertEqual([NUCLEUS], metadata["id"])
        self.assertIn("owl:Class", metadata["rdf:type"])
        self.assertIn("cellular_component", metadata["oio:hasOBONamespace"])

    def test_owl_types(self):
        self.assertIn((NUCLEUS, "owl:Class"), list(self.adapter.owl_types([NUCLEUS])))

    def test_relationships_by_subject_and_predicate(self):
        objects = {o for _, _, o in self.adapter.relationships([NUCLEUS], predicates=[IS_A])}
        self.assertIn("GO:0043231", objects)
        # anonymous class expressions must not leak out as relationship objects
        self.assertFalse([o for o in objects if "bnode" in o])

    def test_relationships_by_subject_only(self):
        relationships = list(self.adapter.relationships([NUCLEUS]))
        self.assertIn((NUCLEUS, IS_A, "GO:0043231"), relationships)
        # literals are metadata, not relationships
        self.assertFalse([r for r in relationships if r[1] == LABEL_PREDICATE])

    def test_relationships_by_object(self):
        relationships = list(self.adapter.relationships(objects=[NUCLEUS], predicates=[IS_A]))
        self.assertGreater(len(relationships), 0)
        # the bound object position is filled back in from the query
        self.assertEqual({(IS_A, NUCLEUS)}, {(p, o) for _, p, o in relationships})
        subjects = {s for s, _, _ in relationships}
        self.assertIn(NUCLEUS, subjects, "ubergraph materializes reflexive subClassOf")
        self.assertFalse([s for s in subjects if "bnode" in s])

    def test_hierarchical_parents(self):
        self.assertIn("GO:0043231", self.adapter.hierarchical_parents(NUCLEUS))

    def test_node(self):
        node = self.adapter.node(NUCLEUS)
        self.assertEqual(NUCLEUS, node.id)
        self.assertEqual("nucleus", node.lbl)
        self.assertEqual("CLASS", node.type)
        self.assertIn("organelle", node.meta.definition.val)
        self.assertIn("cell nucleus", [s.val for s in node.meta.synonyms])

    def test_node_for_unknown_entity(self):
        self.assertIsNone(self.adapter.node("GO:9999999"))
        with self.assertRaises(ValueError):
            self.adapter.node("GO:9999999", strict=True)

    def test_mappings(self):
        mappings = list(self.adapter.sssom_mappings(NUCLEUS))
        self.assertIn("Wikipedia:Cell_nucleus", [m.object_id for m in mappings])
        self.assertTrue(all(m.subject_id == NUCLEUS for m in mappings))

    def test_search(self):
        results = list(self.adapter.basic_search("cell nucleus"))
        self.assertIn(NUCLEUS, results)

    def test_search_is_exact_by_default(self):
        # "nucleus" is a token of "cell nucleus", but only the whole literal counts
        results = list(self.adapter.basic_search("nucle"))
        self.assertEqual([], results)

    def test_partial_search(self):
        config = SearchConfiguration(is_partial=True, limit=20)
        self.assertIn(NUCLEUS, list(self.adapter.basic_search("cell nucleus", config)))

    def test_search_restricted_to_labels(self):
        config = SearchConfiguration(properties=[SearchProperty.LABEL], limit=20)
        self.assertIn(NUCLEUS, list(self.adapter.basic_search("nucleus", config)))

    def test_starts_with_search(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH, limit=20)
        results = list(self.adapter.basic_search("cell nucleus", config))
        self.assertGreater(len(results), 0)

    def test_search_limit_is_respected(self):
        config = SearchConfiguration(is_partial=True, limit=3)
        self.assertEqual(3, len(list(self.adapter.basic_search("nucleus", config))))

    def test_unsupported_search_syntax(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        with self.assertRaises(NotImplementedError):
            list(self.adapter.basic_search("^nucl", config))


@requires_service
class TestKGFSmallBundle(unittest.TestCase):
    """Whole-graph operations, exercised on a bundle small enough to scan."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.adapter = get_adapter(f"kgf:{PHASES}")

    def test_ontologies(self):
        self.assertEqual([PHASES], list(self.adapter.ontologies()))

    def test_entities(self):
        entities = list(self.adapter.entities())
        self.assertGreater(len(entities), 0)
        self.assertEqual(len(entities), len(set(entities)), "entities must not repeat")
        self.assertFalse([e for e in entities if "bnode" in e])

    def test_entities_of_one_owl_type(self):
        classes = list(self.adapter.entities(owl_type="owl:Class"))
        self.assertGreater(len(classes), 0)
        self.assertTrue(set(classes).issubset(set(self.adapter.entities())))

    def test_obsoletes_are_filtered(self):
        obsoletes = set(self.adapter.obsoletes())
        self.assertFalse(obsoletes.intersection(set(self.adapter.entities())))
        self.assertTrue(obsoletes.issubset(set(self.adapter.entities(filter_obsoletes=False))))


@requires_service
class TestKGFNonOntologyBundle(unittest.TestCase):
    """KGF also serves graphs that are not ontologies; labels come from the manifest."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.adapter = get_adapter("kgf:sockg")

    def test_label_predicates_come_from_the_manifest(self):
        self.assertIn("dct:title", self.adapter._label_predicates())

    def test_label(self):
        crop = "https://idir.uta.edu/sockg-ontology/individuals/Crop.48"
        self.assertEqual("Zea mays (Corn)", self.adapter.label(crop))
