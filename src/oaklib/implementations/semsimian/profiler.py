"""Profiler for running Semsimian performance tests"""

import pstats
import sys


def display_stats(filename):
    p = pstats.Stats(filename)
    p.sort_stats("tottime").print_stats(20)


if __name__ == "__main__":
    display_stats(sys.argv[1])
