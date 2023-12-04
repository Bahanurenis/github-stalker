from typing import List
from utils.issue import Issue


class Repository:
    """
    A specific Repository of owner
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)
        self._issues: List[Issue] = []
        self._parse_issuess(entries)

    def _parse_issuess(self, issue_dict: dict):
        if "issues" in issue_dict:
            for i in issue_dict["issues"]["nodes"]:
                issue = Issue(**i)
                self._issues.append(issue)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    @property
    def issues(self):
        return self._issues
