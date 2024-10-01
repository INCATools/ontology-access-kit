import fnmatch
import logging
import os.path
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

from appdirs import user_config_dir
from pystow.utils import base_from_gzip_name, name_from_url

from oaklib.datamodels.vocabulary import APP_NAME

_durations = {"d": 1, "w": 7, "m": 30, "y": 365}
_logger = logging.getLogger(__name__)


class CachePolicy(object):
    """Represents the behaviour of a cache.

    Once a CachePolicy object has been created (typically using the static
    constructor from_string, or one of the static properties for special
    policies), use the refresh_file() method to determine whether a given file
    should be refreshed:

    >>> if my_policy.refresh_file(my_cache_file):
    >>>     # refresh the cache file
    >>> else:
    >>>     # no need to refresh

    Use the refresh() method to check an arbitrary timestamp against the policy
    (e.g. if the cached data is not in a file):

    >>> if my_policy.refresh(timestamp_of_last_refresh):
    >>>     # refresh the data
    """

    def __init__(self, max_age):
        """Creates a new instance.

        If positive, the max_age parameter is the number of seconds after which
        cached data should be refreshed. This parameter can also accept some
        special values:

        - 0 indicates refresh should always occur, regardless of the age of the
          cached data;
        - -1 indicates the cache should be cleared.

        It is recommended to obtain such special policies using either the
        from_string static constructor or the static properties REFRESH, RESET,
        rather than calling this constructor directly. This allows comparing a
        policy against those pre-established policies as follows:

        >>> if my_policy == CachePolicy.RESET:
        >>>     # force reset
        """

        self._max_age = max_age

    def refresh(self, then):
        """Indicates whether a refresh should occur for data last refreshed at
        the indicated time.

        :param then: the time the data were last cached or refreshed, in
            seconds since the Unix epoch
        :return: True if the data should be refreshed, otherwise False
        """

        if self._max_age <= 0:
            # Forceful refresh/reset, even if "then" is somehow in the future
            return True
        return time.time() - then > self._max_age

    def refresh_file(self, pathname):
        """Indicates whether the specified file should be refreshed.

        This uses the last modification time of the file to determine the age
        of the cached data. If the file does not exist, a refresh will
        necessarily be mandated.

        :param pathname: the path to the file that maybe should be refreshed
        :return: True if the file should be refreshed, otherwise False
        """

        if not os.path.exists(pathname):
            return True
        return self.refresh(os.path.getmtime(pathname))

    @property
    def always_refresh(self):
        """Indicates whether this policy mandates a systematic refresh of the
        cache."""

        return self._max_age == 0

    @property
    def never_refresh(self):
        """Indicates whether this policy mandates never refreshing the
        cache."""

        return self._max_age == timedelta.max.total_seconds()

    @property
    def reset(self):
        """Indicates whether this policy mandates a reset of the cache."""

        return self._max_age == -1

    _refresh_policy = None
    _no_refresh_policy = None
    _reset_policy = None
    _click_type = None

    @classmethod
    def from_string(cls, value):
        """Creates a new instance from a string representation.

        This is the recommended way of getting a CachePolicy object. The value
        can be either:

        - a number of seconds, followed by 's';
        - a number of days, optionally followed by 'd';
        - a number of weeks, followed by 'w';
        - a number of months, followed by 'm';
        - a number of years, followed by 'y'.

        Such a value will result in a policy mandating that cached data are
        refreshed after the elapsed number of seconds, days, weeks, months, or
        years since they were last cached. Note that in this context, a 'month'
        is always 30 days and a 'year' is always 365 days. That is, '3m' is
        merely a shortcut for '90d' (or simply '90') and '2y' is merely a
        shortcut for '730d'.

        The value can also be:

        - 'refresh', to get the REFRESH policy;
        - 'no-refresh', to get the NO_REFRESH policy;
        - 'reset' or 'clear', to get the RESET policy.

        Any other value will cause None to be returned.
        """

        value = value.lower()
        if value == "refresh":
            return cls.REFRESH
        elif value == "no-refresh":
            return cls.NO_REFRESH
        elif value in ["reset", "clear"]:
            return cls.RESET
        else:
            if m := re.match("^([0-9]+)([sdwmy])?", value):
                num, qual = m.groups()
                if not qual:
                    qual = "d"
                if qual == "s":
                    return cls(int(num))
                else:
                    return cls(timedelta(days=int(num) * _durations[qual]).total_seconds())
            return None

    @classmethod
    @property
    def REFRESH(cls):
        """A policy that cached data should always be refreshed."""

        if cls._refresh_policy is None:
            cls._refresh_policy = cls(max_age=0)
        return cls._refresh_policy

    @classmethod
    @property
    def NO_REFRESH(cls):
        """A policy that cached data should never be refreshed."""

        if cls._no_refresh_policy is None:
            cls._no_refresh_policy = cls(max_age=timedelta.max.total_seconds())
        return cls._no_refresh_policy

    @classmethod
    @property
    def RESET(cls):
        """A policy that cached data should be cleared and refreshed."""

        if cls._reset_policy is None:
            cls._reset_policy = cls(max_age=-1)
        return cls._reset_policy

    @classmethod
    @property
    def ClickType(cls):
        """Helper method to parse a CachePolicy with Click.

        Use that method as the 'type' of a Click option to let Click
        automatically convert the value of the option into a CachePolicy
        instance.

        Example:

        >>> @click.option("--caching", type=CachePolicy.ClickType,
                          default="1w")
        """

        if cls._click_type is None:
            from click import ParamType

            class CachePolicyParamType(ParamType):
                name = "cache-policy"

                def convert(self, value, param, ctx):
                    if isinstance(value, cls):
                        return value

                    if p := cls.from_string(value):
                        return p
                    else:
                        self.fail(f"Cannot convert '{value}' to a cache policy", param, ctx)

            cls._click_type = CachePolicyParamType()

        return cls._click_type


