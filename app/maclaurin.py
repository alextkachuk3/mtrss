import threading
from math import pi
from decimal import Decimal, getcontext
from bernoulli import Bernoulli
from math import factorial


class TimeoutException(Exception):
    """Користувацьке виключення для таймауту."""
    pass


class Maclaurin:
    @staticmethod
    def cotangent_worker(x, epsilon, result_container):
        """Обчислює значення ряду і записує результат у контейнер."""
        try:
            if x == 0.0 or abs(x) >= pi:
                raise ValueError("x must be in the range (0, π) and not equal 0.")

            getcontext().prec = 100

            x = Decimal(x)
            epsilon = Decimal(epsilon)

            sum_result = Decimal(0)
            n = 0

            while True:
                bernoulli_number = Bernoulli.evaluate(2 * n)
                term = (
                    Decimal((-4) ** n)
                    * Decimal(bernoulli_number.numerator)
                    / Decimal(bernoulli_number.denominator)
                    * (x ** (2 * n - 1))
                    / Decimal(factorial(2 * n))
                )

                if abs(term) < epsilon:
                    break

                sum_result += term
                n += 1

            result_container["result"] = float(sum_result)
        except Exception as e:
            result_container["exception"] = e

    @staticmethod
    def cotangent(x, epsilon, timeout=60):
        """Обчислення значення котангенса з таймаутом."""
        result_container = {"result": None, "exception": None}
        thread = threading.Thread(target=Maclaurin.cotangent_worker, args=(x, epsilon, result_container))
        thread.start()
        thread.join(timeout)  # Очікування завершення потоку

        if thread.is_alive():
            thread.join(0)  # Примусове завершення потоку
            raise TimeoutException("The computation took too long and was terminated.")

        if result_container["exception"]:
            raise result_container["exception"]

        return result_container["result"]


