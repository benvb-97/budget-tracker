from enum import StrEnum


class Currencies(StrEnum):
    """
    Represents ISO 4217 currency codes.
    """
    USD = "USD"  # United States Dollar
    EUR = "EUR"  # Euro
    GBP = "GBP"  # British Pound Sterling
    JPY = "JPY"  # Japanese Yen (often no decimal places, but Decimal handles it)
    CAD = "CAD"  # Canadian Dollar
    AUD = "AUD"  # Australian Dollar
    CHF = "CHF"  # Swiss Franc

    def __str__(self):
        return self.value

    @property
    def symbol(self):
        if self == Currencies.USD:
            return "$"
        elif self == Currencies.EUR:
            return "€"
        elif self == Currencies.GBP:
            return "£"
        elif self == Currencies.JPY:
            return "¥"
        elif self == Currencies.CAD:
            return "C$"
        elif self == Currencies.AUD:
            return "A$"
        elif self == Currencies.CHF:
            return "CHF " # Space for clarity
        return self.value # Fallback to code if symbol not defined