# [예시] 읽기 전용 분석 보고서 (`docs/analysis/YYYY-MM-DD-form-validation-audit.md`)

> 이 문서는 `guidelines/01-analysis.md` 및 `modules/legacy-web-guardrails.md`를 적용해 AI가 생성한 **익명화된 분석 보고서 샘플**입니다.  
> 실제 프로젝트에서는 이처럼 `docs/analysis/` 아래에 날짜별 Markdown으로 저장해 팀원·후속 에이전트와 공유합니다.

---

- **점검 일자**: YYYY-MM-DD
- **대상 작업 사본**: `./app-feature` (기준 커밋/리비전: `rev-1200`)
- **대상 화면**: 회원 신청 폼 (`/apply/form.do`)
- **소스 변경 여부**: **소스는 수정하지 않았다** (읽기 전용 분석)

## 1. 호출 구조 추적

```text
/apply/form.do
  → ApplyController.formView() → 반환 View: "app/apply/registForm.sub"
  → tiles-defs.xml (**/*.sub 매핑)
  → Layout: /WEB-INF/jsp/layout/sub_layout.jsp
  → Body: /WEB-INF/jsp/app/apply/registForm.jsp
  → 공통 JS: /js/common-validator.js
```

## 2. 확인된 문제 원인

1. **동기식 폼 검증 누락 위험**
   - `registForm.jsp`의 `<form onsubmit="return checkApplyForm();">`는 동기 boolean 반환(`false`)에 의존함.
   - 모달 알림 도입 시 `checkApplyForm()`을 `async`로 바꾸면 `Promise`(truthy)가 반환되어 검증 실패 시에도 서버로 제출될 위험이 있음.
2. **접근성 레이블 및 오류 안내 미연결**
   - 필수 입력 필드(`#applicantPhone`)에 `<label for="...">`가 연결되지 않았고, 오류 발생 시 해당 필드로 초점이 이동하지 않음.

## 3. 수정 예정 파일 vs 참고 파일 구분

- **참고만 한 파일**: `ApplyController.java`, `tiles-defs.xml`, `sub_layout.jsp`
- **실제 수정 후보**: `WEB-INF/jsp/app/apply/registForm.jsp` (단일 화면 최소 변경)

## 4. 개선 대안 및 권장 검증 항목

- **개선안**: 기존 `var`/`function` 문법과 `return false;` 동기 반환 구조를 유지한 채 `<label for="applicantPhone">` 추가 및 알림 확인 후 `$('#applicantPhone').focus()` 호출 순서 보완.
- **권장 수동 검증**:
  1. 필수값 공란 상태에서 제출 클릭 시 Alert 표출 및 폼 전송 차단 확인
  2. 브라우저 Console `SyntaxError` / `TypeError` 0건 확인
  3. `Tab` / `Shift+Tab` 이동 및 오류 후 초점 이동 확인
- **현재 확인 범위에 포함되지 않음**: 로그인 세션 연동 이후 단계 및 결제 PG 콜백 흐름(실행 환경 미기동으로 미검증).
