import csv
import json
import logging
import re
import subprocess
import sys
import unittest
from typing import Optional

import rdflib
import yaml
from click.testing import CliRunner
from kgcl_schema.datamodel.kgcl import MappingCreation, NodeChange, RemoveMapping
from linkml_runtime.loaders import json_loader, yaml_loader
from sssom.parsers import parse_sssom_table, to_mapping_set_document

from oaklib import get_adapter
from oaklib.cli import clear_cli_settings, main
from oaklib.datamodels import fhir, obograph, taxon_constraints
from oaklib.datamodels.vocabulary import (
    IN_TAXON,
    IS_A,
    SKOS_CLOSE_MATCH,
    SKOS_EXACT_MATCH,
)
from oaklib.utilities.kgcl_utilities import parse_kgcl_files
from tests import (
    ATOM,
    CATALYTIC_ACTIVITY,
    CELL,
    CELLULAR_COMPONENT,
    CHEBI_NUCLEUS,
    CYTOPLASM,
    EUKARYOTA,
    IMBO,
    INPUT_DIR,
    INTRACELLULAR,
    MEMBRANE,
    NUCLEAR_ENVELOPE,
    NUCLEAR_MEMBRANE,
    NUCLEATED,
    NUCLEUS,
    OUTPUT_DIR,
    PHENOTYPIC_ABNORMALITY,
    SHAPE,
    VACUOLE,
)

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_SIMPLE_OBO = f'simpleobo:{INPUT_DIR / "go-nucleus.obo"}'
TEST_OBOJSON = INPUT_DIR / "go-nucleus.json"
TEST_OWL_RDF = INPUT_DIR / "go-nucleus.owl.ttl"
TEST_OWL_OFN = INPUT_DIR / "go-nucleus.ofn"
TEST_OBO_1 = INPUT_DIR / "entailment-tutorial.obo"
TEST_OBO_2 = INPUT_DIR / "entailment-tutorial-2.obo"
TEST_DB = INPUT_DIR.joinpath("go-nucleus.db")
BAD_ONTOLOGY_DB = INPUT_DIR / "bad-ontology.db"
TEST_OUT = str(OUTPUT_DIR / "tmp")
TEST_OUT_OBO = str(OUTPUT_DIR / "tmp.obo")
TEST_OUT2 = str(OUTPUT_DIR / "tmp-v2")
MAPPING_DIFF_TEST_OBO = INPUT_DIR / "unreciprocated-mapping-test.obo"
TEST_SSSOM_MAPPING = INPUT_DIR / "unreciprocated-mapping-test.sssom.tsv"
TEST_SYNONYMIZER_OBO = "simpleobo:" + str(INPUT_DIR / "synonym-test.obo")
RULES_FILE = INPUT_DIR / "matcher_rules.yaml"
SYNONYMIZER_RULES_FILE = INPUT_DIR / "cli-synonymizer-rules.yaml"


def _outpath(test: str, fmt: str = "tmp") -> str:
    return str(OUTPUT_DIR / test) + "." + fmt


