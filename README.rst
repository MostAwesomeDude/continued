.. include:: <isogrk1.txt>

Continued
=========

Continued is a simple library for representing and operating on numbers
represented as continued fractions.

Features
--------

 * Conversion from a plethora of representations to continued fractions

   * int
   * float
   * decimal.Decimal
   * fractions.Fraction and numbers.Rational

 * Basic arithmetic: addition, subtraction, multiplication, division
 * Popular irrational and transcendental identities, to arbitrary (infinite)
   precision

   * *e* (Euler's number)
   * |pgr|
   * |phgr| (the Golden Ratio)

 * Arbitrary-precision quadratic surds

Bugs
----

Plenty.

 - sqrt(2) * sqrt(2) goes into an infinite loop, as does any other operation
   with an arbitrary string of 0.

Some enhancements are planned.

 - Surds should permit the form (a + sqrt(b))/c without an extra pair of
   combination generators.
 - Trigonometric operators.
 - Radix-based decoding.

Changelog
---------

1.0
^^^

Initial release.
