#!/usr/bin/env python
import sys
import unittest

from fulltextsearch.test import test_score
from fulltextsearch.test import test_search_index


def run_tests():

    suite = unittest.TestLoader().loadTestsFromModule(test_search_index)
    suite.addTests(unittest.TestLoader().loadTestsFromModule(test_score))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.failures:
        sys.exit(1)
    elif result.errors:
        sys.exit(2)
    sys.exit(0)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
