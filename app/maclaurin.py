import math
import os
import datetime
from decimal import Decimal, getcontext
from threading import Thread
from math import factorial
from bernoulli import Bernoulli


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

            result_container["result"] = (float(sum_result), n)
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
        self.file_name = None

    def input_data(self):
        while True:
            x_input = input("Задайте аргумент функції (або введіть 'Кінець' для завершення): ").strip()
            if x_input.lower() == "кінець":
                break

            try:
                x = float(x_input)
                if not (0 < x < math.pi):
                    raise ValueError
            except ValueError:
                print("Некоректне значення x. Спробуйте ще раз.")
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
                self.results.append((x, epsilon, result, n))
                print(f"Значення функції: {result:.12f}, Кількість членів ряду: {n}")
            except TimeoutException:
                print("Обчислення перевищило максимальний час (15 хвилин).")
                self.results.append((x, epsilon, None, None))
            except Exception as e:
                print(f"Помилка: {e}")
                self.results.append((x, epsilon, None, None))

    def save_results(self):
        if not self.results:
            print("Результати відсутні, нічого записувати.")
            return

        save_choice = input("Записати результати у файл? (Так/Ні): ").strip().lower()
        if save_choice != "так":
            print("Дані у файл не записано.")
            return

        if self.file_name:
            reuse_choice = input(f"Записати результати у файл {self.file_name}? (Так/Ні): ").strip().lower()
            if reuse_choice == "так":
                self._write_to_file(self.file_name)
                return

        while True:
            file_name = input(
                "Введіть ім'я нового файлу (до 5 символів, або '*' для відмови): "
            ).strip()
            if file_name == "*":
                print("Дані у файл не записано.")
                return

            if not (1 <= len(file_name) <= 5 and file_name.isalnum()):
                print("Некоректне ім'я файлу. Спробуйте ще раз.")
                continue

            self.file_name = file_name + ".txt"
            break

        self._write_to_file(self.file_name)

    def _write_to_file(self, file_name):
        now = datetime.datetime.now().strftime("%d.%m.%Y")
        total_records = 0
        table_header = (
            "+-----------------+--------------------+--------------------+---------------------+-------------------------+\n"
            "|Дата (ДД.ММ.РРРР)|     Аргумент x     |     Точність e     |  Результат функції  | Кількість членів ряду N |\n"
            "+-----------------+--------------------+--------------------+---------------------+-------------------------+\n"
        )
        table_rows = []

        for x, epsilon, result, n in self.results:
            result_str = f"{result:.12f}" if result is not None else "-"
            n_str = str(n) if n is not None else "-"
            row = (
                f"|{now:^17}|{x:^20.12f}|{epsilon:^20.12f}|{result_str:^21}|{n_str:^21}|\n"
            )
            table_rows.append(row)
            table_rows.append("+-----------------+--------------------+--------------------+---------------------+-------------------------+\n")
            total_records += 1

        with open(file_name, "a") as file:
            if os.stat(file_name).st_size == 0:
                file.write(table_header)
            file.writelines(table_rows)

        print(f"Дані у файл {file_name} записано. Поточна кількість записів дорівнює {total_records}.")
