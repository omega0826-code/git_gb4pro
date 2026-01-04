# Project Overview
본 프로젝트는 데이터 분석 및 모델링을 목적으로 한다.

- 프로젝트 목적:
- 분석 대상 데이터:
- 주요 산출물 (리포트, 노트북, 모델 등):

---

# Response Language
- 모든 응답은 **한국어**로 작성한다.
- 코드 외 설명은 간결하고 명확하게 작성한다.
- 불필요한 영어 설명은 피한다.

---

# Analysis Environment
데이터 분석 실행 환경을 정의한다.

- OS:
- Python 버전:
- 주요 라이브러리:
  - pandas
  - numpy
  - matplotlib / seaborn
  - scikit-learn
  - 기타:

---

# Data Rules
데이터 처리 시 반드시 지켜야 할 규칙.

- 원본 데이터는 수정하지 않는다.
- 전처리 결과는 별도 파일/변수로 관리한다.
- 결측치, 이상치는 처리 이유를 명시한다.
- 컬럼명 변경 시 매핑을 명확히 남긴다.

---

# Code Design Principles
코드 작성 및 설계 기준.

- 분석 로직과 시각화 로직을 분리한다.
- 재사용 가능한 함수 단위로 작성한다.
- 매직 넘버 사용을 피하고 상수로 관리한다.
- 실험용 코드와 운영용 코드를 구분한다.
- 하나의 함수는 하나의 역할만 수행한다.

---

# Notebook Conventions
Jupyter Notebook 사용 시 규칙.

- 셀 실행 순서에 의존하지 않도록 작성
- 데이터 로딩 → 전처리 → 분석 → 시각화 → 결론 흐름 유지
- 중간 결과는 간단한 텍스트 요약 포함
- 그래프에는 반드시 제목, 축 라벨 포함



dddddddddddddddddddddddd
---

# File & Directory Structure
권장 디렉토리 구조.

```text
/
├─ data/
│  ├─ raw/
│  └─ processed/
├─ notebooks/
├─ src/
│  ├─ preprocessing/
│  ├─ analysis/
│  └─ visualization/
├─ reports/
└─ README.md


# Output


파일 생성 시 파일명에 끝에 '_현재 시간'을 입력
산출물은 제일 마지막에 알려줘