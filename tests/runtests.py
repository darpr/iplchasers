#!/usr/bin/env python
# Author: darpr (Pradeep Sivakumar)

"""
1. Change directory t "iplchasers/tests.
2. Run.

[tests]$ python runtests.py
test_is_season_current (scrape_seasons_test.TestScrapeSeasons) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

"""

import os
import sys

testdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.dirname(testdir))

import unittest
import scrape_seasons_test


def suite():
    suite = unittest.TestSuite()
    suite.addTest(scrape_seasons_test.suite())

    return suite


def main():
    return unittest.TextTestRunner(verbosity=2).run(suite())


if __name__ == '__main__':
    sys.exit(not main().wasSuccessful())
