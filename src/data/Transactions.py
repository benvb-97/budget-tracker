import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, TypeAlias

from src.data.BankAccount import BankAccount
from src.data.CounterPart import CounterPart
from src.data.Currencies import Currencies
if TYPE_CHECKING:
    from src.data.Projects import Project
from src.data.TaggedItems import TaggedItems, TaggedItem
from src.data.TransactionCategory import TransactionCategory


class Transaction(TaggedItem):

    def __init__(self,
                 project: "Project",
                 identifier: int,

                 date: datetime.date,
                 counterpart: CounterPart,
                 amount: Decimal,
                 account: BankAccount,
                 currency: Currencies = Currencies.EUR,
                 category: TransactionCategory = None,
                 note: str = "",
                 ):
        """
        :param date: date of the transaction
        :param counterpart: counterpart of the transaction
        :param amount: amount of the transaction (0.00 format)
        :param account: associated account of the user to which this transaction belongs
        :param currency: currency of the transaction
        :param category: optional transaction category to which this transaction belongs
        :param note: optional note
        """
        super().__init__(project=project, identifier=identifier)

        self.date = date
        self.counterpart = counterpart
        self.amount = amount
        self.account = account
        self.currency = currency
        self.category = category
        self.note = note


class IncomeTransactions(TaggedItems[Transaction]):
    pass


class ExpenseTransactions(TaggedItems[Transaction]):
    pass


Transactions: TypeAlias = IncomeTransactions | ExpenseTransactions