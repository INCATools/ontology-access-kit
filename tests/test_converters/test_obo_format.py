"""
OBO Format and OBO Graphs compliance tests.

See:

- https://github.com/owlcollab/oboformat/issues/146
- https://github.com/geneontology/obographs/issues/106

Note: some of these tests may migrate from OAK to a more central location.

Currently the tests in this suite do two things:

1. Compile a compliance suite by converting from a source .obo file (COMPILED_OBO_FILE)
    - writes to tests/input/obo-compliance
    - these may eventually be moved to a separate repo
2. Test that conversion to and from .obo matches these files
    - generates files in tests/output/obo-compliance

Step 1: Generate the compliance suite
--------------------------------------

Step 1 is intended to be run relatively infrequently. It generates the source-of-truth "expected" files.
Note there is some bootstrapping here. We trust a certain version of robot/obographs/owlapi to generate the
canonical files. For the first iteration these should be manually inspected to see if they align to the spec.
Once we are happy with these, in general they should not change again.

The source file COMPILED_OBO_FILE looks like this:

.. code-block:: obo

    !! name: name
    !! description: rdfs:label

    [Term]
    id: X:1
    name: x1

    !! name: invalid-name-duplicate
    !! description: max 1 name
    !! invalid: true

    [Term]
    id: X:1
    name: x1
    name: x2

    !! name: namespace
    !! description: oio:namespace

    [Term]
    id: X:1
    namespace: NS1

    !! name: xref
    !! description: rdfs:label

This is designed for easy editing. New tests can be added by providing !! separators
and name/description metadata.

If new tests are added, test_generate_canonical_files in unskip mode. This will generate the directories in
tests/input/obo-compliance

E.g.

.. code-block:: bash

   alt_id/
      alt_id.obo
      alt_id.meta.yaml

Next, robot will be run from the command line to generate the expected files:

- alt_id.expected.json
- alt_id.expected.obo
- alt_id.expected.ofn
- alt_id.expected.owl

Step 2: Checking current behavior against the compliance suite
--------------------------------------------------------------


"""

import difflib
import json
import logging
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Optional, Tuple, Union

import pytest
import rdflib
from rdflib.compare import isomorphic

from oaklib import get_adapter
from tests import INPUT_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)

COMPILED_OBO_FILE = INPUT_DIR / "obo-compliance.obo"
OBO_COMPLIANCE_DIR = INPUT_DIR / "obo-compliance"
OBO_COMPLIANCE_OUTPUT_DIR = OUTPUT_DIR / "obo-compliance"

CANONICAL_DUMPER = "robot"

KNOWN_ISSUES = [
    "typedef-xref-ro",
    "intersection_of-genus-differentia-annotated",
    "union-of-annotated",
    "property_value-object-annotated",
    "owl-axioms-ObjectInverseOf",
]


@lru_cache
def robot_is_on_path():
    """
    Check if robot is on the path.

    Can be installed from robot.obolibrary.org

    :return:
    """
    return shutil.which("robot") is not None


@lru_cache
def obographs_java_is_on_path():
    """
    Check if ogger is on the path.

    Part of obographs-java
    :return:
    """
    return shutil.which("ogger") is not None


