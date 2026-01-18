

---

# 프로젝트별 규칙: 강남구 피부과 경쟁 및 전략 분석

> **프로젝트 코드명**: `gangnam_skin_strategy`

이 문서는 **강남구 피부과 집중 분석(EDA) 및 O2O 전략 수립** 프로젝트에 특화된 규칙을 정의합니다. `gemini.md`의 글로벌 표준을 따르되, 본 문서의 도메인 로직이 우선합니다.

## 1. 프로젝트 개요

* **프로젝트명**: 강남구 피부과 입지 및 경쟁 전략 분석 (Gangnam Dermatology Analysis)
* **프로젝트 코드**: `gangnam_skin_1st`
* **목적**:
1. **경쟁 구도 시각화**: 전문의 vs 일반의(클리닉) 분포 및 병원 체급별(공장형 vs 프라이빗) 포지셔닝 파악
2. **틈새 시장 발굴**: 야간/심야 진료 현황 및 수술 인프라 보유 여부에 따른 고단가 시장 기회 포착


* **핵심 대상**: 강남구 소재 '피부과' 진료 병의원 (전문의/일반의 포함)

## 2. 파일 및 디렉토리 구조

기본적으로 현재 폴더를 루트로 하여 프로젝트별 하위 디렉토리를 구성합니다.

### 2.1 파일명 규칙 (Naming Convention)

#### 타임스탬프 포맷 (필수)

모든 생성 파일은 **파일명 끝에 생성 시간**을 포함해야 합니다.

* **포맷**: `{파일명}_{YYYYMMDD_HHMMSS}.{확장자}`
* **예시**:
* `skin_doctor_type_eda_20260117_153000.ipynb`
* `night_clinic_map_20260117_153000.html`



#### 파일 유형별 규칙

* **원본 데이터**: `hospital_info_gangnam_YYYYMMDD_HHMMSS.csv`
* **전처리 데이터**: `processed_skin_clinics_YYYYMMDD_HHMMSS.csv`
* **분석 리포트**: `report_{분석주제}_YYYYMMDD_HHMMSS.md`
* 예: `report_night_operation_20260117_160000.md`


* **시각화**: `{차트유형}_{분석변수}_YYYYMMDD_HHMMSS.png`
* 예: `barplot_doctor_scale_20260117_160000.png`



### 2.2 디렉토리 역할

* `data/raw/`: 공공데이터 원본
* `data/processed/`: 필터링(강남구+피부과) 및 파생변수(전문의여부, 야간진료여부 등) 생성 완료 데이터
* `scripts/`: EDA 및 시각화 파이썬 스크립트
* `reports/`: 분석 결과 마크다운 리포트 및 인사이트 정리

## 3. 기술 스택 (Tech Stack)

* **Data**: `pandas`, `numpy`
* **Visualization**: `matplotlib` (Koreanize 필수), `folium` (지도 시각화)
* **Environment**: VS Code, Jupyter Notebook

## 4. 도메인 로직 및 주의사항 (Domain Logic)

본 프로젝트의 데이터 분석은 아래의 **4가지 핵심 로직**을 엄격히 준수합니다.


### 4.2 전문의 vs 일반의 구분 (Doctor Type)

O2O 플랫폼 내 '신뢰도' 경쟁력 분석을 위한 핵심 지표입니다.

* **전문의 병원 (Specialist)**: `dgsbjt_dgsbjtPrSdrCnt` (전문의 수) **> 0**
* *전략*: 압구정/청담 등 프리미엄 상권 분석 시 활용


* **일반 클리닉 (General)**: `dgsbjt_dgsbjtPrSdrCnt` (전문의 수) **== 0**
* *전략*: 강남역/신논현 등 저가형/이벤트 중심 상권 분석 시 활용



### 4.3 병원 규모 및 유형화 (Scale Typology)

병원 규모에 따른 경쟁 상대를 명확히 하기 위해 클러스터링합니다.

* **Type A (대형/공장형)**: 의사 5인 이상 (`총의사수` 기준) + 직원 다수
* *O2O 전략*: 박리다매, 최저가 이벤트 경쟁


* **Type B (중형/표준형)**: 의사 2~4인
* *O2O 전략*: 특정 시술(리프팅, 여드름 등) 특화


* **Type C (1인/프라이빗)**: 의사 1인
* *O2O 전략*: 대표원장 책임진료, 상담 품질 강조



### 4.4 운영 및 인프라 특성 (Operation & Infra)

* **야간 진료 (Night Shift)**: 직장인 타겟팅 분석
* **야간진료**: 평일 진료 종료(`dtl_trmtMonEnd` 등) **19:00 이후**
* **심야진료**: 평일 진료 종료 **20:00 이후**


* **수술 인프라 (Capability)**: 고단가 시술 가능 여부 파악
* **수술 병행**: `eqp_soprmCnt` (수술실 수) **>= 1** (리프팅/체형교정 타겟)
* **시술 중심**: `eqp_soprmCnt` (수술실 수) **== 0** (레이저/쁘띠 타겟)



### 4.5 결측치 처리 (Null Handling)

* `전문의수`, `수술실수`, `입원실수`의 Null 값은 **0 (없음)**으로 간주하여 처리합니다.
* `진료시간`의 Null 값은 '정보 미제공'으로 분류하여 별도 집계합니다.