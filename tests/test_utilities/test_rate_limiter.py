import unittest
from unittest import mock

from oaklib.utilities import rate_limiter


class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        self.clock = 1000.0
        self.sleeps = []

        def sleep(seconds):
            self.sleeps.append(seconds)
            self.clock += seconds

        patches = [
            mock.patch.object(rate_limiter, "CALLS", 3),
            mock.patch.object(rate_limiter, "RATE_LIMIT", 10),
            mock.patch.object(rate_limiter, "_window_start", float("-inf")),
            mock.patch.object(rate_limiter, "_num_calls", 0),
            mock.patch.object(rate_limiter.time, "monotonic", lambda: self.clock),
            mock.patch.object(rate_limiter.time, "sleep", sleep),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def test_calls_within_limit_do_not_sleep(self):
        for _ in range(3):
            rate_limiter.check_limit()
            self.clock += 1
        self.assertEqual([], self.sleeps)

    def test_exceeding_limit_sleeps_until_window_ends(self):
        for _ in range(3):
            rate_limiter.check_limit()
            self.clock += 2
        rate_limiter.check_limit()
        self.assertEqual([4], self.sleeps)
        # a new window has started with this call; two more are allowed
        rate_limiter.check_limit()
        rate_limiter.check_limit()
        self.assertEqual([4], self.sleeps)

    def test_window_resets_after_period(self):
        for _ in range(3):
            rate_limiter.check_limit()
        self.clock += 10
        for _ in range(3):
            rate_limiter.check_limit()
        self.assertEqual([], self.sleeps)