@pytest.fixture(scope="session")
def split_compiled_obo():
    """
    Split the compiled OBO file into individual files,
    adding additional metadata files

    The compiled OBO file is a concatenation of multiple different ontologies,
    separated by yaml metadata after !! characters (obo format comments).

    Note: this procedure may eventually go away and the component files
    managed independently but for now it is easier to manage them together.

    :return:
    """
    blocks = {}
    metadata = {}
    yamls = {}
    ontology_id = None
    paths = {}
    with open(COMPILED_OBO_FILE) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("!!"):
                yaml = line[3:].rstrip()
                if not yaml:
                    continue
                if yaml.startswith("#"):
                    continue
                if ":" not in yaml:
                    raise ValueError(f"Invalid yaml: {yaml}")
                k, v = yaml.strip().split(":", 1)
                v = v.strip()
                if k == "name":
                    ontology_id = v
                    if ontology_id in blocks:
                        raise ValueError(f"Duplicate ontology id: {ontology_id}")
                    metadata[ontology_id] = {}
                    yamls[ontology_id] = [yaml.rstrip()]
                    blocks[ontology_id] = [
                        "format-version: 1.4\n",
                        f"ontology: {ontology_id}\n",
                    ]
                metadata[ontology_id][k.strip()] = v.strip()
                yamls[ontology_id].append(yaml.strip())

            else:
                blocks[ontology_id].append(line)
                if line.startswith("ontology:") and blocks[ontology_id][1].startswith("ontology:"):
                    # normally we auto-populate the ontology id;
                    # however, some tests may explicitly include the ontology tag
                    # (necessary to preserve line ordering). In this case we
                    # remove the auto-populated tag
                    blocks[ontology_id].pop(1)
    for ontology_id, block in blocks.items():
        folder = OBO_COMPLIANCE_DIR / ontology_id
        folder.mkdir(exist_ok=True, parents=True)
        filename = folder / f"{ontology_id}.obo"
        paths[ontology_id] = filename
        # logger.info(f"W")
        with open(filename, "w") as f:
            f.write("".join(block))
        with open(folder / f"{ontology_id}.meta.yaml", "w") as f:
            f.write("\n".join(yamls[ontology_id]))
    return paths, metadata


def test_split(split_compiled_obo):
    paths, metadata = split_compiled_obo
    assert len(paths.items()) > 0


@pytest.mark.parametrize(
    "output_format",
    [
        "owl",
        "json",
        "obo",
        "ofn",
    ],
)
# @pytest.mark.skipif(not robot_is_on_path(), reason="robot not on path")
@pytest.mark.skip("Only to be executed periodically")
def test_generate_canonical_files(split_compiled_obo, output_format):
    """
    Generate canonical converted files using .obo as source.

    Note that this test is intended to serve as a bootstrap,
    and eventually the canonical conversions will be manually edited
    rather than generated automatically.

    This will go through the compliance suite, and generate
    *.expected.{obo,owl,json} files in the input obo-compliance folder.
    These are intended to be checked in.

    If there is a diff between what was previously deposited, a message
    will be written, but the test will pass. We realize that TestByGuru
    is an anti-pattern, but this is temporary until the compliance suite
    settles down.

    We use robot to generate the canonical files, except for json,
    for which we use ogger (part of the obographs java package). These
    are both called on the command line (if they are not found then
    no canonical file will be generated). Again, this is a temporary
    measure, and for now this unit test is intended for execution
    by a small subset of the OAK team. It is expected that the person
    running this will use the appropriate version of each.

    :param split_compiled_obo:
    :param output_format:
    :return:
    """
    paths, metadata = split_compiled_obo
    for ontology_id, path in paths.items():
        # logger.info(f"Testing {ontology_id} to {output_format}")
        if metadata[ontology_id].get("invalid", None):
            logger.info(f"Skipping intentionally invalid ontology: {ontology_id}")
            continue
        output_path = make_filename(ontology_id, "robot", output_format, parent=OUTPUT_DIR)
        # logger.info(f"CONVERTING {path} to {output_path}")
        if output_path == "json":
            ok = ogger_convert(path, output_path)
        else:
            ok = robot_convert(path, output_path)
        assert ok is not False
        if ok:
            canonical_path = Path(
                make_filename(ontology_id, "expected", output_format, parent=OBO_COMPLIANCE_DIR)
            )
            if canonical_path.exists():
                print(f"Comparing {output_path} to {canonical_path}")
                compare_output(output_path, canonical_path, output_format, strict=True)
            else:
                canonical_path.parent.mkdir(exist_ok=True, parents=True)
                # copy the output to the input dir
                # logger.info(f"Copying {output_path} to {canonical_path}")
                shutil.copy(output_path, canonical_path)
                shutil.copy(mk_version_path(output_path), mk_version_path(canonical_path))
        else:
            assert ok is None
            print(f"DID NOT CONVERT {path} to {output_path}")
            raise AssertionError(f"Could not convert {path} to {output_path}")


