# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 통합 HTML 리포트 생성
작성일: 2026-02-03
버전: 1.0 (V5.00 가이드라인 반영)
"""

import os
import pandas as pd
from datetime import datetime

def generate_report():
    print("=" * 80)
    print("통합 HTML 리포트 생성 시작...")
    print("=" * 80)
    
    base_path = r"d:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT"
    output_dir = os.path.join(base_path, "06_최종리포트")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 종합 평가 데이터 로드
    final_score_path = os.path.join(base_path, "05_종합평가", "전체_상권_종합점수.csv")
    if not os.path.exists(final_score_path):
        print(f"[ERROR] 종합 평가 결과 파일이 없습니다: {final_score_path}")
        return
        
    df_final = pd.read_csv(final_score_path)
    # 상위 3개 추천
    top_recommendations = ", ".join(df_final.sort_values(by='종합점수', ascending=False)['상권_명'].head(3).tolist())
    
    # HTML 템플릿 (V5.00 가이드라인 기반)
    html_template = f'''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>피부과 입지 분석 리포트</title>
        <style>
            body {{
                font-family: 'Malgun Gothic', 'Noto Sans KR', sans-serif;
                line-height: 1.6;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #FF6B6B;
                border-bottom: 3px solid #FF6B6B;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #4ECDC4;
                margin-top: 30px;
            }}
            .chart {{
                margin: 20px 0;
                text-align: center;
            }}
            .chart img {{
                max-width: 100%;
                height: auto;
                border: 1px solid #ddd;
                border-radius: 4px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #4ECDC4;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .summary {{
                background-color: #FFF9E6;
                padding: 20px;
                border-left: 4px solid #FFEAA7;
                margin: 20px 0;
            }}
            .insight {{
                background-color: #E8F8F5;
                padding: 15px;
                border-left: 4px solid #4ECDC4;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>의원급 피부과 최적 입지 분석 리포트</h1>
            
            <div class="summary">
                <h2>요약 (Executive Summary)</h2>
                <p><strong>분석 기간:</strong> 2022년 1분기 ~ 2024년 4분기</p>
                <p><strong>분석 대상:</strong> 강남 지역 9개 주요 상권</p>
                <p><strong>최종 추천:</strong> {top_recommendations}</p>
            </div>
            
            <h2>1. 경쟁 환경 분석</h2>
            <div class="chart">
                <img src="../01_경쟁환경분석/경쟁밀도_히트맵.png" alt="경쟁 환경 분석">
            </div>
            
            <h2>2. 고객 분석</h2>
            <div class="chart">
                <img src="../02_고객분석/연령성별_매출분포.png" alt="고객 분석">
            </div>
            
            <h2>3. 인구 유동 분석</h2>
            <div class="chart">
                <img src="../03_인구유동분석/인구구조_피라미드.png" alt="인구 유동 분석">
            </div>
            
            <h2>4. 입지 조건 분석</h2>
            <div class="chart">
                <img src="../04_입지조건분석/집객시설_분포.png" alt="입지 조건 분석">
            </div>
            
            <h2>5. 종합 평가</h2>
            <div class="chart">
                <img src="../05_종합평가/종합점수_순위.png" alt="종합 평가">
                <img src="../05_종합평가/4차원_레이더.png" alt="종합 평가 레이더">
            </div>
            
            <h2>6. 상세 데이터</h2>
            {df_final.head(10).to_html(index=False)}
            
            <div class="insight">
                <h3>핵심 인사이트</h3>
                <ul>
                    <li>추천된 상권은 경쟁력, 타겟 고객, 인구 유동, 입지 조건을 종합적으로 고려하여 선정되었습니다.</li>
                    <li>가로수길 및 압구정로데오는 타겟 고객층인 20-40대 여성의 매출 집중도가 매우 높습니다.</li>
                    <li>강남역은 최대 유동인구를 보유하고 있으나 경쟁 강도(HHI)가 높으므로 차별화된 전략이 필요합니다.</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''
    
    report_file = os.path.join(output_dir, "최종리포트.html")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
        
    print(f"[SUCCESS] 통합 리포트 생성 완료: {report_file}")

if __name__ == "__main__":
    generate_report()
