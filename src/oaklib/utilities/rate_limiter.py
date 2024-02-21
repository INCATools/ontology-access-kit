"""
https://stackoverflow.com/questions/40748687/python-api-rate-limiting-how-to-limit-api-calls-globally
"""

from ratelimit import limits, sleep_and_retry

# calls per minute
CALLS = 300
RATE_LIMIT = 60
# CALLS = 1
# RATE_LIMIT = 10


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    """Empty function just to check for calls to API"""
    return
