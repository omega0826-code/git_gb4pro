# 분석 결과 마크다운 → HTML 변환 가이드라인

> **목적**: 데이터 분석 결과 리포트를 시각화된 HTML 파일로 변환  
> **작성일**: 2026-01-20  
> **버전**: 1.0

---

## 📋 목차

1. [기본 원칙](#기본-원칙)
2. [HTML 구조](#html-구조)
3. [스타일링 가이드](#스타일링-가이드)
4. [이미지 처리](#이미지-처리)
5. [컴포넌트 패턴](#컴포넌트-패턴)
6. [구현 예제](#구현-예제)
7. [체크리스트](#체크리스트)

---

## 기본 원칙

### 1. 단일 파일 원칙
- **모든 리소스를 하나의 HTML 파일에 포함**
- 이미지는 Base64로 인코딩하여 임베딩
- CSS는 `<style>` 태그 내부에 포함
- JavaScript는 `<script>` 태그 내부에 포함 (필요시)

**장점**:
- 파일 공유 용이
- 외부 의존성 없음
- 오프라인 열람 가능

### 2. 반응형 디자인
- 모바일, 태블릿, 데스크톱 모두 지원
- `@media` 쿼리 활용
- 유연한 그리드 레이아웃

### 3. 인쇄 최적화
- `@media print` 스타일 정의
- 페이지 브레이크 고려
- 불필요한 장식 요소 제거

### 4. 접근성
- 시맨틱 HTML 사용
- 적절한 색상 대비
- 명확한 폰트 크기

---

## HTML 구조

### 기본 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[리포트 제목]</title>
    <style>
        /* CSS 스타일 */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <!-- 헤더 -->
        </div>
        
        <div class="content">
            <!-- 본문 -->
        </div>
        
        <div class="footer">
            <!-- 푸터 -->
        </div>
    </div>
</body>
</html>
```

### 섹션 구조

```html
<div class="section">
    <h2>섹션 제목</h2>
    
    <div class="subsection">
        <h3>하위 섹션</h3>
        <!-- 내용 -->
    </div>
</div>
```

---

## 스타일링 가이드

### 1. 색상 팔레트

```css
:root {
    /* 주요 색상 */
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    
    /* 배경 색상 */
    --bg-gradient-start: #667eea;
    --bg-gradient-end: #764ba2;
    
    /* 텍스트 색상 */
    --text-primary: #333;
    --text-secondary: #666;
    --text-light: #999;
    
    /* 상태 색상 */
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
    
    /* 배경 색상 */
    --bg-light: #f8f9fa;
    --bg-highlight: #fff3cd;
    --bg-insight: #e7f3ff;
}
```

### 2. 타이포그래피

```css
body {
    font-family: 'Malgun Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: var(--text-primary);
}

h1 { font-size: 2.5em; font-weight: 700; }
h2 { font-size: 2.0em; font-weight: 600; }
h3 { font-size: 1.5em; font-weight: 600; }
h4 { font-size: 1.2em; font-weight: 600; }
```

### 3. 레이아웃

```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.section {
    margin-bottom: 50px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}
```

---

## 이미지 처리

### 1. Base64 인코딩

```python
import base64

def image_to_base64(image_path):
    """이미지를 Base64로 인코딩"""
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# 사용 예
img_base64 = image_to_base64('chart.png')
```

### 2. HTML 임베딩

```html
<img src="data:image/png;base64,{img_base64}" alt="차트 설명">
```

### 3. 이미지 컨테이너

```html
<div class="image-container">
    <img src="data:image/png;base64,{img_base64}" alt="차트">
    <div class="image-caption">그림 1. 차트 설명</div>
</div>
```

```css
.image-container {
    margin: 30px 0;
    text-align: center;
}

.image-container img {
    max-width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.image-caption {
    margin-top: 15px;
    font-size: 1.1em;
    color: #666;
    font-style: italic;
}
```

---

## 컴포넌트 패턴

### 1. 통계 카드

```html
<div class="stats-grid">
    <div class="stat-card">
        <div class="label">총 병원 수</div>
        <div class="value">1,153</div>
        <div class="subvalue">건</div>
    </div>
</div>
```

```css
.stat-card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.stat-card .value {
    font-size: 2.5em;
    font-weight: bold;
    color: var(--primary-color);
}
```

### 2. 테이블

```html
<table>
    <thead>
        <tr>
            <th>항목</th>
            <th>값</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>데이터 1</td>
            <td>100</td>
        </tr>
    </tbody>
</table>
```

```css
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-radius: 8px;
    overflow: hidden;
}

th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    text-align: left;
}

td {
    padding: 12px 15px;
    border-bottom: 1px solid #eee;
}

tr:hover {
    background: #f5f7fa;
}
```

### 3. 인사이트 박스

```html
<div class="insight-box">
    <h4>💡 인사이트</h4>
    <ul>
        <li>주요 발견사항 1</li>
        <li>주요 발견사항 2</li>
    </ul>
</div>
```

```css
.insight-box {
    background: #e7f3ff;
    border-left: 5px solid var(--primary-color);
    padding: 20px;
    margin: 20px 0;
    border-radius: 8px;
}

.insight-box h4 {
    color: var(--primary-color);
    margin-bottom: 10px;
}
```

### 4. 요약 박스

```html
<div class="summary-box">
    <h3>요약</h3>
    <p>요약 내용...</p>
</div>
```

```css
.summary-box {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 30px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
```

### 5. 핵심 발견사항

```html
<div class="key-findings">
    <h3>💡 핵심 인사이트</h3>
    <ul>
        <li>발견사항 1</li>
        <li>발견사항 2</li>
    </ul>
</div>
```

```css
.key-findings {
    background: #fff9e6;
    border-left: 5px solid #ffc107;
    padding: 25px;
    margin: 20px 0;
    border-radius: 8px;
}
```

---

## 구현 예제

### Python 스크립트 템플릿

```python
import base64
import os
from datetime import datetime

def create_html_report(md_file, output_html, images=[]):
    """
    마크다운 리포트를 HTML로 변환
    
    Args:
        md_file: 마크다운 파일 경로
        output_html: 출력 HTML 파일 경로
        images: 임베딩할 이미지 파일 경로 리스트
    """
    
    # 1. 이미지를 Base64로 인코딩
    img_base64_list = []
    for img_path in images:
        with open(img_path, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
            img_base64_list.append(img_base64)
    
    # 2. HTML 템플릿 생성
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>분석 결과 리포트</title>
    <style>
        /* CSS 스타일 */
        {get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>분석 결과 리포트</h1>
            <div class="meta">
                <p>작성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
        </div>
        
        <div class="content">
            <!-- 본문 내용 -->
            {generate_content()}
            
            <!-- 이미지 -->
            {generate_images(img_base64_list)}
        </div>
        
        <div class="footer">
            <p>리포트 작성: {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 3. HTML 파일 저장
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML 리포트 생성 완료: {output_html}")

def get_css_styles():
    """CSS 스타일 반환"""
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; }
        /* 추가 스타일... */
    """

def generate_content():
    """본문 내용 생성"""
    return """
        <div class="section">
            <h2>분석 결과</h2>
            <!-- 내용 -->
        </div>
    """

def generate_images(img_list):
    """이미지 HTML 생성"""
    html = ""
    for i, img_base64 in enumerate(img_list, 1):
        html += f"""
        <div class="image-container">
            <img src="data:image/png;base64,{img_base64}" alt="그림 {i}">
            <div class="image-caption">그림 {i}. 설명</div>
        </div>
        """
    return html

# 사용 예
if __name__ == "__main__":
    create_html_report(
        md_file='report.md',
        output_html='report.html',
        images=['chart1.png', 'chart2.png']
    )
```

---

## 체크리스트

### 변환 전 확인사항

- [ ] 마크다운 파일 존재 확인
- [ ] 이미지 파일 경로 확인
- [ ] 출력 디렉토리 존재 확인

### HTML 생성 시 확인사항

- [ ] 모든 이미지가 Base64로 인코딩되었는가?
- [ ] CSS가 `<style>` 태그 내부에 포함되었는가?
- [ ] 한글 인코딩이 UTF-8로 설정되었는가?
- [ ] 반응형 디자인이 적용되었는가?

### 생성 후 확인사항

- [ ] 브라우저에서 정상 렌더링되는가?
- [ ] 모든 이미지가 표시되는가?
- [ ] 모바일에서 정상 표시되는가?
- [ ] 인쇄 시 레이아웃이 깨지지 않는가?
- [ ] 파일 크기가 적절한가? (일반적으로 5MB 이하)

### 품질 확인

- [ ] 색상 대비가 충분한가?
- [ ] 폰트 크기가 읽기 편한가?
- [ ] 섹션 구분이 명확한가?
- [ ] 테이블이 정렬되어 있는가?
- [ ] 링크가 작동하는가? (있는 경우)

---

## 고급 기능

### 1. 목차 자동 생성

```javascript
<script>
// 목차 자동 생성
document.addEventListener('DOMContentLoaded', function() {
    const toc = document.getElementById('toc');
    const headings = document.querySelectorAll('h2, h3');
    
    headings.forEach((heading, index) => {
        heading.id = `section-${index}`;
        const link = document.createElement('a');
        link.href = `#section-${index}`;
        link.textContent = heading.textContent;
        toc.appendChild(link);
    });
});
</script>
```

### 2. 인터랙티브 차트

```html
<!-- Chart.js 사용 예 -->
<canvas id="myChart"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: { /* 데이터 */ }
    });
</script>
```

### 3. 다크 모드

```css
@media (prefers-color-scheme: dark) {
    body {
        background: #1a1a1a;
        color: #e0e0e0;
    }
    
    .container {
        background: #2d2d2d;
    }
}
```

---

## 참고 자료

### 유용한 라이브러리

- **Chart.js**: 차트 생성
- **Marked.js**: 마크다운 파싱
- **Prism.js**: 코드 하이라이팅
- **html2pdf.js**: PDF 변환

### 온라인 도구

- **Base64 Image Encoder**: https://www.base64-image.de/
- **CSS Gradient Generator**: https://cssgradient.io/
- **Color Palette Generator**: https://coolors.co/

---

**작성**: 2026-01-20  
**버전**: 1.0  
**라이선스**: MIT
