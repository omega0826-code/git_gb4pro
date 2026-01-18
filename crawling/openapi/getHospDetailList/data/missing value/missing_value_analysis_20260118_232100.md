# 병원전체정보 결측치 분석 및 처리 방법 설정

> **분석 대상**: `병원전체정보_20260116_212603.csv`  
> **분석 일시**: 2026-01-18 23:21:00  
> **총 데이터 건수**: 1,153건  
> **총 컬럼 수**: 93개

---

## 1. 결측치 현황 개요

### 1.1 데이터 구조
- **원본 정보**: 기관코드, 병원명, 주소 (3개 컬럼)
- **시설 정보 (eqp_)**: 30개 컬럼
- **진료과목 정보 (dgsbjt_)**: 4개 컬럼
- **의료장비 정보 (medoft_)**: 3개 컬럼
- **식대가산 정보 (foepaddc_)**: 4개 컬럼
- **간호등급 정보 (nursiggrd_)**: 3개 컬럼
- **특수진료 정보 (spcldiag_)**: 2개 컬럼
- **기타인력 정보 (etchst_)**: 5개 컬럼
- **세부정보 (dtl_)**: 28개 컬럼
- **교통정보 (trnsprt_)**: 6개 컬럼

---

## 2. 결측치 분석 결과

### 2.1 결측치 통계 요약

결측치 분석 결과는 다음 명령어로 확인:
```python
import pandas as pd
df = pd.read_csv('병원전체정보_20260116_212603.csv')
missing_info = df.isnull().sum()
missing_pct = (missing_info / len(df) * 100).round(2)
```

### 2.2 결측치 패턴 분류

결측치는 다음과 같은 패턴으로 분류됩니다:

#### A. 높은 결측률 (80% 이상)
- **교통정보 관련**: 대부분의 병원이 교통정보 미제공
- **세부 운영정보**: 응급실 정보, 특정 진료시간 등

#### B. 중간 결측률 (30-80%)
- **특수 시설/서비스**: 특정 의료장비, 특수진료 정보
- **선택적 정보**: 홈페이지, 주차 정보 등

#### C. 낮은 결측률 (30% 미만)
- **필수 정보**: 기관코드, 병원명, 주소, 전화번호
- **기본 시설정보**: 병상수, 의료인력 등

---

## 3. 결측치 처리 방법 설정

### 3.1 처리 원칙

| 원칙 | 설명 |
|------|------|
| **데이터 보존 우선** | 가능한 한 원본 데이터 유지 |
| **의미 기반 처리** | 결측치의 의미를 고려한 처리 |
| **분석 목적 고려** | 향후 분석 목적에 맞는 처리 |
| **투명성 확보** | 처리 내역 문서화 및 추적 가능 |

### 3.2 컬럼별 처리 방법

#### 📋 **카테고리 1: 필수 정보 (결측 불허)**

| 컬럼명 | 처리방법 | 사유 |
|--------|----------|------|
| `원본_기관코드` | **결측 시 데이터 제외** | 고유 식별자 |
| `원본_병원명` | **결측 시 데이터 제외** | 필수 식별 정보 |
| `원본_주소` | **결측 시 데이터 제외** | 위치 정보 필수 |

#### 📊 **카테고리 2: 시설 정보 (eqp_)**

| 컬럼명 | 처리방법 | 대체값 | 사유 |
|--------|----------|--------|------|
| `eqp_hospUrl` | **결측 유지** | `NULL` | 홈페이지 없는 병원 존재 |
| `eqp_telno` | **'정보없음'** | `'정보없음'` | 연락처는 중요하나 일부 미제공 |
| `eqp_stdSickbdCnt` | **0으로 대체** | `0` | 병상 없는 의원급 존재 |
| `eqp_emymCnt` | **0으로 대체** | `0` | 직원 수 미신고 가능 |
| 기타 시설 수치 | **0으로 대체** | `0` | 해당 시설 없음으로 해석 |

#### 🏥 **카테고리 3: 진료과목 정보 (dgsbjt_)**

| 컬럼명 | 처리방법 | 대체값 | 사유 |
|--------|----------|--------|------|
| `dgsbjt_dgsbjtCd` | **결측 유지** | `NULL` | 진료과목 미등록 병원 존재 |
| `dgsbjt_dgsbjtCdNm` | **결측 유지** | `NULL` | 코드와 연동 |
| `dgsbjt_cdiagDrCnt` | **0으로 대체** | `0` | 전문의 없음 |
| `dgsbjt_dgsbjtPrSdrCnt` | **0으로 대체** | `0` | 전문의 없음 |

#### 🔬 **카테고리 4: 의료장비 정보 (medoft_)**

