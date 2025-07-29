from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional


def convert_string_to_amount(input_string: str) -> Optional[Decimal]:
    """
    Converts a string to a Decimal instance with exactly two decimal places.
    The function handles strings with varying numbers of decimal places,
    rounding to two decimal places if necessary.

    Args:
        input_string: The input string to convert.

    Returns:
        A Decimal instance with two decimal places if conversion is successful,
        otherwise None.
    """
    if type(input_string) is not str:
        return None

    try:
        # Attempt to convert the string to a Decimal
        d = Decimal(input_string)

        # First, ensure it's not NaN or Infinity, which can be valid Decimal objects
        if d.is_nan() or d.is_infinite():
            return None

        # Define the precision for two decimal places
        # This creates a Decimal '0.01' which is used to set the precision context.
        two_places = Decimal('0.01')

        # Quantize the Decimal to two decimal places, rounding if necessary.
        # ROUND_HALF_UP is a common rounding strategy (rounds .5 up).
        return d.quantize(two_places, rounding=ROUND_HALF_UP)

    except InvalidOperation:
        # This exception is raised if the string cannot be converted to a Decimal
        return None
    except TypeError:
        # This might be raised if the input 'input_string' is not a string
        return None