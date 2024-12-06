import math
from decimal import Decimal, getcontext
from threading import Thread
from math import factorial
from app.bernoulli import Bernoulli
from app.file_writer import FileWriter


class TimeoutException(Exception):
    pass


class Maclaurin:
    @staticmethod
    def cotangent_worker(x, epsilon, result_container):
        try:
            getcontext().prec = 100
            x = Decimal(x)
            epsilon = Decimal(epsilon)

            sum_result = Decimal(0)
            n = 0

            while True:
                bernoulli_number = Bernoulli.evaluate(2 * n)
                term = (
                    Decimal((-4) ** n)
                    * Decimal(bernoulli_number.numerator) / Decimal(bernoulli_number.denominator)
                    * (x ** (2 * n - 1))
                    / Decimal(factorial(2 * n))
                )

                if abs(term) < epsilon:
                    break

                sum_result += term
                n += 1

            significant_digits = -int(epsilon.log10())
            result_container["result"] = (round(float(sum_result), significant_digits), n)
        except Exception as e:
            result_container["exception"] = e


    @staticmethod
    def cotangent(x, epsilon, timeout=900):
        result_container = {"result": None, "exception": None}
        thread = Thread(target=Maclaurin.cotangent_worker, args=(x, epsilon, result_container))
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            raise TimeoutException("The computation took too long (timeout exceeded).")

        if result_container["exception"]:
            raise result_container["exception"]

        return result_container["result"]


class CotangentCalculator:
    def __init__(self):
        self.results = []
        self.file_writer = FileWriter()

    def input_data(self):
        while True:
            x_input = input("Задайте аргумент функції (або введіть 'Кінець' для завершення): ").strip()
            if x_input.lower() == "кінець":
                break

            try:
                x = float(x_input)
            except ValueError:
                print("Некоректне значення x. Спробуйте ще раз.")
                continue

            if not (0 < x < math.pi):
                print("Значення x має бути в межах (0, π)")
                continue

            e_input = input("Задайте точність обчислення: ").strip()
            try:
                epsilon = float(e_input)
                if not (0 < epsilon < 1):
                    raise ValueError
            except ValueError:
                print("Некоректне значення точності. Спробуйте ще раз.")
                continue

            try:
                result, n = Maclaurin.cotangent(x, epsilon)
                significant_digits = abs(int(math.log10(epsilon)))
                formatted_result = f"{result:.{significant_digits}f}"
                formatted_x = f"{x:.12g}".rstrip('0').rstrip('.')
                self.results.append((x, epsilon, result, n))
                print(f"Значення функції: {formatted_result}, Аргумент x: {formatted_x}, Кількість членів ряду: {n}")
            except TimeoutException:
                print("Обчислення перевищило максимальний час (15 хвилин).")
                self.results.append((x, epsilon, None, None))
            except Exception as e:
                print(f"Помилка: {e}")
                self.results.append((x, epsilon, None, None))

    def save_results(self):
        self.file_writer.save_results(self.results)
