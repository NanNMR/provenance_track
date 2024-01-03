from typing import runtime_checkable, Protocol, Optional


@runtime_checkable
class PlpyAPI(Protocol):

    @staticmethod
    def execute(query:str,limit:Optional[int]=None):
        pass