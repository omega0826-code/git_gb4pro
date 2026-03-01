# 📦 hwpx-mcp-server 설치 가이드

> **이 문서는 MCP를 처음 접하는 분도 쉽게 따라할 수 있도록 작성되었습니다.**  
> 작성일: 2026-02-24 | GitHub: https://github.com/airmang/hwpx-mcp-server

---

## 🤔 이 프로그램이 뭔가요?

### MCP란?

**MCP(Model Context Protocol)** 는 AI가 "외부 도구"를 사용할 수 있게 해주는 **연결 규격**입니다.

비유하자면:
- AI는 **사람**이고
- MCP 서버는 **도구 상자**입니다
- AI가 "한글 문서 열어줘"라고 말하면, MCP 서버가 대신 문서를 열어서 결과를 알려줍니다

### hwpx-mcp-server란?

**한글(.hwpx) 문서**를 AI가 읽고, 편집하고, 검색할 수 있게 해주는 MCP 서버입니다.

**핵심 특징:**
- ✅ **한글 프로그램 없이 동작** — 파일을 직접 분석하는 방식
- ✅ **Windows, macOS, Linux** 모두 사용 가능
- ✅ **설치가 매우 간단** — 한 줄 명령으로 끝

> ⚠️ `.hwpx` 파일만 지원합니다. `.hwp`(구 버전 포맷)은 지원하지 않습니다.  
> `.hwp` 파일을 다루려면 별도의 `hwp-mcp` 서버가 필요합니다.

---

## 📋 설치 전 확인사항

### 1단계: Python이 설치되어 있는지 확인

터미널(명령 프롬프트 또는 PowerShell)을 열고 아래 명령어를 입력하세요:

```
python --version
```

**정상 결과 예시:**
```
Python 3.12.7
```

> - Python **3.10 이상**이 필요합니다.
> - Python이 없다면 https://www.python.org/downloads/ 에서 다운로드하세요.
> - 설치 시 **"Add Python to PATH"** 옵션을 반드시 체크하세요!

### 2단계: uv 설치

`uv`는 Python 패키지를 쉽게 실행할 수 있게 해주는 도구입니다.  
`uvx`라는 명령어로 패키지를 **설치 없이 바로 실행**할 수 있습니다.

```
pip install uv
```

**정상 결과 예시:**
```
Successfully installed uv-0.10.4
```

설치 확인:
```
python -c "import shutil; print(shutil.which('uvx'))"
```

경로가 출력되면 성공입니다. 예:
```
C:\Users\홍길동\AppData\Roaming\Python\Python312\Scripts\uvx.exe
```

> 💡 **경로가 `None`으로 나온다면?**  
> Scripts 폴더가 PATH에 등록되지 않은 것입니다.  
> 아래 경로를 메모해 두세요 (나중에 설정에 사용):  
> `C:\Users\{사용자이름}\AppData\Roaming\Python\Python3xx\Scripts\uvx.exe`

---

## 🚀 설치 및 첫 실행 테스트

### 방법 1: uvx로 바로 실행 (권장)

```
uvx hwpx-mcp-server
```

이 명령어를 실행하면:
1. 자동으로 가상 환경을 만들고
2. 필요한 패키지를 모두 설치하고
3. MCP 서버를 시작합니다

> 처음 실행 시 패키지 다운로드로 1~2분 소요됩니다.  
> 서버가 시작되면 **입력을 기다리며 멈춘 것처럼 보입니다** — 이것이 정상입니다!  
> `Ctrl+C`를 눌러 종료할 수 있습니다.

### 방법 2: Python 버전 지정 실행

Python 3.13 이상에서 설치 에러가 발생하면, Python 3.12를 지정하세요:

```
uvx --python 3.12 hwpx-mcp-server
```

> `uv`가 자동으로 Python 3.12를 다운로드하여 사용합니다.  
> 시스템에 설치된 Python 버전과 무관하게 동작합니다.

### 자주 발생하는 에러

