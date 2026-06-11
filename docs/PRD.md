# PRD — Unit Converter (Python)

| 항목 | 값 |
|------|-----|
| 버전 | 0.5 (Mom Test criteria 보완) |
| SSOT | 본 문서 ↔ README.md ↔ Test ID |
| 우선순위 | P0 = 이번 스프린트 필수 · P1 = Out of Scope (추가 요구) |
| 구현 상태 | `refactoring` 브랜치 · Dual-Track **8 passed** · Golden **matched** (U-OUT-01) |
| 미작성 P0 TC | U-IN-04, U-IN-05 (REFACTOR 후 추가 예정) |

---

## 1. Problem

### 1.0 Mom Test 인터뷰 메타 (0-A)

| 항목 | 값 |
|------|-----|
| 라운드 | 0-A 1라운드 |
| 질문 수 | 1 |
| Good Data | 1건 (지난주 해외 건축 도면, ~40분, inch→feet 누락 실수) |
| 페르소나 | 해외 도면·내부 보고서 작성 실무자 (엑셀+구글 검산, **CLI 미사용**) |
| 검증 한계 | **부분 검증** — 추가 인터뷰 2~3회 권장 (워크북 순서 5) |

### 1.0.1 주제 (1문장 · Mom Test 기반)

> **길이 단위 변환에서 반복 수식·검산·실수 비용을, 동일 기준의 검증 가능한 변환 결과로 줄인다.**

*(CLI·3단위 동시 출력은 README 실습 SSOT — §1.3 표면 문제 참조)*

### 1.1 Mom Test에서 확정한 진짜 문제 (1문장)

> **해외 도면(feet/inch 혼재)을 내부 meter 보고서로 옮길 때, 스프레드시트 수식·수동 검산에 시간이 들고, 단위 조합·반복 입력 실수로 숫자가 틀릴 수 있다.**

**Good Data (0-A):** 지난주 해외 건축 도면 → 엑셀 `× 0.3048` → 약 40분, inch→feet 누락으로 1회 오류, 구글 검색으로 검산.

### 1.2 Mom Test 증거 3줄 (인터뷰 인용)

1. **40분** — 반복 수식·검산이 실제 비용.
2. **inch→feet 누락** — 단위 **조합** 실수가 핵심 pain (단순 3단위 변환기 아님).
3. **엑셀+구글** — CLI·3단위 동시 출력 요구와 **사용 습관 간격** 존재.

### 1.3 표면 문제 vs 진짜 문제

**표면 문제 (솔루션 혼입 — Mom Test에서 아직 증명되지 않음):**

- “CLI로 meter/feet/yard 3단위 일괄 변환”
- “JSON/CSV/table 출력”
- “`meter:2.5` 파싱 CLI”

| 구분 | 내용 | PRD 반영 |
|------|------|----------|
| **진짜 문제** | 혼합 단위·반복·검산·실수 비용 | Problem·NFR(검증·확장) 동기 |
| **표면/솔루션 혼입** | 위 bullet 3건 | **P0 범위는 README 실습 요구**로 두되, Mom Test로 **우선순위 재검토** 필요 표시 |
| **미검증** | 페르소나1이 CLI·yard 동시 변환을 **쓰지 않음** | P0는 교육·C2C 목표; P1에서 inch·혼합 단위 등 **후속** |

### 1.4 Mom Test 품질 점검 (워크북 순서 5)

| 체크 | 결과 |
|------|------|
| 미래 가정("~하면 좋겠다") 없음 | ✅ |
| 과거 행동·시간·실수 구체성 있음 | ✅ |
| 진짜 문제에 솔루션명(TDD/CLI/Cursor) 없음 | ✅ |
| 표면 문제와 진짜 문제가 분리됨 | ✅ |
| UnitConverter 도메인 반영 (meter/feet/yard·inch 혼재 pain) | ✅ |

**워크북 채점:** **7 / 10** · **판정:** 부분 검증 — 진짜 문제 1문장 확정, 인터뷰 1회·시뮬레이션 기반 한계 명시.

**Mom Test 3원칙 (D1 교재):**

| 원칙 | 0-A 준수 |
|------|----------|
| 내 아이디어 말하지 말 것 | ✅ 솔루션 없이 과거 행동만 수집 |
| 과거·구체·사실만 | ✅ 지난주 도면·40분·1회 오류 |
| 칭찬·미래 의견 무시 | ✅ “좋을 것 같다” 없음 |

