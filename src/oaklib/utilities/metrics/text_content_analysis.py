import gzip
import logging
import sys
from typing import List, Optional

import click
from semsql.sqla.semsql import ObjectPropertyNode, Statements

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import (
    DESCRIPTION,
    EQUIVALENT_CLASS,
    HAS_DEFINITION_CURIE,
    OWL_SOME_VALUES_FROM,
    RDFS_COMMENT,
    SKOS_DEFINITION_CURIE,
    SUBCLASS_OF,
)
from oaklib.implementations import SqlImplementation
from oaklib.query import process_predicates_arg
from oaklib.types import PRED_CURIE

logger = logging.getLogger(__name__)

DEFAULT_ANNOTATION_PREDICATES = [
    RDFS_COMMENT,
    HAS_DEFINITION_CURIE,
    SKOS_DEFINITION_CURIE,
    DESCRIPTION,
]


def compressed_size(texts: List[str]) -> int:
    """
    Calculate the compressed size of a list of texts.

    :param texts:
    :return:
    """
    text = "\n".join(texts)
    if isinstance(text, str):
        text = text.encode("utf-8")
    logger.info(f"Compressing {len(text)} bytes")
    compressed = gzip.compress(text)
    size = len(compressed)
    logger.info(f"Compressed size: {size}")
    return size


def calculate_ontology_text_content(
    adapter: SqlImplementation,
    language="en",
    annotation_predicates: Optional[List[PRED_CURIE]] = None,
) -> float:
    """
    Calculate the text content of an ontology.

    Example:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.db")
        >>> assert isinstance(adapter, SqlImplementation)
        >>> tc = calculate_ontology_text_content(adapter)
        >>> assert tc > 0.5 < 0.99

    :param adapter:
    :param predicates:
    :return:
    """
    session = adapter.session
    texts = []
    objects = []
    object_properties = [x[0] for x in session.query(ObjectPropertyNode.id).all()]
    logger.debug("object_properties", object_properties)
    logger.info(
        f"Calculating text content for {adapter.implementation_name}, "
        f"language={language}, annotation_predicates={annotation_predicates}"
    )
    for row in session.query(Statements).all():
        v = row.value
        p = row.predicate
        if v:
            if annotation_predicates and p not in annotation_predicates:
                continue
            dt = row.datatype
            if dt and dt.startswith("xsd:") and dt != "xsd:string":
                continue
            this_lang = row.language
            if this_lang and this_lang != language:
                continue
            texts.append(str(v))
        else:
            if (
                p not in [SUBCLASS_OF, OWL_SOME_VALUES_FROM, EQUIVALENT_CLASS]
                and p not in object_properties
            ):
                continue
            objects.append(str(row.object))
    ic_t = compressed_size(texts)
    ic_o = compressed_size(objects)
    return ic_t / (ic_t + ic_o)


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-l", "--language", default="en", help="Language to use")
@click.option(
    "-A", "--annotation-predicate", multiple=False, help="Predicates to use (comma-separated)"
)
@click.option(
    "--default-annotations/--no-default-annotations", default=True, help="Use default annotations"
)
@click.argument("inputs", nargs=-1)
def main(
    inputs: List[str],
    verbose: int,
    language: str,
    annotation_predicate: str,
    default_annotations: bool,
):
    """
    Calculate the text content of an ontology.
    """
    sys.tracebacklimit = 0
    if verbose >= 2:
        logger.setLevel(logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    print("ontology\ttext_content")
    for input_name in inputs:
        try:
            adapter = get_adapter(input_name)
            annotation_predicates = process_predicates_arg(annotation_predicate)
            if not annotation_predicates and default_annotations:
                annotation_predicates = DEFAULT_ANNOTATION_PREDICATES
            tc = calculate_ontology_text_content(
                adapter, language=language, annotation_predicates=annotation_predicates
            )
            print(f"{input_name}\t{tc}")
        except Exception as e:
            logger.error(f"Error processing {input_name}: {e}")
            print(f"{input_name}\t")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
