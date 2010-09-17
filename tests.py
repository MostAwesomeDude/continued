#!/usr/bin/env python

import itertools
import unittest

import continued

class ContinuedTest(unittest.TestCase):

    def test_e(self):

        e = continued.Continued.e()
        digits = list(itertools.islice(e.digits, 5))

        self.assertEqual(digits, [2, 1, 2, 1, 1])

    def test_phi(self):

        phi = continued.Continued.phi()
        digits = list(itertools.islice(phi.digits, 5))

        self.assertEqual(digits, [1, 1, 1, 1, 1])

    def test_pi(self):

        pi = continued.Continued.pi()
        digits = list(itertools.islice(pi.digits, 5))

        self.assertEqual(digits, [3, 7, 15, 1, 292])

if __name__ == "__main__":
    unittest.main()