### 1.5 Mom Test 평가 (4기준)

| 기준 | 평가 |
|------|------|
| 사실 (과거 행동) | ✅ 구체적 사건 |
| 구체성 | ✅ 도구·시간·실수 |
| 솔루션 혼입 | ✅ 없음 (엑셀·검색 = 기존 행동) |
| Good Data | ✅ 40분, 1회 오류 |

### 1.6 R-G-I-O (Mom Test 연결)

| 항목 | 내용 |
|------|------|
| **Role** | 길이 단위 변환을 스프레드시트·수기·CLI로 처리하는 실무자 (0-A: 엑셀+검산 중심) |
| **Goal** | **한 입력**으로 meter/feet/yard 간 **일관·검증 가능한** 변환 결과를 얻어, 수식 반복·검산 불안을 줄인다 *(실습 P0: README 기본·품질 요구)* |
| **Input** | `단위:값` 문자열 (예: `meter:2.5`) |
| **Output** | 입력 단위·값 + **지원 단위 전부**에 대한 변환 결과 (stderr/exit code로 명확한 오류) |

**Mom Test → R-G-I-O:** Input/Output 형식은 **실습 SSOT**; Goal은 Mom Test **반복·실수·검산** pain과 연결. feet+inch 혼합은 **본 P0 범위 밖**(후속 후보).

### 1.7 성공 기준 3개 (Mom Test 증거 → 테스트 씨앗)

| # | 성공 기준 | Mom Test 증거 | PRD·Test ID |
|---|-----------|---------------|-------------|
| **SC-01** | feet↔meter 변환 정확도가 TC·Golden으로 **재현 가능** | 증거 1 (40분·검산 pain) | FR-02 · D-CNV-01, D-CNV-02, U-OUT-01 |
| **SC-02** | 잘못된 입력·음수·미지 단위가 **크래시 없이 거부** | 증거 2 (inch→feet 누락류 실수 방지) | FR-03~05 · U-IN-01~05, PFR-03 |
| **SC-03** | 단위 추가 시 **변환 핵심 비수정** (반복 수식 대체 확장성) | 증거 3 (습관·도구 간격 → 확장 가능 구조) | NFR-01 · D-REG-01 *(P1)* |

---

## 2. As-Is (레거시 baseline)

**대상:** `UnitConverter.py` 단일 `main()` (~37줄) — `input` → `split(':', 1)` → `float` → `if unit == "meter"` / `elif …` → `print(상수 연산)`.

### 2.1 동작 예시 3건 (입·출력)

| # | 입력 | 실제 출력 (As-Is) | README 기대와 차이 |
|---|------|-------------------|-------------------|
| **A-1** | `meter:2.5` | `8.2021` *(feet 1줄만, 단위·yard 없음, 포맷 `N meter = …` 아님)* | FR-02 미충족 (전 단위 미출력) |
| **A-2** | `feet:10` | `3.048` *(meter 1줄만)* | 입력 단위별 **서로 다른** 1줄 출력; 대칭 API 없음 |
| **A-3** | `meter:2.5:extra` | `split(':', 1)` → `value="2.5:extra"` → `float` **ValueError** *(처리 없음)* | FR-05 경계 미검증; 크래시 |

**부가 관찰 (As-Is):**

- `yard:3` — yard 분기만 실행, **feet·meter 동시 출력 없음**
- `meter:-1` — **음수 그대로 출력** (FR-04 없음)
- `cubit:1` — **매칭 분기 없음** → 무출력 또는 암묵적 no-op (FR-03 없음)
- `meter` / `abc` — `:` 없음·비숫자 → **예외 또는 오동작**

### 2.2 현재 구현 상태 (To-Be · REFACTOR 완료)

```python
# UnitConverter.py — 하위 호환 진입점
from unit_converter.cli import main
```

| 영역 | 상태 | 비고 |
|------|------|------|
| `unit_converter/cli.py` | ✅ | `python -m unit_converter.cli` 확정 진입점 |
| `input_parser.py` | ✅ | app에서 분리 — FR-01/04/05 |
| `unit_registry.py` | ✅ | domain에서 분리 — FR-03, NFR-01 |
| `domain/converter.py` | ✅ | meter 허브 `convert_all` |
| `app/output_formatter.py` | ✅ | README 1줄 형식 |
| `tests/` Dual-Track | ✅ | 8 passed · U-OUT-01 Golden Master |
| `infrastructure/` | ⏳ P1 | `config_loader.py` 미구현 |

