# 프로젝트 규칙

## Git 커밋 규칙

기능 구현이 완료되면 자동으로 git commit을 생성한다.

- 커밋 타이밍: 하나의 기능 추가 또는 작업 단위가 완료된 직후
- 커밋 메시지 형식: `feat: <구현한 기능 요약>`
- 별도 지시 없이도 작업 완료 시 자동으로 커밋한다
- push는 사용자가 명시적으로 요청할 때만 수행한다

---

## 프로젝트 개요

`json_store`는 JSON 파일 기반의 데이터 영속성 CRUD 라이브러리다. 다른 프로젝트에서 `pip install -e .` 후 `from json_store import JsonRepository` 형태로 import하여 사용한다.

상세 요구사항: `docs/plan.md`  
단계별 구현 스펙: `docs/phase/`

---

## 기술 스택

- Python 3.10+
- 표준 라이브러리만 사용 (`json`, `pathlib`, `dataclasses`, `threading`, `uuid`)
- 테스트: pytest
- 패키지 관리: `pyproject.toml`

---

## 패키지 구조

```
json_store/
├── __init__.py       # 공개 API export
├── base.py           # BaseRepository(ABC)
├── json_repo.py      # JsonRepository 구현체
├── model.py          # BaseModel (dataclass)
└── exceptions.py     # JsonStoreError, RecordNotFoundError, DuplicateKeyError

tests/
├── __init__.py
├── conftest.py
└── test_json_repo.py
```

---

## 아키텍처 규칙

- **레이어 의존 방향**: `json_repo` → `base` → `model` / `exceptions`
- `base.py`(인터페이스)는 파일 I/O를 직접 수행하지 않는다
- `json_repo.py`는 `model.py`의 필드를 직접 수정하지 않는다
- 외부 라이브러리는 어떠한 경우에도 추가하지 않는다

---

## 코딩 규칙

- 모든 함수/메서드에 타입 힌트 필수
- PEP 8 준수: `snake_case` 함수/변수, `PascalCase` 클래스
- 주석은 WHY가 명확히 비자명한 경우에만 한 줄 작성

---

## JSON 저장 형식

파일 내용은 항상 **배열** 형태를 유지한다.

```json
[
  {"id": "uuid-string", "field1": "value1"},
  {"id": "uuid-string", "field2": "value2"}
]
```

- `id` 필드는 `uuid.uuid4()` 로 자동 생성 (외부 주입도 허용)
- 쓰기는 단순 `json.dump(ensure_ascii=False, indent=2)` 사용
- 모든 파일 읽기/쓰기는 `threading.Lock` 안에서 수행

---

## 공개 API

```python
from json_store import BaseModel, BaseRepository, JsonRepository
from json_store import JsonStoreError, RecordNotFoundError, DuplicateKeyError
```

---

## 구현 순서

| 단계 | 내용 |
|------|------|
| Phase 1 | 프로젝트 골격 + 예외 클래스 |
| Phase 2 | BaseModel (UUID 자동 생성, to_dict/from_dict) |
| Phase 3 | BaseRepository ABC 인터페이스 |
| Phase 4 | JsonRepository 구현체 + 공개 API export |
| Phase 5 | pytest 단위 테스트 |