@pytest.mark.parametrize(
    "output_format",
    [
        "obo",
        "json",
        "owl",
    ],
)
@pytest.mark.parametrize("wrapper", [("obo", "simpleobo")])
def test_oak_loaders_dumpers(split_compiled_obo, output_format, wrapper):
    """
    Tests that conversion via OAK generates files that are compliant.

    This tests the conversion from .obo format (these are generated in advance from source, see
    docs above) into other formats using OAK.

    :param split_compiled_obo:
    :param output_format:
    :param wrapper:
    :return:
    """
    paths, metadata = split_compiled_obo
    input_format, loader = wrapper
    for ontology_id, path in paths.items():
        logger.info(f"Exporting {ontology_id} to {output_format}")
        if metadata[ontology_id].get("invalid", None):
            logger.info("Skipping intentionally invalid ontology")
            continue
        adapter = get_adapter(f"{loader}:{path}")
        logger.info(
            f"Loaded {ontology_id} with {loader}, entities: {len(list(adapter.entities()))}"
        )
        output_path = make_filename(ontology_id, loader, output_format)
        output_format_option = output_format
        if output_format == "owl":
            # xml is canonical for OBOFoundry
            output_format_option = "rdfxml"
        logger.info(
            f"Dumping {ontology_id} to {output_path} using {output_format_option} with {loader}"
        )
        adapter.dump(output_path, syntax=output_format_option)
        if metadata[ontology_id].get("non-canonical-form-of", None):
            # non-canonical forms are not expected to be identical
            continue
        canonical = canonical_path(ontology_id, output_format)
        compare_output(
            output_path, canonical, output_format, metadata=metadata[ontology_id], strict=False
        )


def compare_output(
    generated_path: str,
    canonical_path: str,
    format: str = None,
    metadata: dict = None,
    strict=False,
) -> Tuple[int, list, bool]:
    """
    Compare the output of OAK loading and dumping vs canonical files.

    In all cases difflib is used over ascii representations

    - for obo files, the diff is a simple ascii diff (this sensitive to line ordering)
    - for json files, the files are reserialized to canonicalize the order of keys
    - for owl files, the files are reserialized using rdflib

    The constant KNOWN_ISSUES holds the list of test names that are known to be problematic.

    :param generated_path:
    :param canonical_path:
    :param format:
    :return: Tuple of [number of changes, list of diffs, fatal]
    """
    fatal = False
    if not metadata:
        metadata = {}
    if format == "obo":
        num_changes, diffs = diff_files(canonical_path, generated_path)
    elif format.endswith("json"):
        generated_obj = json.load(open(generated_path))
        canonical_obj = json.load(open(canonical_path))
        if generated_obj == canonical_obj:
            diffs = []
        else:
            diffs = list(
                difflib.unified_diff(
                    json.dumps(canonical_obj, indent=2, sort_keys=True).splitlines(),
                    json.dumps(generated_obj, indent=2, sort_keys=True).splitlines(),
                )
            )
        num_changes = len(diffs)
    elif format == "owl":
        canonical_graph = rdflib.Graph()
        canonical_graph.parse(canonical_path, format="xml")
        generated_graph = rdflib.Graph()
        generated_graph.parse(generated_path, format="xml")
        if isomorphic(canonical_graph, generated_graph):
            diffs = []
        else:
            diffs = list(
                difflib.unified_diff(
                    canonical_graph.serialize(format="turtle").splitlines(),
                    generated_graph.serialize(format="turtle").splitlines(),
                )
            )
        num_changes = len(diffs)
    else:
        num_changes, diffs = 0, []
    if num_changes:
        name = metadata.get("name", None)
        if "unstable" in metadata:
            expected = "EXPECTED"
        else:
            if name in KNOWN_ISSUES:
                expected = "TODO"
            else:
                expected = "UNEXPECTED"
                fatal = True
                if strict:
                    raise ValueError(
                        f"UNEXPECTED DIFF {format}: {canonical_path} vs {generated_path}"
                    )
        logger.info(f"## {name}:: {expected} DIFF {format}: {canonical_path} vs {generated_path}:")
        for diff in diffs:
            logger.info(diff)

    else:
        logger.info(f"## IDENTICAL {format}: {canonical_path} vs {generated_path}:")
    return num_changes, diffs, fatal


