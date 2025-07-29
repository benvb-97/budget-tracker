from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.data.Projects import Project
from src.data.TaggedItems import TaggedItem, TaggedItems


class TransactionCSVColumns(StrEnum):
    DATE = "DATE"
    AMOUNT = "AMOUNT"
    COUNTERPART = "COUNTERPART"
    ACCOUNT = "ACCOUNT"
    NOTE = "NOTE"


class TransactionsCSVReader(TaggedItem):

    def __init__(self, project: "Project",
                 identifier: int,
                 name: str = None,
                 column_map: dict[TransactionCSVColumns, int] = None):
        """
        Class that stores information on how to read a .csv file that contains transactional data.
        :param column_map: dict that maps a data column to a column in the .csv file.
        """

        super().__init__(project=project, identifier=identifier)

        self.name = name if name is not None else f"New Reader({identifier})"
        if column_map is None:
            column_map = {col: None for col in TransactionCSVColumns}
        self.column_map = column_map

    def json_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "column_map": self.column_map,
        }

    @classmethod
    def init_from_json(
        cls,
        identifier: int,
        json_dict: dict[str, Any],
        project: "Project",
    ) -> "TransactionsCSVReader":

        return cls(project=project,
                   identifier=identifier,
                   name=json_dict["name"],
                   column_map=json_dict["column_map"],
                   )


class TransactionCSVReaders(TaggedItems[TransactionsCSVReader]):
    pass
