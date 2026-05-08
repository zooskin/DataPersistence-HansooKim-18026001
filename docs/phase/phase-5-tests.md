# Phase 5 — pytest 단위 테스트

## 목표

`JsonRepository`의 모든 CRUD 동작과 예외 케이스를 pytest로 검증한다.

---

## 작업 범위

### 파일: `tests/conftest.py` (Phase 1에서 생성, 내용 확정)

```python
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
```

---

### 파일: `tests/test_json_repo.py`

#### 테스트 그룹 및 케이스

| 그룹 | 테스트 함수 | 검증 내용 |
|------|-------------|----------|
| 초기화 | `test_creates_file_on_init` | 파일이 없을 때 생성되고 내용이 `[]` |
| create | `test_create_returns_item` | 반환값이 입력과 동등 |
| create | `test_create_persists_to_file` | 파일에 레코드가 저장됨 |
| create | `test_create_duplicate_raises` | 동일 id 두 번 → `DuplicateKeyError` |
| get | `test_get_existing_record` | 저장된 레코드를 올바른 타입으로 반환 |
| get | `test_get_missing_raises` | 없는 id → `RecordNotFoundError` |
| update | `test_update_changes_value` | 값 변경 후 `get` 시 새 값 반환 |
| update | `test_update_missing_raises` | 없는 id → `RecordNotFoundError` |
| delete | `test_delete_removes_record` | 삭제 후 `get` 시 `RecordNotFoundError` |
| delete | `test_delete_missing_raises` | 없는 id → `RecordNotFoundError` |
| list_all | `test_list_all_empty` | 빈 저장소 → 빈 리스트 반환 |
| list_all | `test_list_all_returns_all` | 여러 레코드 저장 후 전체 반환 |
| 타입 | `test_get_returns_correct_type` | 반환값이 `SampleModel` 인스턴스 |

#### 테스트 작성 원칙

- 각 테스트는 독립적으로 실행 가능해야 한다 (`repo` fixture가 매번 새 파일 사용)
- `pytest.raises(ExceptionClass)` 컨텍스트 매니저로 예외 검증
- `assert` 문만 사용 (별도 assertion 라이브러리 금지)
- 하나의 테스트 함수는 하나의 동작만 검증

#### 테스트 실행 명령

```bash
pytest tests/ -v
```

---

## 완료 조건

- [ ] `pytest tests/ -v` 실행 시 모든 테스트가 PASSED
- [ ] 총 테스트 케이스 수가 12개 이상
- [ ] `FAILED` 또는 `ERROR` 가 0건
- [ ] 각 테스트가 다른 테스트의 파일 상태에 영향받지 않음 (fixture 격리 확인)

## 커밋

```
feat: JsonRepository pytest 단위 테스트 추가
```
