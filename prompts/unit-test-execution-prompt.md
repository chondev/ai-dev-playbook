# [템플릿] AI 에이전트 기반 엑셀 시나리오 단위테스트 실행 작업 프롬프트

아래 지침을 따라 대상 엑셀 문서의 테스트 시나리오를 읽고, 실제 브라우저 자동화 환경에서 기능 테스트를 수행한 뒤 결과를 엑셀 원본 및 증거 폴더에 기록하라. 단순 소스 검토나 HTTP 응답 코드 확인만으로 실행 결과를 대신하지 않는다.

---

## 0. 실행 설정 파라미터 (작업 시 사용자/작성자가 지정)

```yaml
# [1] 프로젝트 및 다중 환경 프로필 설정
PROJECT_NAME: "대상 프로젝트명"
ACTIVE_ENV: "local"                    # local / dev / stage 중 선택
ENV_PROFILES:
  local:
    base_url: "http://localhost:8080"
  dev:
    base_url: "https://dev.example.com"
  stage:
    base_url: "https://stage.example.com"

EXECUTION_AGENT: "AI Agent + Playwright"
TESTER_NAME: "지정 시험자명"

# [2] 실행 모드 (증분 실행 지원)
EXECUTION_MODE:
  # all / untested_only / failed_only
  run_mode: "all"

# [3] 대상 엑셀 파일 목록
TARGET_EXCEL_FILES:
  - path: "./scenario_file_1.xlsx"
    sheet_name: "단위테스트케이스"
    id_prefix: "SYS-01"

# [4] 엑셀 컬럼 매핑
COLUMN_MAPPING:
  input:
    step_no: "A"
    user_action: "B"
    input_values: "C"
    expected_result: "D"
    prerequisite: "E"
  output:
    tester: "F"
    test_date: "G"
    result: "H"
    remarks: "U"
    evidence: null                     # 전용 열이 있으면 지정 (예: "V")

# [5] 화면 캡처 및 증빙 자료 설정
SCREENSHOT_CONFIG:
  policy: "all"                        # all / failure_only / milestone
  link_method: "hyperlink"             # hyperlink / filename / embed_image
  capture_timing: "after_action"       # after_action / both

# [6] 안정성(Flaky 방지) 및 재시도 설정
STABILITY_CONFIG:
  max_retries: 2
  wait_until: "networkidle"
  retry_delay_ms: 1000

# [7] 웹 접근성(WA) 동시 진단 옵션
A11Y_AUDIT_INTEGRATION:
  enabled: false
  record_summary_in_remarks: true

# [8] 결함(Fail) 발생 시 결함 티켓 자동 생성
DEFECT_REPORTING:
  generate_defect_reports: true

# [9] 도메인 특화 부가 규칙 (필요 시 정의)
DOMAIN_SPECIFIC_RULES:
  session_timeout_minutes: 20
  session_warning_minutes_before: 1
  external_auth_policy: "인증창 호출 여부까지만 검증, 실제 인증은 미수행/부분검증 처리"
```

---

## 1. 목표와 작업 범위

1. **실행 주체와 시험자 표기 구분**:
   - 시험자 열(`output.tester`)에는 지정된 `TESTER_NAME`을 기재하되, 결과 보고서에는 **지정 시험자 / 실제 실행 AI 도구 / 사용자 수동 확인·승인 미수행**을 분리해 명시한다.
2. **실제 브라우저 인터랙션 검증**:
   - 시나리오의 링크 이동, 폼 입력, 탭/모달 전환, 유효성 검증을 실제 브라우저 조작으로 확인한다.
   - `A11Y_AUDIT_INTEGRATION.enabled: true`인 경우 각 화면 로딩 후 `axe-core` 진단을 병행한다.
3. **모바일 에뮬레이션 구분**:
   - PC 브라우저 뷰포트 에뮬레이션으로 확인한 경우 보고서에 **PC 에뮬레이션 검증**임을 명시하고 실제 모바일 기기 검증과 혼동하지 않는다.

