# 📦 hwp-mcp 설치 가이드

> **이 문서는 MCP를 처음 접하는 분도 쉽게 따라할 수 있도록 작성되었습니다.**  
> 작성일: 2026-02-24 | GitHub: https://github.com/jkf87/hwp-mcp

---

## 🤔 이 프로그램이 뭔가요?

### MCP란?

**MCP(Model Context Protocol)** 는 AI(인공지능)가 **컴퓨터의 프로그램을 조작**할 수 있게 해주는 연결 방식입니다.

쉽게 말해:
- 평소에 AI에게 "문서 만들어줘"라고 하면, AI는 **텍스트만** 생성합니다
- MCP를 연결하면, AI가 실제로 **한글 프로그램을 열고, 문서를 만들고, 저장**까지 합니다

### hwp-mcp란?

**한글 프로그램(HWP)을 AI가 원격으로 조종**할 수 있게 해주는 MCP 서버입니다.

**핵심 특징:**
- ✅ 한글 프로그램을 **직접 제어** — 실제로 한글이 열리고 동작합니다
- ✅ `.hwp` 파일 생성, 편집, 저장 가능
- ✅ 표 생성, 글꼴 설정, 일괄 작업 지원

> ⚠️ **필수 조건**: 한글 프로그램(한컴오피스 한글)이 **반드시 설치**되어 있어야 합니다.  
> ⚠️ **Windows 전용**입니다. macOS/Linux에서는 사용할 수 없습니다.

---

## 📋 설치 전 확인사항

### 1단계: 한글 프로그램 확인

한컴오피스 한글이 설치되어 있는지 확인하세요:
- 시작 메뉴에서 "한글" 검색
- 한글 프로그램이 정상적으로 실행되는지 확인

> 한글 프로그램이 없으면 이 MCP 서버는 사용할 수 없습니다.  
> 대신 `.hwpx` 파일을 다루는 `hwpx-mcp-server`를 사용하세요.

### 2단계: Python 확인

터미널(PowerShell 또는 명령 프롬프트)을 열고:

```
python --version
```

**정상 결과 예시:**
```
Python 3.12.7
```

> - Python **3.7 이상**이면 됩니다.
> - Python이 없다면 https://www.python.org/downloads/ 에서 다운로드하세요.
> - 설치 시 **"Add Python to PATH"** 옵션을 반드시 체크하세요!

### 3단계: Git 확인

```
git --version
```

**정상 결과 예시:**
```
git version 2.43.0.windows.1
```

> Git이 없다면 https://git-scm.com/downloads 에서 설치하세요.

---

## 🚀 설치 과정

### 1단계: 저장소 다운로드 (클론)

원하는 폴더에서 아래 명령어를 실행합니다:

```bash
git clone https://github.com/jkf87/hwp-mcp.git
```

이 명령어는 GitHub에서 프로그램 파일을 내 컴퓨터로 복사합니다.

> 💡 **예시**: `D:\tools` 폴더에서 실행하면 `D:\tools\hwp-mcp` 폴더가 생깁니다.

복사가 완료되면 해당 폴더로 이동합니다:

```bash
cd hwp-mcp
```

### 2단계: 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

**설치되는 주요 패키지:**

| 패키지     | 용도                                           |
| ---------- | ---------------------------------------------- |
| `pywin32`  | Windows에서 한글 프로그램을 원격 제어하는 도구 |
| `comtypes` | Windows COM 인터페이스 (프로그램 간 통신)      |
| `fastmcp`  | MCP 서버 프레임워크                            |

**정상 완료 시:**
```
Successfully installed pywin32-xxx comtypes-xxx fastmcp-xxx
```

### 3단계: 설치 테스트

서버가 정상 실행되는지 확인합니다:

```bash
python hwp_mcp_stdio_server.py
```

> 서버가 시작되면 **입력을 기다리며 멈춘 것처럼 보입니다** — 이것이 정상입니다!  
> `Ctrl+C`를 눌러 종료하세요.

### 자주 발생하는 에러

