Continued
=========

Continued is a simple library for representing and operating on numbers
represented as continued fractions.

Bugs
====

Plenty.

 - simplified() might be backwards.
 - Decimal decoding (or any other base, really) is missing.
 - Non-arithmetic operations are missing.
 - The API is too specialized towards simplified fractions.
 - sqrt(2) * sqrt(2) goes into an infinite loop, as does any other operation
   with an arbitrary string of 0.
