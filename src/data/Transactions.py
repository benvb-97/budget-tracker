import datetime
from decimal import Decimal
from enum import StrEnum, IntEnum
from typing import TYPE_CHECKING, TypeAlias, Any

from src.data.BankAccount import BankAccount
from src.data.CounterParts import CounterPart
from src.data.Currencies import Currencies
if TYPE_CHECKING:
    from src.data.Projects import Project
from src.data.TaggedItems import TaggedItems, TaggedItem
from src.data.TransactionCategories import TransactionCategory


class Transaction(TaggedItem):

    def __init__(self,
                 project: "Project",
                 identifier: int,
                 date: datetime.date = None,
                 counterpart: CounterPart = None,
                 amount: Decimal = None,
                 account: BankAccount = None,
                 category: TransactionCategory = None,
                 note: str = "",
                 ):
        """
        :param date: date of the transaction
        :param counterpart: counterpart of the transaction
        :param amount: amount of the transaction (0.00 format)
        :param account: associated account of the user to which this transaction belongs
        :param category: optional transaction category to which this transaction belongs
        :param note: optional note
        """
        super().__init__(project=project, identifier=identifier)

        # Initialize default values if None are passed.
        if date is None:
            date = datetime.date.today()
        if amount is None:
            amount = Decimal("0.00")
        if account is None and len(project.bank_accounts) > 0:
            account = list(project.bank_accounts.values())[0]

        #
        self.date = date
        self.counterpart = counterpart
        self.amount = amount
        self.account = account
        self.category = category
        self.note = note

    def json_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "date": self.date.isoformat(),
            "counterpart": self.counterpart.identifier if self.counterpart is not None else None,
            "amount": str(self.amount),
            "account": self.account.identifier if self.account is not None else None,
            "category": self.category.identifier if self.category is not None else None,
            "note": self.note,
        }


    @classmethod
    def init_from_json(
        cls,
        identifier: int,
        json_dict: dict[str, Any],
        project: "Project",
    ) -> "Transaction":

        return cls(
            project=project,
            identifier=identifier,
            date=datetime.date.fromisoformat(json_dict["date"]),
            counterpart=project.counterparts[json_dict["counterpart"]] if json_dict["counterpart"] is not None else None,
            amount=Decimal(json_dict["amount"]),
            account=project.bank_accounts[json_dict["account"]] if json_dict["account"] is not None else None,
            category=project.transaction_categories[json_dict["category"]] if json_dict["category"] is not None else None,
            note=json_dict["note"],
        )


class Transactions(TaggedItems[Transaction]):
    pass


