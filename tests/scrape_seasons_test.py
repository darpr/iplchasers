#!/usr/bin/env python
# Author: darpr (Pradeep Sivakumar)


import sys
sys.path.append("../")

import os
import unittest
import scrape_seasons


class TestScrapeSeasons(unittest.TestCase):
    def setUp(self):
        pass

    def test_is_season_current(self):
        # setup
        year = 2010
        expected_current = False

        # method under test
        actual_current = scrape_seasons.is_season_current(year)

        # assertion
        self.assertEqual(expected_current, actual_current)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestScrapeSeasons, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main()
