"""
Continued is an implementation of continued fraction handling and mathematical
operations.

Continued fractions are an alternative numbering system that can represent all
rational numbers in finite space and all quadratic irrationals in infinite
space with arbitrary precision.
"""

import decimal
import functools
import fractions
import itertools
import math

INFINITY = object()
"""
A sentinel object representing infinity.

In continued fraction math, positive and negative infinity have the same
meaning, so only one value is necessary.
"""

def gcd(a, b):
    """
    Return the greatest common divisor of a and b.

    One of a and b must be non-zero.

    >>> gcd(3, 6)
    3
    >>> gcd(19872, 526293)
    9
    """

    if not a:
        return b
    elif not b:
        return a

    while a and b and (a != b):
        if a > b:
            chaff, a = divmod(a, b)
        elif b > a:
            chaff, b = divmod(b, a)

    return a if a else b

def simplified(f):
    """
    Decorate a function to turn its generalized continued fraction digits into
    simplified, canonical continued fraction digits.
    """

    @functools.wraps(f)
    def simplifier(*args, **kwargs):
        """
        Given an iterator that yields (p q) generalized continued fraction
        tuples, generate the corresponding simplified continued fraction.
        """

        i = f(*args, **kwargs)

        a, b, c, d = 0, 1, 1, 0
        while True:
            try:
                p, q = next(i)
                a, b, c, d = b * q, a + b * p, d * q, c + d * p

                ac = a // c if c else None
                bd = b // d if d else None

                if ac and bd and ac == bd:
                    r = ac
                    a, b, c, d = c, d, a - c * r, b - d * r
                    yield r

            except ValueError:
                yield b
                return

    return simplifier

class Continued(object):
    """
    An implementation of continued fractions.

    Continued fractions are a complex and elegant method for representing
    certain numbers. In particular, finite continued fractions are terrific
    for representing rationals, and infinite continued fractions can perfectly
    represent quadratic surds and certain transcendental identities.
    """

    finite = True
    """
    Whether this instance is finite or infinite.
    """

    @classmethod
    def from_decimal(cls, d):
        """
        Create a new continued fraction from a `decimal.Decimal` instance.
        """

        numerator = d
        denominator = 1

        # Is there a faster way to do this?
        while numerator != numerator.to_integral_value():
            numerator *= 10
            denominator *= 10

        return Rational(int(numerator), int(denominator))

    @classmethod
    def from_float(cls, f):
        """
        Create a new continued fraction from a float.

        This is hilariously imprecise, but it does the job well enough for
        most people using it.
        """

        return cls.from_decimal(decimal.Decimal(repr(f)))

    @classmethod
    def from_fraction(cls, fraction):
        """
        Create a new continued fraction from a `fractions.Fraction` instance.

        Incidentally, this method works with any `numbers.Rational`
        implementor, not just `Fraction`.
        """

        return Rational(fraction.numerator, fraction.denominator)

    def __init__(self):
        self.digitlist = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        l = list(itertools.islice(self.digits(), 10))
        if len(l) == 10:
            # Truncate and append an ellipsis.
            l = l[:9] + ["..."]
        s = ", ".join(str(x) for x in l)
        return "Continued(%s)" % s

    def __add__(self, other):
        return self.combine(other, (0, 1, 1, 0, 1, 0, 0, 0))

    def __sub__(self, other):
        return self.combine(other, (0, 1, -1, 0, 1, 0, 0, 0))

    def __mul__(self, other):
        return self.combine(other, (0, 0, 0, 1, 1, 0, 0, 0))

    def __div__(self, other):
        return self.combine(other, (0, 1, 0, 0, 0, 0, 1, 0))

    def __truediv__(self, other):
        return self.__div__(other)

    def __cmp__(self, other):
        if not isinstance(other, Continued):
            return NotImplemented

        if not self.finite and not other.finite:
            return NotImplemented

        toggle = False
        for x, y in itertools.izip_longest(self.digits(), other.digits(),
            fillvalue=0):
            if x != y:
                if toggle:
                    return -1 if x > y else 1
                else:
                    return -1 if x < y else 1
            toggle = not toggle
        return 0

    @property
    def approximations(self):
        """
        Retrieve successively closer rational approximants lazily.
        """

        d = self.digits()
        oldoldp = next(d)
        oldoldq = 1
        yield oldoldp, oldoldq
        digit = next(d)
        oldp = digit * oldoldp + 1
        oldq = digit
        yield oldp, oldq
        while True:
            digit = next(d)
            p = digit * oldp + oldoldp
            q = digit * oldq + oldoldq
            yield p, q
            oldp, oldoldp = p, oldp
            oldq, oldoldq = q, oldq


    def digits(self):
        """
        Retrieve the digits of this continued fraction lazily.

        Returns an iterable of some sort.
        """

        raise NotImplementedError

    @property
    def fractions(self):
        """
        A convenience property for retrieving fractional approximants as
        `fractions.Fraction` instances.
        """

        for p, q in self.approximations:
            yield fractions.Fraction(p, q)

    def combine(self, other, initial):
        # XXX this isn't quite right
        cls = Continued

        if isinstance(other, int):
            other = Integer(other)

        instance = cls()
        instance.x = self.digits
        instance.y = other.digits
        instance.initial = initial
        instance.digits = instance.combiner
        instance.finite = self.finite and other.finite
        return instance

    def combiner(self):
        a, b, c, d, e, f, g, h = self.initial

        iterx = itertools.chain(self.x(), itertools.repeat(INFINITY))
        itery = itertools.chain(self.y(), itertools.repeat(INFINITY))

        use_x = True
        x_is_empty = False
        y_is_empty = False
        while any((e, f, g, h)):
            old = a, b, c, d, e, f, g, h
            # print old
            ae = a // e if e else None
            bf = b // f if f else None
            cg = c // g if g else None
            dh = d // h if h else None
            if ae == bf and bf == cg and cg == dh:
                r = ae
                # print r
                # Output a term.
                a, b, c, d, e, f, g, h = (e, f, g, h,
                    a - e * r, b - f * r, c - g * r, d - h * r)
                yield r
            elif self.finite and x_is_empty and y_is_empty:
                return
            else:
                # Which input to choose?
                if x_is_empty:
                    use_x = False
                elif y_is_empty:
                    use_x = True
                # If we've had the same state in the state machine since
                # last time, why not try the other input?
                elif old == (a, b, c, d, e, f, g, h):
                    use_x = not use_x
                # if None not in (ae, bf, cg) and abs(bf - ae) > abs(cg - ae):
                if use_x:
                    # Input from x.
                    p = next(iterx)
                    if p is INFINITY:
                        # Infinity: Replicate channels.
                        a, c, e, g = b, d, f, h
                        x_is_empty = True
                    else:
                        # Ingestion.
                        a, b, c, d, e, f, g, h = (
                            b, a + b * p, d, c + d * p,
                            f, e + f * p, h, g + h * p)
                else:
                    # Input from y.
                    q = next(itery)
                    if q is INFINITY:
                        # Infinity: Replicate channels.
                        a, b, e, f = c, d, g, h
                        y_is_empty = True
                    else:
                        # Ingestion.
                        a, b, c, d, e, f, g, h = (
                            c, d, a + c * q, b + d * q,
                            g, h, e + g * q, f + h * q)

    def normalize(self):
        if not self.finite:
            raise ValueError, "Can't normalize infinite continued fractions!"
        try:
            while True:
                index = self.digitlist.index(0, 1)
                if index == len(self.digitlist) + 1:
                    self.digitlist = self.digitlist[:-1]
                else:
                    digit = sum(self.digitlist[index - 1:index + 2])
                    self.digitlist = (self.digitlist[:index - 1] + [digit] +
                        self.digitlist[index + 2:])
        except ValueError:
            pass

