# EDA 라이브러리 설치 가이드

본 프로젝트의 EDA를 수행하기 위해 필요한 Python 라이브러리 설치 방법입니다.

## 1. 필수 라이브러리
- **pandas**: 데이터 처리 및 분석
- **matplotlib**: 기본 시각화
- **seaborn**: 고급 시각화
- **tabulate**: 마크다운 테이블 출력 지원

## 2. 텍스트 분석 라이브러리
- **kiwipiepy**: 한국어 형태소 분석 (속도 빠름, 정확도 높음)
- **wordcloud**: 워드클라우드 시각화

## 3. 설치 명령어
```bash
pip install pandas matplotlib seaborn tabulate kiwipiepy wordcloud
```

## 4. 트러블슈팅
- **kiwipiepy 설치 에러:** Windows 환경에서 Microsoft Visual C++ 14.0 이상이 필요할 수 있습니다. Visual Studio Build Tools를 설치해야 합니다.
- **WordCloud 설치 에러:** 마찬가지로 C++ 컴파일 환경이 필요할 수 있습니다.
- **ImportError (DLL load failed):** 특정 라이브러리 버전 충돌 시 발생할 수 있습니다. 가상환경을 새로 만들어서 설치하는 것을 권장합니다.
