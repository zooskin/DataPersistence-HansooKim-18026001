import json
import pytest
from json_store import JsonRepository, RecordNotFoundError, DuplicateKeyError
from tests.conftest import SampleModel


# --- 초기화 ---

def test_creates_file_on_init(tmp_json_file):
    JsonRepository(tmp_json_file, SampleModel)
    assert tmp_json_file.exists()
    assert json.loads(tmp_json_file.read_text(encoding="utf-8")) == []


# --- create ---

def test_create_returns_item(repo):
    item = SampleModel(name="Alice", value=1)
    result = repo.create(item)
    assert result == item


def test_create_persists_to_file(repo, tmp_json_file):
    item = SampleModel(name="Bob", value=2)
    repo.create(item)
    data = json.loads(tmp_json_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["name"] == "Bob"
    assert data[0]["value"] == 2


def test_create_duplicate_raises(repo):
    item = SampleModel(name="Carol", value=3)
    repo.create(item)
    with pytest.raises(DuplicateKeyError):
        repo.create(item)


# --- get ---

def test_get_existing_record(repo):
    item = SampleModel(name="Dave", value=4)
    repo.create(item)
    fetched = repo.get(item.id)
    assert fetched == item


def test_get_missing_raises(repo):
    with pytest.raises(RecordNotFoundError):
        repo.get("non-existent-id")


def test_get_returns_correct_type(repo):
    item = SampleModel(name="Eve", value=5)
    repo.create(item)
    fetched = repo.get(item.id)
    assert isinstance(fetched, SampleModel)


# --- update ---

def test_update_changes_value(repo):
    item = SampleModel(name="Frank", value=6)
    repo.create(item)
    item.name = "Frank Updated"
    item.value = 99
    repo.update(item)
    fetched = repo.get(item.id)
    assert fetched.name == "Frank Updated"
    assert fetched.value == 99


def test_update_missing_raises(repo):
    with pytest.raises(RecordNotFoundError):
        repo.update(SampleModel(id="non-existent-id", name="Ghost", value=0))


# --- delete ---

def test_delete_removes_record(repo):
    item = SampleModel(name="Heidi", value=7)
    repo.create(item)
    repo.delete(item.id)
    with pytest.raises(RecordNotFoundError):
        repo.get(item.id)


def test_delete_missing_raises(repo):
    with pytest.raises(RecordNotFoundError):
        repo.delete("non-existent-id")


# --- list_all ---

def test_list_all_empty(repo):
    assert repo.list_all() == []


def test_list_all_returns_all(repo):
    items = [SampleModel(name=f"Item{i}", value=i) for i in range(3)]
    for item in items:
        repo.create(item)
    result = repo.list_all()
    assert len(result) == 3
    assert all(isinstance(r, SampleModel) for r in result)
    assert {r.name for r in result} == {"Item0", "Item1", "Item2"}
