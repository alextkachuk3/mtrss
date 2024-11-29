import unittest
from fractions import Fraction
from app.Bernoulli import Bernoulli


class TestBernoulli(unittest.TestCase):
    def test_min(self):
        n = 0
        result = Bernoulli.evaluate(n)

        expected = Fraction(1, 1)
        self.assertEqual(str(expected), str(result))

    def test_big(self):
        n = 100
        result = Bernoulli.evaluate(n)

        expected = Fraction(
            -94598037819122125295227433069493721872702841533066936133385696204311395415197247711,
            33330
        )
        self.assertEqual(str(expected), str(result))

    def test_out_of_range(self):
        n = -5
        with self.assertRaises(ValueError):
            Bernoulli.evaluate(n)

    def test_middle(self):
        n = 50
        result = Bernoulli.evaluate(n)

        expected = Fraction(495057205241079648212477525, 66)
        self.assertEqual(str(expected), str(result))

    def test_odd(self):
        n = 49
        result = Bernoulli.evaluate(n)

        expected = Fraction(0, 1)
        self.assertEqual(str(expected), str(result))

    def test_cache(self):
        n = 100
        result = Bernoulli.evaluate(n)
        expected_100 = Fraction(
            -94598037819122125295227433069493721872702841533066936133385696204311395415197247711,
            33330
        )
        self.assertEqual(str(expected_100), str(result))

        n = 50
        result = Bernoulli.evaluate(n)
        expected_50 = Fraction(495057205241079648212477525, 66)
        self.assertEqual(str(expected_50), str(result))


if __name__ == "__main__":
    unittest.main()