**Golden Master:** `tests/golden/u_out_01_meter_2_5.approved.txt` — U-OUT-01 stdout 계약 (`tests/_approval.py`).

레거시 baseline(§2.1) 대비 To-Be 구현·REFACTOR 결과는 `Report/04`(GREEN), `Report/05`(REFACTOR) 참조.

---

## 3. 코드 스멜 (레거시 baseline)

| 스멜 | 위반 | 근거 |
|------|------|------|
| **OCP** | 단위 추가 시 `main()` **if/elif 수정** | meter/feet/yard마다 분기·상수 |
| **SRP** | **입력 파싱·변환·출력·검증** 한 함수 | `input`/`split`/`float`/`print` 혼재 |
| **하드코딩** | `3.28084`, `1.09361` 등 **소스 내 상수** | README: meter 기준 비율; 설정 외부화(P1) 미적용 |
| **검증 누락** | 음수·미지 단위·형식 오류 | README 품질 요구 미구현 |
| **split 경계** | `split(':', 1)` — `meter:2.5:extra` 등 **추가 `:`** 미처리 | D2 슬라이드 RED 후보 |
| **출력 계약 불일치** | README: `2.5 meter = 8.2 feet` 형식·**전 단위** | As-Is: 분기당 1줄·레이블 없음 |
| **테스트 불가 구조** | 전역 `input()`·`print` | README: TC로 변환 검증 요구 |

---

## 4. To-Be — 기능·비기능 요구 (P0)

### 4.1 비즈니스 규칙

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet ↔ yard는 **meter 기준** 환산

### 4.2 Functional Requirements (FR)

| ID | 요구사항 | Given | Then | 우선순위 |
|----|----------|-------|------|----------|
| **FR-01** | `단위:값` 파싱 | `meter:2.5` | `unit=meter`, `value=2.5` | P0 |
| **FR-02** | **지원 단위 전부**로 변환 출력 | `meter:2.5` | `feet≈8.2021`, `yard≈2.7340` 등 README 형식 | P0 |
| **FR-03** | 미등록 단위 거부 | `cubit:1` *(등록 없음)* | 명확한 오류 메시지·비zero exit | P0 |
| **FR-04** | 음수 입력 거부 | `meter:-1` | 거부/예외·오류 메시지 | P0 |
| **FR-05** | 잘못된 형식 거부 | `meter` / `abc` / `meter:2.5:extra` | 형식 오류·**크래시 없음** | P0 |

**Mom Test 메모:** FR-02의 yard·3단위 동시 출력은 **실습 P0**; 사용자 빈도는 Mom Test상 **feet↔meter**가 더 높음 → TC·Golden Master는 **feet/meter 정확도**를 우선 검증.

### 4.3 Non-Functional Requirements (NFR)

| ID | 요구사항 | 검증 관점 | Then | 우선순위 |
|----|----------|-----------|------|----------|
| **NFR-01** | **OCP** | `inch` 등 단위 추가 | 기존 **변환기 핵심** 코드 비수정(등록·설정 확장) | P0 |
| **NFR-02** | **SRP** | 모듈 분리 | **Parser / Registry / Converter / Formatter** (또는 동등) 책임 분리 | P0 |
| **NFR-03** | **테스트 가능** | README Activities | Dual-Track 8건 PASS · U-OUT-01 Golden Master | P0 |

### 4.4 지원 단위 (P0)

- meter, feet, yard

### 4.5 To-Be Architecture (D2 단계 1 · Design → REFACTOR 확정)

**상태:** 설계 확정 · GREEN 8건 PASS · REFACTOR 완료 · Golden Master(U-OUT-01) matched (`Report/05.REPORT.md`)

#### 4.5.1 패키지 구조

