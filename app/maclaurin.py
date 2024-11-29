from math import pi
from decimal import Decimal, getcontext
from bernoulli import Bernoulli
from math import factorial


class Maclaurin:
    @staticmethod
    def cotangent(x, epsilon):
        if x == 0.0 or abs(x) >= pi:
            raise ValueError("x must be in the range (0, π) and not equal 0.")

        # Налаштування точності Decimal
        getcontext().prec = 1000  # Встановлення високої точності для обчислень

        x = Decimal(x)
        epsilon = Decimal(epsilon)

        sum_result = Decimal(0)
        n = 0

        while True:
            # Обчислення поточного члена ряду
            bernoulli_number = Bernoulli.evaluate(2 * n)
            bernoulli_decimal = Decimal(bernoulli_number.numerator) / Decimal(bernoulli_number.denominator)
            factor = Decimal((-4) ** n)
            denominator = Decimal(factorial(2 * n))
            term = factor * bernoulli_decimal * (x ** (2 * n - 1)) / denominator

            if abs(term) < epsilon:
                break

            sum_result += term
            n += 1

        print(n)
        return float(sum_result)
