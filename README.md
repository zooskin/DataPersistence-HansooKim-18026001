# json_store

JSON 파일 기반의 데이터 영속성 CRUD 라이브러리 (Python PoC)

## 요구사항

- Python 3.10+
- 표준 라이브러리만 사용 (외부 의존성 없음)

## 설치

다른 프로젝트에서 사용할 때 editable 모드로 설치한다.

```bash
pip install -e /path/to/json_store
```

## 빠른 시작

```python
from dataclasses import dataclass
from json_store import BaseModel, JsonRepository

@dataclass
class User(BaseModel):
    name: str = ""
    age: int = 0

repo = JsonRepository("users.json", User)

# Create
user = repo.create(User(name="Alice", age=30))

# Read
fetched = repo.get(user.id)

# Update
user.age = 31
repo.update(user)

# Delete
repo.delete(user.id)

# List all
all_users = repo.list_all()
```

## JSON 저장 형식

```json
[
  {"id": "uuid-string", "name": "Alice", "age": 30},
  {"id": "uuid-string", "name": "Bob",   "age": 25}
]
```

## 공개 API

```python
from json_store import (
    BaseModel,           # 모든 모델의 기반 dataclass (UUID 자동 생성)
    BaseRepository,      # CRUD 추상 인터페이스 (ABC)
    JsonRepository,      # JSON 파일 기반 구현체
    JsonStoreError,      # 모든 라이브러리 예외의 기반 클래스
    RecordNotFoundError, # get/update/delete 시 id 없을 때
    DuplicateKeyError,   # create 시 동일 id 존재할 때
)
```

### BaseModel

| 항목 | 설명 |
|------|------|
| `id: str` | 인스턴스 생성 시 `uuid4()` 자동 할당. 외부 주입도 허용 |
| `to_dict()` | 인스턴스를 `dict`로 직렬화 |
| `from_dict(data)` | `dict`에서 인스턴스 복원 (`@classmethod`) |

### JsonRepository

| 메서드 | 설명 | 예외 |
|--------|------|------|
| `create(item)` | 레코드 저장, 저장된 item 반환 | `DuplicateKeyError` |
| `get(id)` | id로 단건 조회 | `RecordNotFoundError` |
| `update(item)` | 기존 레코드 덮어쓰기, item 반환 | `RecordNotFoundError` |
| `delete(id)` | 레코드 삭제 | `RecordNotFoundError` |
| `list_all()` | 전체 레코드 반환 | — |

## 패키지 구조

```
json_store/
├── __init__.py       # 공개 API export
├── base.py           # BaseRepository(ABC)
├── json_repo.py      # JsonRepository 구현체
├── model.py          # BaseModel (dataclass)
└── exceptions.py     # 커스텀 예외

tests/
├── conftest.py       # pytest fixture
└── test_json_repo.py # 단위 테스트 (13개)
```

## 테스트 실행

```bash
pip install pytest
pytest tests/ -v
```

## 커스텀 Repository 구현

`BaseRepository`를 상속해 다른 저장 백엔드로 교체할 수 있다.

```python
from json_store import BaseRepository, BaseModel

class InMemoryRepository(BaseRepository[BaseModel]):
    def __init__(self):
        self._store = {}

    def create(self, item): ...
    def get(self, id): ...
    def update(self, item): ...
    def delete(self, id): ...
    def list_all(self): ...
```