class TestCommandLineInterface(unittest.TestCase):
    """
    Tests all command-line subcommands
    """

    def setUp(self) -> None:
        # TODO. Use contexts. https://stackoverflow.com/questions/64381222/python-click-access-option-values-globally
        clear_cli_settings()
        runner = CliRunner(mix_stderr=False)
        self.runner = runner

    def _out(self, path: Optional[str] = TEST_OUT) -> str:
        with open(path) as f:
            return "".join(f.readlines())

    def test_main_help(self):
        result = self.runner.invoke(main, ["--help"])
        out = result.stdout
        print("STDERR", result.stderr)
        self.assertIn("search", out)
        self.assertIn("subset", out)
        self.assertIn("validate", out)
        self.assertEqual(0, result.exit_code)

    def test_multilingual(self):
        for input_arg in [INPUT_DIR / "hp-international-test.db"]:
            results = self.runner.invoke(main, ["-i", str(input_arg), "languages"])
            self.assertEqual(0, results.exit_code)
            self.assertIn("fr", results.stdout)
            self.assertIn("nl", results.stdout)
            results = self.runner.invoke(
                main, ["--preferred-language", "nl", "-i", str(input_arg), "languages"]
            )
            self.assertEqual(0, results.exit_code)
            self.assertIn("nl*", results.stdout)
            self.assertIn("fr", results.stdout)
            result = self.runner.invoke(
                main,
                [
                    "--preferred-language",
                    "fr",
                    "-i",
                    str(input_arg),
                    "labels",
                    PHENOTYPIC_ABNORMALITY,
                ],
            )
            self.assertEqual(0, result.exit_code)
            self.assertIn("Anomalie phénotypique", result.stdout, "French label should be present")

    def test_languages(self):
        for input_arg in [INPUT_DIR / "hp-international-test.db"]:
            results = self.runner.invoke(main, ["-i", str(input_arg), "languages"])
            self.assertEqual(0, results.exit_code)
            self.assertIn("fr", results.stdout)
            self.assertIn("nl", results.stdout)
            results = self.runner.invoke(
                main, ["--preferred-language", "nl", "-i", str(input_arg), "languages"]
            )
            self.assertEqual(0, results.exit_code)
            self.assertIn("nl*", results.stdout)
            self.assertIn("fr", results.stdout)

    def test_info(self):
        for input_arg in [TEST_ONT, f"sqlite:{TEST_DB}", TEST_OWL_RDF]:
            result = self.runner.invoke(
                main,
                ["-i", str(input_arg), "info", NUCLEUS, "-o", TEST_OUT, "-D", "x,d"],
            )
            print("STDERR", result.stdout)
            print("STDERR", result.stderr)
            self.assertEqual(0, result.exit_code)
            with open(TEST_OUT) as file:
                contents = "\n".join(file.readlines())
                self.assertIn(NUCLEUS, contents)
                self.assertIn("Wikipedia:Cell_nucleus", contents)
                self.assertIn("A membrane-bounded organelle", contents)
            result = self.runner.invoke(
                main, ["-i", str(input_arg), "info", NUCLEUS, "-o", TEST_OUT, "-D", "x"]
            )
            print("STDERR", result.stdout)
            print("STDERR", result.stderr)
            self.assertEqual(0, result.exit_code)
            with open(TEST_OUT) as file:
                contents = "\n".join(file.readlines())
                self.assertIn(NUCLEUS, contents)
                self.assertIn("Wikipedia:Cell_nucleus", contents)
                self.assertNotIn("A membrane-bounded organelle", contents)

    def test_labels(self):
        for input_arg in [f"sqlite:{TEST_DB}"]:
            result = self.runner.invoke(main, ["-i", str(input_arg), "labels", ".all"])
            assert "cytoplasm" in result.stdout
            assert "IAO:0000078" in result.stdout
            result = self.runner.invoke(
                main,
                ["-i", str(input_arg), "labels", ".all", "--if-absent", "present-only"],
            )
            assert "cytoplasm" in result.stdout
            assert "IAO:0000078" not in result.stdout
            result = self.runner.invoke(
                main,
                ["-i", str(input_arg), "labels", ".all", "--if-absent", "absent-only"],
            )
            assert "cytoplasm" not in result.stdout
            assert "IAO:0000078" in result.stdout

    def test_definitions(self):
        for input_arg in [f"sqlite:{TEST_DB}"]:
            result = self.runner.invoke(main, ["-i", str(input_arg), "definitions", ".all"])
            self.assertIn("cytoplasm", result.stdout, "cytoplasm should be defined in .all")
            self.assertIn("IAO:0000078", result.stdout, "IAO:0000078 should be included in .all")
            result = self.runner.invoke(
                main,
                [
                    "-i",
                    str(input_arg),
                    "definitions",
                    ".all",
                    "--if-absent",
                    "present-only",
                ],
            )
            self.assertIn(
                "cytoplasm",
                result.stdout,
                "cytoplasm should be included with present-only query",
            )
            self.assertNotIn("IAO:0000078", result.stdout)
            result = self.runner.invoke(
                main,
                [
                    "-i",
                    str(input_arg),
                    "definitions",
                    ".all",
                    "--if-absent",
                    "absent-only",
                ],
            )
            self.assertNotIn(
                "cytoplasm",
                result.stdout,
                "cytoplasm should be excluded with absent-only query",
            )
            self.assertIn("IAO:0000078", result.stdout)
            result = self.runner.invoke(
                main,
                [
                    "-i",
                    str(input_arg),
                    "definitions",
                    "--additional-metadata",
                    "cytoplasm",
                ],
            )
            self.assertIn(
                "ISBN:0198547684",
                result.stdout,
                "cytoplasm should be included in additional metadata",
            )

    # OBOGRAPH

    def test_obograph_local(self):
        outpath = _outpath("obograph_local")
        # inputs = [str(TEST_ONT), f"sqlite:{TEST_DB}", str(TEST_OWL_RDF)]
        inputs = [str(TEST_ONT), f"sqlite:{TEST_DB}"]
        for input_arg in inputs:
            logging.info(f"INPUT={input_arg}")
            self.runner.invoke(main, ["-i", input_arg, "ancestors", NUCLEUS, "-o", outpath])
            out = self._out(outpath)
            assert "GO:0043226" in out
            self.runner.invoke(
                main,
                [
                    "-i",
                    input_arg,
                    "ancestors",
                    "-p",
                    "i",
                    "plasma membrane",
                    "-o",
                    outpath,
                ],
            )
            out = self._out(outpath)
            assert "GO:0016020" in out
            assert "GO:0043226" not in out
            self.runner.invoke(
                main,
                [
                    "-i",
                    input_arg,
                    "descendants",
                    "-p",
                    "i",
                    "GO:0016020",
                    "-o",
                    outpath,
                ],
            )
            out = self._out(outpath)
            # TODO:
            # assert 'GO:0016020 ! membrane' not in out
            assert "GO:0043226" not in out
            # test fetching ancestor graph and saving as obo
            outpath_obo = _outpath("obograph_local-tmp", "obo")
            self.runner.invoke(
                main,
                [
                    "-i",
                    input_arg,
                    "descendants",
                    "-p",
                    "i,p",
                    MEMBRANE,
                    "-O",
                    "obo",
                    "-o",
                    outpath_obo,
                ],
            )
            self.runner.invoke(main, ["-i", outpath_obo, "info", ".all", "-o", outpath])
            out = self._out(outpath)
            logging.info(out)
            self.assertIn(MEMBRANE, out, f"reflexive by default, input={input_arg}")
            self.assertIn("GO:0031965", out)
            self.assertNotIn("subClassOf", out)
            self.assertNotIn("BFO", out)

    def test_logical_definitions(self):
        for input_arg in [str(TEST_ONT), f"sqlite:{TEST_DB}"]:
            logging.info(f"INPUT={input_arg}")
            result = self.runner.invoke(
                main,
                [
                    "-i",
                    input_arg,
                    "logical-definitions",
                    "--unmelt",
                    "-O",
                    "csv",
                    ".all",
                    "-o",
                    TEST_OUT,
                ],
            )
            self.assertEqual(0, result.exit_code)
            out = self._out(TEST_OUT)
            logging.info(out)
            cases = [
                {
                    "defined_class": "GO:0004857",
                    "defined_class_label": "enzyme inhibitor activity",
                    "genus_class": "GO:0003674",
                    "genus_class_label": "molecular_function",
                    "negatively_regulates": "GO:0003824",
                    "negatively_regulates_label": "catalytic activity",
                    "part_of": "",
                    "part_of_label": "",
                    "has_primary_input_or_output": "",
                    "has_primary_input_or_output_label": "",
                    "positively_regulates": "",
                    "positively_regulates_label": "",
                    "regulates": "",
                    "regulates_label": "",
                    "has_part": "",
                    "has_part_label": "",
                },
                {
                    "defined_class": "GO:0099568",
                    "defined_class_label": "cytoplasmic region",
                    "genus_class": "GO:0005737",
                    "genus_class_label": "cytoplasm",
                    "negatively_regulates": "",
                    "negatively_regulates_label": "",
                    "part_of": "GO:0005737",
                    "part_of_label": "cytoplasm",
                    "has_primary_input_or_output": "",
                    "has_primary_input_or_output_label": "",
                    "positively_regulates": "",
                    "positively_regulates_label": "",
                    "regulates": "",
                    "regulates_label": "",
                    "has_part": "",
                    "has_part_label": "",
                },
            ]
            with open(TEST_OUT) as file:
                reader = csv.DictReader(file, delimiter="\t")
                rows = [row for row in reader]
                for case in cases:
                    self.assertIn(case, rows)

    def test_gap_fill(self):
        result = self.runner.invoke(
            main,
            [
                "-i",
                str(TEST_DB),
                "viz",
                "--gap-fill",
                "-p",
                f"i,p,{IN_TAXON}",
                NUCLEUS,
                VACUOLE,
                CELLULAR_COMPONENT,
                "-O",
                "json",
                "-o",
                TEST_OUT,
            ],
        )
        print("STDERR", result.stdout)
        print("STDERR", result.stderr)
        self.assertEqual(0, result.exit_code)
        contents = self._out()
        self.assertIn(NUCLEUS, contents)
        self.assertIn(VACUOLE, contents)
        self.assertIn(CELLULAR_COMPONENT, contents)
        # parse json to check it conforms
        with open(TEST_OUT) as f:
            g = json.load(f)
            nodes = g["nodes"]
            g["edges"]
            [nucleus_node] = [n for n in nodes if n["id"] == NUCLEUS]
            self.assertEqual(nucleus_node["lbl"], "nucleus")

    def test_roots_and_leafs(self):
        # TODO: improve performance for ttl
        for input_arg in [str(TEST_ONT), f"sqlite:{TEST_DB}", str(TEST_OWL_RDF)]:
            result = self.runner.invoke(main, ["-i", input_arg, "roots", "-p", "i"])
            out = result.stdout
            assert "CHEBI:36342" in out
            result = self.runner.invoke(main, ["-i", input_arg, "leafs", "-p", "i"])
            out = result.stdout
            assert NUCLEAR_ENVELOPE in out
            result = self.runner.invoke(main, ["-i", input_arg, "singletons", "-p", "i"])
            out = result.stdout
            assert NUCLEAR_ENVELOPE not in out

    def test_paths(self):
        """Test paths command on core adapters"""
        cases = [
            ([NUCLEAR_MEMBRANE], VACUOLE, False, "endomembrane system", None),
            ([NUCLEAR_MEMBRANE], VACUOLE, True, "endomembrane system", None),
            ([CELL], VACUOLE, True, "", "GO"),
            ([VACUOLE], CELL, True, "cytoplasm", None),
        ]
        for input_arg in [TEST_ONT, TEST_DB, TEST_OWL_RDF, TEST_SIMPLE_OBO]:
            for case in cases:
                args, target, directed, expected, unexpected = case
                all_args = ["-i", input_arg, "paths", "--target", target, *args]
                if directed:
                    all_args.append("--directed")
                result = self.runner.invoke(main, all_args, catch_exceptions=False)
                self.assertEqual(0, result.exit_code)
                out = result.stdout
                # print(input_arg, case, out)
                self.assertIn(expected, out)
                if unexpected:
                    self.assertNotIn(unexpected, out)

    def test_tree(self):
        """Test tree command on core adapters"""
        for input_arg in [TEST_ONT, TEST_DB, TEST_OWL_RDF, TEST_SIMPLE_OBO]:
            cases = [
                (
                    ["-p", "i", NUCLEUS, VACUOLE],
                    [NUCLEUS, VACUOLE, IMBO, CELLULAR_COMPONENT],
                    [CYTOPLASM],
                ),
                (["-p", "i,p", NUCLEUS], [NUCLEUS, IMBO, CELLULAR_COMPONENT], []),
                (
                    ["-p", "i,p", NUCLEUS, "--max-hops", "1"],
                    [NUCLEUS, IMBO],
                    [CELLULAR_COMPONENT, CELL],
                ),
                (
                    ["-p", "i,p", CYTOPLASM, "--down"],
                    [CYTOPLASM, VACUOLE, "GO:0110165"],
                    [],
                ),
            ]
            for args, expected_in, expected_not_in in cases:
                result = self.runner.invoke(main, ["-i", input_arg, "tree", *args])
                self.assertEqual(0, result.exit_code)
                out = result.stdout
                for term in expected_in:
                    self.assertIn(term, out)
                for term in expected_not_in:
                    self.assertNotIn(term, out)

    def test_obsoletes(self):
        """
        Tests the obsoletes command using the obsoletion test ontology.

        This should return
        """
        input_args = [
            str(INPUT_DIR / f"obsoletion_test.{suffix}") for suffix in ["obo", "owl", "db"]
        ]
        cases = [
            {
                "id": "CL:2",
                "label": "obsolete x2",
                "IAO:0100001": "CL:2replacement",
                "oio:consider": "",
            }
        ]
        for input_arg in input_args:
            result = self.runner.invoke(
                main,
                [
                    "-i",
                    input_arg,
                    "obsoletes",
                    "-o",
                    TEST_OUT,
                    "--show-migration-relationships",
                ],
            )
            self.assertEqual(0, result.exit_code)
            with open(TEST_OUT) as file:
                reader = csv.DictReader(file, delimiter="\t")
                rows = [row for row in reader]
                for case in cases:
                    self.assertIn(case, rows, f"input={input_arg}")

    # MAPPINGS

    def test_mappings_local(self):
        result = self.runner.invoke(
            main,
            [
                "-i",
                str(TEST_ONT),
                "mappings",
                "GO:0016740",
                "-o",
                TEST_OUT,
                "-O",
                "csv",
            ],
        )
        self.assertEqual(0, result.exit_code)
        out = self._out()
        self.assertIn("EC:2.-.-.-", out)
        self.assertIn("Reactome:R-HSA-1483089", out)

    def test_mappings_curie_map(self):
        mappings_output = OUTPUT_DIR.joinpath("test_mappings.tsv")
        if sys.platform == "win32":
            shell = True
        else:
            shell = False
        result = subprocess.run(
            [
                "runoak",
                "-i",
                f"sqlite:{TEST_DB}",
                "mappings",
                "-O",
                "sssom",
                "-o",
                mappings_output,
            ],
            shell=shell,  # noqa
        )
        self.assertEqual(0, result.returncode)
        msdf = parse_sssom_table(mappings_output)
        self.assertTrue(isinstance(msdf.prefix_map, dict))
        self.assertEqual(len(msdf.prefix_map), 14)
        self.assertIn("BFO", msdf.prefix_map)

    def test_mappings_json(self):
        mappings_output = OUTPUT_DIR.joinpath("test_mappings.json")

        if sys.platform == "win32":
            shell = True
        else:
            shell = False
        result = subprocess.run(
            [
                "runoak",
                "-i",
                f"sqlite:{TEST_DB}",
                "mappings",
                "-O",
                "json",
                "-o",
                mappings_output,
            ],
            shell=shell,  # noqa
        )

        self.assertEqual(0, result.returncode)

        with open(mappings_output) as f:
            parsed_mapping = json.load(f)
            self.assertEqual(len(parsed_mapping), 123)

    # DUMPER
    def test_dump(self):
        obojson_input = f"obograph:{TEST_OBOJSON}"
        fhir_conf = {
            "code_system_id": "test",
            "code_system_url": "http://purl.obolibrary.org/obo/go.owl",
            "native_uri_stems": ["http://purl.obolibrary.org/obo/GO_"],
        }
        cases = [
            (TEST_OWL_OFN, "turtle", None),
            (TEST_OWL_RDF, "turtle", None),
            (obojson_input, "obojson", None),
            (obojson_input, "obo", None),
            (obojson_input, "fhirjson", fhir_conf),
            (obojson_input, "fhirjson", None),
            (obojson_input, "owl", None),
            (TEST_ONT, "obo", None),
            (TEST_DB, "obo", None),
            (TEST_ONT, "obojson", None),
            (TEST_DB, "obojson", None),
            (TEST_ONT, "fhirjson", None),
            (TEST_DB, "fhirjson", None),
            (TEST_DB, "owl", None),
        ]
        for input, output_format, conf_object in cases:
            output_path = str(OUTPUT_DIR / f"test_dump-{output_format}.out")
            if conf_object is not None:
                conf_path = INPUT_DIR / f"{output_format}_conf.json"
                with open(conf_path, "w", encoding="utf-8") as f:
                    json.dump(conf_object, f)
            else:
                conf_path = None
            logging.info(f"input={input}, output_format={output_format}")
            cmd = ["-i", str(input), "dump", "-o", output_path, "-O", output_format]
            if conf_path:
                cmd.extend(["-c", conf_path])
            result = self.runner.invoke(main, cmd)
            if result.exit_code != 0:
                print("STDOUT", result.stdout)
                print("STDERR", result.stderr)
            self.assertEqual(0, result.exit_code, f"input={input}, output_format={output_format}")
            if output_format == "obojson":
                obj: obograph.GraphDocument
                obj = json_loader.load(output_path, target_class=obograph.GraphDocument)
                g = obj.graphs[0]
                nucleus_node = [n for n in g.nodes if n.lbl == "nucleus"][0]
                self.assertTrue(nucleus_node is not None)
                # TODO
                # self.assertTrue(nucleus_node.meta.definition.val.startswith("A membrane-bounded organelle"))
            elif output_format == "fhirjson":
                obj: fhir.CodeSystem
                obj = json_loader.load(output_path, target_class=fhir.CodeSystem)
                nucleus_concept = [n for n in obj.concept if n.code == NUCLEUS][0]
                self.assertEqual("nucleus", nucleus_concept.display)
                # TODO
                # self.assertTrue(nucleus_concept.definition.startswith("A membrane-bounded organelle"))
            elif output_format == "owl" or output_format == "turtle":
                g = rdflib.Graph()
                g.parse(output_path, format="turtle")
                self.assertGreater(len(list(g.triples((None, None, None)))), 0)
            elif output_format == "obo":
                oi = get_adapter(f"simpleobo:{output_path}")
                self.assertEqual("nucleus", oi.label(NUCLEUS))
            elif output_format == "ofn":
                oi = get_adapter(f"funowl:{output_path}")
                self.assertEqual("nucleus", oi.label(NUCLEUS))
            else:
                raise AssertionError(f"Unexpected output format: {output_format}")

    def test_transform(self):
        cases = [
            (TEST_ONT, "obo", None),
            (TEST_ONT, "obojson", None),
        ]
        transformers = [
            ("SEPTransformer", {}, (413, None)),
            ("EdgeFilterTransformer", {}, (176, None)),
            ("EdgeFilterTransformer", {"include_predicates": [IS_A]}, (176, None)),
        ]
        for transformer, conf_object, (expected_n_terms, expected_n_edges) in transformers:
            for input, output_format, _ in cases:
                if conf_object:
                    conf_path = INPUT_DIR / f"{output_format}_conf.yaml"
                    with open(conf_path, "w", encoding="utf-8") as f:
                        yaml.dump(conf_object, f)
                else:
                    conf_path = None
                output_path = str(OUTPUT_DIR / f"test_transform-{output_format}.out")
                logging.info(f"input={input}, output_format={output_format}")
                cmd = [
                    "-i",
                    str(input),
                    "transform",
                    "-t",
                    transformer,
                    "-o",
                    output_path,
                    "-O",
                    output_format,
                ]
                if conf_path:
                    cmd.extend(["-c", conf_path])
                result = self.runner.invoke(main, cmd)
                self.assertEqual(
                    0, result.exit_code, f"input={input}, output_format={output_format}"
                )
                if output_format == "obo":
                    output_path = f"simpleobo:{output_path}"
                elif output_format == "obojson":
                    output_path = f"obograph:{output_path}"
                adapter = get_adapter(output_path)
                terms = list(adapter.entities())
                edges = list(adapter.relationships())
                if expected_n_terms is not None:
                    assert len(terms) == expected_n_terms
                if expected_n_edges is not None:
                    assert len(edges) == expected_n_edges

    def test_extract(self):
        obojson_input = f"obograph:{TEST_OBOJSON}"
        cases = [
            #   (TEST_OWL_OFN, "turtle"), # TODO
            #   (TEST_OWL_RDF, "ofn"), # TODO
            (TEST_OWL_RDF, "turtle"),
            (obojson_input, "obojson"),
            (obojson_input, "obo"),
            (obojson_input, "fhirjson"),
            (obojson_input, "owl"),
            (TEST_SIMPLE_OBO, "obo"),
            (TEST_ONT, "obo"),
            (TEST_DB, "obo"),
            (TEST_ONT, "obojson"),
            (TEST_DB, "obojson"),
            (TEST_ONT, "fhirjson"),
            (TEST_DB, "fhirjson"),
            (TEST_DB, "owl"),
        ]
        for input, output_format in cases:
            for dangling in [True, False]:
                logging.info(f"input={input}, output_format={output_format}")
                query = [".desc//p=i", IMBO, ".anc//p=i", IMBO]
                cmd = [
                    "-i",
                    str(input),
                    "extract",
                    "-o",
                    TEST_OUT,
                    "-O",
                    output_format,
                ] + query
                # print(cmd)
                if dangling:
                    cmd += ["--dangling"]
                result = self.runner.invoke(main, cmd)
                self.assertEqual(
                    0, result.exit_code, f"input={input}, output_format={output_format}"
                )
                if output_format == "obojson":
                    obj: obograph.GraphDocument
                    obj = json_loader.load(TEST_OUT, target_class=obograph.GraphDocument)
                    g = obj.graphs[0]
                    nucleus_node = [n for n in g.nodes if n.lbl == "nucleus"][0]
                    self.assertTrue(nucleus_node is not None)
                    # TODO
                    # print(nucleus_node)
                    # self.assertTrue(nucleus_node.meta.definition.val.startswith("A membrane-bounded organelle"))
                elif output_format == "fhirjson":
                    obj: fhir.CodeSystem
                    obj = json_loader.load(TEST_OUT, target_class=fhir.CodeSystem)
                    nucleus_concept = [n for n in obj.concept if n.code == NUCLEUS][0]
                    self.assertEqual("nucleus", nucleus_concept.display)
                    # TODO
                    # self.assertTrue(nucleus_concept.definition.startswith("A membrane-bounded organelle"))
                elif output_format == "owl" or output_format == "turtle":
                    g = rdflib.Graph()
                    g.parse(TEST_OUT, format="turtle")
                    self.assertGreater(len(list(g.triples((None, None, None)))), 0)
                elif output_format == "obo":
                    oi = get_adapter(f"simpleobo:{TEST_OUT}")
                    self.assertEqual("nucleus", oi.label(NUCLEUS), "failed with simpleobo")
                    oi = get_adapter(f"pronto:{TEST_OUT}")
                    self.assertEqual("nucleus", oi.label(NUCLEUS), "failed with pronto")
                elif output_format == "ofn":
                    oi = get_adapter(f"funowl:{TEST_OUT}")
                    self.assertEqual("nucleus", oi.label(NUCLEUS))
                else:
                    raise AssertionError(f"Unexpected output format: {output_format}")

    # TAXON

    def test_taxon_constraints_local(self):
        for input_arg in [TEST_ONT, f"sqlite:{TEST_DB}", TEST_OWL_RDF]:
            for fmt in ["yaml", "csv", "html"]:
                result = self.runner.invoke(
                    main,
                    [
                        "-i",
                        str(input_arg),
                        "taxon-constraints",
                        NUCLEUS,
                        "-o",
                        TEST_OUT,
                        "-O",
                        fmt,
                    ],
                )
                self.assertEqual(0, result.exit_code)
                contents = self._out()
                self.assertIn("Eukaryota", contents)
                if fmt == "yaml":
                    st = yaml_loader.load(TEST_OUT, target_class=taxon_constraints.SubjectTerm)
                    only_in = st.only_in[0]
                    self.assertEqual(NUCLEUS, only_in.subject)
                    self.assertEqual(EUKARYOTA, only_in.taxon.id)

    # SEARCH

    def test_search_help(self):
        result = self.runner.invoke(main, ["search", "--help"])
        out = result.stdout
        self.assertEqual(0, result.exit_code)
        self.assertIn("Usage:", out)
        self.assertIn("Example:", out)

    def test_search_local(self):
        for input_arg in [str(TEST_ONT), f"sqlite:{TEST_DB}", TEST_OWL_RDF]:
            logging.info(f"INPUT={input_arg}")
            result = self.runner.invoke(main, ["-i", input_arg, "search", "l~nucl", "-o", TEST_OUT])
            out = self._out()
            err = result.stderr
            if result.exit_code != 0:
                logging.info(f"INPUT: {input_arg} code = {result.exit_code}")
                logging.info(f"OUTPUT={out}")
                logging.info(f"ERR={err}")
            logging.info(f"OUTPUT={out}")
            logging.info(f"ERR={err}")
            self.assertEqual(0, result.exit_code)
            self.assertIn(NUCLEUS, out)
            self.assertIn("nucleus", out)
            self.assertEqual("", err)

    def test_search_local_advanced(self):
        """
        Tests boolean combinations of search results
        """
        # tuples of (terms, complete, expected, excluded)
        search_tests = [
            (["nucleus"], True, [NUCLEUS], []),
            (["t^nucleus"], True, [NUCLEUS], []),
            (["t/^n.....s$"], True, [NUCLEUS], []),
            (["t~nucleus"], True, [NUCLEUS, CHEBI_NUCLEUS], []),
            (["l=protoplasm"], True, [], []),
            (["t=protoplasm"], True, [INTRACELLULAR], []),
            ([".=protoplasm"], True, [INTRACELLULAR], []),
            (
                # terms that start with "nucl" are in PATO, with one exception
                ["t/^nucl", ".and", "i/^PATO", ".not", "PATO:0001404"],
                True,
                [NUCLEATED],
                [TEST_OWL_RDF],
            ),
            (
                # is-a descendants of nucleus
                [".desc//p=i,p", "nucleus"],
                True,
                [NUCLEUS, NUCLEAR_ENVELOPE, NUCLEAR_MEMBRANE],
                [TEST_OWL_RDF],
            ),
            (
                # is-a ancestors of nucleus that are not a particular term
                [".anc//p=i", "nucleus", ".not", ".anc//p=i", IMBO],
                True,
                [NUCLEUS],
                [TEST_OWL_RDF],
            ),
            (
                # is-a/part-of descendants of nucleus are not found in a label search for "membrane"
                [".desc//p=i,p", "nucleus", ".not", "l~membrane"],
                True,
                [NUCLEUS, NUCLEAR_ENVELOPE],
                [TEST_OWL_RDF],
            ),
            (
                # nesting
                [".desc//p=i,p", "[", "nucleus", VACUOLE, "]", ".not", "l~membrane"],
                True,
                [NUCLEUS, NUCLEAR_ENVELOPE, VACUOLE],
                [TEST_OWL_RDF],
            ),
            (
                # filter query
                [
                    ".anc//p=i",
                    "nucleus",
                    ".filter",
                    "[x for x in terms if not impl.definition(x)]",
                ],
                True,
                ["CARO:0000000", "CARO:0030000"],
                [TEST_OWL_RDF],
            ),
            (
                # all terms
                [".all"],
                False,
                [NUCLEUS, NUCLEAR_ENVELOPE],
                [TEST_OWL_RDF],
            ),
            (
                # no terms
                [".all", ".not", ".all"],
                True,
                [],
                [TEST_OWL_RDF],
            ),
            (
                # xor
                [NUCLEUS, MEMBRANE, ".xor", NUCLEUS, ".or", NUCLEAR_MEMBRANE],
                True,
                [MEMBRANE, NUCLEAR_MEMBRANE],
                [TEST_OWL_RDF],
            ),
            (
                # set difference with additional term
                [NUCLEUS, MEMBRANE, ".not", NUCLEUS, ".or", NUCLEAR_MEMBRANE],
                True,
                [MEMBRANE],
                [TEST_OWL_RDF],
            ),
            (
                # set difference with trivial second term that is empty
                [NUCLEUS, MEMBRANE, ".not", NUCLEUS, ".and", NUCLEAR_MEMBRANE],
                True,
                [NUCLEUS, MEMBRANE],
                [TEST_OWL_RDF],
            ),
            (
                # order of precedence
                [NUCLEUS, MEMBRANE, ".not", NUCLEUS, ".or", MEMBRANE],
                True,
                [],
                [TEST_OWL_RDF],
            ),
        ]
        inputs = [TEST_ONT, f"sqlite:{TEST_DB}", TEST_OWL_RDF]
        for input_arg in inputs:
            logging.info(f"INPUT={input_arg}")
            for t in search_tests:
                logging.info(f"{input_arg} // {t}")
                terms, complete, expected, excluded = t
                if input_arg in excluded:
                    logging.info(f"Skipping {terms} as {input_arg} in Excluded: {excluded}")
                    continue
                result = self.runner.invoke(
                    main, ["-i", str(input_arg), "info"] + terms + ["-o", TEST_OUT]
                )
                out = self._out()
                err = result.stderr
                if result.exit_code != 0:
                    logging.error(f"INPUT: {input_arg} code = {result.exit_code}")
                    logging.error(f"OUTPUT={out}")
                    logging.error(f"ERR={err}")
                self.assertEqual(0, result.exit_code)
                logging.info(f"OUTPUT={out}")
                logging.info(f"ERR={err}")
                self.assertEqual(0, result.exit_code)
                self.assertEqual("", err)
                lines = out.split("\n")
                curies = []
                for line in lines:
                    m = re.match(r"(\S+)\s+!", line)
                    if m:
                        curies.append(m.group(1))
                logging.info(f"SEARCH: {terms} => {curies} // {input_arg}")
                if complete:
                    self.assertCountEqual(expected, set(curies), f"{input_arg} // {terms}")
                else:
                    for e in expected:
                        self.assertIn(e, curies)

    @unittest.skip("includes network dependency")
    def test_search_pronto_obolibrary(self):
        """
        Tests remote prontolib

        TODO: replace with mock test
        """
        to_out = ["-o", str(TEST_OUT)]
        result = self.runner.invoke(
            main, ["-i", "prontolib:pato.obo", "search", "t~shape"] + to_out
        )
        out = self._out()
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        self.assertIn(SHAPE, out)
        self.assertIn("PATO:0002021", out)  # conical - matches a synonym
        self.assertEqual("", err)
        result = self.runner.invoke(
            main, ["-i", "prontolib:pato.obo", "search", "l=shape"] + to_out
        )
        out = self._out()
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        self.assertIn(SHAPE, out)
        self.assertNotIn("PATO:0002021", out)  # conical - matches a synonym
        self.assertEqual("", err)
        result = self.runner.invoke(main, ["-i", "prontolib:pato.obo", "search", "shape"] + to_out)
        out = self._out()
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        self.assertIn(SHAPE, out)
        self.assertNotIn("PATO:0002021", out)  # conical - matches a synonym
        self.assertEqual("", err)

    def test_query(self):
        cases = [
            (
                TEST_DB,
                f'SELECT predicate, object FROM edge WHERE subject="{NUCLEUS}"',
                [],
                [
                    {
                        "predicate": "RO:0002160",
                        "predicate_label": "only_in_taxon",
                        "object": "NCBITaxon:2759",
                        "object_label": "Eukaryota",
                    }
                ],
            ),
            (
                TEST_DB,
                f'SELECT predicate, object FROM edge WHERE subject="{NUCLEUS}"',
                ["--no-autolabel"],
                [{"predicate": "RO:0002160", "object": "NCBITaxon:2759"}],
            ),
            (
                TEST_OWL_RDF,
                f"SELECT ?p ?o WHERE {{ {NUCLEUS} ?p ?o }}",
                ["-P", "GO"],
                [
                    {
                        "p": IS_A,
                        "p_label": "None",
                        "o": IMBO,
                        "o_label": "intracellular membrane-bounded organelle",
                    }
                ],
            ),
        ]
        for adapter, query, args, expected in cases:
            result = self.runner.invoke(
                main, ["-i", adapter, "query", "-q", query, "-o", TEST_OUT] + args
            )
            self.assertEqual(0, result.exit_code)
            with open(TEST_OUT, "r") as file:
                reader = csv.DictReader(file, delimiter="\t")
                rows = [row for row in reader]
                for e in expected:
                    self.assertIn(
                        e, rows, f"Expected {expected} for {query} in {adapter} with args {args}"
                    )
                # for case in cases:
                #    self.assertIn(case, rows)

    # VALIDATE

    def test_validate_help(self):
        result = self.runner.invoke(main, ["validate", "--help"])
        print("STDERR", result.stdout)
        print("STDERR", result.stderr)
        self.assertEqual(0, result.exit_code)

    def test_validate_bad_ontology(self):
        for input_arg in [f"sqlite:{BAD_ONTOLOGY_DB}"]:
            logging.info(f"INPUT={input_arg}")
            result = self.runner.invoke(main, ["-i", input_arg, "validate"])
            out = result.stdout
            err = result.stderr
            logging.info(f"ERR={err}")
            self.assertEqual(0, result.exit_code)
            self.assertIn("EXAMPLE:1", out)
            self.assertIn("EXAMPLE:2", out)
            self.assertEqual("", err)

    def test_check_definitions(self):
        for input_arg in [TEST_ONT, f"sqlite:{TEST_DB}"]:
            logging.info(f"INPUT={input_arg}")
            result = self.runner.invoke(main, ["-i", input_arg, "validate-definitions"])
            out = result.stdout
            err = result.stderr
            logging.info(f"ERR={err}")
            self.assertEqual(0, result.exit_code)
            self.assertIn(ATOM, out)
            self.assertEqual("", err)

    @unittest.skip("includes network dependency")
    def test_validate_mappings(self):
        for input_arg in [TEST_ONT, f"sqlite:{TEST_DB}"]:
            logging.info(f"INPUT={input_arg}")
            result = self.runner.invoke(main, ["-i", input_arg, "validate-mappings"])
            err = result.stderr
            logging.info(f"ERR={err}")
            self.assertEqual(0, result.exit_code)
            # self.assertIn(ATOM, out)

    # LEXICAL

    def test_lexmatch(self):
        """
        Test lexical matching of two ontologies.

        We cycle through all formats for the core test ontology (go-nucleus), and
        align it against another ontology.

        We test both directions (e.g. go-nucleus vs alignment-test, and vice versa).

        The test alignment ontology includes a custom prefix (XX), to test the scenario
        where we want to align an unregistered otology.

        The output SSSOM is parsed to check all expected mappings are there
        with expected predicates, and that the prefix map has the expected prefixes.
        """
        outfile = f"{OUTPUT_DIR}/matcher-test-cli.sssom.tsv"
        nucleus_match = "XX:1"
        intracellular_match = "XX:2"
        OTHER_ONTOLOGY = f"{INPUT_DIR}/alignment-test.obo"
        for input_arg in [
            TEST_SIMPLE_OBO,
            TEST_OBOJSON,
            TEST_OWL_RDF,
            TEST_ONT,
            TEST_DB,
        ]:
            for reversed in [False, True]:
                if reversed:
                    args = [
                        "-a",
                        input_arg,
                        "-i",
                        OTHER_ONTOLOGY,
                    ]
                else:
                    args = [
                        "-i",
                        input_arg,
                        "-a",
                        OTHER_ONTOLOGY,
                    ]
                result = self.runner.invoke(
                    main,
                    args
                    + [
                        "lexmatch",
                        "-R",
                        RULES_FILE,
                        "-o",
                        outfile,
                        "--no-ensure-strict-prefixes",
                    ],
                )
                err = result.stderr
                self.assertEqual(0, result.exit_code)
                with open(outfile) as stream:
                    contents = "\n".join(stream.readlines())
                    self.assertIn("skos:closeMatch", contents)
                    self.assertIn("skos:exactMatch", contents)
                    self.assertIn(nucleus_match, contents)
                    self.assertIn(intracellular_match, contents)
                msdf = parse_sssom_table(outfile)
                msd = to_mapping_set_document(msdf)
                self.assertIn(
                    msd.prefix_map["XX"],
                    [
                        "http://purl.obolibrary.org/obo/XX_",
                        "http://w3id.org/sssom/unknown_prefix/xx/",
                    ],
                )
                cases = [
                    (nucleus_match, NUCLEUS, SKOS_EXACT_MATCH),
                    (intracellular_match, INTRACELLULAR, SKOS_CLOSE_MATCH),
                    ("BFO:0000023", "CHEBI:50906", SKOS_EXACT_MATCH),
                ]
                for mapping in msd.mapping_set.mappings:
                    tpl = (mapping.subject_id, mapping.object_id, mapping.predicate_id)
                    tpl2 = (mapping.object_id, mapping.subject_id, mapping.predicate_id)
                    if tpl in cases:
                        cases.remove(tpl)
                    elif tpl2 in cases:
                        cases.remove(tpl2)
                self.assertEqual(0, len(cases), f"Cases not found: {cases} for {input_arg}")
                self.assertEqual("", err)

    def test_lexmatch_owl(self):
        outfile = f"{OUTPUT_DIR}/matcher-test-cli.owl.sssom.tsv"
        result = self.runner.invoke(
            main,
            [
                "-i",
                f"pronto:{INPUT_DIR}/matcher-test.owl",
                "lexmatch",
                "-R",
                RULES_FILE,
                "-o",
                outfile,
                "--no-ensure-strict-prefixes",
            ],
        )
        print("STDERR", result.stdout)
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        with open(outfile) as stream:
            contents = "\n".join(stream.readlines())
            self.assertIn("skos:closeMatch", contents)
            self.assertIn("skos:exactMatch", contents)
            # TODO change below once mapping_justification for this is finalized.
            self.assertIn("semapv:RegularExpressionReplacement", contents)
        self.assertEqual("", err)

    def test_lexmatch_sqlite(self):
        outfile = f"{OUTPUT_DIR}/matcher-test-cli.db.sssom.tsv"
        result = self.runner.invoke(
            main,
            [
                "--prefix",
                "x=http://example.org/x/",
                "-i",
                f"sqlite:{INPUT_DIR}/matcher-test.db",
                "lexmatch",
                "-R",
                RULES_FILE,
                "-o",
                outfile,
                "--no-ensure-strict-prefixes",
            ],
        )
        print("STDERR", result.stdout)
        err = result.stderr
        self.assertEqual("", err)
        self.assertEqual(0, result.exit_code)
        with open(outfile) as stream:
            contents = "\n".join(stream.readlines())
            self.assertIn("skos:closeMatch", contents)
            self.assertIn("skos:exactMatch", contents)
            self.assertIn("x:bone_element", contents)
            self.assertIn("bone tissue", contents)

    def test_similarity(self):
        result = self.runner.invoke(
            main,
            [
                "-i",
                TEST_DB,
                "similarity",
                NUCLEAR_MEMBRANE,
                "@",
                VACUOLE,
                "-p",
                "i,p",
                "-o",
                TEST_OUT,
            ],
        )
        self.assertEqual(0, result.exit_code)
        out = self._out(TEST_OUT)
        self.assertIn(IMBO, out)
        with open(TEST_OUT) as f:
            objs = list(yaml.load_all(f, yaml.SafeLoader))
            obj = objs[0]
            self.assertEqual(obj["subject_id"], NUCLEAR_MEMBRANE)
            self.assertEqual(obj["object_id"], VACUOLE)
            self.assertEqual(obj["ancestor_id"], IMBO)
            self.assertGreater(obj["jaccard_similarity"], 0.5)
            self.assertGreater(obj["ancestor_information_content"], 3.0)

    def test_diffs(self):
        outfile = f"{OUTPUT_DIR}/diff.json"
        combos = [
            #            (True, TEST_ONT),
            # (True, f"sqlite:{TEST_DB}"),
            (False, TEST_ONT),
            (True, TEST_ONT),
        ]
        for simple, input_arg in combos:
            alt_input = str(input_arg).replace("nucleus.", "nucleus-modified.")
            args = ["-i", str(input_arg), "diff"]
            if simple:
                args += ["--simple"]
            args += ["-X", alt_input, "-O", "json", "-o", outfile]
            result = self.runner.invoke(main, args)
            self.assertEqual(0, result.exit_code)
            changes = list(parse_kgcl_files([outfile]))
            self.assertTrue(
                any(c.about_node == "GO:0033673" for c in changes if isinstance(c, NodeChange))
            )
            self.assertTrue(
                any(c.subject == NUCLEUS for c in changes if isinstance(c, MappingCreation))
            )
            self.assertTrue(
                any(
                    c.about_node == CELLULAR_COMPONENT
                    for c in changes
                    if isinstance(c, RemoveMapping)
                )
            )
            catalytic_activity_changed = any(
                c.about_node == CATALYTIC_ACTIVITY for c in changes if isinstance(c, NodeChange)
            )

            self.assertTrue(catalytic_activity_changed)

            # if simple:
            #     self.assertFalse(catalytic_activity_changed)
            # else:
            #     self.assertTrue(catalytic_activity_changed)

    def test_diff_via_mappings(self):
        cases = [
            (
                [],
                [
                    {
                        "category": "IndirectFormOfEdgeOnRight",
                        "left_object_id": "X:1",
                        "left_predicate_id": "rdfs:subClassOf",
                        "left_subject_id": "X:2",
                        "right_object_id": "Y:1",
                        "right_subject_id": "Y:2",
                    },
                    {
                        "category": "Identical",
                        "left_object_id": "X:2",
                        "left_predicate_id": "rdfs:subClassOf",
                        "left_subject_id": "X:3",
                        "right_object_id": "Y:2",
                        "right_predicate_ids": ["rdfs:subClassOf"],
                        "right_subject_id": "Y:3",
                    },
                    {
                        "category": "NoRelationship",
                        "left_object_id": "X:3",
                        "left_predicate_id": "rdfs:subClassOf",
                        "left_subject_id": "X:4",
                        "right_object_id": "Y:3",
                        "right_subject_id": "Y:4",
                    },
                    {
                        "category": "NonEntailedRelationship",
                        "left_object_id": "X:4",
                        "left_predicate_id": "rdfs:subClassOf",
                        "left_subject_id": "X:5",
                        "right_object_id": "Y:4",
                        "right_subject_id": "Y:5",
                    },
                    {
                        "category": "MissingMapping",
                        "left_object_id": "Y:1",
                        "left_predicate_id": "rdfs:subClassOf",
                        "left_subject_id": "Y:1b",
                        "subject_mapping_cardinality": "1:0",
                    },
                    {
                        "category": "MissingMapping",
                        "left_object_id": "Y:1b",
                        "left_predicate_id": "rdfs:subClassOf",
                        "left_subject_id": "Y:2",
                        "subject_mapping_cardinality": "1:n",
                    },
                    {
                        "category": "Identical",
                        "left_object_id": "Y:2",
                        "left_predicate_id": "rdfs:subClassOf",
                        "left_subject_id": "Y:3",
                        "right_object_id": "X:2",
                        "right_predicate_ids": ["rdfs:subClassOf"],
                        "right_subject_id": "X:3",
                    },
                    {
                        "category": "MoreSpecificPredicateOnRight",
                        "left_object_id": "Y:4",
                        "left_predicate_id": "BFO:0000050",
                        "left_subject_id": "Y:5",
                        "right_object_id": "X:4",
                        "right_subject_id": "X:5",
                    },
                ],
            ),
            (
                ["X:2"],
                [
                    {
                        "category": "IndirectFormOfEdgeOnRight",
                        "left_object_id": "X:1",
                        "left_predicate_id": "rdfs:subClassOf",
                        "left_subject_id": "X:2",
                        "right_object_id": "Y:1",
                        "right_subject_id": "Y:2",
                    },
                ],
            ),
        ]
        for terms, expected in cases:
            outfile = f"{OUTPUT_DIR}/diff-mapping-test-cli-using-{'-'.join(terms)}.yaml"
            result = self.runner.invoke(
                main,
                [
                    "-i",
                    MAPPING_DIFF_TEST_OBO,
                    "diff-via-mappings",
                    "--mapping-input",
                    TEST_SSSOM_MAPPING,
                    "--no-autolabel",
                    "--intra",
                    "-S",
                    "X",
                    "-S",
                    "Y",
                    "-o",
                    outfile,
                ]
                + terms,
            )
            self.assertEqual(0, result.exit_code)

            with open(outfile) as f:
                docs = list(yaml.load_all(f, yaml.FullLoader))
                self.assertCountEqual(expected, docs)

    def test_generate_synonyms_and_apply(self):
        patch_file = OUTPUT_DIR / "synonym-test-patch.kgcl"
        outfile = OUTPUT_DIR / "synonym-test-output.obo"
        patch_file.unlink(missing_ok=True)
        outfile.unlink(missing_ok=True)
        result = self.runner.invoke(
            main,
            [
                "-i",
                TEST_SYNONYMIZER_OBO,
                "generate-synonyms",
                "-R",
                SYNONYMIZER_RULES_FILE,
                "--patch",
                patch_file,
                "--apply-patch",
                "-o",
                outfile,
                ".all",
            ],
        )
        self.assertEqual(0, result.exit_code)
        with open(patch_file, "r") as p, open(outfile, "r") as t:
            patch = p.readlines()
            self.assertTrue(len(patch), 3)
            self.assertTrue("create exact synonym 'eyeball'" in "\n".join(patch))
            output = t.readlines()
            self.assertTrue('synonym: "bone element" EXACT []\n' in output)

    def test_generate_synonyms_no_apply(self):
        patch_file = OUTPUT_DIR / "synonym-test-patch.kgcl"
        patch_file.unlink(missing_ok=True)
        result = self.runner.invoke(
            main,
            [
                "-i",
                TEST_SYNONYMIZER_OBO,
                "generate-synonyms",
                "-R",
                SYNONYMIZER_RULES_FILE,
                "-o",
                patch_file,
                ".all",
            ],
        )

        self.assertEqual(0, result.exit_code)
        with open(patch_file, "r") as p:
            patch = p.readlines()
            self.assertTrue(len(patch), 3)
            self.assertTrue("create exact synonym 'eyeball'" in "\n".join(patch))

    def test_create_ontology_with_kcgl(self):
        outfile = OUTPUT_DIR / "create-ontology"
        format_schemes = [
            ("obo", "simpleobo"),
            ("obo", "pronto"),
        ]
        for fmt, scheme in format_schemes:
            result = self.runner.invoke(
                main,
                [
                    "-i",
                    f"{scheme}:",
                    "apply",
                    "--changes-input",
                    str(INPUT_DIR / "test-create.kgcl.txt"),
                    "-o",
                    f"{outfile}.{fmt}",
                ],
            )
        self.assertEqual(0, result.exit_code)

    def test_statistics(self):
        # TODO: sqlite version of go-nucleus has a different number of classes from the obo version
        # unify these then implement stricter checks
        combos = [
            ("default", [], lambda obj: self.assertGreater(obj["class_count"], 200)),
            (
                "by-namespace",
                ["--group-by-obo-namespace"],
                lambda obj: self.assertGreater(
                    obj["partitions"]["biological_process"]["class_count"], 40
                ),
            ),
            # ("by-prefix",
            # ["--group-by-prefix"],
            # lambda obj: self.assertGreater(obj["partitions"]["GO"]["class_count"], 100)),
        ]
        for input_arg in [TEST_ONT, f"sqlite:{TEST_DB}"]:
            for name, opts, test in combos:
                out_path = str(OUTPUT_DIR / f"statistics-{name}.yaml")
                logging.info(f"INPUT={input_arg}")
                args = ["-i", str(input_arg), "statistics", "-o", str(out_path)] + opts
                result = self.runner.invoke(main, args)
                err = result.stderr
                # print(" ".join(args))
                logging.info(f"ERR={err}")
                self.assertEqual(0, result.exit_code)
                with open(out_path) as file:
                    obj = yaml.safe_load(file)
                    test(obj)

    # ANNOTATE
    def test_annotate_file(self):
        outfile = f"{OUTPUT_DIR}/matcher-test-annotate-file.txt"
        input_file = f"{INPUT_DIR}/matcher-text.txt"
        exclusion_file = f"{INPUT_DIR}/exclude.txt"
        result = self.runner.invoke(
            main,
            [
                "-i",
                f"sqlite:{INPUT_DIR}/matcher-test.db",
                "annotate",
                "--text-file",
                input_file,
                "--exclude-tokens",
                exclusion_file,
                "-o",
                outfile,
            ],
        )
        print("STDERR", result.stdout)
        err = "\n".join(
            [line for line in result.stderr.split("\n") if not line.startswith("WARNING")]
        )
        self.assertEqual("", err)
        self.assertEqual(0, result.exit_code)
        with open(outfile) as stream:
            contents = "\n".join(stream.readlines())
            self.assertIn("y:bone", contents)
            self.assertIn("oio:hasBroadSynonym", contents)
            self.assertIn("x:bone_element", contents)
            self.assertIn("z:bone_tissue", contents)

    def test_annotate_words(self):
        outfile = f"{OUTPUT_DIR}/matcher-test-annotate-words.txt"
        exclusion_file = f"{INPUT_DIR}/exclude.txt"
        result = self.runner.invoke(
            main,
            [
                "-i",
                f"sqlite:{INPUT_DIR}/matcher-test.db",
                "annotate",
                "bone element bone tissue bone of foot",
                "--exclude-tokens",
                exclusion_file,
                "-o",
                outfile,
            ],
        )
        print("STDERR", result.stdout)
        err = result.stderr
        self.assertEqual("", err)
        self.assertEqual(0, result.exit_code)
        with open(outfile) as stream:
            contents = "\n".join(stream.readlines())
            self.assertIn("y:bone", contents)
            self.assertIn("oio:hasBroadSynonym", contents)
            self.assertIn("x:bone_element", contents)
            self.assertIn("z:bone_tissue", contents)

    def test_diff_md(self):
        outfile = f"{OUTPUT_DIR}/diff.md"
        result = self.runner.invoke(
            main,
            ["-i", TEST_OBO_1, "diff", "-X", TEST_OBO_2, "-o", outfile, "-O", "md"],
        )
        self.assertEqual(0, result.exit_code)
        with open(outfile) as f:
            contents = f.read()

            # Check for Nodes Created section
            self.assertIn("<details>", contents)
            self.assertIn("<summary>Other nodes added: 1</summary>", contents)
            self.assertIn("| has characteristic (RO:0000053) |", contents)

            # Check for Classes Created section
            self.assertIn("<summary>Classes added: 1</summary>", contents)
            self.assertIn("| liquid configuration (PATO:0001735) |", contents)
