from typing import List


class Issue:
    """An issue for a repository"""

    def __init__(self, **entries):
        if entries != None:
            self.__dict__.update(entries)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