```
UnitConverter_22/
├── UnitConverter.py              # 하위 호환 엔트리포인트 (cli 위임)
├── unit_converter/
│   ├── cli.py                    # I/O 오케스트레이션 (python -m unit_converter.cli)
│   ├── input_parser.py           # "unit:value" 파싱·검증 (app에서 분리)
│   ├── unit_registry.py          # 등록·조회 (domain에서 분리, OCP)
│   ├── domain/
│   │   ├── length_unit.py        # 단위 Protocol·구현체 (meter/feet/yard)
│   │   └── converter.py          # meter 허브 기반 순수 변환
│   ├── infrastructure/           # P1 — P0 핵심 범위 밖
│   │   └── config_loader.py      # JSON/YAML 비율 로드 (미구현)
│   └── app/
│       └── output_formatter.py   # README 1줄 형식 출력 (P1: json/csv/table)
└── tests/
    ├── _approval.py              # Golden Master harness
    ├── golden/                   # Approval 기준 (U-OUT-01)
    ├── test_converter.py         # Track B (Domain)
    └── test_cli.py               # Track A (Boundary)
```

**의존 방향:** `domain` ← `unit_registry` ← `cli` ← `input_parser` / `output_formatter` (app). Domain은 I/O·CLI에 비의존 (NFR-03). `input_parser`·`unit_registry`는 패키지 루트에 두어 app/domain 경계와 SRP 4모듈을 명확히 함.

#### 4.5.2 모듈 단일 책임 (SRP)

| 모듈 | 단일 책임 | 담당 FR/NFR |
|------|-----------|-------------|
| `length_unit.py` | 단위 계약 (`name`, `to_meter`) | NFR-01 |
| `unit_registry.py` | 이름 기준 등록·조회 | FR-03, NFR-01 |
| `converter.py` | meter 허브 → 전 단위 숫자 변환 | FR-02, NFR-01 |
| `input_parser.py` | `단위:값` 파싱·형식·음수 검증 | FR-01, FR-04, FR-05 |
| `output_formatter.py` | README 형식 문자열 출력 | FR-02 |
| `cli.py` | parser → registry → converter → formatter 조립 | FR-02, FR-03 |
| `config_loader.py` *(P1)* | 외부 설정에서 비율 로드 | EXT-01 |

#### 4.5.3 OCP 확장 규칙

| 변경 | 수정 대상 | 수정하지 않는 대상 |
|------|-----------|-------------------|
| `inch` 등 단위 추가 (NFR-01) | `length_unit.py` 구현체 + `registry.register()` | `converter.py` 핵심, `cli.py` if/elif |
| 동적 등록 (EXT-02) | `registry.register()` 호출부 | `converter.convert_all()` 내부 |
| 출력 포맷 (EXT-03) | `output_formatter.py` | `converter.py` |

#### 4.5.4 데이터 흐름 (P0 Happy Path)

```
stdin/argv "meter:2.5"
  → input_parser.parse()           → ("meter", 2.5)          [FR-01]
  → unit_registry.get("meter")                               [FR-03 경계]
  → converter.convert_all(...)     → {feet, yard, meter, …}  [FR-02]
  → output_formatter.format(...)   → stdout                  [FR-02]
```

오류 경로: parser 실패(FR-04/05) 또는 registry 미등록(FR-03) → `cli`가 stderr·exit code 통일.

#### 4.5.5 FR/NFR → 파일 매핑

| ID | 주 책임 모듈 | 보조 모듈 | Test ID |
|----|-------------|-----------|---------|
| FR-01 | `input_parser.py` | `cli.py` | U-OUT-01 |
| FR-02 | `converter.py` | `output_formatter.py`, `unit_registry.py`, `cli.py` | D-CNV-01, D-CNV-02, D-CNV-03, U-OUT-01 |
| FR-03 | `unit_registry.py` | `cli.py` | PFR-03 *(별칭 U-ERR-01)* |
| FR-04 | `input_parser.py` | `cli.py` | U-IN-03 |
| FR-05 | `input_parser.py` | `cli.py` | U-IN-01, U-IN-02, U-IN-04, U-IN-05 |
| NFR-01 | `length_unit.py`, `unit_registry.py` | — | D-REG-01 *(P1)* |
| NFR-02 | 전체 패키지 레이아웃 | — | 구조 리뷰 |
| NFR-03 | `tests/test_converter.py`, `tests/test_cli.py` | — | Dual-Track TC |
| EXT-01 | `config_loader.py` | — | D-CFG-01 |
| EXT-02 | `unit_registry.py` | `cli.py` | D-REG-01 |
| EXT-03 | `output_formatter.py` | `cli.py` | *(P1 별도)* |

