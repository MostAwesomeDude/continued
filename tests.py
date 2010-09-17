#!/usr/bin/env python

import itertools
import unittest

import continued

class ContinuedTest(unittest.TestCase):

    def test_pi(self):

        pi = continued.Continued.pi()
        digits = list(itertools.islice(pi.digits, 5))

        self.assertEqual(digits, [3, 7, 15, 1, 292])

if __name__ == "__main__":
    unittest.main()
