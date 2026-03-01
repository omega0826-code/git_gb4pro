# 📊 PPT Automation

> 통계표 기반 PPTX 편집 가능 차트 자동 생성 도구

## 개요

Excel 통계표에서 데이터를 추출하여 PowerPoint 네이티브 차트(편집 가능)를 자동 생성합니다.

### 지원 차트 유형
| 유형        | 용도             |
| ----------- | ---------------- |
| 수평 막대   | 항목별 비율 비교 |
| 파이 / 도넛 | 구성비           |
| 레이더      | 다항목 균형 비교 |
| 누적 막대   | 그룹별 교차 비교 |

---

## 빠른 시작

### 1. 설치
```bash
pip install -r scripts/requirements.txt
```

### 2. 설정
프로젝트별 설정 파일 작성 (`examples/ulsan_config.py` 참조):
```python
from create_chart_pptx import Cfg

XLSX = r"경로/데이터파일.xlsx"
SHEET = "Sheet1"

TABLES = [
    Cfg(1, "표 제목", total_row=3, name_row=4, chart="pie"),
    Cfg(2, "표 제목2", total_row=21, name_row=19, chart="hbar"),
    # ...
]
```

### 3. 실행
```bash
python scripts/create_chart_pptx.py --config examples/ulsan_config.py
```
또는 스크립트 내 직접 경로 수정 후:
```bash
python scripts/create_chart_pptx.py
```

### 4. 출력
- `프로젝트_차트_PPT_YYMMDD_HHMM.pptx`
- 무결성 자동 검증 포함

---

## 폴더 구조

```
PPT Automation/
├── README.md                          ← 이 파일
├── scripts/
│   ├── create_chart_pptx.py           # 범용 차트 생성 스크립트
│   └── requirements.txt               # 의존성
├── docs/
│   ├── design/
│   │   ├── chart_design_master.md     # 디자인 총괄 가이드라인
│   │   └── themes/
│   │       ├── white_clean.md         # 흰 배경 테마 (기본)
│   │       └── dark_premium.md        # 다크 테마
│   ├── chart_dev_manual.md            # 개발 매뉴얼
│   ├── chart_user_manual.md           # 사용 매뉴얼
│   ├── chart_error_report.md          # 오류 리포트
│   └── changelog.md                   # 변경 이력
└── examples/
    └── ulsan_config.py                # 울산 프로젝트 설정 예시
```

---

## 테마

현재 2개 테마 포함:
- **White Clean** — 흰 배경, 검정 라벨 (워드 삽입용, 기본)
- **Dark Premium** — 진남색 배경, 흰 라벨 (프레젠테이션용)

새 테마: `docs/design/themes/`에 파일 추가 → `Theme` 클래스 값만 교체

---

## 문서

| 문서                                                    | 설명                               |
| ------------------------------------------------------- | ---------------------------------- |
| [디자인 가이드라인](docs/design/chart_design_master.md) | 차트 유형, 레이아웃, 라벨, 축 규칙 |
| [개발 매뉴얼](docs/chart_dev_manual.md)                 | 코드 구조, API, 확장 방법          |
| [사용 매뉴얼](docs/chart_user_manual.md)                | 실행, 편집, 체크리스트             |
| [오류 리포트](docs/chart_error_report.md)               | 과거 오류 이력 + 교훈              |
| [변경 이력](docs/changelog.md)                          | 버전별 변경 기록                   |
