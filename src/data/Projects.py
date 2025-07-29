import json
import os
from os.path import isdir
from typing import Any, ItemsView, KeysView, ValuesView

from PySide6.QtCore import QObject

from src.data.BankAccount import BankAccounts, BankAccount
from src.data.CounterParts import CounterPart, CounterParts
from src.data.TransactionCategories import TransactionCategories, TransactionCategory
from src.data.Transactions import Transactions, Transaction
from src.data.settings.AppSettings import AppSettings


class Project(QObject):
    def __init__(
        self,
        identifier: int,
        project_directory: str,
        settings: AppSettings,
        load_from_dir: bool = False,
    ):
        """
        :param identifier: unique project identifier
        :param project_directory: path of project directory
        :param load_from_dir: boolean indicating whether to load project from specified directory
        """
        super().__init__(None)

        self.identifier = identifier
        self.project_dir = project_directory
        self.settings = settings

        self.transactions = Transactions(project=self, settings=self.settings, factory=Transaction)
        self.transaction_categories = TransactionCategories(project=self, settings=self.settings, factory=TransactionCategory)
        self.bank_accounts = BankAccounts(project=self, settings=self.settings, factory=BankAccount)
        self.counterparts = CounterParts(project=self, settings=self.settings, factory=CounterPart)

        self._data_map = {
            "transaction_categories": self.transaction_categories,
            "bank_accounts": self.bank_accounts,
            "counterparts": self.counterparts,
            # Put transactions AFTER categories/bank accounts/counterparts.
            # Loading a project JSON requires these to be instantiated before instantiating transactions.
            "transactions": self.transactions,
        }

        if load_from_dir:
            self._load_project()

    def _load_json(self, json_dict: dict[str, dict]) -> None:
        """Load project data from a specified json dictionary"""
        for key, data in self._data_map.items():
            if key in json_dict:
                data.load_from_json(json_dict[key])

    @property
    def folder_name(self) -> str:
        return self.project_dir.split("/")[-1]

    def _load_project(self):
        """
        Loads project data.
        Load order should be hierarchical, with lowest levels being loaded first.
        For instance, sets can be part of variables and should be loaded after variables.
        """

        # Load projects dict
        filename = f"{self.project_dir}/project.json"
        if not os.path.isfile(filename):
            return
        with open(filename, "r") as read_file:
            project_dict: dict[str, dict[int, Any]] = json.load(read_file)

        self._load_json(json_dict=project_dict)

    def save_project(self) -> None:
        with open(f"{self.project_dir}/project.json", "w") as write_file:
            json.dump(self.json_dict(), write_file, indent=4)

    def json_dict(self) -> dict[str, dict]:
        json_dict = {}  # type: dict[str, dict[int, Any]]

        for key, items in self._data_map.items():
            if items:
                json_dict[key] = items.json_dict()
        return json_dict


class Projects:
    """
    Class that contains all opened projects
    """

    def __init__(self, settings: AppSettings):
        self._settings = settings
        self._projects_dict = {}  # type: dict[int, Project]

    def __getitem__(self, key: int) -> Project:
        return self._projects_dict[key]

    def __bool__(self) -> bool:
        """Returns True when at least 1 project is opened"""
        if self._projects_dict:
            return True
        else:
            return False

    def keys(self) -> KeysView[int]:
        return self._projects_dict.keys()

    def values(self) -> ValuesView[Project]:
        return self._projects_dict.values()

    def items(self) -> ItemsView[int, Project]:
        return self._projects_dict.items()

    def pop(self, key: int) -> Project:
        return self._projects_dict.pop(key)

    def create_new_project(
        self, project_directory: str, load_from_dir: bool = False
    ) -> Project:

        if not isdir(project_directory):
            raise NotADirectoryError(f"{project_directory}")
        identifier = self._get_new_identifier()

        project = Project(
            identifier=identifier,
            project_directory=project_directory,
            load_from_dir=load_from_dir,
            settings=self._settings,
        )

        self._projects_dict[identifier] = project

        return project

    def _get_new_identifier(self) -> int:
        identifier = 0
        while identifier in self._projects_dict.keys():
            identifier += 1
        return identifier

    @property
    def n_projects(self) -> int:
        return len(self._projects_dict.keys())