def diff_files(file_path1, file_path2):
    """
    Diff two files, at the ascii level.

    ignores the format-version line for obo format

    :param file_path1:
    :param file_path2:
    :return:
    """

    def readlines(file):
        lines = []
        for line in file.readlines():
            line = line.rstrip()
            if line.startswith("format-version:"):
                continue
            lines.append(line)
        return lines

    with open(file_path1, "r") as file1, open(file_path2, "r") as file2:
        file1_contents = readlines(file1)
        file2_contents = readlines(file2)
        differ = difflib.Differ()
        diffs = list(differ.compare(file1_contents, file2_contents))

        def is_change(line):
            if line.startswith("+") or line.startswith("-"):
                if line[1:].strip() == "":
                    return False
                else:
                    return True
            else:
                return False

        return len([line for line in diffs if is_change(line)]), diffs


def make_filename(
    ontology_id: str, loader: str, output_format: str, parent=OBO_COMPLIANCE_OUTPUT_DIR
) -> str:
    """
    Make a filename for a given ontology id, loader, and output format.

    :param ontology_id:
    :param loader:
    :param output_format:
    :param parent:
    :return:
    """
    outdir = parent / ontology_id
    outdir.mkdir(exist_ok=True, parents=True)
    return str(outdir / f"{ontology_id}.{loader}.{output_format}")
    # return str(source_path.parent / f"{ontology_id}.{loader}.{output_format}")


def canonical_path(ontology_id: str, output_format: str) -> str:
    """
    Get the canonical path for a given ontology id and output format.

    :param ontology_id:
    :param output_format:
    :return:
    """
    return str(OBO_COMPLIANCE_DIR / ontology_id / f"{ontology_id}.expected.{output_format}")


def mk_version_path(path: Union[str, Path]) -> str:
    """
    Make a version path for a given path.

    :param path:
    :return:
    """
    return f"{path}.versioninfo"


def robot_convert(input_path: str, output_path: str) -> Optional[bool]:
    """
    Convert an ontology using robot.

    :param input_path:
    :param output_path:
    :return:
    """
    if not robot_is_on_path():
        logger.warning("ROBOT NOT ON PATH")
        return None
    cmd = [
        "robot",
        "convert",
        "-i",
        input_path,
        # "-t",
        # "http://www.geneontology.org/formats/oboInOwl#id",
        # "convert",
        "-o",
        output_path,
    ]
    try:
        print(f"Running {cmd}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stderr:
            logging.warning(result.stderr)
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.info(f"Robot call failed: {e}")
        return False
    try:
        version_meta_file = mk_version_path(output_path)
        version_cmd = [
            "robot",
            "--version",
        ]
        with open(version_meta_file, "w") as outfile:
            result = subprocess.run(version_cmd, check=True, stdout=outfile, text=True)
            if result.stderr:
                logging.warning(result.stderr)
            logging.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.info(f"Robot --version call failed: {e}")
        return False


def ogger_convert(input_path: str, output_path: str) -> Optional[bool]:
    """
    Convert an ontology using ogger.

    :param input_path:
    :param output_path:
    :return:
    """
    if not obographs_java_is_on_path():
        return None
    cmd = [
        "ogger",
        input_path,
        "-o",
        output_path,
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stderr:
            logging.warning(result.stderr)
        logging.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.info(f"Ogger call failed: {e}")
        return False
