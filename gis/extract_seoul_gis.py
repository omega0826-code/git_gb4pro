import shapefile
import os
import shutil
from pathlib import Path

# 경로 설정
SRC_PATH = Path(r'd:\git_gb4pro\gis\BND\gemini_md\BND_SIGUNGU_PG\BND_SIGUNGU_PG.shp')
DST_DIR = Path(r'd:\git_gb4pro\gis\BND\Seoul_SIGUNGU')
DST_DIR.mkdir(parents=True, exist_ok=True)

DST_BASE_NAME = 'Seoul_SIGUNGU'
DST_PATH = DST_DIR / DST_BASE_NAME

print(f"데이터 추출 시작: {SRC_PATH}")

# Shapefile 읽기 (원본 인코딩 CP949 적용)
try:
    with shapefile.Reader(str(SRC_PATH), encoding='cp949') as sf:
        # 새로운 Shapefile 작성을 위한 Writer 생성 (UTF-8 고정)
        w = shapefile.Writer(str(DST_PATH), shapeType=sf.shapeType, encoding='utf-8')
        w.fields = sf.fields[1:] # deletion flag 제외한 필드 정보 복사
        
        count = 0
        for i, shape_rec in enumerate(sf.shapeRecords()):
            sig_cd = shape_rec.record[1]
            if sig_cd.startswith('11'):
                w.record(*shape_rec.record)
                w.shape(shape_rec.shape)
                count += 1
        
        w.close()
        print(f"\n추출 완료: 총 {count}개의 구 데이터가 저장되었습니다 (UTF-8).")

    # 메타데이터 파일 처리 (.prj, .cpg)
    for ext in ['.prj', '.cpg']:
        src_meta = SRC_PATH.with_suffix(ext)
        dst_meta = DST_PATH.with_suffix(ext)
        
        if ext == '.prj' and src_meta.exists():
            shutil.copy(src_meta, dst_meta)
            print(f"  좌표계 파일 복사 완료: {ext}")
        elif ext == '.cpg':
            with open(dst_meta, 'w', encoding='utf-8') as f:
                f.write('UTF-8')
            print(f"  인코딩 파일 생성 완료 (UTF-8): {ext}")

except Exception as e:
    print(f"에러 발생: {e}")
    import traceback
    traceback.print_exc()
