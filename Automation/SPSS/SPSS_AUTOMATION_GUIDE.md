# SPSS Guideline CSV → Syntax 자동 변환 가이드

## 개요

`guideline_to_spss_syntax.py`는 설문조사 Column Guideline CSV 파일을 SPSS `VARIABLE LABELS` / `VALUE LABELS` syntax로 자동 변환하는 범용 Python 스크립트입니다.

## 빠른 시작

```bash
# 기본 사용 (md + sps 모두 생성)
python guideline_to_spss_syntax.py -g "가이드라인.csv" -r "원본데이터.csv"

# 마크다운만 생성
python guideline_to_spss_syntax.py -g "가이드라인.csv" -r "원본데이터.csv" -f md

# 제목 지정
python guideline_to_spss_syntax.py -g "가이드라인.csv" -r "원본데이터.csv" -t "프로젝트명"
```

## CLI 옵션

| 옵션          | 단축 | 필수 | 기본값          | 설명                                   |
| ------------- | ---- | ---- | --------------- | -------------------------------------- |
| `--guideline` | `-g` | ✅    | -               | 가이드라인 CSV 파일 경로               |
| `--rawdata`   | `-r` | ❌    | -               | raw data CSV (시스템 변수 자동 라벨용) |
| `--output`    | `-o` | ❌    | 가이드라인 폴더 | 출력 파일 경로 (확장자 제외)           |
| `--format`    | `-f` | ❌    | `both`          | 출력 형식: `md`, `sps`, `both`         |
| `--encoding`  | `-e` | ❌    | `utf-8-sig`     | CSV 인코딩                             |
| `--title`     | `-t` | ❌    | -               | 문서 제목                              |

## 가이드라인 CSV 포맷 규격

스크립트가 인식하는 CSV 구조:

| 열  | 이름          | 설명                               |
| --- | ------------- | ---------------------------------- |
| 1   | QtnType       | 문항 유형 코드 (11, 13, 21, 51 등) |
| 2   | 문항/보기번호 | 변수명 또는 보기 번호              |
| 3   | 내용          | 변수 라벨 또는 보기 내용           |
| 4   | VALUE LABELS  | SPSS syntax 단편 (참고용)          |

**규칙:**
- QtnType + 변수명(문자 포함) → 새 변수 정의
- QtnType 없음 + 숫자 → 직전 변수의 값 라벨
- `TO` 표현 지원 (예: `A5_1 TO A5_6`)
- `&amp;` → `&` 자동 디코딩
- 마지막 `EXECUTE.` / `CACHE.` 행 자동 무시

## 자동 처리 기능

1. **시스템 변수 자동 라벨**: idx, grpid, resid, browser 등 공통 변수에 기본 라벨 부여
2. **_etc 변수 자동 라벨**: `SQ1_10_etc` → "SQ1 기타 응답"
3. **TO 범위 전파**: `A5_1 TO A5_6` → A5_2~A5_6에 해당 보기 내용을 라벨로 사용
4. **값 라벨 그룹핑**: 동일 패턴 자동 감지 후 그룹 출력
5. **HTML 엔티티 디코딩**: `&amp;` → `&` 자동 변환

## 향후 업데이트 로드맵

| 버전 | 기능                                          | 상태   |
| ---- | --------------------------------------------- | ------ |
| V1.0 | CSV → VARIABLE LABELS + VALUE LABELS (md/sps) | ✅ 완료 |
| V1.1 | 시스템 변수 사전 확장                         | 📋 계획 |
| V2.0 | 역방향 검증 (syntax ↔ raw data 불일치 리포트) | 📋 계획 |
| V2.1 | 변수 요약 테이블 자동 생성                    | ✅ 완료 |
| V3.0 | SPSS 직접 실행 (savReaderWriter 연동)         | 📋 계획 |
