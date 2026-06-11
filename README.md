
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)
### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 실행
python UnitConverter.py

# 가상환경 비활성화
deactivate
```

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능** 
   - JSON / CSV / 표 형태 출력


## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성 
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점

> **요구사항 SSOT:** 상세 FR/NFR·Mom Test는 [docs/PRD.md](docs/PRD.md) — README는 실행·구조 요약만 유지.

---

## 빠른 시작

```bash
# 가상환경 (최초 1회)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install pytest

# 실행 (stdin 또는 argv)
python UnitConverter.py
python UnitConverter.py meter:2.5
python -m unit_converter.cli meter:2.5

# 테스트
python -m pytest tests/ -v

# Golden 기준 갱신 (출력 계약 변경 시에만)
# UPDATE_GOLDEN=1 python -m pytest tests/test_cli.py::test_u_out_01_meter_input_prints_three_or_more_lines -v
```

**입·출력 예시 (`meter:2.5`):**

```
meter:2.5
→
2.5 meter = 2.5 meter
2.5 meter = 8.2021 feet
2.5 meter = 2.734 yard
```

**pytest (Doc — 8/10 P0 TC PASS):**

```
8 passed
```

P0 TC 10건 중 **U-IN-04** · **U-IN-05** 미작성 (구현은 `input_parser.parse()`에서 처리). 상세 추적은 [Report/06.REPORT.md](Report/06.REPORT.md).

---

## 프로젝트 구조

```
UnitConverter_22/
├── UnitConverter.py              # 하위 호환 진입점 → unit_converter.cli 위임
├── unit_converter/
│   ├── cli.py                    # I/O 오케스트레이션 (python -m unit_converter.cli)
│   ├── input_parser.py           # unit:value 파싱·검증
│   ├── unit_registry.py          # 등록·조회 (OCP)
│   ├── domain/
│   │   ├── length_unit.py        # 단위 계약·meter/feet/yard 구현
│   │   └── converter.py          # meter 허브 변환
│   └── app/
│       └── output_formatter.py   # README 1줄 형식 출력
├── tests/
│   ├── _approval.py              # Golden Master harness
│   ├── golden/                   # Approval 기준 파일 (U-OUT-01)
│   ├── test_converter.py         # Track B — Domain (D-CNV-*)
│   └── test_cli.py               # Track A — Boundary (U-IN-*, U-OUT-01, PFR-03)
├── docs/PRD.md
├── Report/ · Prompting/
└── guide/                        # 로컬 실습 HTML (gitignore)
```

**확정 진입점:** `UnitConverter.py`는 `unit_converter.cli.main`에 위임하며, 모듈 실행은 `python -m unit_converter.cli`를 사용합니다.

**OCP/SRP 4모듈:** `input_parser`(파싱) · `unit_registry`(등록) · `converter`(변환) · `output_formatter`(출력) — 각각 단일 책임, 신규 단위는 Registry 등록만으로 확장.

### Golden Master (`tests/golden/`)

U-OUT-01 CLI stdout을 `tests/golden/*.approved.txt`에 고정해 출력 계약을 보호합니다. `tests/_approval.py`의 `assert_matches_golden`이 실제 stdout과 golden 파일을 바이트 단위로 비교하며, REFACTOR·포맷 변경 시 diff 0을 유지합니다. 기준 갱신은 `UPDATE_GOLDEN=1`로만 수행합니다(수동 편집으로 통과 우회 금지).

### Dual-Track (pytest)

| Track | 파일 | Mock |
|-------|------|------|
| **B — Domain** | `tests/test_converter.py` | 없음 |
| **A — Boundary** | `tests/test_cli.py` | Domain 허용 |

**P0 Test ID × 상태** (PRD §7.1 · [Report/06](Report/06.REPORT.md) §6):

| Test ID | FR/NFR | Given | 상태 |
|---------|--------|-------|------|
| D-CNV-01 | FR-02 | 1 feet → ≈0.3048 m | PASS |
| D-CNV-02 | FR-02 | 2.5 m → feet 5자리 | PASS |
| D-CNV-03 | FR-02 | feet↔yard meter 허브 일치 | PASS |
| U-IN-01 | FR-05 | `""` | PASS |
| U-IN-02 | FR-05 | `meter` | PASS |
| U-IN-03 | FR-04 | `meter:-1` | PASS |
| U-IN-04 | FR-05 | `meter:2.5:extra` | **TC 미작성** |
| U-IN-05 | FR-05 | `abc` | **TC 미작성** |
| PFR-03 | FR-03 | `cubit:1` | PASS |
| U-OUT-01 | FR-01·FR-02 | `meter:2.5` Golden | PASS |

**P1:** D-REG-01 · D-CFG-01 — `new_features` 브랜치. Given/Then·파일/함수 매핑은 [docs/PRD.md](docs/PRD.md).

**PRD ID → Test ID → 주 모듈** (파일/함수 상세: [Report/06 §6](Report/06.REPORT.md)):

| PRD ID | Test ID | 주 모듈 |
|--------|---------|---------|
| FR-01 | U-OUT-01 | `input_parser` · `cli` |
| FR-02 | D-CNV-01~03, U-OUT-01 | `length_unit` · `converter` · `output_formatter` |
| FR-03 | PFR-03 | `unit_registry` · `cli` |
| FR-04 | U-IN-03 | `input_parser` · `cli` |
| FR-05 | U-IN-01~05 | `input_parser` · `cli` |
| NFR-02 | *(구조)* | parser · registry · converter · formatter |
| NFR-03 | Dual-Track 10건 | `tests/test_converter.py` · `tests/test_cli.py` |

---

## REFACTOR To-Do

> **갱신 시점:** 단계 4 REFACTOR 완료 (Agent 프롬pt **4-B**). Change Budget: **계약·Golden 불변**.

### P0 완료

| 항목 | 상태 |
|------|------|
| Golden Master (`tests/golden/`) — U-OUT-01 출력 계약 고정 | **완료** |
| OCP/SRP 4모듈 분리 (Parser · Registry · Converter · Formatter) | **완료** |
| `input_parser`·`unit_registry` app/domain 분리 · `unit_converter.cli` 진입점 | **완료** |

### 잔여 스멜

| 우선순위 | 스멜 | 위치 | 근거 | 후보 |
|----------|------|------|------|------|
| — | *(P0 없음)* | — | Safe Refactor 완료, pytest 8/8·Golden diff 0 | — |
| P1 | Hardcoded unit list | `unit_registry.py:default_registry` | P0 단위가 코드에 고정 | `units.json` 외부화 |
| P1 | Concrete unit classes | `domain/length_unit.py` | 비율 상수가 클래스에 내장 | inch 등 신규 단위·동적 등록 |

### P1 후보 (`new_features` 브랜치)

| 항목 | 설명 | 상태 |
|------|------|------|
| **inch** | `1 meter = 39.3701 inch` 등 길이 단위 확장 | 미착수 |
| **units.json** | 변환 비율·단위 목록 설정 외부화 | 미착수 |
| **--format** | `json` / `csv` / `table` 출력 포맷 선택 | 미착수 |

### Doc 잔여 (P0 TC)

| 항목 | Test ID | 상태 |
|------|---------|------|
| 추가 `:` 경계 | U-IN-04 (`meter:2.5:extra`) | TC 미작성 |
| 비단위 문자열 | U-IN-05 (`abc`) | TC 미작성 |

구현은 `input_parser.parse()`에 존재 — 회귀 방지 TC만 추가하면 P0 **10/10** 달성.

---

## Cursor Commands

| Command | 용도 | 모드 |
|---------|------|------|
| `/export-report-transcript` | Report/NN + Prompting/NN 쌍 저장 | Agent |

- **Skill:** `~/.cursor/skills/export-report-transcript/`
- **Project:** `.cursor/commands/export-report-transcript.md`

---

## D2 실습 · 문서 구조 (C2C)

| 경로 | Git | 용도 |
|------|-----|------|
| [docs/PRD.md](docs/PRD.md) | **추적** | C2C SSOT (요구사항·FR/NFR) |
| [guide/D2-진행가이드.html](guide/D2-진행가이드.html) | **제외** (`guide/`) | 개인 실습 HTML 가이드 |
| `Report/` · `Prompting/` | 추적 | 단계별 Export (`/export-report-transcript`) |

### P0 / P1 요약

| 구분 | ID | 상태 |
|------|-----|------|
| **P0 FR** | FR-01~05 | 구현 **완료** · FR-05 중 U-IN-04/05 **TC만 미작성** |
| **P0 NFR** | NFR-01 | OCP 구조 완료 · D-REG-01은 P1 |
| **P0 NFR** | NFR-02 | SRP 4모듈 **완료** |
| **P0 NFR** | NFR-03 | Dual-Track **8/10 PASS** |
| **P1** | EXT-01 | `units.json` 설정 외부화 — 미착수 |
| **P1** | EXT-02 | cubit 동적 등록 — 미착수 |
| **P1** | EXT-03 | `--format json\|csv\|table` — 미착수 |

### Report · Prompting (ARRR)

| NN | D2 단계 | Phase | Report | Prompting |
|----|---------|-------|--------|-----------|
| 01 | 0 | Mom+PRD | [01.REPORT.md](Report/01.REPORT.md) | [01.Export-Transcript.md](Prompting/01.Export-Transcript.md) |
| 02 | 1 | Design | [02.REPORT.md](Report/02.REPORT.md) | [02.Export-Transcript.md](Prompting/02.Export-Transcript.md) |
| 03 | 2 | RED | [03.REPORT.md](Report/03.REPORT.md) | [03.Export-Transcript.md](Prompting/03.Export-Transcript.md) |
| 04 | 3 | GREEN | [04.REPORT.md](Report/04.REPORT.md) | [04.Export-Transcript.md](Prompting/04.Export-Transcript.md) |
| 05 | 4 | REFACTOR | [05.REPORT.md](Report/05.REPORT.md) | [05.Export-Transcript.md](Prompting/05.Export-Transcript.md) |
| 06 | 5 | Doc | [06.REPORT.md](Report/06.REPORT.md) | [06.Export-Transcript.md](Prompting/06.Export-Transcript.md) |
| 07 | 6 | KPT | *(예정)* | *(예정)* |

**ARRR 현황:** Mom+PRD → Design → RED(8 fail) → GREEN(8 pass) → REFACTOR(Golden) → **Doc(8/10 TC)** · 다음: U-IN-04/05 또는 P1 `new_features`

### C2C 문서 역할

| 문서 | 역할 |
|------|------|
| `docs/PRD.md` | 요구사항 SSOT — Mom Test, FR/NFR, Test ID |
| `Report/` · `Prompting/` | ARRR 단계 기록 (매 Export) |
| `README.md` | **프로젝트 입구** — 실행·구조·Command (구조/API 바뀔 때만) |

### README 갱신 타이밍

| D2 단계 | README |
|---------|--------|
| 0 Mom+PRD · 1 Design · 2 RED | **보류** — PRD·Report에 기록 |
| **3 GREEN** | **1차** — 빠른 시작·pytest·구조·Dual-Track |
| **4 REFACTOR** | **2차** — Golden Master·REFACTOR To-Do·진입점 |
| **5 추적표** | **3차** ✅ — P0/P1 요약·Dual-Track 10건·PRD→모듈·Report 01~06 표 |
| 6 KPT | 선택 |

> **3차 갱신 (완료):** 단계 5 Doc — P0/P1 요약 · Test ID 10건 상태 · PRD→Test→모듈 · Report/Prompting 01~06 ([Report/06](Report/06.REPORT.md)).

- **단계 종료:** Cursor Agent에서 `/export-report-transcript`
- **상세:** `guide/D2-진행가이드.html` §README

### 실무 규칙

1. **요구 바뀜** → `docs/PRD.md`
2. **세션 끝** → `/export-report-transcript`
3. **실행/구조/API 바뀜** → `README.md`
4. README에 Report·PRD 전문 복사 금지

`guide/` 폴더는 gitignore — HTML 가이드는 로컬에서만 사용. PRD·Report·Prompting은 저장소에 커밋.
