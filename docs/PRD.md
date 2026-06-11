# PRD — Unit Converter (Python)

| 항목 | 값 |
|------|-----|
| 버전 | 0.1 (초안) |
| SSOT | 본 문서 ↔ README.md ↔ Test ID |
| 우선순위 | P0 = 이번 스프린트 필수 · P1 = Out of Scope (추가 요구) |

---

## 1. Problem

### 1.1 Mom Test에서 확정한 진짜 문제 (1문장)

> **해외 도면(feet/inch 혼재)을 내부 meter 보고서로 옮길 때, 스프레드시트 수식·수동 검산에 시간이 들고, 단위 조합·반복 입력 실수로 숫자가 틀릴 수 있다.**

**Good Data (0-A):** 지난주 해외 건축 도면 → 엑셀 `× 0.3048` → 약 40분, inch→feet 누락으로 1회 오류, 구글 검색으로 검산.

### 1.2 표면 문제 vs 진짜 문제

| 구분 | 내용 | PRD 반영 |
|------|------|----------|
| **진짜 문제** | 혼합 단위·반복·검산·실수 비용 | Problem·NFR(검증·확장) 동기 |
| **표면/솔루션 혼입** | “CLI 3단위 일괄 변환”, “JSON 출력” | **P0 범위는 README 실습 요구**로 두되, Mom Test로 **우선순위 재검토** 필요 표시 |
| **미검증** | 페르소나1이 CLI·yard 동시 변환을 **쓰지 않음** | P0는 교육·C2C 목표; P1에서 inch·혼합 단위 등 **후속** |

### 1.3 R-G-I-O (Mom Test 연결)

| 항목 | 내용 |
|------|------|
| **Role** | 길이 단위 변환을 스프레드시트·수기·CLI로 처리하는 실무자 (0-A: 엑셀+검산 중심) |
| **Goal** | **한 입력**으로 meter/feet/yard 간 **일관·검증 가능한** 변환 결과를 얻어, 수식 반복·검산 불안을 줄인다 *(실습 P0: README 기본·품질 요구)* |
| **Input** | `단위:값` 문자열 (예: `meter:2.5`) |
| **Output** | 입력 단위·값 + **지원 단위 전부**에 대한 변환 결과 (stderr/exit code로 명확한 오류) |

**Mom Test → R-G-I-O:** Input/Output 형식은 **실습 SSOT**; Goal은 Mom Test **반복·실수·검산** pain과 연결. feet+inch 혼합은 **본 P0 범위 밖**(후속 후보).

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

### 2.2 현재 워킹트리 참고

```python
# UnitConverter.py (현재) — 레거시 로직 제거, cli 위임만 존재
from unit_converter.app.cli import main  # ← 미구현
```

레거시 스멜 분석·P0 구현 대상은 **§2.1 baseline**이다.

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
| **NFR-03** | **테스트 가능** | README Activities | 단위 변환·입력 검증 **TC** 존재 | P0 |

### 4.4 지원 단위 (P0)

- meter, feet, yard

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

| Mom Test 신호 | PRD 반영 |
|---------------|----------|
| 반복 수식·40분 | Goal: 일관 변환·검증 가능 출력 |
| inch→feet 누락 | FR-04/05 강화; **inch·혼합 단위**는 P1+ 후속 |
| 엑셀·구글 검산 | P0 CLI는 실습 SSOT; UX는 **후속** 검토 |
| yard 거의 미사용 | FR-02 유지(실습); 우선순위·TC는 feet/meter |

---

## 7. C2C 추적 (다음 단계 placeholder)

| PRD ID | Test ID (예정) | 비고 |
|--------|----------------|------|
| FR-01 | U-IN-* / Parser | |
| FR-02 | D-CNV-02, U-OUT-01 | Golden Master |
| FR-03 | U-OUT-01, PFR-03 | |
| FR-04 | U-IN-03 | |
| FR-05 | U-IN-01,02 + `meter:2.5:extra` | |
| NFR-01 | D-REG-01 | P1과 구분 |
| NFR-02 | 구조 리뷰 | REFACTOR |

---

## 8. 참조

- [README.md](../README.md) — 기본·품질·추가 요구
- [Report/01.REPORT.md](../Report/01.REPORT.md) — Mom Test 요약
- [guide/D2-진행가이드.html](../guide/D2-진행가이드.html) — D2 실습 가이드 (로컬, gitignored)
