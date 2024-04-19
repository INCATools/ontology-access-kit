import difflib
import math
from pathlib import Path
from typing import List

from linkml_runtime.utils.yamlutils import YAMLRoot

ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "input"
OUTPUT_DIR = ROOT / "output"
SCHEMA_DIR = Path(ROOT) / "../src/linkml"
EXTERNAL_DB_DIR = Path(ROOT) / "../db"  # for integration tests: optional
EXAMPLE_ONTOLOGY_OBO = Path(INPUT_DIR) / "go-nucleus.obo"
EXAMPLE_ONTOLOGY_DB = Path(INPUT_DIR) / "go-nucleus.db"


def output_path(fn: str) -> str:
    return str(Path(OUTPUT_DIR) / fn)


DIGIT = "UBERON:0002544"
VACUOLE = "GO:0005773"
ENDOMEMBRANE_SYSTEM = "GO:0012505"
CYTOPLASM = "GO:0005737"
CYTOPLASMIC_REGION = "GO:0099568"
PLASMA_MEMBRANE = "GO:0005886"
CELL_CORTEX = "GO:0005938"
CELL_CORTEX_REGION = "GO:0099738"
CELL_PERIPHERY = "GO:0071944"
CELLULAR_ANATOMICAL_ENTITY = "GO:0110165"
HUMAN = "NCBITaxon:9606"
MAMMALIA = "NCBITaxon:40674"
NEURON = "CL:0000540"
CELLULAR_COMPONENT = "GO:0005575"
CELLULAR_ANATOMICAL_ENTITY = "GO:0110165"
CELL = "CL:0000000"
SHAPE = "PATO:0000052"
NUCLEATED = "PATO:0002505"
PHOTORECEPTOR_OUTER_SEGMENT = "GO:0001750"
CATALYTIC_ACTIVITY = "GO:0003824"
REGULATION_OF_BIOLOGICAL_PROCESS = "GO:0050789"
REGULATION_OF_PHOSPHORYLATION = "GO:0042325"

CHEBI_NUCLEUS = "CHEBI:33252"
SUBATOMIC_PARTICLE = "CHEBI:36342"
NUCLEUS = "GO:0005634"
ORGANELLE_MEMBRANE = "GO:0031090"
NUCLEAR_ENVELOPE = "GO:0005635"
ORGANELLE_ENVELOPE = "GO:0031967"
ENVELOPE = "GO:0031975"
THYLAKOID = "GO:0009579"
ATOM = "CHEBI:33250"
INTERNEURON = "CL:0000099"
BACTERIA = "NCBITaxon:2"
ARCHAEA = "NCBITaxon:2157"
EUKARYOTA = "NCBITaxon:2759"
FUNGI = "NCBITaxon:4751"
OPISTHOKONTA = "NCBITaxon:33154"
CELLULAR_ORGANISMS = "NCBITaxon:131567"
PLANTS_OR_CYANOBACTERIA = "NCBITaxon_Union:0000002"
FUNGI_OR_DICTYOSTELIUM = "NCBITaxon_Union:0000022"
FUNGI_OR_BACTERIA = "NCBITaxon_Union:0000020"

BIOLOGICAL_PROCESS = "GO:0008150"
BIOLOGICAL_ENTITY = "CARO:0030000"
NEGEG_PHOSPH = "GO:0042326"
DICTYOSTELIUM = "NCBITaxon:5782"
DICTYOSTELIUM_DISCOIDEUM = "NCBITaxon:44689"
NUCLEAR_MEMBRANE = "GO:0031965"
MEMBRANE = "GO:0016020"
PHOTOSYNTHETIC_MEMBRANE = "GO:0034357"
SOROCARP_STALK_DEVELOPMENT = "GO:0031150"

INTRACELLULAR = "GO:0005622"
IMBO = "GO:0043231"
ORGANELLE = "GO:0043226"
INTRACELLULAR_ORGANELLE = "GO:0043229"

TISSUE = "UBERON:0000479"

FAKE_ID = "FAKE:001"
FAKE_PREDICATE = "RO:666"

REGULATES = "RO:0002211"
REGULATED_BY = "RO:0002334"
CAUSALLY_UPSTREAM_OF = "RO:0002411"
PROCESS = "BFO:0000015"

PHENOTYPIC_ABNORMALITY = "HP:0000118"
BONE_FRACTURE = "HP:0020110"

PROTEIN1 = "UniProtKB:P1"
PROTEIN2 = "UniProtKB:P2"
PROTEIN3 = "UniProtKB:P3"
GENE1 = "HGCN:1"
GENE2 = "HGCN:2"
GENE3 = "HGCN:3"
GENE4 = "HGCN:4"
GENE5 = "HGCN:5"
GENE6 = "HGCN:6"
GENE7 = "HGCN:7"
GENE8 = "HGCN:8"
GENE9 = "HGCN:9"
PMID1 = "PMID:1"
PMID2 = "PMID:2"


def object_subsumed_by(sub: YAMLRoot, parent: YAMLRoot, float_abs_tol=0.001) -> bool:
    """
    Check if one object is subsumed by another, where subsumption holds
    when all non-null/default values in the parent are set in the sub.

    :param sub:
    :param parent:
    :return:
    """
    if sub == parent:
        return True
    for k, v in vars(parent).items():
        if v is not None and v != []:
            if isinstance(v, float):
                if not math.isclose(v, getattr(sub, k), abs_tol=float_abs_tol):
                    return False
            else:
                if v != getattr(sub, k):
                    return False
    return True


def object_is_subsumed_by_member_of(obj: YAMLRoot, obj_list: List[YAMLRoot], **kwargs) -> bool:
    """
    Check if an object is subsumed by any member of a list of objects.

    :param obj:
    :param obj_list:
    :return:
    """
    for o in obj_list:
        if object_subsumed_by(o, obj, **kwargs):
            return True
    return False


def filecmp_difflib(left_path: Path, right_path: Path) -> bool:
    """
    Platform neutral filecmp.cmp(..) function for text files

    Files are read in text mode to ignore newline differences.
    """
    with open(left_path) as left, open(right_path) as right:
        diff = difflib.unified_diff(left.readlines(), right.readlines())

    return list(diff) == []
