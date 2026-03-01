# 📄 한글(HWP/HWPX) MCP 서버 설치 및 사용 가이드

> **작성일**: 2026-02-24  
> **대상**: AI MCP 클라이언트(Gemini CLI, VS Code Copilot, Claude Desktop 등)에서 한글 문서를 자동화하려는 사용자

---

## 📋 목차

1. [개요](#1-개요)
2. [두 서버 비교](#2-두-서버-비교)
3. [사전 준비](#3-사전-준비)
4. [Server 1: hwpx-mcp-server 설치](#4-server-1-hwpx-mcp-server-설치)
5. [Server 2: hwp-mcp 설치](#5-server-2-hwp-mcp-설치)
6. [MCP 클라이언트 설정](#6-mcp-클라이언트-설정)
7. [사용 가이드](#7-사용-가이드)
8. [트러블슈팅](#8-트러블슈팅)
9. [참고 링크](#9-참고-링크)

---

## 1. 개요

한글 문서를 AI로 자동화하기 위한 **두 가지 MCP 서버**를 소개합니다.

- **hwpx-mcp-server** — `.hwpx` 파일을 순수 파이썬으로 파싱 (한글 프로그램 불필요)
- **hwp-mcp** — `.hwp` 파일을 한글 프로그램 COM API로 직접 제어 (한글 프로그램 필수)

> **MCP(Model Context Protocol)** 란?  
> AI 모델이 외부 도구(문서 편집, 데이터 조회 등)를 호출할 수 있게 해주는 표준 프로토콜입니다.

---

## 2. 두 서버 비교

| 항목              | hwpx-mcp-server                                                       | hwp-mcp                                           |
| ----------------- | --------------------------------------------------------------------- | ------------------------------------------------- |
| **GitHub**        | [airmang/hwpx-mcp-server](https://github.com/airmang/hwpx-mcp-server) | [jkf87/hwp-mcp](https://github.com/jkf87/hwp-mcp) |
| **대상 포맷**     | `.hwpx` (XML 기반)                                                    | `.hwp` (바이너리)                                 |
| **한글 프로그램** | ❌ 불필요                                                              | ✅ 필수                                            |
| **OS**            | Windows / macOS / Linux                                               | Windows 전용                                      |
| **동작 방식**     | 파일 파싱 (python-hwpx)                                               | COM 자동화 (pywin32)                              |
| **설치 방식**     | `uvx` 원클릭                                                          | git clone + pip install                           |
| **도구 수**       | 기본 27개 + 고급 10개                                                 | 문서/테이블/배치 등                               |
| **라이선스**      | MIT                                                                   | MIT                                               |

### 어떤 서버를 선택해야 할까?

- **`.hwpx` 파일을 다루고 한글 프로그램이 없는 환경** → `hwpx-mcp-server`
- **`.hwp` 파일을 다루고 한글 프로그램이 설치된 Windows 환경** → `hwp-mcp`
- **두 포맷 모두 다뤄야 하는 경우** → 두 서버 모두 설치 (충돌 없음)

---

## 3. 사전 준비

### 3.1 공통 요구사항

| 항목   | 최소 버전 | 확인 명령어        |
| ------ | --------- | ------------------ |
| Python | 3.10 이상 | `python --version` |

### 3.2 uv 설치 (hwpx-mcp-server용)

`uv`는 Python 패키지 도구 실행기입니다. `uvx` 명령으로 패키지를 바로 실행할 수 있습니다.

```bash
pip install uv
```

설치 확인:
```bash
# Windows
python -c "import shutil; print(shutil.which('uvx'))"

# 또는 직접 경로 확인
# 보통 C:\Users\{사용자}\AppData\Roaming\Python\Python3xx\Scripts\uvx.exe
```

> **⚠️ 참고**: Python 3.14처럼 최신 버전에서는 일부 패키지(lxml 등)의 바이너리가 없어 빌드 에러가 날 수 있습니다.  
> 이 경우 `uvx --python 3.12 hwpx-mcp-server`처럼 **Python 3.12를 지정**하면 `uv`가 자동으로 해당 버전을 다운로드하여 사용합니다.

### 3.3 한글 프로그램 (hwp-mcp용)

- **한컴오피스 한글** (또는 **한글과컴퓨터 한글**)이 설치되어 있어야 합니다.
- COM 자동화를 위해 한글이 실행 가능한 상태여야 합니다.

---

## 4. Server 1: hwpx-mcp-server 설치

### 4.1 설치 (원클릭)

별도 설치 과정 없이 `uvx`로 바로 실행 가능합니다:

```bash
uvx hwpx-mcp-server
```

또는 Python 버전을 지정하여 실행:
```bash
uvx --python 3.12 hwpx-mcp-server
```

> `uvx`는 가상 환경을 자동 생성하고 패키지를 설치한 뒤 실행합니다.  
> 처음 실행 시 패키지 다운로드로 약간의 시간이 소요되며, 이후에는 캐시되어 빠르게 실행됩니다.

### 4.2 선택: pip으로 직접 설치

```bash
pip install hwpx-mcp-server
```

> ⚠️ Python 3.14에서는 `lxml` 빌드 실패 가능. Python 3.12 이하 권장.

### 4.3 제공 도구 목록

#### 📖 읽기 & 탐색

| 도구                       | 설명                              |
| -------------------------- | --------------------------------- |
| `get_document_info`        | 문서 기본 정보 조회               |
| `get_document_text`        | 전체 텍스트 추출 (max_chars 제한) |
| `get_document_outline`     | 문서 목차/구조 조회               |
| `get_paragraph_text`       | 특정 문단 텍스트 조회             |
| `get_paragraphs_text`      | 여러 문단 범위 텍스트 조회        |
| `list_available_documents` | 사용 가능한 .hwpx 파일 목록       |

#### 🔎 검색 & 치환

| 도구                 | 설명           |
| -------------------- | -------------- |
| `find_text`          | 텍스트 검색    |
| `search_and_replace` | 검색 후 치환   |
| `batch_replace`      | 다건 일괄 치환 |

#### ✏️ 편집

| 도구               | 설명                  |
| ------------------ | --------------------- |
| `add_heading`      | 제목 추가             |
| `add_paragraph`    | 문단 추가             |
| `insert_paragraph` | 특정 위치에 문단 삽입 |
| `delete_paragraph` | 문단 삭제             |
| `add_page_break`   | 페이지 나누기         |
| `add_memo`         | 메모 추가             |
| `remove_memo`      | 메모 삭제             |
| `copy_document`    | 문서 복사             |

#### 📊 표

| 도구                  | 설명         |
| --------------------- | ------------ |
| `add_table`           | 표 생성      |
| `get_table_text`      | 표 내용 읽기 |
| `set_table_cell_text` | 셀 내용 설정 |
| `merge_table_cells`   | 셀 병합      |
| `split_table_cell`    | 셀 분할      |
| `format_table`        | 표 서식 설정 |

#### 🎨 스타일

| 도구                  | 설명                              |
| --------------------- | --------------------------------- |
| `format_text`         | 텍스트 서식 (글꼴, 크기, 색상 등) |
| `create_custom_style` | 사용자 정의 스타일 생성           |
| `list_styles`         | 사용 가능한 스타일 목록           |

#### 🔬 고급 (HWPX_MCP_ADVANCED=1 필요)

| 도구                                        | 설명                        |
| ------------------------------------------- | --------------------------- |
| `package_parts`                             | 문서 내부 파트 목록         |
| `package_get_xml`                           | 특정 파트의 XML 조회        |
| `package_get_text`                          | 특정 파트의 텍스트 조회     |
| `plan_edit` / `preview_edit` / `apply_edit` | 편집 계획 → 미리보기 → 적용 |
| `validate_structure`                        | 문서 구조 검증              |
| `lint_text_conventions`                     | 텍스트 규칙 검사            |

### 4.4 환경 변수 설정

| 변수                  | 기본값  | 설명                        |
| --------------------- | ------- | --------------------------- |
| `HWPX_MCP_MAX_CHARS`  | `10000` | 텍스트 조회 시 최대 글자 수 |
| `HWPX_MCP_AUTOBACKUP` | `1`     | 편집 전 `.bak` 자동 백업    |
| `HWPX_MCP_ADVANCED`   | `0`     | 고급 도구 활성화 (1=활성)   |
| `LOG_LEVEL`           | `INFO`  | 로그 레벨                   |

---

## 5. Server 2: hwp-mcp 설치

### 5.1 저장소 클론

```bash
git clone https://github.com/jkf87/hwp-mcp.git
cd hwp-mcp
```

### 5.2 의존성 설치

```bash
pip install -r requirements.txt
```

주요 의존성:
- `pywin32>=228` — Windows COM 자동화
- `comtypes>=1.1.14` — COM 인터페이스
- `fastmcp>=0.1.0` — MCP 프레임워크

### 5.3 제공 도구 목록

| 도구                       | 설명                      |
| -------------------------- | ------------------------- |
| `hwp_create`               | 새 문서 생성              |
| `hwp_open`                 | 기존 문서 열기            |
| `hwp_save`                 | 문서 저장                 |
| `hwp_insert_text`          | 텍스트 삽입               |
| `hwp_set_font`             | 글꼴 설정 (크기, 굵기 등) |
| `hwp_insert_table`         | 표 생성                   |
| `hwp_fill_table_with_data` | 표에 데이터 채우기        |
| `hwp_fill_column_numbers`  | 열에 연속 숫자 채우기     |
| `hwp_batch_operations`     | 여러 작업 일괄 실행       |

### 5.4 보안 모듈

한글 프로그램은 외부 파일 접근 시 보안 경고를 표시합니다.  
`security_module/FilePathCheckerModuleExample.dll`을 등록하면 이를 우회할 수 있습니다.

> 보안 모듈 등록 실패 시에도 기능은 정상 작동하지만, 파일 열기/저장 시 보안 대화 상자가 표시됩니다.

---

## 6. MCP 클라이언트 설정

각 클라이언트별 설정 파일에 아래 내용을 추가합니다.

### 6.1 Gemini CLI

**파일 위치**: `~/.gemini/settings.json` (Windows: `C:\Users\{사용자}\.gemini\settings.json`)

```json
{
  "mcpServers": {
    "hwpx": {
      "command": "C:\\Users\\{사용자}\\AppData\\Roaming\\Python\\Python314\\Scripts\\uvx.exe",
      "args": ["--python", "3.12", "hwpx-mcp-server"],
      "env": {
        "HWPX_MCP_MAX_CHARS": "12000",
        "HWPX_MCP_AUTOBACKUP": "1",
        "HWPX_MCP_ADVANCED": "0",
        "LOG_LEVEL": "INFO"
      }
    },
    "hwp": {
      "command": "python",
      "args": ["{hwp-mcp 경로}/hwp_mcp_stdio_server.py"]
    }
  }
}
```

> **⚠️ 주의**: `{사용자}`와 `{hwp-mcp 경로}`를 실제 경로로 변경하세요.

### 6.2 VS Code (GitHub Copilot)

**파일 위치**: `.vscode/mcp.json` (프로젝트 루트)

```json
{
  "servers": {
    "hwpx": {
      "command": "uvx",
      "args": ["--python", "3.12", "hwpx-mcp-server"]
    },
    "hwp": {
      "command": "python",
      "args": ["{hwp-mcp 경로}/hwp_mcp_stdio_server.py"]
    }
  }
}
```

### 6.3 Claude Desktop

**파일 위치**: `claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "hwpx": {
      "command": "uvx",
      "args": ["--python", "3.12", "hwpx-mcp-server"]
    },
    "hwp": {
      "command": "python",
      "args": ["{hwp-mcp 경로}/hwp_mcp_stdio_server.py"]
    }
  }
}
```

### 6.4 설정 후 적용

> **중요**: 설정 파일 수정 후 반드시 **클라이언트를 재시작**해야 MCP 서버가 연결됩니다.

---

## 7. 사용 가이드

### 7.1 hwpx-mcp-server 사용 예시

AI 대화에서 자연어로 요청하면 MCP 도구가 자동으로 호출됩니다.

#### 문서 정보 조회
```
"보고서.hwpx 파일의 내용을 보여줘"
→ get_document_text 도구 호출
```

#### 텍스트 검색 및 치환
```
"보고서.hwpx에서 '2025년'을 '2026년'으로 모두 바꿔줘"
→ batch_replace 도구 호출
```

#### 새 문서 작성
```
"새로운 hwpx 문서를 만들고 제목 '월간 보고서'를 추가해줘"
→ add_heading + add_paragraph 도구 호출
```

#### 표 추가
```
"3행 4열 표를 추가하고, 첫 행에 '이름', '부서', '직급', '연락처'를 넣어줘"
→ add_table + set_table_cell_text 도구 호출
```

#### 서식 적용
```
"제목 텍스트를 16pt 굵은 글씨로 바꿔줘"
→ format_text 도구 호출
```

### 7.2 hwp-mcp 사용 예시

#### 새 문서 생성 및 저장
```
"새 한글 문서를 만들어서 '회의록'이라고 제목을 쓰고 D:\문서\회의록.hwp로 저장해줘"
→ hwp_create + hwp_insert_text + hwp_set_font + hwp_save 호출
```

#### 표 생성 및 데이터 입력
```
"5행 2열 표를 만들고 '월별 판매량' 데이터를 입력해줘"
→ hwp_insert_table + hwp_fill_table_with_data 호출
```

#### 일괄 작업 (배치)
```
"문서 생성 → 제목 입력 → 글꼴 설정 → 본문 작성 → 저장을 순서대로 해줘"
→ hwp_batch_operations 호출 (한번에 여러 작업 실행)
```

### 7.3 두 서버 함께 사용하기

두 서버는 대상 포맷이 다르므로 동시에 등록해도 충돌하지 않습니다.

```
"보고서.hwpx 파일의 내용을 읽어서, 새 한글(.hwp) 문서에 옮겨줘"
→ hwpx 서버: get_document_text 호출
→ hwp 서버: hwp_create + hwp_insert_text + hwp_save 호출
```

---

## 8. 트러블슈팅

### 8.1 공통 문제

| 증상                      | 원인                    | 해결 방법                                    |
| ------------------------- | ----------------------- | -------------------------------------------- |
| 서버가 인식되지 않음      | 클라이언트 미재시작     | 클라이언트(Gemini CLI 등) 재시작             |
| `uvx` 명령을 찾을 수 없음 | PATH 미등록             | 전체 경로 사용 또는 PATH에 Scripts 폴더 추가 |
| Python 버전 호환 문제     | 3.14에서 lxml 빌드 실패 | `--python 3.12` 옵션 사용                    |

### 8.2 hwpx-mcp-server 문제

| 증상                     | 원인                      | 해결 방법                        |
| ------------------------ | ------------------------- | -------------------------------- |
| `hwpx.package` 관련 경고 | python-hwpx 버전 변경     | 서버가 자동 처리하므로 무시 가능 |
| 텍스트가 잘림            | `HWPX_MCP_MAX_CHARS` 제한 | 환경 변수 값을 늘림 (예: 20000)  |

### 8.3 hwp-mcp 문제

| 증상                | 원인                        | 해결 방법                               |
| ------------------- | --------------------------- | --------------------------------------- |
| 한글 연결 실패      | 한글 프로그램 미설치/미실행 | 한글 프로그램 설치 및 실행 확인         |
| 보안 대화 상자 표시 | 보안 모듈 미등록            | `FilePathCheckerModuleExample.dll` 등록 |
| 표 데이터 입력 오류 | 커서 위치 문제              | 최신 버전으로 업데이트 (`git pull`)     |
| `comtypes` 오류     | Windows 전용 패키지         | Windows에서만 사용 가능                 |

### 8.4 PATH에 Scripts 폴더 추가하기

`uvx`가 PATH에 없는 경우, 아래와 같이 추가합니다:

```powershell
# 현재 세션에만 적용
$env:PATH += ";C:\Users\{사용자}\AppData\Roaming\Python\Python314\Scripts"

# 영구 적용 (관리자 권한 PowerShell)
[Environment]::SetEnvironmentVariable(
    "PATH",
    [Environment]::GetEnvironmentVariable("PATH", "User") + ";C:\Users\{사용자}\AppData\Roaming\Python\Python314\Scripts",
    "User"
)
```

---

## 9. 참고 링크

| 항목                   | URL                                        |
| ---------------------- | ------------------------------------------ |
| hwpx-mcp-server GitHub | https://github.com/airmang/hwpx-mcp-server |
| hwp-mcp GitHub         | https://github.com/jkf87/hwp-mcp           |
| MCP 공식 사양          | https://modelcontextprotocol.io            |
| uv 공식 문서           | https://docs.astral.sh/uv                  |
| python-hwpx (PyPI)     | https://pypi.org/project/python-hwpx       |

---

> **문서 버전**: v1.0 | **최종 수정**: 2026-02-24
