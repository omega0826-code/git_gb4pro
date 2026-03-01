# 강남언니 프로젝트 디렉토리 구조

**프로젝트 코드**: `26_p001_gangnamunni`
**생성일**: 2026-03-01
**설명**: 강남언니 플랫폼 기반 병원 경쟁 및 리뷰 분석 프로젝트

---

## 디렉토리 트리

```
26_p001_gangnamunni/
├── project_rules.md              # 프로젝트 규칙 (네이밍, 구조, 기술스택)
├── directory_structure.md        # 이 문서
│
├── data/                         # 데이터 저장소
│   ├── raw/                      # 원본 데이터 (불변)
│   ├── processed/                # 가공 데이터
│   ├── archive/                  # 아카이브
│   └── hira/                     # HIRA OpenAPI 수집 데이터
│       ├── basis/                # 병원 기본정보 (3개)
│       │   ├── (CSV)서울_강남구_피부과_*.csv
│       │   ├── 서울_강남구_피부과_*.xlsx
│       │   └── 서울_강남구_피부과_*.csv (최신)
│       ├── detail/               # 병원 상세정보 + 결합 데이터
│       │   ├── 병원전체정보_*.csv/md    # 11개 API 통합
│       │   ├── *_geocoded_*.csv        # 지오코딩 버전
│       │   ├── 피부과_병원정보_*.csv    # 피부과 필터
│       │   ├── 병원데이터_결합완료_*.csv # 최종 결합
│       │   ├── 매칭결과_*.md/json       # 매칭 리포트
│       │   ├── merge_hospital_data.py   # 결합 스크립트
│       │   ├── missing_value/           # 결측치 분석
│       │   └── _recycle_bin/            # 이전 버전 보관
│       └── eda/                  # EDA 분석 결과
│           ├── EDA_260116/       # 초기 EDA (16개)
│           ├── EDA_260119/       # 2차 EDA
│           ├── EDA_step2_260119/ # 2단계 심층 분석
│           ├── EDA_260124/       # 피부과 EDA (12개)
│           ├── EDA_20260125_1713/# geocoded EDA
│           ├── EDA260127/        # 최종 EDA (10개)
│           └── missing_value/    # 결측치 분석
│
├── docs/                         # 프로젝트 가이드 문서
│   ├── gangnam_eda_guideline.md
│   ├── hospital crawling_step1_*.md
│   ├── hospital crawling_step2_*.md
│   └── 전국 병의원 및 약국 현황_병합 가이드라인.md
│
├── reports/                      # 분석 리포트
│   ├── analysis/                 # 최종 리포트 (5개)
│   ├── archive/                  # 이전 리포트 보관 (7개)
│   └── errors/                   # 에러 리포트 (2개)
│
└── scripts/                      # 실행 스크립트
    ├── crawling/                 # 강남언니 크롤링 (4개)
    │   ├── gangnam_crawling_*.py           # 기본 크롤링
    │   ├── gangnam_hospitals_detail_*.py   # 상세정보 크롤링
    │   ├── *_resume.py                     # 중단 재개
    │   └── retry_crawling_html.py          # HTML 재시도
    ├── etl/                      # 데이터 가공 (5개)
    │   ├── add_address_columns.py          # 주소 파싱
    │   ├── extract_seoul_hospitals.py      # 서울 필터링
    │   ├── filter_hospitals_seoul_skin.py  # 피부과 필터
    │   └── extract_filtered_reviews*.py    # 리뷰 추출
    └── eda/                      # 탐색적 분석 (1개)
        └── eda_reviews_final.py            # 리뷰 EDA
```

## 관련 범용 도구

| 도구         | 경로                     | 설명                              |
| ------------ | ------------------------ | --------------------------------- |
| HIRA OpenAPI | `crawling/hira_openapi/` | 병원정보 수집 범용 도구 (1·2단계) |

## 데이터 파이프라인

```
1. crawling/hira_openapi → 병원 기본·상세정보 수집 (범용)
2. scripts/crawling/     → 강남언니 리뷰·상세 크롤링 (전용)
3. scripts/etl/          → 주소 파싱, 필터링, 리뷰 매칭
4. scripts/eda/          → 리뷰 EDA 분석
5. data/hira/            → HIRA 수집 결과 보관
6. reports/              → 분석 결과 리포트
```
