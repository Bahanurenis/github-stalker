from typing import List
from utils.repository import Repository


class User:
    """
    User Data Class
    """

    def __init__(self, user: dict):
        self._user = user
        self._repositories: List[Repository] = []
        self._parse_repos(user)

    def _parse_repos(self, user_dict: dict):
        if "repositories" in user_dict:
            for r in user_dict["repositories"]["nodes"]:
                repo = Repository(**r)
                self._repositories.append(repo)

    @property
    def name(self) -> str:
        return self._user["name"]

    @property
    def email(self) -> str:
        return self._user["email"]

    @property
    def company(self) -> str:
        return self._user["company"]

    @property
    def location(self) -> str:
        return self._user["location"]

    @property
    def bio(self) -> str:
        return self._user["bio"]

    @property
    def followers(self) -> int:
        return self._user["followers"]["totalCount"]

    @property
    def following(self) -> int:
        return self._user["following"]["totalCount"]

    @property
    def first_ten_repos(self) -> list:
        return self._user["repositories"]["nodes"]

    @property
    def pinnedItems(self) -> list:
        return self._user["pinnedItems"]["nodes"]

    @property
    def repositories(self):
        return self._repositories