class FileCache(object):
    """Represents a file-based cache.

    This is intended as a layer built on top of Pystow, to add cache management
    features that are lacking in Pystow.
    """

    def __init__(self, module):
        """Creates a new instance.

        :param module: a Pystow module representing the location where cached
            data will be stored; all methods in this class will defer to this
            object whenever a file needs to be actually refreshed
        """

        self._module = module
        self._default_policy = CachePolicy.from_string("1w")
        self._forced_policy = None
        self._policies = []
        self._config_file = os.path.join(user_config_dir(APP_NAME), "cache.conf")
        self._config_read = False

    def force_policy(self, policy):
        """Forces the cache to use the specified policy, regardless of any
        otherwise configured policies.

        :param policy: the policy to use; may be None to allow the use of
            configured policies
        """

        self._forced_policy = policy

    def ensure_gunzip(self, url, name=None, autoclean=True):
        """Looks up and maybe downloads and gunzips a file.

        This is a wrapper around Pystow's method of the same name. It behaves
        similarly but, if the file is already present in the cache, it will
        additionally check whether it needs to be downloaded again, according
        to the current caching policy.
        """

        if self._forced_policy == CachePolicy.RESET:
            self.clear(pattern="*.db*")

        if not name:
            name = name_from_url(url)

        ungz_name = base_from_gzip_name(name)
        db_path = self._module.join(name=ungz_name)

        if self._get_policy(ungz_name).refresh_file(db_path):
            self._module.ensure_gunzip(url=url, name=name, autoclean=autoclean, force=True)

        return db_path

    def ensure(self, *subkeys, url, name=None):
        """Looks up and maybe downloads a file."""

        if self._forced_policy == CachePolicy.RESET:
            self.clear(pattern="*.db*")

        if not name:
            name = name_from_url(url)

        path = self._module.join(*subkeys, name=name)

        if self._get_policy(name).refresh_file(path):
            self._module.ensure(*subkeys, url=url, name=name, force=True)

        return path

    def get_contents(self, subdirs=False):
        """Gets a list of files present in the cache.

        This returns a list of (name, size, mtime) tuples, where:

        - name is the filename (relative to the cache directory);
        - size is its size in bytes;
        - mtime is its modification time, as a datetime object.

        If subdirs is True, the list includes files present in any subdirectory
        within the cache. The default is to list only the files immediately
        under the cache directory, excluding any subdirectory.
        """

        contents = []
        for path, name in self._iter_files(subdirs=subdirs):
            stat = path.stat()
            contents.append((name, stat.st_size, datetime.fromtimestamp(stat.st_mtime)))
        return contents

    def clear(self, subdirs=False, older_than=None, pattern="*"):
        """Deletes files present in the cache.

        :param subdirs: if True, deletes files in subdirectories
        :param older_than: if set, only deletes files that were last modified
            longer ago than the specified number of days
        :param pattern: only deletes files matching the specified pattern
        :return: a list of tuples describing the files that were deleted; the
            tuples are similar to the ones returned by get_contents, except
            that the third item is the age of the deleted file (as a timedelta
            object relative to current time)
        """

        now = time.time()
        cleared = []
        for path, name in self._iter_files(subdirs=subdirs, pattern=pattern):
            stat = path.stat()
            age = now - stat.st_mtime
            if older_than is not None and age <= older_than * 86400:
                continue
            cleared.append((name, stat.st_size, timedelta(seconds=age)))
            path.unlink()
        return cleared

    def _iter_files(self, subdirs=False, pattern="*"):
        """Helper method to get the files present in the cache.

        :param subdirs: if True, get files in subdirectories
        :param pattern: get files matching the pattern
        :return: a list of (path, name) tuples where path is a Path object
            pointing to a file in the cache, and name is its name relative to
            the cache directory
        """

        base = self._module.join()
        if subdirs:
            pattern = "**/" + pattern
        return [(c, str(c.relative_to(base))) for c in Path(base).glob(pattern) if c.is_file()]

    def _get_policy(self, name):
        """Gets the caching policy to use for the specified name."""

        if self._forced_policy is not None:
            return self._forced_policy

        if not self._config_read:
            self._get_configuration(self._config_file)

        for pattern, policy in self._policies:
            if fnmatch.fnmatch(name, pattern):
                return policy

        return self._default_policy

    def _get_configuration(self, pathname):
        """Gets cache policies from a configuration file."""

        if not os.path.exists(pathname):
            return

        filename = os.path.basename(pathname)
        with open(pathname, "r") as f:
            for n, line in enumerate(f):
                if line.startswith("#") or line.isspace():
                    continue

                items = line.split("=", maxsplit=1)
                pattern = items[0].strip()
                if len(items) != 2:
                    _logger.warning(
                        f"{filename}({n}): Ignoring missing caching policy for {pattern}"
                    )
                    continue

                policy = CachePolicy.from_string(items[1].strip())
                if policy is None:
                    _logger.warning(
                        f"{filename}({n}): Ignoring invalid caching policy for {pattern}"
                    )
                    continue

                if pattern in ["default", "*"]:
                    self._default_policy = policy
                else:
                    self._policies.append((pattern, policy))

        self._config_read = True
