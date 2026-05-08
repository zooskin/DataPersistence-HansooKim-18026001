from __future__ import annotations
import uuid
import dataclasses
from dataclasses import dataclass, field


@dataclass
class BaseModel:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> BaseModel:
        return cls(**data)
