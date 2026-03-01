# -*- coding: utf-8 -*-
"""
SPSS Guideline CSV → SPSS Syntax 범용 변환 스크립트
====================================================
Column Guideline CSV 파일을 읽어 SPSS VARIABLE LABELS / VALUE LABELS syntax를
마크다운(.md) 및 SPSS syntax(.sps) 형식으로 자동 생성합니다.

사용법:
    python guideline_to_spss_syntax.py --guideline <guideline.csv> [옵션]

Version: 1.0
"""

import csv
import re
import html
import argparse
import os
from collections import OrderedDict
from typing import Optional

# ──────────────────────────────────────────────
# 시스템 변수 기본 라벨 사전
# ──────────────────────────────────────────────
SYSTEM_VAR_LABELS = {
    "idx": "응답 인덱스",
    "grpid": "그룹 ID",
    "resid": "응답자 고유번호",
    "onpage": "페이지 유형",
    "fwid": "포워드 ID",
    "mobileaccess": "모바일 접속 여부",
    "browser": "브라우저",
    "st_date": "조사 시작일시",
    "reg_date": "등록일시",
    "total_time": "총 소요시간(분)",
    "rtpage": "응답 페이지수",
}


# ──────────────────────────────────────────────
# CSV 파싱 엔진
# ──────────────────────────────────────────────
def clean_label(text: str) -> str:
    """라벨 텍스트 정리: HTML 엔티티 디코딩, 줄바꿈 제거, 앞뒤 공백 제거."""
    text = html.unescape(text)
    text = text.replace("\\n", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_guideline_csv(filepath: str, encoding: str = "utf-8-sig") -> dict:
    """
    가이드라인 CSV를 파싱하여 구조화된 딕셔너리를 반환합니다.

    Returns:
        {
            "variables": OrderedDict {
                변수명: {
                    "label": str,
                    "qtn_type": str,
                    "values": OrderedDict { 값번호: 라벨 }
                }
            }
        }
    """
    variables = OrderedDict()
    current_var = None
    current_var_names = []  # TO 표현 시 여러 변수명

    with open(filepath, "r", encoding=encoding) as f:
        reader = csv.reader(f)
        header = next(reader)  # 헤더 건너뜀

        for row in reader:
            if len(row) < 3:
                continue

            qtn_type = row[0].strip()
            col2 = row[1].strip()
            content = row[2].strip() if len(row) > 2 else ""

            # 마지막 EXECUTE/CACHE 행 무시
            if not qtn_type and not col2 and not content:
                continue
            if content in ("", ) and len(row) > 3:
                val_label_col = row[3].strip() if len(row) > 3 else ""
                if val_label_col in ("EXECUTE.", "CACHE."):
                    continue

            # 변수 정의 행: QtnType이 있고, col2가 변수명(문자 포함)
            if qtn_type and col2 and re.search(r"[A-Za-z]", col2):
                label = clean_label(content.strip('"'))

                # TO 범위 표현 처리 (예: "A5_1 TO A5_6")
                if " TO " in col2:
                    parts = col2.split(" TO ")
                    base_var = parts[0].strip()
                    current_var = base_var
                    current_var_names = [base_var]  # TO 범위의 대표 변수

                    # 일단 대표 변수만 등록
                    if base_var not in variables:
                        variables[base_var] = {
                            "label": label,
                            "qtn_type": qtn_type,
                            "values": OrderedDict(),
                            "to_range": col2,  # 원본 범위 보존
                        }
                else:
                    current_var = col2
                    current_var_names = [col2]
                    if col2 not in variables:
                        variables[col2] = {
                            "label": label,
                            "qtn_type": qtn_type,
                            "values": OrderedDict(),
                        }
                    else:
                        # 이미 존재하면 라벨만 업데이트
                        variables[col2]["label"] = label

            # 값 라벨 행: QtnType이 비어있고, col2가 숫자
            elif not qtn_type and col2 and re.match(r"^\d+$", col2):
                if current_var and current_var in variables:
                    value_label = clean_label(content.strip('"'))
                    variables[current_var]["values"][int(col2)] = value_label

    return {"variables": variables}


# ──────────────────────────────────────────────
# Raw Data 헤더 매칭
# ──────────────────────────────────────────────
def read_raw_data_headers(filepath: str, encoding: str = "utf-8-sig") -> list:
    """raw data CSV의 첫 번째 행(헤더)에서 변수명 목록을 추출합니다."""
    with open(filepath, "r", encoding=encoding) as f:
        reader = csv.reader(f)
        headers = next(reader)
    return [h.strip() for h in headers]


def _build_to_range_map(guideline_vars: dict) -> dict:
    """
    TO 범위 변수 매핑 테이블을 구축합니다.
    예: "A5_1 TO A5_6" → A5_1이 대표 변수, A5_2~A5_6은 같은 라벨/값을 공유
    반환: { 접두사: (대표변수명, 시작번호, 끝번호) }
    """
    to_map = {}
    for var_name, info in guideline_vars.items():
        to_range = info.get("to_range", "")
        if not to_range or " TO " not in to_range:
            continue
        parts = to_range.split(" TO ")
        start_var = parts[0].strip()
        end_var = parts[1].strip()

        # 접두사와 번호 추출 (예: A5_1 → prefix="A5_", num=1)
        start_match = re.match(r"^(.+?)(\d+)$", start_var)
        end_match = re.match(r"^(.+?)(\d+)$", end_var)
        if start_match and end_match:
            prefix = start_match.group(1)
            start_num = int(start_match.group(2))
            end_num = int(end_match.group(2))
            to_map[prefix] = (var_name, start_num, end_num)

    return to_map


def match_with_raw_data(
    parsed: dict, raw_headers: list
) -> OrderedDict:
    """
    파싱된 가이드라인과 raw data 헤더를 매칭하여 전체 변수 라벨 딕셔너리를 생성합니다.
    - 시스템 변수에 기본 라벨 부여
    - _etc 변수에 기타 응답 라벨 자동 생성
    - TO 범위 변수의 라벨 및 값 라벨 전파
    - 가이드라인에 있는 변수 라벨 매핑
    """
    guideline_vars = parsed["variables"]
    to_map = _build_to_range_map(guideline_vars)
    result = OrderedDict()

    for header in raw_headers:
        if header in guideline_vars:
            result[header] = guideline_vars[header]
        elif header.lower() in SYSTEM_VAR_LABELS:
            result[header] = {
                "label": SYSTEM_VAR_LABELS[header.lower()],
                "qtn_type": "SYS",
                "values": OrderedDict(),
            }
        elif header.endswith("_etc"):
            # _etc 변수: 기타 응답 라벨 자동 생성
            base = header.replace("_etc", "")
            base_parts = base.rsplit("_", 1)
            if len(base_parts) == 2 and base_parts[1].isdigit():
                parent_var = base_parts[0]
            else:
                parent_var = base
            result[header] = {
                "label": f"{parent_var} 기타 응답",
                "qtn_type": "ETC",
                "values": OrderedDict(),
            }
        else:
            # TO 범위 변수 매칭 시도
            matched = False
            header_match = re.match(r"^(.+?)(\d+)$", header)
            if header_match:
                prefix = header_match.group(1)
                num = int(header_match.group(2))
                if prefix in to_map:
                    rep_var, start_num, end_num = to_map[prefix]
                    if start_num <= num <= end_num:
                        rep_info = guideline_vars[rep_var]
                        # 값 라벨에서 해당 번호의 보기 내용을 라벨로 사용
                        if num in rep_info["values"]:
                            var_label = rep_info["values"][num]
                        else:
                            var_label = rep_info["label"]
                        result[header] = {
                            "label": var_label,
                            "qtn_type": rep_info["qtn_type"],
                            "values": OrderedDict(rep_info["values"]),
                        }
                        matched = True

            if not matched:
                result[header] = {
                    "label": header,
                    "qtn_type": "UNKNOWN",
                    "values": OrderedDict(),
                }

    return result


# ──────────────────────────────────────────────
# 값 라벨 그룹핑
# ──────────────────────────────────────────────
def group_value_labels(all_vars: OrderedDict) -> list:
    """
    동일한 값 라벨 세트를 가진 변수들을 그룹핑합니다.

    Returns:
        [(변수명 리스트, 값 라벨 OrderedDict), ...]
    """
    groups = []
    seen = set()

    vars_with_values = [
        (name, info) for name, info in all_vars.items() if info["values"]
    ]

    for i, (name, info) in enumerate(vars_with_values):
        if name in seen:
            continue

        # 현재 변수의 값 라벨 패턴을 키로 생성
        value_key = tuple(sorted(info["values"].items()))
        group_vars = [name]
        seen.add(name)

        # 동일한 패턴을 가진 다른 변수 찾기
        for j in range(i + 1, len(vars_with_values)):
            other_name, other_info = vars_with_values[j]
            if other_name in seen:
                continue
            other_key = tuple(sorted(other_info["values"].items()))
            if value_key == other_key:
                group_vars.append(other_name)
                seen.add(other_name)

        groups.append((group_vars, info["values"]))

    return groups


# ──────────────────────────────────────────────
# SPSS Syntax 생성
# ──────────────────────────────────────────────
def generate_variable_labels_sps(all_vars: OrderedDict) -> str:
    """VARIABLE LABELS syntax 블록을 생성합니다."""
    lines = ["VARIABLE LABELS"]
    items = list(all_vars.items())

    for i, (name, info) in enumerate(items):
        label = info["label"].replace("'", "''")  # SPSS 작은따옴표 이스케이프
        suffix = "." if i == len(items) - 1 else ""
        lines.append(f"   {name} '{label}'{suffix}")

    return "\n".join(lines)


def generate_value_labels_sps(all_vars: OrderedDict) -> str:
    """VALUE LABELS syntax 블록을 생성합니다."""
    groups = group_value_labels(all_vars)
    if not groups:
        return ""

    lines = ["VALUE LABELS"]

    for gi, (var_names, values) in enumerate(groups):
        is_first = gi == 0
        is_last = gi == len(groups) - 1

        # 변수명 행 (한 줄 또는 여러 줄)
        if len(var_names) <= 3:
            var_line = " ".join(var_names)
        else:
            # 한 줄에 최대 8개씩 배열
            var_parts = []
            for ci in range(0, len(var_names), 8):
                chunk = var_names[ci : ci + 8]
                var_parts.append(" ".join(chunk))
            var_line = "\n    ".join(var_parts)

        prefix = "   " if is_first else "   /"
        lines.append(f"{prefix}{var_line}")

        # 값 라벨 행
        for value, label in values.items():
            label_escaped = label.replace("'", "''")
            lines.append(f"      {value} '{label_escaped}'")

    lines[-1] = lines[-1] + "."
    return "\n".join(lines)


def generate_summary_table(all_vars: OrderedDict) -> str:
    """변수 요약 테이블을 마크다운 형식으로 생성합니다."""
    lines = [
        "| 구분 | 변수명 | 라벨 | 유형 |",
        "|------|--------|------|------|",
    ]

    def get_type_label(info):
        qtn = info.get("qtn_type", "")
        has_values = bool(info["values"])
        if qtn == "SYS" or qtn == "ETC":
            return "문자" if not has_values else "숫자"
        if qtn in ("51", "52", "93"):
            return "문자"
        if qtn in ("41", "43"):
            return "숫자"
        if qtn == "13":
            return "5점 척도"
        if qtn == "21":
            return "중복선택"
        if qtn in ("11", "61", "67"):
            return "단일선택" if has_values else "문자"
        return "숫자" if has_values else "문자"

    current_section = ""
    for name, info in all_vars.items():
        # 섹션 분류
        if info["qtn_type"] == "SYS":
            section = "시스템"
        elif name.startswith("AG") or name.startswith("DQ"):
            section = "기본정보"
        elif name.startswith("SQ"):
            section = "스크리닝"
        else:
            # 변수 접두사 기반 섹션
            prefix_match = re.match(r"^([A-Z]+\d*)", name)
            section = prefix_match.group(1) if prefix_match else "기타"

        section_display = f"**{section}**" if section != current_section else ""
        current_section = section

        type_label = get_type_label(info)
        label_short = info["label"][:50] + "..." if len(info["label"]) > 50 else info["label"]

        lines.append(f"| {section_display} | {name} | {label_short} | {type_label} |")

    return "\n".join(lines)


# ──────────────────────────────────────────────
# 출력 생성기
# ──────────────────────────────────────────────
def write_sps(all_vars: OrderedDict, output_path: str, title: str = ""):
    """순수 SPSS syntax (.sps) 파일을 생성합니다."""
    sections = []

    if title:
        sections.append(f"* {title}.")
        sections.append(f"* 자동 생성: guideline_to_spss_syntax.py V1.0.")
        sections.append("")

    # VARIABLE LABELS
    sections.append(generate_variable_labels_sps(all_vars))
    sections.append("")

    # VALUE LABELS
    value_labels = generate_value_labels_sps(all_vars)
    if value_labels:
        sections.append(value_labels)
        sections.append("")

    sections.append("EXECUTE.")

    content = "\n".join(sections)
    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(content)

    print(f"[완료] SPSS syntax 파일 생성: {output_path}")
    return content


def write_md(all_vars: OrderedDict, output_path: str, title: str = ""):
    """마크다운 (.md) 파일을 생성합니다."""
    sections = []

    sections.append(f"# SPSS 변수 라벨 Syntax")
    if title:
        sections.append("")
        sections.append(f"> **{title}**")
    sections.append("")
    sections.append("---")
    sections.append("")

    # VARIABLE LABELS
    sections.append("## 1. VARIABLE LABELS (변수 라벨)")
    sections.append("")
    sections.append("```spss")
    sections.append(generate_variable_labels_sps(all_vars))
    sections.append("```")
    sections.append("")
    sections.append("---")
    sections.append("")

    # VALUE LABELS
    value_labels = generate_value_labels_sps(all_vars)
    if value_labels:
        sections.append("## 2. VALUE LABELS (값 라벨)")
        sections.append("")
        sections.append("```spss")
        sections.append(value_labels)
        sections.append("```")
        sections.append("")
        sections.append("---")
        sections.append("")

    # 요약 테이블
    sections.append("## 3. 변수 요약 테이블")
    sections.append("")
    sections.append(generate_summary_table(all_vars))
    sections.append("")

    content = "\n".join(sections)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[완료] 마크다운 파일 생성: {output_path}")
    return content


# ──────────────────────────────────────────────
# 통계 리포트
# ──────────────────────────────────────────────
def print_stats(all_vars: OrderedDict, guideline_vars: dict):
    """변환 결과 통계를 출력합니다."""
    total = len(all_vars)
    with_values = sum(1 for v in all_vars.values() if v["values"])
    sys_vars = sum(1 for v in all_vars.values() if v["qtn_type"] == "SYS")
    etc_vars = sum(1 for v in all_vars.values() if v["qtn_type"] == "ETC")
    guideline_count = len(guideline_vars.get("variables", {}))
    groups = group_value_labels(all_vars)

    print("\n" + "=" * 50)
    print("변환 결과 통계")
    print("=" * 50)
    print(f"  가이드라인 정의 변수:  {guideline_count}개")
    print(f"  전체 출력 변수:        {total}개")
    print(f"  시스템 변수 (자동):    {sys_vars}개")
    print(f"  기타응답 변수 (자동):  {etc_vars}개")
    print(f"  값 라벨 보유 변수:     {with_values}개")
    print(f"  값 라벨 그룹:          {len(groups)}개")
    print("=" * 50 + "\n")


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="SPSS Column Guideline CSV → SPSS Syntax 변환 스크립트",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python guideline_to_spss_syntax.py --guideline "guideline.csv"
  python guideline_to_spss_syntax.py --guideline "guideline.csv" --rawdata "rawdata.csv" --format both
  python guideline_to_spss_syntax.py --guideline "guideline.csv" --title "프로젝트명" --format sps
        """,
    )
    parser.add_argument(
        "--guideline", "-g", required=True, help="가이드라인 CSV 파일 경로"
    )
    parser.add_argument(
        "--rawdata", "-r", default=None, help="raw data CSV 파일 경로 (선택)"
    )
    parser.add_argument(
        "--output", "-o", default=None, help="출력 파일 경로 (확장자 제외, 기본: 가이드라인 폴더)"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["md", "sps", "both"],
        default="both",
        help="출력 형식 (기본: both)",
    )
    parser.add_argument(
        "--encoding", "-e", default="utf-8-sig", help="CSV 인코딩 (기본: utf-8-sig)"
    )
    parser.add_argument("--title", "-t", default="", help="문서 제목 (선택)")

    args = parser.parse_args()

    # 1. 가이드라인 CSV 파싱
    print(f"[1/4] 가이드라인 CSV 파싱 중: {args.guideline}")
    parsed = parse_guideline_csv(args.guideline, args.encoding)
    guideline_var_count = len(parsed["variables"])
    print(f"       → {guideline_var_count}개 변수 정의 발견")

    # 2. Raw Data 매칭 (있을 경우)
    if args.rawdata:
        print(f"[2/4] Raw Data 헤더 매칭 중: {args.rawdata}")
        headers = read_raw_data_headers(args.rawdata, args.encoding)
        all_vars = match_with_raw_data(parsed, headers)
        print(f"       → {len(headers)}개 헤더 변수 매칭 완료")
    else:
        print("[2/4] Raw Data 없음 → 가이드라인 변수만 사용")
        all_vars = OrderedDict()
        for name, info in parsed["variables"].items():
            all_vars[name] = info

    # 3. 출력 경로 결정
    if args.output:
        output_base = args.output
    else:
        guideline_dir = os.path.dirname(os.path.abspath(args.guideline))
        guideline_name = os.path.splitext(os.path.basename(args.guideline))[0]
        output_base = os.path.join(guideline_dir, f"SPSS_Syntax_{guideline_name}")

    # 4. 파일 생성
    print(f"[3/4] Syntax 파일 생성 중...")
    if args.format in ("sps", "both"):
        write_sps(all_vars, output_base + ".sps", args.title)
    if args.format in ("md", "both"):
        write_md(all_vars, output_base + ".md", args.title)

    # 5. 통계
    print_stats(all_vars, parsed)
    print("[4/4] 완료!")


if __name__ == "__main__":
    main()
