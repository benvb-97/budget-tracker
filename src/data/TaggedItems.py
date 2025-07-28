from typing import TYPE_CHECKING, Any, Generic, ItemsView, KeysView, TypeVar, ValuesView


if TYPE_CHECKING:
    from src.data.Projects import Project
    from src.data.settings.AppSettings import AppSettings

from collections import OrderedDict

from PySide6.QtCore import QObject


class TaggedItem(QObject):
    """Used for project data that requires a unique identifier."""

    def __init__(self, project: "Project", identifier: int) -> None:
        """
        :param project: project to which the tagged item belongs
        :param identifier: unique identifier (tag) of the item
        """
        super().__init__(None)
        self.project = project
        self.identifier = identifier

    def json_dict(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def init_from_json(
        cls,
        identifier: int,
        json_dict: dict[str, Any],
        project: "Project",
    ) -> "TaggedItemType":
        raise NotImplementedError

    def copy(self, new_identifier: int) -> "TaggedItemType":
        return self.__class__.init_from_json(identifier=new_identifier,
                                             json_dict=self.json_dict(),
                                             project=self.project,
                                             )


TaggedItemType = TypeVar("TaggedItemType", bound=TaggedItem)


class TaggedItems(Generic[TaggedItemType]):
    """Used for project data collections that require unique identifiers for each item"""
    def __init__(self,
                 project: "Project",
                 settings: "AppSettings",
                 factory: type[TaggedItemType],
                 ):
        """

        :param project:
        :param settings:
        :param factory: Used to create new tagged item instances of the right Class.
        """
        self._project = project
        self._settings = settings

        self._factory = factory

        self._data: OrderedDict[int, TaggedItemType] = OrderedDict()

    def __getitem__(self, key: int) -> TaggedItemType:
        return self._data[key]

    def __setitem__(self, key: int, value: TaggedItemType) -> None:
        self._data[key] = value

    def __delitem__(self, key: int) -> None:
        del self._data[key]

    def __contains__(self, key: int) -> bool:
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data})"

    def __bool__(self) -> bool:
        return bool(self._data)

    def keys(self) -> KeysView[int]:
        return self._data.keys()

    def items(self) -> ItemsView[int, TaggedItemType]:
        return self._data.items()

    def values(self) -> ValuesView[TaggedItemType]:
        return self._data.values()

    def pop(self, key: int) -> TaggedItemType:
        item = self._data.pop(key)
        return item

    def clear(self) -> None:
        self._data.clear()

    def get_new_identifier(self) -> int:
        identifier = 0
        while identifier in self._data.keys():
            identifier += 1
        return identifier

    def json_dict(self) -> dict[int, dict[str, Any]]:
        json_dict = {}  # type: dict[int, dict[str, Any]]

        for identifier, item in self._data.items():
            json_dict[identifier] = item.json_dict()

        return json_dict

    def create_new_item(
        self,
        identifier: int = None,
        json_dict: dict[str, Any] = None,
    ) -> "TaggedItemType":
        if identifier:
            assert identifier not in self._data.keys()
        else:
            identifier = self.get_new_identifier()

        if json_dict:
            item = self._factory.init_from_json(
                identifier=identifier,
                json_dict=json_dict,
                project=self._project,
            )
        else:
            item = self._factory(
                identifier=identifier, project=self._project
            )

        self._data[identifier] = item
        return item

    def copy_item(self, item: "TaggedItemType") -> "TaggedItemType":
        identifier = self.get_new_identifier()
        new_item = item.copy(new_identifier=identifier)

        self._data[identifier] = new_item
        return new_item

    def load_from_json(self, json_dict: dict[int, dict[str, Any]]) -> None:
        for identifier, item_dict in json_dict.items():
            self.create_new_item(
                identifier=int(identifier),
                json_dict=json_dict[identifier],
            )


TaggedItemsType = TypeVar("TaggedItemsType", bound=TaggedItems)