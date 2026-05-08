# Phase 3 — BaseRepository ABC 인터페이스

## 목표

CRUD 연산의 추상 인터페이스 `BaseRepository`를 정의한다.

---

## 작업 범위

### 파일: `json_store/base.py`

```python
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
```

#### 추상 메서드 계약

| 메서드 | 인자 | 반환 | 예외 |
|--------|------|------|------|
| `create(item)` | `T` | 저장된 `T` | `DuplicateKeyError` — 동일 id 존재 시 |
| `get(id)` | `str` | `T` | `RecordNotFoundError` — id 없을 시 |
| `update(item)` | `T` | 업데이트된 `T` | `RecordNotFoundError` — id 없을 시 |
| `delete(id)` | `str` | `None` | `RecordNotFoundError` — id 없을 시 |
| `list_all()` | — | `list[T]` | 없음 (빈 리스트 반환) |

#### 규칙
- `BaseRepository`는 순수 인터페이스다. 파일 I/O, 상태(state) 보유 금지
- 예외 타입은 `json_store.exceptions` 에 정의된 것만 사용 (구현체가 따라야 할 계약)
- `T`는 항상 `BaseModel`의 서브타입으로 바인딩된다

---

## 완료 조건

- [ ] `python -c "from json_store.base import BaseRepository"` 오류 없이 실행된다
- [ ] `BaseRepository()` 직접 인스턴스화 시 `TypeError` 가 발생한다
- [ ] 추상 메서드를 일부만 구현한 서브클래스 인스턴스화 시 `TypeError` 가 발생한다
- [ ] 모든 추상 메서드를 구현한 서브클래스는 정상 인스턴스화된다

## 커밋

```
feat: BaseRepository ABC 인터페이스 정의
```
