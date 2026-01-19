"""
마크다운 리포트를 HTML로 변환 (이미지 임베딩)
작성 일시: 2026-01-20 00:40
"""

import base64
import os
from datetime import datetime

# 출력 디렉토리
output_dir = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_step2_260119'
timestamp = '20260120_003156'

# 이미지 파일 경로
img1_path = f'{output_dir}/comparison_overview_{timestamp}.png'
img2_path = f'{output_dir}/district_penetration_rate_{timestamp}.png'

# 이미지를 Base64로 인코딩
def image_to_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

img1_base64 = image_to_base64(img1_path)
img2_base64 = image_to_base64(img2_path)

# HTML 생성
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>강남언니 입점 업체 vs 미입점 업체 비교 분석 결과</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Malgun Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header .meta {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 2em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .section h3 {{
            color: #764ba2;
            font-size: 1.5em;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        .summary-box {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .summary-box h3 {{
            color: #667eea;
            margin-top: 0;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        
        .stat-card .label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-card .subvalue {{
            font-size: 1.1em;
            color: #999;
            margin-top: 5px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        
        tr:hover {{
            background: #f5f7fa;
        }}
        
        .highlight {{
            background: #fff3cd;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        .positive {{
            color: #28a745;
            font-weight: bold;
        }}
        
        .negative {{
            color: #dc3545;
            font-weight: bold;
        }}
        
        .image-container {{
            margin: 30px 0;
            text-align: center;
        }}
        
        .image-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        
        .image-caption {{
            margin-top: 15px;
            font-size: 1.1em;
            color: #666;
            font-style: italic;
        }}
        
        .insight-box {{
            background: #e7f3ff;
            border-left: 5px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }}
        
        .insight-box h4 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .key-findings {{
            background: #fff9e6;
            border-left: 5px solid #ffc107;
            padding: 25px;
            margin: 20px 0;
            border-radius: 8px;
        }}
        
        .key-findings h3 {{
            color: #f57c00;
            margin-top: 0;
        }}
        
        .key-findings ul {{
            margin-left: 20px;
            margin-top: 15px;
        }}
        
        .key-findings li {{
            margin-bottom: 10px;
            font-size: 1.05em;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 강남언니 입점 업체 vs 미입점 업체 비교 분석</h1>
            <div class="meta">
                <p>분석 일시: 2026-01-20 00:32 | 데이터: 병원명 기준 매칭 (188건 입점)</p>
            </div>
        </div>
        
        <div class="content">
            <!-- 분석 결과 요약 -->
            <div class="section">
                <h2>📊 분석 결과 요약</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="label">총 병원 수</div>
                        <div class="value">1,153</div>
                        <div class="subvalue">건</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">입점 업체</div>
                        <div class="value">188</div>
                        <div class="subvalue">16.3%</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">미입점 업체</div>
                        <div class="value">965</div>
                        <div class="subvalue">83.7%</div>
                    </div>
                </div>
            </div>
            
            <!-- Part 1: 입점 업체 특징 -->
            <div class="section">
                <h2>Part 1: 강남언니 입점 업체 특징 분석</h2>
                
                <h3>1.1 기본 프로필</h3>
                <table>
                    <thead>
                        <tr>
                            <th>지표</th>
                            <th>값</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>총 병원 수</td><td><strong>188건</strong></td></tr>
                        <tr><td>평균 병상 수</td><td>0.52개</td></tr>
                        <tr><td>평균 의사 수</td><td>0.84명</td></tr>
                        <tr><td>평균 직원 수</td><td>0.00명</td></tr>
                        <tr><td>평균 수술실 수</td><td><span class="highlight">0.57개</span></td></tr>
                    </tbody>
                </table>
                
                <div class="insight-box">
                    <h4>💡 인사이트</h4>
                    <ul>
                        <li>입점 업체는 대부분 <strong>소규모 클리닉</strong></li>
                        <li>평균 의사 수 0.84명 → <strong>1인 원장 체제 중심</strong></li>
                        <li>평균 수술실 0.57개 → <strong>절반 이상이 수술실 보유</strong></li>
                    </ul>
                </div>
                
                <h3>1.2 의사 유형 분포</h3>
                <table>
                    <thead>
                        <tr>
                            <th>유형</th>
                            <th>병원 수</th>
                            <th>비율</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>일반의</td><td>97건</td><td>51.6%</td></tr>
                        <tr><td>전문의</td><td>91건</td><td><span class="highlight">48.4%</span></td></tr>
                    </tbody>
                </table>
                
                <div class="insight-box">
                    <h4>💡 인사이트</h4>
                    <ul>
                        <li>전문의 vs 일반의 비율이 거의 <strong>1:1</strong></li>
                        <li>전문의 비율(48.4%)이 전체 평균(37.4%)보다 높음</li>
                        <li>강남언니 플랫폼이 <strong>전문의 병원을 선호</strong>하는 경향</li>
                    </ul>
                </div>
                
                <h3>1.3 지역 분포 (TOP 5)</h3>
                <table>
                    <thead>
                        <tr>
                            <th>순위</th>
                            <th>행정동</th>
                            <th>병원 수</th>
                            <th>비율</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>1</td><td><strong>신사동</strong></td><td>68건</td><td><span class="highlight">36.2%</span></td></tr>
                        <tr><td>2</td><td><strong>역삼동</strong></td><td>47건</td><td>25.0%</td></tr>
                        <tr><td>3</td><td><strong>논현동</strong></td><td>44건</td><td>23.4%</td></tr>
                        <tr><td>4</td><td>청담동</td><td>14건</td><td>7.4%</td></tr>
                        <tr><td>5</td><td>삼성동</td><td>8건</td><td>4.3%</td></tr>
                    </tbody>
                </table>
                
                <div class="insight-box">
                    <h4>💡 인사이트</h4>
                    <ul>
                        <li><strong>신사동이 압도적 1위</strong> (36.2%)</li>
                        <li>상위 3개 동(신사동, 역삼동, 논현동)이 <strong>84.6% 차지</strong></li>
                        <li>강남역/신논현 상권에 입점 업체 집중</li>
                    </ul>
                </div>
            </div>
            
            <!-- Part 2: 비교 분석 -->
            <div class="section">
                <h2>Part 2: 입점 vs 미입점 업체 비교 분석</h2>
                
                <h3>2.1 규모 비교</h3>
                <table>
                    <thead>
                        <tr>
                            <th>지표</th>
                            <th>입점</th>
                            <th>미입점</th>
                            <th>차이</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>평균 병상 수</td>
                            <td>0.52개</td>
                            <td>2.42개</td>
                            <td class="negative">-1.90개 (-78.7%)</td>
                        </tr>
                        <tr>
                            <td>평균 의사 수</td>
                            <td>0.84명</td>
                            <td>0.79명</td>
                            <td class="positive">+0.05명 (+6.3%)</td>
                        </tr>
                        <tr>
                            <td>평균 직원 수</td>
                            <td>0.00명</td>
                            <td>0.09명</td>
                            <td class="negative">-0.09명 (-100%)</td>
                        </tr>
                        <tr>
                            <td>평균 수술실 수</td>
                            <td>0.57개</td>
                            <td>0.24개</td>
                            <td class="positive"><strong>+0.33개 (+137.5%)</strong></td>
                        </tr>
                    </tbody>
                </table>
                
                <h3>2.2 전문의 비율 비교</h3>
                <table>
                    <thead>
                        <tr>
                            <th>구분</th>
                            <th>입점</th>
                            <th>미입점</th>
                            <th>차이</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>전문의 비율</td>
                            <td><span class="highlight">48.4%</span></td>
                            <td>35.2%</td>
                            <td class="positive"><strong>+13.2%p</strong></td>
                        </tr>
                    </tbody>
                </table>
                
                <h3>2.3 수술실 보유율 비교</h3>
                <table>
                    <thead>
                        <tr>
                            <th>구분</th>
                            <th>입점</th>
                            <th>미입점</th>
                            <th>차이</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>수술실 보유율</td>
                            <td><span class="highlight">27.1%</span></td>
                            <td>9.3%</td>
                            <td class="positive"><strong>+17.8%p</strong></td>
                        </tr>
                    </tbody>
                </table>
                
                <div class="insight-box">
                    <h4>💡 인사이트</h4>
                    <ul>
                        <li>입점 업체의 수술실 보유율이 <strong>3배 높음</strong></li>
                        <li>수술 인프라가 입점의 <strong>가장 강력한 차별화 요소</strong></li>
                        <li>고단가 시술/수술 제공 능력이 플랫폼 성공의 핵심</li>
                    </ul>
                </div>
            </div>
            
            <!-- 시각화 -->
            <div class="section">
                <h2>📈 시각화 분석</h2>
                
                <div class="image-container">
                    <img src="data:image/png;base64,{img1_base64}" alt="입점 vs 미입점 종합 비교">
                    <div class="image-caption">그림 1. 입점 vs 미입점 업체 종합 비교 (규모, 전문의, 평균 지표, 수술 인프라)</div>
                </div>
                
                <div class="image-container">
                    <img src="data:image/png;base64,{img2_base64}" alt="행정동별 입점률">
                    <div class="image-caption">그림 2. 강남구 행정동별 입점률</div>
                </div>
            </div>
            
            <!-- 핵심 인사이트 -->
            <div class="section">
                <div class="key-findings">
                    <h3>💡 핵심 인사이트</h3>
                    
                    <h4>1. 입점 업체의 특징</h4>
                    <ul>
                        <li><strong>✅ 강점 요소</strong>: 전문의 자격 (48.4%), 수술실 보유 (27.1%), 강남역/신논현 상권 입지</li>
                        <li><strong>📊 규모 특성</strong>: 1인 원장 소규모 클리닉, 무병상 또는 소수 병상, 시술/수술 중심 운영</li>
                    </ul>
                    
                    <h4>2. 입점 성공 요인</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>요인</th>
                                <th>영향력</th>
                                <th>근거</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>수술 인프라</strong></td>
                                <td>⭐⭐⭐</td>
                                <td>입점 업체가 3배 높음 (27.1% vs 9.3%)</td>
                            </tr>
                            <tr>
                                <td><strong>전문의 자격</strong></td>
                                <td>⭐⭐</td>
                                <td>입점 업체가 13.2%p 높음</td>
                            </tr>
                            <tr>
                                <td><strong>입지</strong></td>
                                <td>⭐⭐</td>
                                <td>상위 3개 동이 84.6% 차지</td>
                            </tr>
                            <tr>
                                <td>병원 규모</td>
                                <td>⭐</td>
                                <td>1인 원장도 충분히 입점 가능</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- 전략적 시사점 -->
            <div class="section">
                <h2>🎯 전략적 시사점</h2>
                
                <h3>1. 입점 희망 업체를 위한 가이드</h3>
                <div class="summary-box">
                    <h4><strong>필수 요소</strong></h4>
                    <ul>
                        <li>✅ 수술실 보유 (가장 중요)</li>
                        <li>✅ 전문의 자격 (선호)</li>
                        <li>✅ 강남역/신논현 상권 입지 (유리)</li>
                    </ul>
                    
                    <h4><strong>선택 요소</strong></h4>
                    <ul>
                        <li>병원 규모 (1인 원장도 가능)</li>
                        <li>병상 수 (무병상도 가능)</li>
                    </ul>
                </div>
                
                <h3>2. 플랫폼 확장 전략</h3>
                <div class="summary-box">
                    <h4><strong>타겟 업체</strong></h4>
                    <ol>
                        <li>수술실 보유 + 전문의 병원</li>
                        <li>신사/역삼/논현 외 지역의 우수 병원</li>
                        <li>청담동 프리미엄 병원 (현재 입점률 낮음)</li>
                    </ol>
                    
                    <h4><strong>확장 방향</strong></h4>
                    <ul>
                        <li>수술실 미보유 시술 중심 클리닉 확대</li>
                        <li>일반의 병원 중 우수 업체 발굴</li>
                        <li>저침투 지역 공략 (대치동, 도곡동 등)</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>리포트 작성</strong>: 2026-01-20 00:32 | <strong>분석자</strong>: Data Analysis System | <strong>버전</strong>: 1.0</p>
            <p style="margin-top: 10px;">생성된 파일: comparison_overview_{timestamp}.png, district_penetration_rate_{timestamp}.png</p>
        </div>
    </div>
</body>
</html>
"""

# HTML 파일 저장
output_html = f'{output_dir}/분석결과_리포트_20260120_004000.html'
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML 리포트 생성 완료: {output_html}")
