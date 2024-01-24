from collections.abc import Mapping
from typing import runtime_checkable, Protocol, Optional


@runtime_checkable
class PyResult(Protocol):
    def nrows(self)->int:
        pass

@runtime_checkable
class PlpyAPI(Protocol):

    @staticmethod
    def execute(query:str,limit:Optional[int]=None)->PyResult:
        pass

    @staticmethod
    def info(s:str)->None:
        pass