---

## 2. 작업 경계와 안전 원칙 (Safety Boundaries)

1. **읽기 및 검증 전용 (Side-Effect 금지)**:
   - **소스 코드·설정 파일·DB 데이터 조작·관리자 저장·결제·신청 최종 제출·VCS 커밋/머지·서버 재시작/배포는 절대 수행하지 않는다.**
   - 결함을 발견해도 소스를 수정하지 않고 재현 절차와 실제 관찰 결과를 기록한다.
2. **개인정보 및 자격증명 보호**:
   - 실제 계정 ID, 비밀번호, 주민등록번호 등 민감 자격증명은 엑셀·프롬프트·스크립트·로그·보고서에 평문으로 저장하지 않는다.
   - 환경변수(`TEST_USER_ID` 등)로 주입받아 사용하고 보고서에는 `테스트 계정 A` 등의 식별명만 기록한다.
3. **엑셀 원본 파일 무결성 보호**:
   - 수정 전 반드시 `backup/` 폴더에 원본을 복사하고 **SHA-256 해시**를 기록한다.
   - 임시 잠금 파일(`~$*.xlsx`)이 있거나 파일이 열려 있으면 강제 덮어쓰기나 삭제를 하지 말고 사용자에게 파일 닫기를 요청한다.

---

## 3. 시험 준비와 실행 원칙

- **증분 필터링**: `run_mode`(`all` / `untested_only` / `failed_only`)에 따라 대상 행만 실행한다.
- **실제 동작 관찰**: HTTP 200 응답이나 정적 HTML 존재만으로 `Pass` 처리하지 않는다.
- **복합 조건 검증**: 한 스텝에 여러 링크·조건이 있으면 모든 하위 동작이 일치해야 `Pass`로 판정한다.
- **타임아웃·외부 인증**: 세션 만료/경고 시험은 실제 시간 경과가 필요하며, 자연 대기를 수행하지 못한 경우 `미검증`으로 남긴다.

---

## 4. 판정 기준 및 엑셀 기록 규칙

| 판정 값 | 정의 및 적용 기준 |
|---|---|
| **Pass** | 요구된 모든 동작과 조건을 실제로 수행했고 예상 결과와 완전히 일치함 |
| **Fail** | 유효한 선행 조건 하에서 실제 화면 동작이나 결과가 예상 결과와 다름 |
| **N/A** | 현재 승인된 적용 범위상 명확히 대상 아님 (계정·데이터·시간 부족은 N/A가 아님) |
| **(공란)** | **미검증 / 부분 검증 / 환경 차단**. 결과 열(`H`)과 시험일자(`G`)를 비우고 비고(`U`)에 사유 명시 |

- **캡처 명명 규칙**: `screenshots/{id_prefix}-STEP-{step_no}_{result}.png`
- **하이퍼링크 연계(`hyperlink`)**: `=HYPERLINK("screenshots/...", "📸 캡처보기")`

---

## 5. 증거 보존, 결함 티켓 및 완료 보고

```text
단위테스트_실행증거_<YYYYMMDD_HHMMSS>/
├── backup/
├── screenshots/
├── defects/
│   └── {id_prefix}-STEP-{step_no}_defect.md
├── a11y-summary.json
├── execution-results.json
└── 단위테스트_실행결과_보고서.md
```

- `Fail` 스텝은 발생 일시, 환경, URL, 선행 조건, 기대/실제 결과, 캡처 이미지, 콘솔 에러 로그를 포함한 `defects/*.md` 티켓을 생성한다.
- 최종 보고 시 **실행 환경/모드, 결과 집계표(전체/Pass/Fail/N/A/미검증), 엑셀 반영 상태, 결함 티켓 목록, 소스·DB·서버 무변경 확인**을 함께 보고한다.
