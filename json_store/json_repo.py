from __future__ import annotations
import json
import threading
from pathlib import Path
from typing import TypeVar
from json_store.base import BaseRepository
from json_store.model import BaseModel
from json_store.exceptions import RecordNotFoundError, DuplicateKeyError

T = TypeVar("T", bound=BaseModel)


class JsonRepository(BaseRepository[T]):

    def __init__(self, file_path: str | Path, model_class: type[T]) -> None:
        self._path = Path(file_path)
        self._model_class = model_class
        self._lock = threading.Lock()
        if not self._path.exists():
            self._save([])

    def create(self, item: T) -> T:
        with self._lock:
            records = self._load()
            if any(r["id"] == item.id for r in records):
                raise DuplicateKeyError(item.id)
            records.append(item.to_dict())
            self._save(records)
        return item

    def get(self, id: str) -> T:
        with self._lock:
            records = self._load()
        for r in records:
            if r["id"] == id:
                return self._model_class.from_dict(r)
        raise RecordNotFoundError(id)

    def update(self, item: T) -> T:
        with self._lock:
            records = self._load()
            for i, r in enumerate(records):
                if r["id"] == item.id:
                    records[i] = item.to_dict()
                    self._save(records)
                    return item
        raise RecordNotFoundError(item.id)

    def delete(self, id: str) -> None:
        with self._lock:
            records = self._load()
            filtered = [r for r in records if r["id"] != id]
            if len(filtered) == len(records):
                raise RecordNotFoundError(id)
            self._save(filtered)

    def list_all(self) -> list[T]:
        with self._lock:
            records = self._load()
        return [self._model_class.from_dict(r) for r in records]

    def _load(self) -> list[dict]:
        with self._path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, records: list[dict]) -> None:
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
