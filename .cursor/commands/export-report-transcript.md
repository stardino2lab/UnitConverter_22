# /export-report-transcript

`export-report-transcript` Skill을 따라 **현재 Cursor 세션**을 Export한다.

## 산출물 (항상 쌍)

- `Report/NN.REPORT.md` — 구조화된 단계 요약
- `Prompting/NN.Export-Transcript.md` — User/Cursor 대화 전문

## 규칙

1. Skill: `@export-report-transcript` (또는 `~/.cursor/skills/export-report-transcript/SKILL.md`)
2. `Report/`·`Prompting/` 기존 최대 NN + 1 (2자리). **덮어쓰기 금지**
3. 현재 채팅에서 **자동 추출** — NN·주제·형식 **추가 질문 금지**
4. Transcript는 요약 금지 — **대화 전문** 포함
5. pytest·변경 파일·브랜치가 있으면 Report에 반영

## D2 단계별 기대 NN (참고)

| 단계 | NN |
|------|-----|
| 0 Mom+PRD | 01 |
| 1 Design | 02 |
| 2 RED | 03 |
| 3 GREEN | 04 |
| 4 REFACTOR | 05 |
| 5 Doc | 06 |
| 6 KPT | 07 |

지금 Export를 실행하라.
