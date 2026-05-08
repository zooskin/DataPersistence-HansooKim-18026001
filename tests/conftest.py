import pytest
from pathlib import Path


@pytest.fixture
def tmp_json_file(tmp_path: Path) -> Path:
    return tmp_path / "test_data.json"
