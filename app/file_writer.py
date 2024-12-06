import os
import datetime
import math


class FileWriter:
    def __init__(self, last_used_file_path="last_used_file.config"):
        self.file_name = None
        self.last_used_file_path = last_used_file_path
        self._load_last_used_file()

    def _load_last_used_file(self):
        if os.path.exists(self.last_used_file_path):
            with open(self.last_used_file_path, "r", encoding="utf-8") as file:
                self.file_name = file.read().strip()

    def _save_last_used_file(self):
        with open(self.last_used_file_path, "w", encoding="utf-8") as file:
            file.write(self.file_name)

    def save_results(self, results):
        if not results:
            print("Результати відсутні, нічого записувати.")
            return

        save_choice = input("Записати результати у файл? (Так/Ні): ").strip().lower()
        if save_choice != "так":
            print("Дані у файл не записано.")
            return

        if self.file_name:
            reuse_choice = input(
                f"Записати результати у файл {self.file_name}? (Так/Ні): "
            ).strip().lower()
            if reuse_choice == "так":
                self._write_to_file(results, self.file_name)
                return

        while True:
            file_name = input("Введіть ім’я файлу: ").strip()
            if file_name == "*":
                print("Дані у файл не записано.")
                return

            if not (1 <= len(file_name) <= 5):
                print("Некоректне ім’я файлу. Назва файлу повинна містити від 1 до 5 символів. Спробуйте ще раз.")
                continue
            if not file_name.isalnum():
                print("Некоректне ім’я файлу. Назва файлу повинна містити лише літери і цифри.")
                continue

            self.file_name = file_name + ".txt"
            break

        self._write_to_file(results, self.file_name)

    def _write_to_file(self, results, file_name):
        now = datetime.datetime.now().strftime("%d.%m.%Y")
        total_records = 0
        table_header = (
            "+-----------------+--------------------+--------------------+---------------------+-------------------------+\n"
            "|Дата (ДД.ММ.РРРР)|     Аргумент x     |     Точність e     |  Результат функції  | Кількість членів ряду N |\n"
            "+-----------------+--------------------+--------------------+---------------------+-------------------------+\n"
        )
        table_rows = []

        for x, epsilon, result, n in results:
            if x is None or epsilon is None or result is None or n is None:
                continue

            epsilon_str = f"{epsilon:.10f}".rstrip('0').rstrip('.')
            result_str = f"{result:.{abs(int(math.log10(epsilon)))}f}" if result is not None else "-"
            n_str = str(n) if n is not None else "-"

            row = (
                f"|{now:^17}|{x:^20.12f}|{epsilon_str:^20}|{result_str:^21}|{n_str:^25}|\n"
            )
            table_rows.append(row)
            table_rows.append(
                "+-----------------+--------------------+--------------------+---------------------+-------------------------+\n")
            total_records += 1

        if not table_rows:
            print("Усі записи некоректні. Файл не було оновлено.")
            return

        with open(file_name, "a", encoding="utf-8") as file:
            if os.stat(file_name).st_size == 0:
                file.write(table_header)
            file.writelines(table_rows)

        self._save_last_used_file()
        print(f"Дані у файл {file_name} записано. Поточна кількість записів дорівнює {total_records}.")
