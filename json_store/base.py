from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from json_store.model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):

    @abstractmethod
    def create(self, item: T) -> T: ...

    @abstractmethod
    def get(self, id: str) -> T: ...

    @abstractmethod
    def update(self, item: T) -> T: ...

    @abstractmethod
    def delete(self, id: str) -> None: ...

    @abstractmethod
    def list_all(self) -> list[T]: ...
