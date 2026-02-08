# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 통합 HTML 리포트 생성
작성일: 2026-02-03
버전: 5.01
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
        
    df_final = pd.read_csv(final_score_path, encoding='utf-8-sig')
    # 상위 3개 추천
    top_3 = df_final.head(3)['상권_명'].tolist()
    top_recommendations = ", ".join(top_3)
    
    # HTML 템플릿
    html_template = f'''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>피부과 입지 분석 리포트</title>
        <style>
            body {{ font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; max-width: 1000px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; }}
            .container {{ background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1 {{ color: #e74c3c; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; }}
            h2 {{ color: #2c3e50; border-left: 5px solid #3498db; padding-left: 10px; margin-top: 40px; }}
            .summary {{ background: #fff3f3; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
            .recommendation {{ font-size: 1.5em; color: #c0392b; font-weight: bold; }}
            .chart-box {{ text-align: center; margin: 20px 0; }}
            .chart-box img {{ max-width: 90%; border: 1px solid #eee; border-radius: 8px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
            th {{ background: #3498db; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>의원급 피부과 최적 입지 분석 리포트</h1>
            
            <div class="summary">
                <h2>필수 요약</h2>
                <p><strong>분석 일시:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                <p><strong>최종 추천 상권:</strong> <span class="recommendation">{top_recommendations}</span></p>
            </div>
            
            <h2>1. 경쟁 환경 분석</h2>
            <div class="chart-box">
                <img src="../01_경쟁환경분석/경쟁밀도_히트맵.png">
                <p>상권별 피부과 의원 분포 상세</p>
            </div>
            
            <h2>2. 고객 수요 분석</h2>
            <div class="chart-box">
                <img src="../02_고객분석/연령성별_매출분포.png">
                <p>타겟 고객(20-40대 여성) 매출 밀집도</p>
            </div>
            
            <h2>3. 인구 유동 분석</h2>
            <div class="chart-box">
                <img src="../03_인구유동분석/인구유동_분석결과.png">
                <p>상주 및 직장 인구 구조 비교</p>
            </div>
            
            <h2>4. 입지 조건 분석</h2>
            <div class="chart-box">
                <img src="../04_입지조건분석/집객시설_분포.png">
                <p>주요 집객시설 분포 현황</p>
            </div>
            
            <h2>5. 종합 평가 결과</h2>
            <div class="chart-box">
                <img src="../05_종합평가/종합점수_순위.png">
            </div>
            
            <h2>6. 상권별 종합 지표 데이터</h2>
            {df_final.to_html(index=False, classes='table')}
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
