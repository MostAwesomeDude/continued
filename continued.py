import fractions
import itertools
import math

def simplified(i):
    """
    Given an iterator that yields (p q) generalized continued fraction tuples,
    generate the corresponding simplified continued fraction.
    """

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
            raise StopIteration

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

    This is to avoid isinstance() calls on `digits`.
    """

    @classmethod
    def from_int(cls, i):
        instance = cls()
        instance.digitlist = [i]
        return instance

    @classmethod
    def from_fraction(cls, fraction):
        """
        Create a new continued fraction from a `fractions.Fraction` instance.

        Incidentally, this method works with any `numbers.Rational`
        implementor, not just `Fraction`.
        """

        return cls.from_rational(fraction.numerator, fraction.denominator)

    @classmethod
    def from_rational(cls, numerator, denominator):
        instance = cls()
        factor = gcd(numerator, denominator)

        # Special case: If GCD(p, q) is zero, then we have 0 / 0 == [0].
        if not factor:
            instance.digitlist.append(0)
            return instance

        numerator //= factor
        denominator //= factor
        if denominator > numerator:
            instance.digitlist.append(0)
            numerator, denominator = denominator, numerator
        # Do the divmod() dance to generate GCD slices.
        while True:
            digit, numerator = divmod(numerator, denominator)
            # print digit, numerator, denominator
            if not digit:
                break
            instance.digitlist.append(digit)
            if not numerator:
                break
            numerator, denominator = denominator, numerator
        # In the line above, we switched names, but this is still the previous
        # denominator.
        # Only record it if not 1; if it's 1, add it to the last item instead.
        if instance.digitlist[-1] == 1:
            instance.digitlist = instance.digitlist[:-1]
            instance.digitlist[-1] += 1
        instance.normalize()
        return instance

    @classmethod
    def e(cls):
        instance = cls()
        instance.finite = False
        def generator():
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
        instance.make_digits = generator()
        return instance

    @classmethod
    def phi(cls):
        """
        Generate phi, the golden ratio.
        """

        instance = cls()
        instance.finite = False
        instance.make_digits = itertools.repeat(1)
        return instance

    @classmethod
    def pi(cls):
        """
        Generate pi.

        There are several formulae for pi as a generalized continued fraction,
        including these three:

         - (0 4); (1 1), (2 9), (2 25), (2 49), (2 81), ...
         - (3 1); (6 9), (6 25), (6 49), (6 81), ...
         - (0 4); (1 1), (3 4), (5 9), (7 16), ...

        Of these three, the third grows the slowest and so it is the one
        implmented here.
        """

        instance = cls()
        instance.finite = False
        def generator():
            yield (0, 4)
            p = 1
            q = 1
            while True:
                yield (p, q**2)
                p += 2
                q += 1
        instance.make_digits = simplified(generator())
        return instance

    @classmethod
    def sqrt(cls, i):
        instance = cls()
        instance.finite = False
        def generator(i):
            l = []
            m = 0
            d = 1
            a = int(math.sqrt(i))
            while (m, d, a) not in l:
                l.append((m, d, a))
                yield a
                m = d * a - m
                d = (i - m**2) / d
                a = int((math.sqrt(i) + m) / d)
            # Extract just the a component (index 2)
            repeating = zip(*l[l.index((m, d, a)):])[2]
            iterator = itertools.cycle(repeating)
            while True:
                yield next(iterator)
        instance.make_digits = generator(i)
        return instance

    def __init__(self):
        self.digitlist = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.finite:
            l = self.digitlist
        else:
            l = list(itertools.islice(self.digits, 10)) + ["..."]
        return "Continued(%s)" % l

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

    @property
    def approximations(self):
        """
        Retrieve successively closer rational approximants lazily.
        """

        d = self.digits
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


    @property
    def digits(self):
        """
        Retrieve the digits of this continued fraction lazily.

        Returns an iterable of some sort.
        """

        if self.finite:
            return self.digitlist
        else:
            self.make_digits, retval = itertools.tee(self.make_digits)
            return retval

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
            other = Continued.from_int(other)

        instance = cls()
        instance.x = self.digits
        instance.y = other.digits
        instance.make_digits = instance.combiner(initial)
        if self.finite and other.finite:
            instance.digitlist = list(instance.make_digits)
        else:
            instance.finite = False
        return instance

    def combiner(self, initial):
        a, b, c, d, e, f, g, h = initial

        iterx = itertools.chain(self.x, itertools.repeat(None))
        itery = itertools.chain(self.y, itertools.repeat(None))

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
                raise StopIteration
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
                    if p is None:
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
                    if q is None:
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
            a -= b
        elif b > a:
            b -= a

    return a if a else b
