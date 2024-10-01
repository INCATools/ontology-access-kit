import os
import time
import unittest

from oaklib.utilities.caching import CachePolicy, FileCache


class TestCachePolicy(unittest.TestCase):

    def test_refresh_policy(self):
        policy = CachePolicy.from_string("refresh")

        self.assertTrue(policy.always_refresh)
        self.assertFalse(policy.never_refresh)
        self.assertFalse(policy.reset)

        self.assertEqual(CachePolicy.REFRESH, policy)

        now = time.time()
        self.assertTrue(policy.refresh(now))
        self.assertTrue(policy.refresh(now + 86400))  # 1 day in the future
        self.assertTrue(policy.refresh(now - 86400))  # 1 day in the past

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
        policy = CachePolicy.from_string("1d")

        self.assertFalse(policy.always_refresh)
        self.assertFalse(policy.never_refresh)
        self.assertFalse(policy.reset)

        now = time.time()
        self.assertTrue(policy.refresh(now - 90000))  # 25 hours in the past
        self.assertFalse(policy.refresh(now - 82800))  # 23 hours in the past

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
        self.assertTrue(CachePolicy.from_string("2d").refresh_file(path))
        self.assertFalse(CachePolicy.from_string("4d").refresh_file(path))

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


class TestFileCache(unittest.TestCase):

    def test_parse_cache_configuration(self):
        cache = FileCache(None)  # we don't need a Pystow module here

        with self.assertLogs() as log:
            cache._get_configuration("tests/input/cache.conf")
        self.assertTrue("missing caching policy" in log.output[0])
        self.assertTrue("invalid caching policy" in log.output[1])

        self.assertEqual(cache._default_policy._max_age, 86400 * 7)
        self.assertEqual(cache._policies[0][0], "uberon.db")
        self.assertEqual(cache._policies[0][1]._max_age, 86400 * 7 * 2)
        self.assertEqual(cache._policies[1][0], "fb*.db")
        self.assertEqual(cache._policies[1][1]._max_age, 86400 * 30)

    def test_policy_selector(self):
        cache = FileCache(None)
        cache._policies.append(("uberon.db", CachePolicy.from_string("2w")))
        cache._policies.append(("fbbt.db", CachePolicy.from_string("3w")))
        cache._policies.append(("fb*.db", CachePolicy.from_string("1m")))
        cache._policies.append(("fbcv.db", CachePolicy.from_string("1y")))

        # Prevent a configuration file from messing with the test
        cache._config_read = True

        # Check the right policy is selected
        self.assertEqual(cache._get_policy("uberon.db")._max_age, 86400 * 7 * 2)
        self.assertEqual(cache._get_policy("fbbt.db")._max_age, 86400 * 7 * 3)
        self.assertEqual(cache._get_policy("fbdv.db")._max_age, 86400 * 30)
        self.assertEqual(cache._get_policy("fbcv.db")._max_age, 86400 * 30)
        self.assertEqual(cache._get_policy("other.db")._max_age, 86400 * 7)

        # Check that "forced policy" takes precedence
        cache.force_policy(CachePolicy.from_string("2d"))
        self.assertEqual(cache._get_policy("uberon.db")._max_age, 86400 * 2)
        self.assertEqual(cache._get_policy("fbbt.db")._max_age, 86400 * 2)
        self.assertEqual(cache._get_policy("fbdv.db")._max_age, 86400 * 2)
        self.assertEqual(cache._get_policy("fbcv.db")._max_age, 86400 * 2)
        self.assertEqual(cache._get_policy("other.db")._max_age, 86400 * 2)
