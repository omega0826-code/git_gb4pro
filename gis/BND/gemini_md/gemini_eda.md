# Project Overview
본 프로젝트는 탐색적 데이터 분석(EDA)을 목적으로 한다.

- 분석 목적:
- 데이터 출처:
- 데이터 단위(행/컬럼 기준 의미):

---

# Response Language
- 모든 응답은 한국어로 작성한다.
- EDA 맥락에 맞는 직관적인 설명을 우선한다.
- 통계 용어는 필요한 경우에만 사용한다.

---

# EDA Principles
EDA 수행 시 기본 원칙.

- 가설을 단정하지 않는다.
- 분포, 패턴, 이상치를 우선적으로 확인한다.
- 수치 요약과 시각화를 함께 제시한다.
- 모든 해석은 데이터 근거와 함께 제시한다.

---

# Data Inspection Rules
데이터 확인 규칙.

- shape, info, describe 결과를 먼저 확인
- 컬럼 타입 및 의미를 명시
- 범주형/수치형 컬럼을 구분
- 결측치 비율을 반드시 수치로 표현

---

# Visualization Guidelines
EDA 시각화 가이드.

- 기본 분포: histogram / boxplot
- 관계 분석: scatter / pairplot
- 범주 비교: bar / countplot
- 시간 흐름: line plot
- 하나의 그래프는 하나의 메시지만 전달

---

# Code Style for EDA
EDA 코드 작성 기준.

- 빠른 반복 분석이 가능하도록 간결하게 작성
- 전처리는 최소 수준으로 유지
- 시각화 코드는 재사용 가능한 함수로 분리
- 실험성 코드임을 명확히 주석으로 표시

---

# Notebook Flow
EDA Notebook 권장 흐름.

1. 데이터 로드
2. 기본 정보 확인
3. 결측치 / 이상치 탐색
4. 단변량 분석
5. 이변량 / 다변량 분석
6. 주요 인사이트 요약

---

# Insight Summary
인사이트 정리 방식.

- 관찰 사실과 해석을 분리
- 수치 기반으로 표현
- 추가 분석 필요 사항 명시

---

# Notes for Gemini
- 결론을 서두르지 않는다
- “~로 보인다” 수준의 표현 사용
- 시각화 해석을 코드보다 우선 설명
