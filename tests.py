#!/usr/bin/env python

import itertools
import unittest

import continued

class ContinuedBugfixTest(unittest.TestCase):

    def test_one(self):

        one = continued.Rational(1, 1)

class ContinuedFunctionalityTest(unittest.TestCase):

    def test_arithmetic(self):

        first = continued.Rational(3, 5)
        second = continued.Rational(7, 11)

        third = continued.Rational(68, 55)

        self.assertTrue(first + second == third)

        fourth = continued.Rational(21, 55)

        self.assertTrue(first * second == fourth)

    def test_comparisons(self):

        smaller = continued.Rational(100, 89)
        larger = continued.Rational(244, 217)

        self.assertTrue(smaller < larger)

        threeonefive = continued.Continued.from_float(3.15)
        pi = continued.Pi()

        self.assertTrue(threeonefive > pi)

        one = continued.Rational(1, 1)

        self.assertTrue(one == one)

    def test_e(self):

        e = continued.E()
        digits = list(itertools.islice(e.digits(), 5))

        self.assertEqual(digits, [2, 1, 2, 1, 1])

    def test_phi(self):

        phi = continued.Phi()
        digits = list(itertools.islice(phi.digits(), 5))

        self.assertEqual(digits, [1, 1, 1, 1, 1])

    def test_pi(self):

        pi = continued.Pi()
        digits = list(itertools.islice(pi.digits(), 5))

        self.assertEqual(digits, [3, 7, 15, 1, 292])

    def test_rational(self):

        eighth = continued.Rational(1, 8)

        self.assertEqual(list(eighth.digits()), [0, 8])

        fortytwo = continued.Rational(42, 10)

        self.assertEqual(list(fortytwo.digits()), [4, 5])

        fiveeighths = continued.Rational(5, 8)

        self.assertEqual(list(fiveeighths.digits()), [0, 1, 1, 1, 2])

if __name__ == "__main__":
    unittest.main()