| 에러 메시지                                 | 원인                                     | 해결 방법                           |
| ------------------------------------------- | ---------------------------------------- | ----------------------------------- |
| `error: Microsoft Visual C++ 14.0 required` | Python 버전이 너무 높아 패키지 빌드 실패 | `uvx --python 3.12` 사용            |
| `uvx: command not found`                    | uvx가 PATH에 없음                        | 전체 경로로 실행 (아래 참조)        |
| `pip is not recognized`                     | Python PATH 미등록                       | Python 재설치 시 "Add to PATH" 체크 |

**uvx 전체 경로로 실행하는 방법:**
```
"C:\Users\{사용자}\AppData\Roaming\Python\Python312\Scripts\uvx.exe" --python 3.12 hwpx-mcp-server
```

---

## ⚙️ AI 클라이언트에 연결하기

MCP 서버를 AI 클라이언트에 연결해야 실제로 사용할 수 있습니다.

### Gemini CLI에 연결하기

1. 아래 파일을 메모장으로 엽니다:
   ```
   C:\Users\{사용자이름}\.gemini\settings.json
   ```

2. 아래 내용을 추가합니다:

```json
{
  "mcpServers": {
    "hwpx": {
      "command": "C:\\Users\\{사용자}\\AppData\\Roaming\\Python\\Python312\\Scripts\\uvx.exe",
      "args": ["--python", "3.12", "hwpx-mcp-server"],
      "env": {
        "HWPX_MCP_MAX_CHARS": "12000",
        "HWPX_MCP_AUTOBACKUP": "1",
        "HWPX_MCP_ADVANCED": "0",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

> ⚠️ `{사용자}`를 실제 Windows 사용자 이름으로 변경하세요.  
> ⚠️ 경로 구분자는 `\\` (역슬래시 2개)를 사용해야 합니다.

3. **Gemini CLI를 재시작**합니다.

### VS Code (GitHub Copilot)에 연결하기

1. 프로젝트 루트에 `.vscode/mcp.json` 파일을 만듭니다:

```json
{
  "servers": {
    "hwpx": {
      "command": "uvx",
      "args": ["--python", "3.12", "hwpx-mcp-server"]
    }
  }
}
```

2. VS Code를 재시작합니다.

### Claude Desktop에 연결하기

1. 설정 파일을 엽니다:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. 아래 내용을 추가합니다:

```json
{
  "mcpServers": {
    "hwpx": {
      "command": "uvx",
      "args": ["--python", "3.12", "hwpx-mcp-server"]
    }
  }
}
```

3. Claude Desktop을 재시작합니다.

---

## 🔧 설정 옵션 (환경 변수)

필요에 따라 환경 변수를 조정할 수 있습니다:

| 변수명                | 기본값  | 설명                                                          |
| --------------------- | ------- | ------------------------------------------------------------- |
| `HWPX_MCP_MAX_CHARS`  | `10000` | 문서 텍스트를 읽을 때 최대 글자 수. 큰 문서라면 값을 늘리세요 |
| `HWPX_MCP_AUTOBACKUP` | `1`     | 문서 편집 전 자동 백업 여부 (1=백업함, 0=안 함)               |
| `HWPX_MCP_ADVANCED`   | `0`     | 고급 도구 활성화 (1=활성). 문서 내부 XML 직접 조작 가능       |
| `LOG_LEVEL`           | `INFO`  | 로그 상세 수준 (DEBUG, INFO, WARNING, ERROR)                  |

---

## ✅ 설치 완료 체크리스트

- [ ] Python 3.10 이상 설치 확인
- [ ] `pip install uv` 실행 완료
- [ ] `uvx --python 3.12 hwpx-mcp-server` 테스트 실행 성공
- [ ] AI 클라이언트 설정 파일에 서버 등록 완료
- [ ] AI 클라이언트 재시작 완료
- [ ] AI에게 "hwpx 문서 관련 도구 목록을 보여줘"라고 물어서 응답 확인

모든 항목을 완료했다면 설치가 성공한 것입니다! 🎉  
사용 방법은 **hwpx_mcp_server_usage_guide.md**를 참고하세요.
