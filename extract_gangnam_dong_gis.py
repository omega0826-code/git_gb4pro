import shapefile
import os
import shutil
from pathlib import Path

# 경로 설정
SRC_PATH = Path(r'd:\git_gb4pro\gis\BND_ADM_DONG_PG\BND_ADM_DONG_PG.shp')
DST_DIR = Path(r'd:\git_gb4pro\gis\BND_ADM_DONG_PG\Gangnam_ADM_DONG')
DST_DIR.mkdir(parents=True, exist_ok=True)

DST_BASE_NAME = 'Gangnam_ADM_DONG'
DST_PATH = DST_DIR / DST_BASE_NAME

print(f"강남구 행정동 추출 시작: {SRC_PATH}")

# Shapefile 읽기 (원본 인코딩 CP949 적용)
try:
    with shapefile.Reader(str(SRC_PATH), encoding='cp949') as sf:
        # 새로운 Shapefile 작성을 위한 Writer 생성 (UTF-8 고정)
        w = shapefile.Writer(str(DST_PATH), shapeType=sf.shapeType, encoding='utf-8')
        w.fields = sf.fields[1:] # deletion flag 제외한 필드 정보 복사
        
        count = 0
        for i, shape_rec in enumerate(sf.shapeRecords()):
            # ADM_CD 컬럼 위치 확인 (fields 리스트의 첫 번째는 DeletionFlag이므로 인덱스 1이 ADM_CD)
            adm_cd = shape_rec.record[1]
            
            # 강남구 코드가 '11230'으로 시작하는 경우만 추출 (본 데이터셋 특성)
            if adm_cd.startswith('11230'):
                w.record(*shape_rec.record)
                w.shape(shape_rec.shape)
                count += 1
                if count <= 5:
                    print(f"  발견: {shape_rec.record[2]} ({adm_cd})")
        
        w.close()
        print(f"\n추출 완료: 총 {count}개의 행정동 데이터가 저장되었습니다 (UTF-8).")

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
