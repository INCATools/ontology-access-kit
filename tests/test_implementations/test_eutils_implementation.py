import os
import traceback
import unittest
from unittest.mock import MagicMock, patch

import requests

from oaklib import get_adapter
from oaklib.constants import TIMEOUT_SECONDS
from oaklib.implementations.ncbi.eutils_implementation import (
    EFETCH_URL,
    REQUEST_INTERVAL,
    REQUEST_INTERVAL_WITH_KEY,
)

EMPTY_SET = b"<PubmedArticleSet></PubmedArticleSet>"
SLEEP = "oaklib.implementations.ncbi.eutils_implementation.time.sleep"
# On coarse clocks (Windows, Python < 3.13) consecutive monotonic() calls can be equal,
# so the computed wait is (t + interval) - t, which float rounding can put just above interval
TOLERANCE = 1e-9


def _response(content: bytes = EMPTY_SET, from_cache: bool = False) -> MagicMock:
    response = MagicMock()
    response.content = content
    response.from_cache = from_cache
    response.raise_for_status.return_value = None
    return response


class TestEUtilsImplementation(unittest.TestCase):
    """
    Tests the efetch helper on :ref:`EUtilsImplementation`, via the PubMed adapter.
    """

    def setUp(self) -> None:
        self.adapter = get_adapter("pubmed:")
        self.session = MagicMock()
        self.adapter._requests_session = self.session
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("NCBI_API_KEY", None)

    def test_efetch_request(self):
        self.session.get.return_value = _response()
        root = self.adapter._efetch(["1", "2"])
        self.assertEqual(root.tag, "PubmedArticleSet")
        self.session.get.assert_called_once_with(
            EFETCH_URL,
            params={"db": "pubmed", "id": "1,2", "retmode": "xml"},
            timeout=TIMEOUT_SECONDS,
        )

    def test_api_key_from_env(self):
        os.environ["NCBI_API_KEY"] = "secret"
        self.session.get.return_value = _response()
        self.adapter._efetch(["1"])
        self.assertEqual(self.session.get.call_args.kwargs["params"]["api_key"], "secret")

    def test_throttles_uncached_requests(self):
        self.session.get.return_value = _response(from_cache=False)
        with patch(SLEEP) as sleep:
            self.adapter._efetch(["1"])
            self.adapter._efetch(["2"])
        sleep.assert_called_once()
        self.assertTrue(0 < sleep.call_args[0][0] <= REQUEST_INTERVAL + TOLERANCE)

    def test_throttle_interval_with_api_key(self):
        os.environ["NCBI_API_KEY"] = "secret"
        self.session.get.return_value = _response(from_cache=False)
        with patch(SLEEP) as sleep:
            self.adapter._efetch(["1"])
            self.adapter._efetch(["2"])
        sleep.assert_called_once()
        self.assertTrue(0 < sleep.call_args[0][0] <= REQUEST_INTERVAL_WITH_KEY + TOLERANCE)

    def test_cached_responses_do_not_throttle(self):
        self.session.get.return_value = _response(from_cache=True)
        with patch(SLEEP) as sleep:
            self.adapter._efetch(["1"])
            self.adapter._efetch(["2"])
        sleep.assert_not_called()

    def test_http_error_raised(self):
        response = _response()
        response.raise_for_status.side_effect = requests.HTTPError("400 Client Error")
        self.session.get.return_value = response
        with self.assertRaises(requests.HTTPError):
            self.adapter._efetch(["1"])

    def test_http_error_redacts_api_key(self):
        os.environ["NCBI_API_KEY"] = "secret"
        response = _response()
        response.raise_for_status.side_effect = requests.HTTPError(
            f"400 Client Error: Bad Request for url: {EFETCH_URL}?db=pubmed&id=1&api_key=secret"
        )
        self.session.get.return_value = response
        with self.assertRaises(requests.HTTPError) as raised:
            self.adapter._efetch(["1"])
        self.assertNotIn("secret", "".join(traceback.format_exception(raised.exception)))