class Integer(Continued):
    """
    An integer.
    """

    finite = True

    def __init__(self, integer):
        self.i = integer

    def digits(self):
        yield self.i

class Rational(Continued):
    """
    A standard rational number.

    Continued fractions can represent all rational numbers precisely with a
    finite number of digits.
    """

    finite = True

    def __init__(self, numerator, denominator):
        self.n = numerator
        self.d = denominator

    def digits(self):
        n, d = self.n, self.d

        # Special cases. 0 / q == [0].
        if n == 0:
            yield 0
            return

        # Should this raise ValueError instead, maybe?
        if d == 0:
            yield 0
            return

        # If it's in [0, 1] then switch it around to avoid a divide-by-zero.
        if d > n:
            yield 0
            n, d = d, n

        while True:
            # divmod() the next digit.
            digit, n = divmod(n, d)

            # Catch trailing 1/1 (or any other equivalent ratio).
            if n == d:
                yield digit + 1
                return

            # A zero snuck into the fraction; the previous term was an exact
            # division and we can end now.
            if digit == 0:
                return

            yield digit

            # A zero will be in the next fraction; we are finished.
            if n == 0:
                break

            n, d = d, n

class Surd(Continued):
    """
    A quadratic irrational.
    """

    finite = False

    def __init__(self, integer):
        self.i = integer

    def digits(self):
        l = []
        m = 0
        d = 1
        a = int(math.sqrt(self.i))
        while (m, d, a) not in l:
            l.append((m, d, a))
            yield a
            m = d * a - m
            d = (self.i - m**2) / d
            a = int((math.sqrt(self.i) + m) / d)
        # Extract just the a component (index 2)
        repeating = zip(*l[l.index((m, d, a)):])[2]
        iterator = itertools.cycle(repeating)
        while True:
            yield next(iterator)

class E(Continued):
    """
    Euler's number.
    """

    finite = False

    def digits(self):
        yield 2
        i = 2
        mod = 1
        while True:
            mod += 1
            if mod % 3:
                yield 1
            else:
                yield i
                i += 2
                mod = 0

class Phi(Continued):
    """
    The Golden Ratio.
    """

    finite = False

    def digits(self):
        return itertools.repeat(1)

class Pi(Continued):
    """
    Pi.
    """

    finite = False

    @simplified
    def digits(self):
        """
        There are several formulae for pi as a generalized continued fraction,
        including these three:

         - (0 4); (1 1), (2 9), (2 25), (2 49), (2 81), ...
         - (3 1); (6 9), (6 25), (6 49), (6 81), ...
         - (0 4); (1 1), (3 4), (5 9), (7 16), ...

        Of these three, the third grows the slowest and so it is the one
        implmented here.
        """
        yield (0, 4)
        p = 1
        q = 1
        while True:
            yield (p, q**2)
            p += 2
            q += 1
