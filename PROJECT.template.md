# PROJECT.md (프로젝트 설정 템플릿)

> 새 프로젝트에 `ai-dev-playbook`을 적용할 때 이 파일을 `PROJECT.md`로 복사해 프로젝트 고유 정보만 채워 사용합니다.
> 루트의 `PROJECT.md`는 기본 Git 제외 대상입니다. 공개 저장소에는 이 템플릿을 사용하세요.

---

## 1. 프로젝트 개요

- **프로젝트명**: `<프로젝트명>`
- **목표**: `<핵심 목표 (예: 웹 접근성 품질인증 / 기능 고도화 / 장애 개선)>`
- **기술 스택**: `<예: Java 8, Spring MVC, JSP/JSTL, Apache Tiles, jQuery 1.12.4, MSSQL, SVN>`
- **로컬 실행 환경**: `<예: http://localhost:8080 (Tomcat)>`

---

## 2. 디렉터리 및 작업 사본 역할

| 경로 (상대 경로 권장) | VCS 브랜치/역할 | 수정 가능 여부 | 비고 |
|---|---|---|---|
| `./app-trunk` | 기준(trunk/main) 비교용 | 읽기 전용 | |
| `./app-feature` | 기본 작업 대상 브랜치 | 수정 가능 | |
| `./admin-app` | 관리자 연동 참고용 | 읽기 전용 (요청 시 수정) | |
| `./docs` | 프로젝트별 분석·계획·검증 보고서 | 문서 작성 가능 | `analysis/`, `planning/`, `testing/` |

- 제외할 로컬/IDE 폴더: `.metadata/`, `.recommenders/`, `target/`, `bin/`, `node_modules/`

---

## 3. 활성화할 선택 모듈 (`modules/`)

이 프로젝트에서 추가로 준수해야 할 모듈을 체크한다.

- [ ] [`modules/legacy-web-guardrails.md`](modules/legacy-web-guardrails.md) — 레거시 Java/JSP/jQuery 안전 규칙
- [ ] [`modules/web-a11y-kwcag.md`](modules/web-a11y-kwcag.md) — KWCAG/WAI-ARIA 웹 접근성 기준
- [ ] [`modules/vcs-svn-windows.md`](modules/vcs-svn-windows.md) — Windows 환경 SVN 커밋·인코딩 규칙
- [ ] [`modules/multi-agent-and-docs.md`](modules/multi-agent-and-docs.md) — 다중 AI 에이전트 역할 분리 및 인계 규칙
- [ ] [`modules/docs-notion-sync.md`](modules/docs-notion-sync.md) — Notion/협업 문서 안전 동기화 규칙
- [ ] [`modules/mcp-setup-and-governance.md`](modules/mcp-setup-and-governance.md) — Playwright·Notion·DB MCP 안전 운영 규칙

---

## 4. 보호 대상 및 제외 범위

- **기존 로컬 변경 보호 대상**:
  - `<예: src/main/resources/.../globals.properties>`
  - `<예: .classpath, .project, .settings>`
- **자동 생성되어 덮어쓰기 위험이 있는 경로**:
  - `<예: CMS/관리자 저장 기능으로 생성되는 JSP 경로>`
- **현재 작업 제외 범위 (별도 담당 등)**:
  - `<예: GNB/LNB 공통 영역, 외부 연계 서브 사이트 등>`

---

## 5. 커밋 및 외부 문서 기준

- **커밋 메시지 형식**: `<예: [TAG][SCOPE][ISSUE-ID] 한 줄 요약>`
- **협업 기준 문서 링크**: `<필요 시 사내 문서/이슈 트래커 URL (로컬 전용)>`
