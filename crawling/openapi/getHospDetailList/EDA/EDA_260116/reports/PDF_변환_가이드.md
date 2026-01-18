# EDA 리포트 PDF 변환 가이드

**생성일시**: 2026-01-16 01:20:00

---

## 📄 생성된 파일

### HTML 리포트 (PDF 인쇄용)
- **파일**: [`eda_report_20260116_011000.html`](file:///d:/git_gb4pro/crawling/openapi/getHospDetailList/EDA/reports/eda_report_20260116_011000.html)
- **크기**: 825 KB
- **특징**: 
  - 모든 시각화 이미지가 Base64로 임베딩되어 단일 파일로 배포 가능
  - 브라우저에서 바로 열람 가능
  - 인쇄 최적화 CSS 스타일 적용

---

## 🖨️ PDF로 변환하는 방법

### 방법 1: 브라우저에서 직접 PDF 저장 (권장)

1. **HTML 파일 열기**
   - `d:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\reports\eda_report_20260116_011000.html` 파일을 더블클릭
   - 또는 브라우저(Chrome, Edge 등)로 드래그 앤 드롭

2. **인쇄 대화상자 열기**
   - `Ctrl + P` 단축키 누르기
   - 또는 브라우저 메뉴 → 인쇄

3. **PDF로 저장 설정**
   - **대상**: "PDF로 저장" 선택
   - **레이아웃**: 세로
   - **용지 크기**: A4
   - **여백**: 기본값
   - **배경 그래픽**: 체크 (차트 색상 유지)

4. **저장**
   - 파일명: `eda_report_20260116_011000.pdf`
   - 저장 위치: `d:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\reports\`
   - "저장" 버튼 클릭

### 방법 2: wkhtmltopdf 설치 후 자동 변환

**wkhtmltopdf 설치**:
1. https://wkhtmltopdf.org/downloads.html 접속
2. Windows 버전 다운로드 및 설치
3. 환경 변수 PATH에 wkhtmltopdf 경로 추가

**스크립트 실행**:
```bash
cd d:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\scripts
python convert_to_pdf_pdfkit.py
```

---

## 📊 HTML 리포트 내용

### 포함된 섹션
1. **데이터 개요** - 기본 정보, API별 구성
2. **데이터 품질 분석** - 결측치 현황, 무결성
3. **단변량 분석** - 6개 주요 변수 분석
4. **주요 인사이트** - 데이터 품질, 비즈니스, 개선 제안
5. **분석 요약** - 발견사항, 활용 방안

### 포함된 시각화 (7개)
1. 결측치 히트맵
2. 병원 종별 분포
3. 시군구별 분포
4. 설립연도 분포
5. 진료과목 분포
6. 주차 정보 분석
7. 진료시간 패턴

---

## 💡 참고사항

### HTML 파일 특징
- **이미지 임베딩**: 모든 차트가 Base64로 인코딩되어 HTML 파일에 포함
- **단일 파일**: 추가 파일 없이 HTML 파일 하나만으로 완전한 리포트
- **반응형 디자인**: 화면 크기에 따라 최적화된 레이아웃
- **인쇄 최적화**: PDF 변환 시 페이지 나눔 최적화

### PDF 변환 시 주의사항
- **배경 그래픽 활성화**: 차트 색상이 제대로 표시되도록 설정
- **여백 설정**: 기본 여백 사용 권장 (2cm)
- **용지 크기**: A4 권장

---

**작성일시**: 2026-01-16 01:20:00  
**HTML 파일**: [eda_report_20260116_011000.html](file:///d:/git_gb4pro/crawling/openapi/getHospDetailList/EDA/reports/eda_report_20260116_011000.html)
