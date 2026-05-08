# Phase 4 — JsonRepository 구현체 + 공개 API

## 목표

JSON 배열 파일 기반의 CRUD 구현체 `JsonRepository`를 완성하고 라이브러리 공개 API를 export한다.

---

## 작업 범위

### 파일: `json_store/json_repo.py`

```python
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

    def __init__(self, file_path: str | Path, model_class: type[T]) -> None: ...
    def create(self, item: T) -> T: ...
    def get(self, id: str) -> T: ...
    def update(self, item: T) -> T: ...
    def delete(self, id: str) -> None: ...
    def list_all(self) -> list[T]: ...

    def _load(self) -> list[dict]: ...
    def _save(self, records: list[dict]) -> None: ...
```

#### 생성자

| 인자 | 타입 | 설명 |
|------|------|------|
| `file_path` | `str \| Path` | JSON 파일 경로. 없으면 자동 생성 |
| `model_class` | `type[T]` | 복원에 사용할 모델 클래스 (예: `User`) |

생성자 동작:
1. `self._path = Path(file_path)`
2. `self._model_class = model_class`
3. `self._lock = threading.Lock()`
4. 파일이 없으면 `_save([])` 로 빈 배열 파일 생성

#### JSON 저장 형식

```json
[
  {"id": "uuid-1", "name": "Alice", "age": 30},
  {"id": "uuid-2", "name": "Bob",   "age": 25}
]
```

#### 내부 메서드

| 메서드 | 동작 |
|--------|------|
| `_load()` | `self._path` 를 읽어 `list[dict]` 반환 |
| `_save(records)` | `list[dict]` 를 `json.dump(indent=2)` 로 파일에 씀 |

#### CRUD 동작 상세

| 메서드 | 동작 |
|--------|------|
| `create(item)` | `_load` → id 중복 검사 → append → `_save` → `item` 반환. 중복 시 `DuplicateKeyError` |
| `get(id)` | `_load` → id 매칭 → `model_class.from_dict` 반환. 없으면 `RecordNotFoundError` |
| `update(item)` | `_load` → id 매칭 → 해당 dict 교체 → `_save` → `item` 반환. 없으면 `RecordNotFoundError` |
| `delete(id)` | `_load` → id 매칭 확인 → 해당 항목 제거 → `_save`. 없으면 `RecordNotFoundError` |
| `list_all()` | `_load` → 전체를 `model_class.from_dict` 리스트로 반환 |

#### 규칙
- 모든 파일 읽기/쓰기는 `with self._lock:` 블록 안에서 수행
- `_load` / `_save` 는 lock 밖에서 직접 호출하지 않는다 (항상 public 메서드가 lock을 잡은 뒤 호출)
- `json.dump` 시 `ensure_ascii=False`, `indent=2` 적용

---

### 파일: `json_store/__init__.py`

```python
from json_store.model import BaseModel
from json_store.base import BaseRepository
from json_store.json_repo import JsonRepository
from json_store.exceptions import JsonStoreError, RecordNotFoundError, DuplicateKeyError

__all__ = [
    "BaseModel",
    "BaseRepository",
    "JsonRepository",
    "JsonStoreError",
    "RecordNotFoundError",
    "DuplicateKeyError",
]
```

---

## 완료 조건

- [ ] `from json_store import BaseModel, JsonRepository, RecordNotFoundError, DuplicateKeyError` 오류 없이 실행된다
- [ ] `JsonRepository(path, Model)` 생성 시 파일이 없으면 `[]` 내용의 JSON 파일이 생성된다
- [ ] `create(item)` 호출 후 파일에 해당 레코드가 JSON 배열 형태로 저장된다
- [ ] 동일 id로 `create` 두 번 호출 시 `DuplicateKeyError` 가 발생한다
- [ ] `get(id)` 로 존재하는 레코드를 조회하면 원본과 동등한 인스턴스가 반환된다
- [ ] 존재하지 않는 id로 `get` / `update` / `delete` 호출 시 `RecordNotFoundError` 가 발생한다
- [ ] `update(item)` 후 파일의 해당 레코드가 변경된 값으로 저장된다
- [ ] `delete(id)` 후 파일에서 해당 레코드가 제거된다
- [ ] `list_all()` 이 저장된 모든 레코드를 올바른 타입으로 반환한다

## 커밋

```
feat: JsonRepository 구현체 및 공개 API export 추가
```