| 컬럼명 | 처리방법 | 대체값 | 사유 |
|--------|----------|--------|------|
| `medoft_oftCd` | **결측 유지** | `NULL` | 장비 없는 병원 존재 |
| `medoft_oftCdNm` | **결측 유지** | `NULL` | 코드와 연동 |
| `medoft_oftCnt` | **0으로 대체** | `0` | 장비 없음 |

#### 🍽️ **카테고리 5: 식대가산 정보 (foepaddc_)**

| 컬럼명 | 처리방법 | 대체값 | 사유 |
|--------|----------|--------|------|
| `foepaddc_calcNopCnt` | **0으로 대체** | `0` | 해당 인력 없음 |
| `foepaddc_gnmAddcYn` | **'N'으로 대체** | `'N'` | 가산 없음 |
| `foepaddc_tyCd` | **결측 유지** | `NULL` | 유형 미해당 |
| `foepaddc_tyCdNm` | **결측 유지** | `NULL` | 코드와 연동 |

#### 👨‍⚕️ **카테고리 6: 간호등급 정보 (nursiggrd_)**

| 컬럼명 | 처리방법 | 대체값 | 사유 |
|--------|----------|--------|------|
| `nursiggrd_careGrd` | **결측 유지** | `NULL` | 등급 미해당 병원 존재 |
| `nursiggrd_tyCd` | **결측 유지** | `NULL` | 유형 미해당 |
| `nursiggrd_tyCdNm` | **결측 유지** | `NULL` | 코드와 연동 |

#### 🏥 **카테고리 7: 특수진료 정보 (spcldiag_)**

| 컬럼명 | 처리방법 | 대체값 | 사유 |
|--------|----------|--------|------|
| `spcldiag_srchCd` | **결측 유지** | `NULL` | 특수진료 미제공 병원 존재 |
| `spcldiag_srchCdNm` | **결측 유지** | `NULL` | 코드와 연동 |

#### 👥 **카테고리 8: 기타인력 정보 (etchst_)**

| 컬럼명 | 처리방법 | 대체값 | 사유 |
|--------|----------|--------|------|
| `etchst_dtlGnlNopCdNm` | **결측 유지** | `NULL` | 해당 인력 없음 |
| `etchst_gnlNopCnt` | **0으로 대체** | `0` | 인력 없음 |
| `etchst_gnlNopDtlCd` | **0으로 대체** | `0` | 코드 없음 |
| `etchst_yadmNm` | **결측 유지** | `NULL` | 병원명과 동일 가능 |
| `etchst_ykiho` | **결측 유지** | `NULL` | 요양기호 중복 |

#### 🕐 **카테고리 9: 세부 운영정보 (dtl_)**

| 컬럼 그룹 | 처리방법 | 대체값 | 사유 |
|-----------|----------|--------|------|
| **응급실 정보** (`dtl_emy*`) | **결측 유지** | `NULL` | 응급실 없는 병원 다수 |
| **진료시간** (`dtl_trmt*`) | **결측 유지** | `NULL` | 미제공 정보 |
| **점심시간** (`dtl_lunch*`) | **결측 유지** | `NULL` | 미제공 정보 |
| **휴무일** (`dtl_noTrmt*`) | **결측 유지** | `NULL` | 미제공 정보 |
| **주차정보** (`dtl_park*`) | **결측 유지** | `NULL` | 주차장 없는 병원 존재 |
| **위치정보** (`dtl_plc*`) | **결측 유지** | `NULL` | 미제공 정보 |
| **진료접수** (`dtl_rcv*`) | **결측 유지** | `NULL` | 미제공 정보 |

#### 🚇 **카테고리 10: 교통정보 (trnsprt_)**

| 컬럼명 | 처리방법 | 대체값 | 사유 |
|--------|----------|--------|------|
| 모든 교통정보 컬럼 | **결측 유지** | `NULL` | 대부분 미제공 (80% 이상) |

---

## 4. 처리 구현 코드

### 4.1 Python 구현 예시

