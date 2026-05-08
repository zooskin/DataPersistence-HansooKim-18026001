import pytest
from pathlib import Path
from dataclasses import dataclass
from json_store import BaseModel, JsonRepository


@dataclass
class SampleModel(BaseModel):
    name: str = ""
    value: int = 0


@pytest.fixture
def tmp_json_file(tmp_path: Path) -> Path:
    return tmp_path / "test_data.json"


@pytest.fixture
def repo(tmp_json_file: Path) -> JsonRepository:
    return JsonRepository(tmp_json_file, SampleModel)