#### 4.5.6 As-Is → To-Be 대응

| As-Is | 원인 | To-Be 모듈 | Test ID |
|-------|------|-----------|---------|
| A-1 `meter:2.5` → feet 1줄만 | if/elif·비대칭 출력 | `converter` + `output_formatter` | U-OUT-01 |
| A-2 `feet:10` → meter 1줄만 | 동일 | 동일 | D-CNV-03 |
| A-3 `meter:2.5:extra` → ValueError | `split(':',1)` 경계 미처리 | `input_parser` | U-IN-04 |

---

## 5. Out of Scope (P1 — README 추가 요구)

| ID | 요구사항 | 설명 | 우선순위 |
|----|----------|------|----------|
| **EXT-01** | 설정 외부화 | JSON/YAML(`units.json`)에서 비율 로드 | **P1** |
| **EXT-02** | 동적 단위 등록 | `1 cubit = 0.4572 meter` 런타임 등록·사용 | **P1** |
| **EXT-03** | 출력 포맷 선택 | `--format json \| csv \| table` | **P1** |

**P0 vs P1:** FR-03 `cubit:1` **오류**는 P0(미등록 거부); EXT-02 **등록 후 사용**은 P1.

---

## 6. Mom Test → PRD 추적 (요약)

### 6.1 증거 → 신호 → PRD

| Mom Test 증거 (§1.2) | Mom Test 신호 | PRD 반영 |
|----------------------|---------------|----------|
| 40분·반복·검산 | 반복 수식·검산 비용 | §1.7 SC-01 · Goal · FR-02 · D-CNV-01/02, U-OUT-01 |
| inch→feet 누락 | 단위 조합 실수 | §1.7 SC-02 · FR-04/05 · U-IN-01~05 |
| 엑셀+구글 vs CLI 간격 | 사용 습관·도구 불일치 | §1.3 표면 문제 · P0=실습 SSOT · UX 후속 |
| yard 거의 미사용 | 3단위 동시 출력 미검증 | FR-02 유지(실습); TC 우선순위 feet/meter |

### 6.2 성공 기준 → FR/NFR/TC

| 성공 기준 | Mom Test 근거 | PRD ID | Test ID |
|-----------|---------------|--------|---------|
| **SC-01** 변환 정확도 재현 | 증거 1 | FR-02 | D-CNV-01, D-CNV-02, D-CNV-03, U-OUT-01 |
| **SC-02** 오류 입력 거부 | 증거 2 | FR-03, FR-04, FR-05 | U-IN-01~05, PFR-03 |
| **SC-03** OCP 확장 | 증거 3 | NFR-01 | D-REG-01 *(P1)* |

### 6.3 품질 점검 → 검증 범위

| 품질 점검 (§1.4) | PRD·구현 함의 |
|------------------|---------------|
| 7/10 · 부분 검증 | P0는 README·C2C; inch·혼합 단위는 P1+ |
| 도메인 반영 ✅ | feet↔meter pain → TC·Golden 우선 (§4.2 Mom Test 메모) |
| 인터뷰 1회 한계 | 0-A 2라운드 권장 — Report/01 §7 |

---

## 7. C2C 추적 (PRD → Test ID → 모듈)

### 7.1 P0 Test Case

| PRD ID | Test ID | Track | Given | Then | 주 모듈 | RED |
|--------|---------|-------|-------|------|---------|-----|
| FR-02 | D-CNV-01 | B | 1 feet | ≈ 0.3048 m | `length_unit`, `converter` | ✅ |
| FR-02 | D-CNV-02 | B | 2.5 meter | feet ≈ 8.20210 | `converter` | ✅ |
| FR-02 | D-CNV-03 | B | feet 입력 | yard·meter 상호 일관 | `converter` | ✅ |
| FR-05 | U-IN-01 | A | `""` | 형식 오류·비zero exit | `input_parser`, `cli` | ✅ |
| FR-05 | U-IN-02 | A | `meter` | 형식 오류 | `input_parser` | ✅ |
| FR-04 | U-IN-03 | A | `meter:-1` | 거부·오류 메시지 | `input_parser` | ✅ |
| FR-05 | U-IN-04 | A | `meter:2.5:extra` | 형식 오류·크래시 없음 | `input_parser` | ⏳ |
| FR-05 | U-IN-05 | A | `abc` | 형식 오류 | `input_parser` | ⏳ |
| FR-03 | PFR-03 | A | `cubit:1` | 명확한 오류·비zero exit | `unit_registry`, `cli` | ✅ |
| FR-01, FR-02 | U-OUT-01 | A | `meter:2.5` | README 형식 전 단위 · **Golden matched** | `cli` (E2E) | ✅ Golden |

