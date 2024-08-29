import pytest

from oaklib.utilities.publication_utils.pubmed_wrapper import PubmedWrapper


@pytest.fixture
def pubmed_wrapper():
    return PubmedWrapper()


def test_retracted(pubmed_wrapper):
    objs = pubmed_wrapper.objects_by_ids(["PMID:19717156"])
    [obj] = objs
    assert obj["retracted"]
