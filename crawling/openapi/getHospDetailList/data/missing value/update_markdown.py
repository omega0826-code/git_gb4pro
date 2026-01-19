import json

# JSON 데이터 로드
with open(r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\missing value\missing_stats.json', 'r', encoding='utf-8') as f:
    stats = json.load(f)

def get_stats(col_name):
    """컬럼명에 대한 통계 정보 반환"""
    if col_name in stats:
        s = stats[col_name]
        return f"(전체: {s['total']:,}건 / 결측: {s['missing']:,}건 / 비율: {s['pct']}%)"
    return "(통계 없음)"

# 테스트
print("=== 통계 정보 테스트 ===")
print(f"원본_기관코드: {get_stats('원본_기관코드')}")
print(f"eqp_hospUrl: {get_stats('eqp_hospUrl')}")
print(f"eqp_telno: {get_stats('eqp_telno')}")
print(f"dgsbjt_dgsbjtCd: {get_stats('dgsbjt_dgsbjtCd')}")
print(f"medoft_oftCd: {get_stats('medoft_oftCd')}")
print(f"foepaddc_calcNopCnt: {get_stats('foepaddc_calcNopCnt')}")
print(f"nursiggrd_careGrd: {get_stats('nursiggrd_careGrd')}")
print(f"spcldiag_srchCd: {get_stats('spcldiag_srchCd')}")
print(f"etchst_dtlGnlNopCdNm: {get_stats('etchst_dtlGnlNopCdNm')}")
print(f"dtl_emyDayYn: {get_stats('dtl_emyDayYn')}")
print(f"trnsprt_arivPlc: {get_stats('trnsprt_arivPlc')}")

print("\n통계 정보 생성 완료!")
