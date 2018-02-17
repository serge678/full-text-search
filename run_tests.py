#!/usr/bin/env python
import sys
import unittest

from full_text_search.test import test_score
from full_text_search.test import test_search_index


def run_tests():

    unittest.TestLoader().loadTestsFromModule(test_score)
    suite = unittest.TestLoader().loadTestsFromModule(test_search_index)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.failures:
        sys.exit(1)
    elif result.errors:
        sys.exit(2)
    sys.exit(0)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])