| 에러 메시지                                       | 원인                 | 해결 방법                           |
| ------------------------------------------------- | -------------------- | ----------------------------------- |
| `ModuleNotFoundError: No module named 'win32com'` | pywin32 미설치       | `pip install pywin32` 재실행        |
| `ModuleNotFoundError: No module named 'comtypes'` | comtypes 미설치      | `pip install comtypes` 재실행       |
| `pywintypes.com_error: 한글을 찾을 수 없습니다`   | 한글 프로그램 미설치 | 한컴오피스 한글 설치 필요           |
| `pip is not recognized`                           | Python PATH 미등록   | Python 재설치 시 "Add to PATH" 체크 |

---

## ⚙️ AI 클라이언트에 연결하기

### Gemini CLI에 연결하기

1. 메모장으로 아래 파일을 엽니다:
   ```
   C:\Users\{사용자이름}\.gemini\settings.json
   ```

2. 아래 내용을 추가합니다:

```json
{
  "mcpServers": {
    "hwp": {
      "command": "python",
      "args": ["D:\\tools\\hwp-mcp\\hwp_mcp_stdio_server.py"]
    }
  }
}
```

> ⚠️ `args`의 경로를 **실제 hwp-mcp 폴더 경로**로 변경하세요.  
> ⚠️ 경로 구분자는 `\\` (역슬래시 2개)를 사용해야 합니다.

3. **Gemini CLI를 재시작**합니다.

### VS Code (GitHub Copilot)에 연결하기

1. 프로젝트 루트에 `.vscode/mcp.json` 파일을 만듭니다:

```json
{
  "servers": {
    "hwp": {
      "command": "python",
      "args": ["D:\\tools\\hwp-mcp\\hwp_mcp_stdio_server.py"]
    }
  }
}
```

2. VS Code를 재시작합니다.

### Claude Desktop에 연결하기

1. 설정 파일을 엽니다:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. 아래 내용을 추가합니다:

```json
{
  "mcpServers": {
    "hwp": {
      "command": "python",
      "args": ["D:\\tools\\hwp-mcp\\hwp_mcp_stdio_server.py"]
    }
  }
}
```

3. Claude Desktop을 재시작합니다.

---

## 🔐 보안 모듈 설정 (선택)

한글 프로그램은 외부에서 파일에 접근하면 **보안 경고 창**이 뜹니다.  
이를 방지하려면 보안 모듈을 등록할 수 있습니다.

### 보안 모듈이란?

- `hwp-mcp/security_module/FilePathCheckerModuleExample.dll` 파일
- 한글 프로그램에 "이 프로그램은 안전해요"라고 알려주는 역할
- **등록하지 않아도 기능은 정상 작동**합니다 (보안 창이 뜰 뿐)

### 등록 방법

보안 모듈은 서버 시작 시 **자동으로 등록을 시도**합니다.  
수동으로 등록이 필요한 경우:

```bash
regsvr32 "D:\tools\hwp-mcp\security_module\FilePathCheckerModuleExample.dll"
```

> 관리자 권한 PowerShell에서 실행하세요.

---

## 📁 프로젝트 폴더 구조

설치가 완료되면 아래와 같은 폴더 구조를 확인할 수 있습니다:

```
hwp-mcp/
├── hwp_mcp_stdio_server.py  ← 메인 서버 파일 (이것을 실행합니다)
├── requirements.txt         ← 필요한 패키지 목록
├── src/
│   ├── tools/
│   │   ├── hwp_controller.py  ← 한글 제어 핵심 코드
│   │   └── hwp_table_tools.py ← 표 관련 기능
│   └── utils/                 ← 유틸리티 함수
└── security_module/
    └── FilePathCheckerModuleExample.dll  ← 보안 모듈
```

---

## ✅ 설치 완료 체크리스트

- [ ] 한글 프로그램(한컴오피스 한글) 설치 확인
- [ ] Python 3.7 이상 설치 확인
- [ ] Git 설치 확인
- [ ] `git clone` 으로 저장소 다운로드 완료
- [ ] `pip install -r requirements.txt` 실행 완료
- [ ] `python hwp_mcp_stdio_server.py` 테스트 실행 성공
- [ ] AI 클라이언트 설정 파일에 서버 등록 완료
- [ ] AI 클라이언트 재시작 완료

모든 항목을 완료했다면 설치가 성공한 것입니다! 🎉  
사용 방법은 **hwp_mcp_usage_guide.md**를 참고하세요.
