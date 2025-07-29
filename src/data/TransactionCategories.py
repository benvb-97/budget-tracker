from src.data.TaggedItems import TaggedItems, TaggedItem
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.data.Projects import Project


class TransactionCategory(TaggedItem):

    def __init__(self,
                 project: "Project",
                 identifier: int,
                 name: str = None,
                 note: str = ""
                 ) -> None:
        super().__init__(project=project, identifier=identifier)

        self.name = name if name is not None else f"New Category({identifier})"
        self.note = note

    def json_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "note": self.note,
        }

    @classmethod
    def init_from_json(
        cls,
        identifier: int,
        json_dict: dict[str, Any],
        project: "Project",
    ) -> "TransactionCategory":
        return cls(project=project,
                            identifier=identifier,
                            name=json_dict["name"],
                            note=json_dict["note"],
                            )

class TransactionCategories(TaggedItems[TransactionCategory]):
    pass