# Project Overview
본 프로젝트는 데이터 분석 결과를 기반으로
리포트를 자동 생성하는 것을 목표로 한다.

- 리포트 대상:
- 주요 독자(비기술/기술):
- 리포트 산출 형식 (PDF, HTML, PPT 등):

---

# Response Language
- 모든 텍스트 결과물은 한국어로 작성한다.
- 비기술 독자도 이해할 수 있는 표현을 사용한다.
- 코드 설명은 최소화한다.

---

# Report Structure
자동 생성 리포트 기본 구조.

1. 요약 (Executive Summary)
2. 분석 목적 및 데이터 개요
3. 주요 지표 요약
4. 핵심 인사이트
5. 시각화 결과
6. 한계 및 향후 과제

---

# Writing Style
리포트 문장 작성 규칙.

- 결론을 먼저 제시한다
- 수치는 문장으로 풀어서 설명한다
- 표·그래프는 해석 문장과 함께 제시한다
- 전문 용어는 필요 시 괄호로 설명한다

---

# Visualization Rules
리포트용 시각화 기준.

- 색상 최소화 (2~3개)
- 단위 및 기준 명확히 표기
- 그래프 하나당 핵심 메시지 1개
- 캡션에 해석 요약 포함

---

# Automation Rules
자동 생성 관련 규칙.

- 리포트는 재실행 시 동일 결과를 보장해야 한다
- 코드 실행 → 결과 저장 → 문서 생성 흐름 유지
- 모든 출력물은 파일로 저장
- 날짜, 데이터 버전 명시

---

# File Output Rules
산출물 관리 기준.

```text
/
├─ outputs/
│  ├─ figures/
│  ├─ tables/
│  └─ reports/
│     ├─ report_YYYYMMDD.pdf
│     └─ report_YYYYMMDD.html
