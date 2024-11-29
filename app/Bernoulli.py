from fractions import Fraction
from math import comb


class Bernoulli:
    _cache = [Fraction(1, 1)]

    @staticmethod
    def evaluate(n):
        if n < 0:
            raise ValueError("The index of Bernoulli number cannot be negative.")

        if n % 2 != 0 and n > 1:
            return Fraction(0, 1)

        if n < len(Bernoulli._cache):
            return Bernoulli._cache[n]

        for m in range(len(Bernoulli._cache), n + 1):
            total_sum = Fraction(0, 1)

            for k in range(m):
                binomial = comb(m + 1, k)
                total_sum += binomial * Bernoulli._cache[k]

            b_m = -total_sum / Fraction(m + 1, 1)
            Bernoulli._cache.append(b_m)

        return Bernoulli._cache[n]
