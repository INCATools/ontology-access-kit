import os
import time
import unittest

from oaklib.utilities.caching import CachePolicy


class TestCachePolicy(unittest.TestCase):

    def test_refresh_policy(self):
        policy = CachePolicy.from_string("refresh")

        self.assertTrue(policy.always_refresh)
        self.assertFalse(policy.never_refresh)
        self.assertFalse(policy.reset)

        self.assertEqual(CachePolicy.REFRESH, policy)

        now = time.time()
        self.assertTrue(policy.refresh(now))
        self.assertTrue(policy.refresh(now + 86400)) # 1 day in the future
        self.assertTrue(policy.refresh(now - 86400)) # 1 day in the past

    def test_never_refresh_policy(self):
        policy = CachePolicy.from_string("no-refresh")

        self.assertTrue(policy.never_refresh)
        self.assertFalse(policy.always_refresh)
        self.assertFalse(policy.reset)

        self.assertEqual(CachePolicy.NO_REFRESH, policy)

        now = time.time()
        self.assertFalse(policy.refresh(now))
        self.assertFalse(policy.refresh(now + 86400))
        self.assertFalse(policy.refresh(now - 86400))

        # inexistent file is always refreshed even under "no-refresh"
        self.assertTrue(policy.refresh_file("inexistent-file"))

    def test_reset_policy(self):
        policy = CachePolicy.from_string("reset")
        self.assertEqual(policy, CachePolicy.from_string("clear"))

        self.assertTrue(policy.reset)
        self.assertFalse(policy.always_refresh)
        self.assertFalse(policy.never_refresh)

        self.assertEqual(CachePolicy.RESET, policy)

        now = time.time()
        self.assertTrue(policy.refresh(now))
        self.assertTrue(policy.refresh(now + 86400))
        self.assertTrue(policy.refresh(now - 86400))

    def test_refresh_after_1day_policy(self):
        policy = CachePolicy.from_string('1d')

        self.assertFalse(policy.always_refresh)
        self.assertFalse(policy.never_refresh)
        self.assertFalse(policy.reset)

        now = time.time()
        self.assertTrue(policy.refresh(now - 90000)) # 25 hours in the past
        self.assertFalse(policy.refresh(now - 82800)) # 23 hours in the past

    def test_refresh_file(self):
        now = time.time()

        # Create dummy file with known mtime 3 days in the past
        path = "tests/output/dummy-cache"
        with open(path, "w"):
            pass
        os.utime(path, (now - 259200, now - 259200))

        self.assertTrue(CachePolicy.REFRESH.refresh_file(path))
        self.assertTrue(CachePolicy.RESET.refresh_file(path))
        self.assertFalse(CachePolicy.NO_REFRESH.refresh_file(path))
        self.assertTrue(CachePolicy.from_string('2d').refresh_file(path))
        self.assertFalse(CachePolicy.from_string('4d').refresh_file(path))

        os.unlink(path)

        # Inexistent file gets refreshed even under no-refresh
        self.assertTrue(CachePolicy.NO_REFRESH.refresh_file(path))

    def test_parsing_durations(self):
        self.assertEqual(CachePolicy.from_string("1")._max_age, 86400)
        self.assertEqual(CachePolicy.from_string("1d")._max_age, 86400)
        self.assertEqual(CachePolicy.from_string("86400s")._max_age, 86400)
        self.assertEqual(CachePolicy.from_string("1w")._max_age, 86400 * 7)
        self.assertEqual(CachePolicy.from_string("1m")._max_age, 86400 * 30)
        self.assertEqual(CachePolicy.from_string("1y")._max_age, 86400 * 365)

        self.assertIsNone(CachePolicy.from_string("bogus"))
