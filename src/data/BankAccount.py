from schwifty.iban import IBAN
from typing import Any

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.data.Projects import Project
from src.data.TaggedItems import TaggedItem, TaggedItems


class BankAccount(TaggedItem):

    def __init__(self,
                 project: "Project",
                 identifier: int,
                 iban: IBAN = None,
                 name: str = None,
                 note: str = "",
                 ):
        super().__init__(project=project, identifier=identifier)

        self.iban = iban
        self.name = name if name is not None else f"New Account({identifier})"
        self.note = note

    def json_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "iban": str(self.iban) if self.iban is not None else None,
            "note": self.note,
        }

    @classmethod
    def init_from_json(
        cls,
        identifier: int,
        json_dict: dict[str, Any],
        project: "Project",
    ) -> "BankAccount":
        return cls(project=project,
                   identifier=identifier,
                   iban=IBAN(json_dict["iban"]) if json_dict["iban"] is not None else None,
                   name=json_dict["name"],
                   note=json_dict["note"],
                   )


class BankAccounts(TaggedItems[BankAccount]):
    pass