"""
Global rate limiting for calls to remote APIs.

All callers share a single fixed window of RATE_LIMIT seconds, within which at most
CALLS calls are allowed. Once the limit is reached, :func:`check_limit` blocks until
the window ends.
"""

import threading
import time

# calls per minute
CALLS = 300
RATE_LIMIT = 60

_lock = threading.Lock()
_window_start = float("-inf")
_num_calls = 0


def check_limit():
    """Block until another call to an API is allowed."""
    global _window_start, _num_calls
    with _lock:
        now = time.monotonic()
        if now - _window_start >= RATE_LIMIT:
            _window_start = now
            _num_calls = 0
        if _num_calls >= CALLS:
            time.sleep(RATE_LIMIT - (now - _window_start))
            _window_start = time.monotonic()
            _num_calls = 0
        _num_calls += 1
