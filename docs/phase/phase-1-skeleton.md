# Phase 1 — 프로젝트 골격 + 예외 클래스

## 목표

패키지 디렉토리 구조와 커스텀 예외 클래스를 만들어 프로젝트의 뼈대를 구성한다.

---

## 작업 범위

### 파일: `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "json_store"
version = "0.1.0"
description = "JSON file-based CRUD persistence library"
requires-python = ">=3.10"
dependencies = []

[tool.setuptools.packages.find]
where = ["."]
include = ["json_store*"]
```

#### 규칙
- 외부 의존성 없음 (`dependencies = []`)
- `pip install -e .` 명령으로 다른 프로젝트에서 import 가능해야 함

---

### 파일: `json_store/__init__.py`

초기에는 빈 파일로 생성한다. Phase 4에서 공개 API를 export한다.

```python
```

---

### 파일: `json_store/exceptions.py`

```python
class JsonStoreError(Exception): ...

class RecordNotFoundError(JsonStoreError):
    def __init__(self, id: str) -> None: ...

class DuplicateKeyError(JsonStoreError):
    def __init__(self, id: str) -> None: ...
```

#### 메서드 상세

| 클래스 | `__init__` 메시지 형식 |
|--------|----------------------|
| `RecordNotFoundError` | `f"Record not found: id='{id}'"` |
| `DuplicateKeyError` | `f"Record already exists: id='{id}'"` |

#### 규칙
- 세 클래스 모두 `Exception` 계층으로만 구성 (비즈니스 로직 없음)
- `JsonStoreError`는 catch-all 기반 클래스 역할

---

### 파일: `tests/__init__.py`

빈 파일로 생성한다.

### 파일: `tests/conftest.py`

```python
import pytest
from pathlib import Path

@pytest.fixture
def tmp_json_file(tmp_path: Path) -> Path:
    return tmp_path / "test_data.json"
```

#### 규칙
- `tmp_path`는 pytest 내장 fixture 사용 (별도 구현 불필요)

---

## 완료 조건

- [ ] `pip install -e .` 실행 시 오류 없이 완료된다
- [ ] `python -c "from json_store.exceptions import RecordNotFoundError, DuplicateKeyError"` 오류 없이 실행된다
- [ ] `RecordNotFoundError("abc")` 생성 시 메시지에 `"abc"` 가 포함된다
- [ ] `DuplicateKeyError("abc")` 생성 시 메시지에 `"abc"` 가 포함된다

## 커밋

```
feat: 프로젝트 골격 및 커스텀 예외 클래스 추가
```
