# 기능 요구사항 계획서

> 검토 후 각 항목에 ✅ / ❌ / 수정 요청을 표시해 주세요.

---

## 1. 프로젝트 개요

`json_store`는 JSON 파일 기반의 데이터 영속성 처리 라이브러리다. Python 3.10+ 표준 라이브러리만 사용하며, `ABC` 추상 클래스로 Repository 인터페이스를 정의하고 `JsonRepository`가 이를 구현한다. 다른 프로젝트에서 `from json_store import JsonRepository` 형태로 import하여 즉시 사용할 수 있는 PoC 라이브러리를 목표로 한다.

---

## 2. 아키텍처 레이어 구조

| 레이어 | 모듈 | 역할 | 금지사항 |
|--------|------|------|----------|
| Model | `model.py` | 데이터 구조 정의 (dataclass 기반 `BaseModel`) | 외부 라이브러리 의존 금지 |
| Repository Interface | `base.py` | CRUD 추상 인터페이스 (`BaseRepository`) | 파일 I/O 직접 수행 금지 |
| Repository Impl | `json_repo.py` | JSON 파일 기반 CRUD 구현체 (`JsonRepository`) | Model 레이어 직접 수정 금지 |
| Exceptions | `exceptions.py` | 도메인 전용 예외 클래스 | 표준 예외 그대로 노출 금지 |

### 패키지 구조

```
json_store/                  # 라이브러리 루트
├── __init__.py              # 공개 API export
├── base.py                  # BaseRepository(ABC)
├── json_repo.py             # JsonRepository
├── model.py                 # BaseModel (dataclass)
└── exceptions.py            # 커스텀 예외

tests/
├── __init__.py
├── conftest.py              # pytest fixture (임시 디렉토리 등)
└── test_json_repo.py        # JsonRepository 단위 테스트

docs/
├── plan.md
└── phase/
```

---

## 3. 기능 요구사항

### 3-1. Model (`model.py`)

| 항목 | 내용 |
|------|------|
| `BaseModel` | `@dataclass`로 정의. `id: str` 필드 포함 |
| `id` 생성 | 생성자에서 `uuid.uuid4()` 로 자동 생성 (외부 주입도 허용) |
| `to_dict()` | 인스턴스를 `dict`로 직렬화 |
| `from_dict(data: dict)` | `dict`에서 인스턴스 복원 (`@classmethod`) |

### 3-2. Repository Interface (`base.py`)

`BaseRepository(ABC, Generic[T])` — T는 `BaseModel` 서브타입

| 추상 메서드 | 시그니처 | 설명 |
|-------------|----------|------|
| `create` | `(item: T) -> T` | 레코드 저장, 중복 id 시 예외 |
| `get` | `(id: str) -> T` | id로 단건 조회, 없으면 예외 |
| `update` | `(item: T) -> T` | 기존 레코드 덮어쓰기, 없으면 예외 |
| `delete` | `(id: str) -> None` | 레코드 삭제, 없으면 예외 |
| `list_all` | `() -> list[T]` | 전체 레코드 반환 |

### 3-3. JsonRepository (`json_repo.py`)

| 항목 | 내용 |
|------|------|
| 생성자 | `__init__(self, file_path: str \| Path, model_class: type[T])` |
| 저장 형식 | JSON 배열 `[{"id": "...", ...}, ...]` |
| 파일 없을 때 | 자동 생성 (빈 배열 `[]` 로 초기화) |
| 동시성 | `threading.Lock`으로 파일 읽기/쓰기 보호 |
| 쓰기 방식 | 단순 `json.dump` (원자적 쓰기 없음) |

### 3-4. Exceptions (`exceptions.py`)

| 예외 클래스 | 발생 시점 |
|-------------|----------|
| `JsonStoreError` | 모든 라이브러리 예외의 기반 클래스 |
| `RecordNotFoundError` | `get`, `update`, `delete` 시 id 없음 |
| `DuplicateKeyError` | `create` 시 동일 id 존재 |

### 3-5. 공개 API (`__init__.py`)

```python
from json_store import BaseModel, BaseRepository, JsonRepository
from json_store import JsonStoreError, RecordNotFoundError, DuplicateKeyError
```

---

## 4. 비기능 요구사항

| 항목 | 내용 |
|------|------|
| Python 버전 | 3.10 이상 |
| 외부 라이브러리 | 표준 라이브러리만 허용 (`json`, `pathlib`, `dataclasses`, `threading`, `uuid` 등) |
| 타입 힌트 | 모든 함수/메서드에 타입 힌트 필수 |
| 네이밍 컨벤션 | PEP 8 준수 (snake_case 함수/변수, PascalCase 클래스) |
| 테스트 프레임워크 | pytest |
| 패키지 관리 | `pyproject.toml` 포함 — `pip install -e .` 로 다른 프로젝트에서 바로 사용 가능 |

---

## 5. 구현 순서

각 단계별 상세 스펙은 `docs/phase/` 를 참조한다.

| 단계 | 파일 | 내용 |
|------|------|------|
| Phase 1 | [phase-1-skeleton.md](phase/phase-1-skeleton.md) | 프로젝트 골격 + 예외 클래스 |
| Phase 2 | [phase-2-model.md](phase/phase-2-model.md) | BaseModel (dataclass + UUID) |
| Phase 3 | [phase-3-base-repository.md](phase/phase-3-base-repository.md) | BaseRepository ABC 인터페이스 |
| Phase 4 | [phase-4-json-repository.md](phase/phase-4-json-repository.md) | JsonRepository 구현체 + 공개 API |
| Phase 5 | [phase-5-tests.md](phase/phase-5-tests.md) | pytest 단위 테스트 |

---

## 검토 요청 사항

아래 항목을 확인 후 피드백 부탁드립니다.

- [✅] JSON 저장 형식 `{"records": {"<id>": {...}}}` 방식이 적합한가? (대안: 배열 `[{...}, ...]` 방식) 배열 방식
- [✅] `BaseModel.id` 자동 생성 여부 — id를 외부에서 주입받을지, 생성자에서 `uuid4()`로 자동 생성할지? 자동 UUID생성
- [✅] 원자적 쓰기 (임시파일 → replace) 방식이 필요한가? PoC라면 단순 `json.dump`로 대체 가능 json.dump로 대체
- [✅] `pyproject.toml` 포함 여부 — 라이브러리 배포 설정까지 포함할지, 소스 파일만 작성할지? 둘중 다른 프로젝트에서 사용하기 쉬운 방식으로
