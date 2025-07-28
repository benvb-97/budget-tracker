from schwifty.iban import IBAN
from typing import Any


class BankAccount:

    def __init__(self,
                 iban: IBAN,
                 name: str = "",
                 ):
        self.iban = iban
        self.name = name

    def json_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "iban": self.iban.account_holder_id,
        }