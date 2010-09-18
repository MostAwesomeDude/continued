#!/usr/bin/env python

import itertools
import unittest

import continued

class ContinuedBugfixTest(unittest.TestCase):

    def test_one(self):

        one = continued.Continued.from_rational(1, 1)

class ContinuedFunctionalityTest(unittest.TestCase):

    def test_comparisons(self):

        smaller = continued.Continued.from_rational(100, 89)
        larger = continued.Continued.from_rational(244, 217)

        self.assertTrue(smaller < larger)

        pi = continued.Continued.pi()
        threeonefive = continued.Continued.from_float(3.15)

        self.assertTrue(threeonefive > pi)

        one = continued.Continued.from_rational(1, 1)

        self.assertTrue(one == one)

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

    def test_rational(self):

        eighth = continued.Continued.from_rational(1, 8)

        self.assertEqual(eighth.digits, [0, 8])

        fortytwo = continued.Continued.from_rational(42, 10)

        self.assertEqual(fortytwo.digits, [4, 5])

        fiveeighths = continued.Continued.from_rational(5, 8)

        self.assertEqual(fiveeighths.digits, [0, 1, 1, 1, 2])

if __name__ == "__main__":
    unittest.main()
