import math
import unittest
from decimal import Decimal
from unittest.mock import patch

from app.maclaurin import Maclaurin, CotangentCalculator, TimeoutException


class TestMaclaurin(unittest.TestCase):
    def test_cotangent_simple(self):
        """Тестуємо правильність обчислення для простих значень"""
        result, n = Maclaurin.cotangent(1.0, 0.001)
        self.assertAlmostEqual(result, 0.6420926159, places=4)  # очікуване значення для cot(1)
        self.assertGreater(n, 0)

    def test_cotangent_precision(self):
        """Тестуємо обчислення з високою точністю"""
        result, _ = Maclaurin.cotangent(1.0, 0.000001)
        self.assertAlmostEqual(result, 0.6420926159, places=6)

    def test_cotangent_invalid_input(self):
        """Тестуємо некоректні значення x"""
        with self.assertRaises(ValueError):
            Maclaurin. .cotangent(math.pi + 0.01, 0.001)

    def test_cotangent_timeout(self):
        """Тестуємо випадок, коли обчислення перевищують таймаут"""
        with self.assertRaises(TimeoutException):
            Maclaurin.cotangent(1.0, 1e-10, timeout=0.001)


class TestCotangentCalculator(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "0.01", "кінець"])
    def test_input_data(self, mock_input):
        """Тестуємо введення даних і обчислення"""
        calculator = CotangentCalculator()
        calculator.input_data()
        self.assertEqual(len(calculator.results), 1)
        x, epsilon, result, n = calculator.results[0]
        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(epsilon, 0.01)
        self.assertIsNotNone(result)
        self.assertGreater(n, 0)

    @patch("builtins.input", side_effect=["1", "0.01", "кінець"])
    @patch("builtins.print")
    def test_save_results_to_file(self, mock_print, mock_input):
        """Тестуємо збереження результатів у файл"""
        calculator = CotangentCalculator()
        calculator.input_data()
        calculator.file_name = "test"
        calculator.save_results()

        # Перевіряємо, чи створений файл і чи містить потрібні записи
        with open("test.txt", "r") as file:
            lines = file.readlines()
            self.assertIn("Дата (ДД.ММ.РРРР)", lines[0])
            self.assertIn("|", lines[-1])

        # Видаляємо файл після тестування
        import os
        os.remove("test.txt")