```python
import pandas as pd
import numpy as np

def process_missing_values(df):
    """
    병원 데이터 결측치 처리 함수
    
    Parameters:
    -----------
    df : pandas.DataFrame
        원본 데이터프레임
    
    Returns:
    --------
    pandas.DataFrame
        처리된 데이터프레임
    """
    df_processed = df.copy()
    
    # 1. 필수 정보 결측 시 제외
    essential_cols = ['원본_기관코드', '원본_병원명', '원본_주소']
    df_processed = df_processed.dropna(subset=essential_cols)
    
    # 2. 수치형 컬럼 0으로 대체
    numeric_fill_zero = [
        'eqp_stdSickbdCnt', 'eqp_emymCnt', 'eqp_aduChldSprmCnt',
        'eqp_anvirTrrmSbdCnt', 'eqp_chldSprmCnt', 'eqp_hghrSickbdCnt',
        'eqp_isnrSbdCnt', 'eqp_nbySprmCnt', 'eqp_partumCnt',
        'eqp_permSbdCnt', 'eqp_psydeptClsGnlSbdCnt', 'eqp_psydeptClsHigSbdCnt',
        'eqp_psydeptOpenGnlSbdCnt', 'eqp_psydeptOpenHigSbdCnt', 'eqp_ptrmCnt',
        'eqp_soprmCnt', 'dgsbjt_cdiagDrCnt', 'dgsbjt_dgsbjtPrSdrCnt',
        'medoft_oftCnt', 'foepaddc_calcNopCnt', 'etchst_gnlNopCnt',
        'etchst_gnlNopDtlCd', 'dtl_parkQty'
    ]
    
    for col in numeric_fill_zero:
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].fillna(0)
    
    # 3. Y/N 컬럼 'N'으로 대체
    yn_cols = ['foepaddc_gnmAddcYn', 'dtl_emyDayYn', 'dtl_emyNgtYn', 'dtl_parkXpnsYn']
    for col in yn_cols:
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].fillna('N')
    
    # 4. 전화번호 '정보없음'으로 대체
    if 'eqp_telno' in df_processed.columns:
        df_processed['eqp_telno'] = df_processed['eqp_telno'].fillna('정보없음')
    
    # 5. 나머지는 결측 유지 (NULL)
    
    return df_processed

# 사용 예시
df = pd.read_csv('병원전체정보_20260116_212603.csv')
df_clean = process_missing_values(df)

# 처리 결과 저장
df_clean.to_csv('병원전체정보_결측치처리완료.csv', index=False, encoding='utf-8-sig')
```

### 4.2 처리 전후 비교

```python
# 처리 전 결측치 확인
print("=== 처리 전 ===")
print(df.isnull().sum()[df.isnull().sum() > 0])

# 처리 후 결측치 확인
print("\n=== 처리 후 ===")
print(df_clean.isnull().sum()[df_clean.isnull().sum() > 0])

# 데이터 건수 변화
print(f"\n원본 데이터: {len(df)}건")
print(f"처리 후 데이터: {len(df_clean)}건")
print(f"제외된 데이터: {len(df) - len(df_clean)}건")
```

---

## 5. 주의사항 및 권장사항

### ⚠️ 주의사항

1. **필수 정보 결측 데이터 제외**
   - 기관코드, 병원명, 주소가 없는 데이터는 분석 불가능
   - 제외된 데이터는 별도 로그 파일로 저장 권장

2. **0 대체의 의미**
   - 수치형 컬럼의 0은 "없음"을 의미
   - "미제공"과 "없음"을 구분해야 하는 경우 별도 플래그 컬럼 추가 고려

3. **NULL 유지의 의미**
   - NULL은 "정보 미제공" 또는 "해당 없음"을 의미
   - 분석 시 NULL 처리 방법 명확히 정의 필요

### 💡 권장사항

1. **처리 이력 관리**
   ```python
   # 처리 이력 저장
   processing_log = {
       '처리일시': '2026-01-18 23:21:00',
       '원본파일': '병원전체정보_20260116_212603.csv',
       '원본건수': len(df),
       '처리후건수': len(df_clean),
       '제외건수': len(df) - len(df_clean)
   }
   ```

2. **데이터 품질 검증**
   - 처리 후 데이터 분포 확인
   - 이상치 탐지 및 검증
   - 비즈니스 로직 검증

3. **백업 및 버전 관리**
   - 원본 데이터 백업 필수
   - 처리 버전별 파일 관리
   - 처리 스크립트 버전 관리

---

## 6. 다음 단계

### 6.1 즉시 수행
- [ ] 결측치 처리 스크립트 실행
- [ ] 처리 결과 검증
- [ ] 처리 로그 저장

### 6.2 추가 분석
- [ ] 결측치 패턴 심층 분석
- [ ] 결측치와 병원 유형 간 상관관계 분석
- [ ] 지역별 결측치 분포 분석

### 6.3 데이터 품질 개선
- [ ] 데이터 수집 프로세스 개선 방안 검토
- [ ] 필수 정보 수집률 향상 방안 수립
- [ ] 데이터 검증 규칙 수립

---

## 7. 참고 자료

### 관련 문서
- `병원전체정보_20260116_212603.csv`: 원본 데이터
- `의료기관전체정보_조회_v2.00_260115.py`: 데이터 수집 스크립트

### 데이터 출처
- 건강보험심사평가원 Open API (11개 API 통합)

---

**문서 작성**: 2026-01-18 23:21:00  
**작성자**: Data Analysis System  
**버전**: 1.0