**Test ID 별칭:** `PFR-03` = Mom Test·D2 슬라이드 ID; PRD §4.2 **FR-03**과 동일 요구. 코드·커밋에서는 `PFR-03`, 문서 추적용으로 `U-ERR-01` 병기 가능.

**P0 Dual-Track 1차:** 8건 — **GREEN·REFACTOR 완료** (`pytest` 8 passed). **Golden:** U-OUT-01 → `tests/golden/u_out_01_meter_2_5.approved.txt`. **미작성:** U-IN-04, U-IN-05 (§7.1 10건 완료 전).

**RED 규칙 (D1/D2):** `pytest.fail("RED: [TestID]")` · skip/xfail 금지 · Given/When/Then 주석 · RED 단계에서만 구현 코드 금지.

### 7.1.1 RED 커밋 (`red` 브랜치)

| 커밋 | Test ID | 파일 |
|------|---------|------|
| 1 | D-CNV-01, D-CNV-02 | `tests/test_converter.py` |
| 2 | D-CNV-03 | `tests/test_converter.py` |
| 3 | U-IN-01~03 | `tests/test_cli.py` |
| 4 | U-OUT-01, PFR-03 | `tests/test_cli.py` |

**RED 검증:** `pytest tests/` → **8 failed** (ERROR 0, skip 0).

### 7.1.2 GREEN · REFACTOR (`green` → `refactoring`)

| Phase | pytest | Golden | 브랜치 | Report |
|-------|--------|--------|--------|--------|
| GREEN | 8 passed | — | `green` | [Report/04](../Report/04.REPORT.md) |
| REFACTOR | 8 passed | U-OUT-01 matched | `refactoring` | [Report/05](../Report/05.REPORT.md) |

**Golden 갱신:** `UPDATE_GOLDEN=1 python -m pytest tests/test_cli.py::test_u_out_01_meter_input_prints_three_or_more_lines -v` — 출력 계약 변경 시에만.

### 7.2 P1 Test Case (Out of Scope)

| PRD ID | Test ID | Given | Then | 주 모듈 |
|--------|---------|-------|------|---------|
| NFR-01, EXT-02 | D-REG-01 | cubit 0.4572 m 등록 | 변환 성공 | `unit_registry` |
| EXT-01 | D-CFG-01 | 깨진 units.json | ConfigError | `config_loader` |

### 7.3 구현 순서 (ARRR)

1. **RED** — §7.1 Dual-Track 1차 8건 스켈레톤 ✅ · U-IN-04/05 추가 후 §7.1 10건 완료
2. **GREEN** — D-CNV-01~03 + U-OUT-01 최소 통과 ✅ (`Report/04`)
3. **REFACTOR** — Golden Master · SRP 4모듈 분리 · `unit_converter.cli` 진입점 ✅ (`Report/05`)
4. **P1** — §7.2 + `new_features` 브랜치 (inch · `units.json` · `--format`)

---

## 8. 참조

- [README.md](../README.md) — 실행·구조·Golden·REFACTOR To-Do
- [Report/01.REPORT.md](../Report/01.REPORT.md) — Mom Test 세션 기록 (단계 0; criteria SSOT는 본 문서 §1)
- [Report/02.REPORT.md](../Report/02.REPORT.md) — OCP/SRP 아키텍처 설계 (단계 1)
- [Report/03.REPORT.md](../Report/03.REPORT.md) — Dual-Track RED·pytest FAIL (단계 2)
- [Report/04.REPORT.md](../Report/04.REPORT.md) — GREEN 최소 구현 (단계 3)
- [Report/05.REPORT.md](../Report/05.REPORT.md) — Golden Master + REFACTOR (단계 4)
- `tests/_approval.py`, `tests/golden/` — Golden Master harness·approve 파일
- `tests/test_converter.py` — Track B (D-CNV-01~03)
- `tests/test_cli.py` — Track A (U-IN-01~03, U-OUT-01 Golden, PFR-03)
