# Phase 2 — BaseModel

## 목표

JSON 직렬화/역직렬화를 지원하는 `BaseModel` dataclass를 구현한다.

---

## 작업 범위

### 파일: `json_store/model.py`

```python
from __future__ import annotations
import uuid
from dataclasses import dataclass, field

@dataclass
class BaseModel:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        ...

    @classmethod
    def from_dict(cls, data: dict) -> BaseModel:
        ...
```

#### 메서드 상세

| 메서드 | 동작 |
|--------|------|
| `to_dict()` | `dataclasses.asdict(self)` 반환. 서브클래스의 모든 필드 포함 |
| `from_dict(data)` | `cls(**data)` 로 인스턴스 복원. 서브클래스에서 호출 시 해당 타입으로 반환 |

#### 규칙
- `id` 필드는 `default_factory`를 사용해 인스턴스 생성 시 자동으로 `uuid4()` 값이 할당된다
- 외부에서 `id="custom-id"` 를 명시하면 그 값을 그대로 사용한다
- `to_dict` / `from_dict` 는 `BaseModel` 서브클래스에서도 올바르게 동작해야 한다
- 외부 라이브러리 import 금지

#### 사용 예시

```python
@dataclass
class User(BaseModel):
    name: str = ""
    age: int = 0

u = User(name="Alice", age=30)
# u.id → 자동 생성된 UUID 문자열

d = u.to_dict()
# {"id": "...", "name": "Alice", "age": 30}

u2 = User.from_dict(d)
# u2 == u
```

---

## 완료 조건

- [ ] `python -c "from json_store.model import BaseModel"` 오류 없이 실행된다
- [ ] `BaseModel()` 생성 시 `id` 필드에 UUID 형식 문자열이 자동 할당된다
- [ ] `BaseModel(id="fixed")` 생성 시 `id == "fixed"` 다
- [ ] `to_dict()` 반환값이 `dict` 타입이고 `"id"` 키를 포함한다
- [ ] `from_dict(instance.to_dict())` 의 결과가 원본 인스턴스와 동등(`==`)하다
- [ ] 서브클래스에서 `from_dict` 호출 시 서브클래스 인스턴스가 반환된다

## 커밋

```
feat: BaseModel dataclass 구현 (UUID 자동 생성, to_dict/from_dict)
```
