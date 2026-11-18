# [예시] 커밋 준비 diff 리포트 (`docs/planning/YYYY-MM-DD/commit-prep.md`)

> 이 문서는 `guidelines/04-commit-record.md` 및 `modules/vcs-svn-windows.md`에 따라 커밋 전 AI가 정리한 **익명화된 커밋 준비 산출물 샘플**입니다.

---

- **대상 작업 사본**: `./app-feature` (기준: `rev-1200`)
- **로컬 상태 점검**: `ignore-on-commit` 대상(`.classpath`, `globals.properties`) 변경 없음, 커밋 대상 외 파일 미포함

## 1. 작업 단위별 변경 요약

| 작업 ID | 수정 파일 | 핵심 변경 | 검증 상태 |
|---|---|---|---|
| `APPLY-01` | `WEB-INF/jsp/app/apply/registForm.jsp` | `#applicantPhone` `<label>` 연결 및 검증 실패 시 초점 이동 보완(동기 `return false` 유지) | `python tools/jsp_tag_attr_check.py src/main/webapp/WEB-INF` → `hits 0` (변경한 `registForm.jsp` 포함 확인). 로컬 브라우저에서 폼 제출 차단 확인. 스크린리더 미검증. |

## 2. 커밋 메시지 초안

```text
[A11Y][APP][APPLY-01] 신청 폼 연락처 레이블 연결 및 오류 초점 보완

목적: 필수 입력 필드 스크린리더 인식 및 검증 실패 시 초점 복귀 보완
수정 파일: WEB-INF/jsp/app/apply/registForm.jsp (1개 파일)
정적 검사: jsp_tag_attr_check.py src/main/webapp/WEB-INF → hits 0 (변경한 registForm.jsp 포함 확인)
화면 검증: 로컬 브라우저에서 폼 제출 차단·Tab 이동 확인 (스크린리더 미검증)
```

## 3. 커밋 실행 명령 예시 (Windows UTF-8 인코딩 보존)

```powershell
# SVN 사용 시 CP949 콘솔 깨짐 방지를 위해 --encoding UTF-8 필수 지정
svn commit -F docs/planning/YYYY-MM-DD/commit-msg-apply01.txt --encoding UTF-8 src/main/webapp/WEB-INF/jsp/app/apply/registForm.jsp
```
