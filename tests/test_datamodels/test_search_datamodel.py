import unittest

from linkml_runtime.utils.introspection import package_schemaview

from oaklib.datamodels import search_datamodel
from oaklib.datamodels.search import create_search_configuration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax

TEST_PROPS = [SearchProperty.LABEL, SearchProperty.ALIAS]


class TestSearchDatamodel(unittest.TestCase):
    def test_create(self):
        """
        Tests the creation of an example instance of the OboGraph datamodel
        """
        sc = create_search_configuration("foo")
        self.assertEqual(sc.search_terms, ["foo"])
        # logging.info(yaml_dumper.dumps(sc))
        self.assertIn(SearchProperty(SearchProperty.LABEL), sc.properties)
        self.assertIn(SearchProperty(SearchProperty.ALIAS), sc.properties)
        sc = create_search_configuration("t/foo")
        self.assertEqual(sc.search_terms, ["foo"])
        # logging.info(yaml_dumper.dumps(sc))
        self.assertEqual(sc.syntax, SearchTermSyntax(SearchTermSyntax.REGULAR_EXPRESSION))
        # logging.info(json_dumper.dumps(sc))
        sc = create_search_configuration("t~foo")
        self.assertEqual(sc.search_terms, ["foo"])
        # logging.info(yaml_dumper.dumps(sc))
        self.assertEqual(sc.is_partial, True)
        sc = create_search_configuration("t=foo")
        self.assertEqual(sc.search_terms, ["foo"])
        # logging.info(yaml_dumper.dumps(sc))
        self.assertEqual(sc.is_partial, False)
        sc = create_search_configuration("t^foo")
        self.assertEqual(sc.search_terms, ["foo"])
        # logging.info(yaml_dumper.dumps(sc))
        self.assertEqual(sc.syntax, SearchTermSyntax(SearchTermSyntax.STARTS_WITH))

    def test_introspect(self):
        """
        Tests ability to introspect the schema and examine the schema elements
        """
        sv = package_schemaview(search_datamodel.__name__)
        assert "search_terms" in sv.all_slots()
        assert "SearchResult" in sv.all_classes()
