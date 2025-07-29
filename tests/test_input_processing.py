from src.utils.input_processing import convert_string_to_amount
import unittest
from decimal import Decimal


class TestConvertStringToAmount(unittest.TestCase):
    """
    Comprehensive unit tests for the convert_string_to_amount function.
    """

    def test_valid_inputs_two_decimal_places(self):
        """
        Test cases for valid strings that already have two decimal places.
        """
        self.assertEqual(convert_string_to_amount("123.45"), Decimal("123.45"))
        self.assertEqual(convert_string_to_amount("0.00"), Decimal("0.00"))
        self.assertEqual(convert_string_to_amount("-99.99"), Decimal("-99.99"))
        self.assertEqual(convert_string_to_amount("1000000.00"), Decimal("1000000.00"))

    def test_valid_inputs_more_than_two_decimal_places_rounding(self):
        """
        Test cases for strings with more than two decimal places,
        verifying correct ROUND_HALF_UP behavior.
        """
        # Rounds up
        self.assertEqual(convert_string_to_amount("123.456"), Decimal("123.46"))
        self.assertEqual(convert_string_to_amount("123.455"), Decimal("123.46"))
        self.assertEqual(convert_string_to_amount("0.005"), Decimal("0.01"))
        self.assertEqual(convert_string_to_amount("-0.005"), Decimal("-0.01")) # Rounds away from zero

        # Rounds down
        self.assertEqual(convert_string_to_amount("123.454"), Decimal("123.45"))
        self.assertEqual(convert_string_to_amount("0.004"), Decimal("0.00"))
        self.assertEqual(convert_string_to_amount("-0.004"), Decimal("0.00")) # Rounds towards zero

        # Longer decimals
        self.assertEqual(convert_string_to_amount("1.23456789"), Decimal("1.23"))
        self.assertEqual(convert_string_to_amount("1.99999"), Decimal("2.00"))

    def test_valid_inputs_fewer_than_two_decimal_places(self):
        """
        Test cases for strings with fewer than two decimal places,
        expecting padding with zeros.
        """
        self.assertEqual(convert_string_to_amount("123"), Decimal("123.00"))
        self.assertEqual(convert_string_to_amount("123."), Decimal("123.00"))
        self.assertEqual(convert_string_to_amount("123.4"), Decimal("123.40"))
        self.assertEqual(convert_string_to_amount("0"), Decimal("0.00"))
        self.assertEqual(convert_string_to_amount("0."), Decimal("0.00"))
        self.assertEqual(convert_string_to_amount("-5"), Decimal("-5.00"))
        self.assertEqual(convert_string_to_amount("-5.1"), Decimal("-5.10"))

    def test_valid_inputs_leading_trailing_zeros(self):
        """
        Test cases for strings with leading/trailing zeros or specific formatting.
        """
        self.assertEqual(convert_string_to_amount("007.89"), Decimal("7.89"))
        self.assertEqual(convert_string_to_amount(".12"), Decimal("0.12"))
        self.assertEqual(convert_string_to_amount("-.12"), Decimal("-0.12"))
        self.assertEqual(convert_string_to_amount("0.1"), Decimal("0.10"))

    def test_invalid_inputs_non_numeric_strings(self):
        """
        Test cases for non-numeric strings, expecting None.
        """
        self.assertIsNone(convert_string_to_amount("abc"))
        self.assertIsNone(convert_string_to_amount("123a"))
        self.assertIsNone(convert_string_to_amount("a123"))
        self.assertIsNone(convert_string_to_amount(""))  # Empty string
        self.assertIsNone(convert_string_to_amount(" "))  # Whitespace
        self.assertIsNone(convert_string_to_amount("1.2.3")) # Multiple decimal points
        self.assertIsNone(convert_string_to_amount("NaN")) # Not a Number
        self.assertIsNone(convert_string_to_amount("Infinity")) # Infinity
        self.assertIsNone(convert_string_to_amount("-Infinity")) # Negative Infinity

    def test_invalid_inputs_non_string_types(self):
        """
        Test cases for inputs that are not strings, expecting None.
        """
        self.assertIsNone(convert_string_to_amount(None))
        self.assertIsNone(convert_string_to_amount(123))
        self.assertIsNone(convert_string_to_amount(123.45))
        self.assertIsNone(convert_string_to_amount([]))
        self.assertIsNone(convert_string_to_amount({}))
        self.assertIsNone(convert_string_to_amount(True))

    def test_edge_cases_large_and_small_numbers(self):
        """
        Test edge cases with very large or very small numbers.
        """
        self.assertEqual(convert_string_to_amount("123456789012345.6789"), Decimal("123456789012345.68"))
        self.assertEqual(convert_string_to_amount("0.000000000000001"), Decimal("0.00"))
        self.assertEqual(convert_string_to_amount("0.0050000000000000000000000000001"), Decimal("0.01"))