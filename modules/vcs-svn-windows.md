# 모듈: Windows 환경 SVN 운영·커밋 규칙

- 적용: Windows(로케일 CP949 등) 환경에서 SVN 작업 사본을 다루는 프로젝트
- 상위 지침: [`../AGENTS.md`](../AGENTS.md)

## 1. 인코딩 가드 (실행 전 필수 확인)

Windows 콘솔 환경에서 UTF-8로 작성한 커밋 메시지 파일을 옵션 없이 넘기면 콘솔 로케일로 오해석되어 저장소에 한글 깨짐(mojibake)으로 기록될 수 있다.

- 커밋 시 반드시 `--encoding UTF-8`을 포함한다.
  ```bash
  svn commit -F commit_msg.txt --encoding UTF-8 <targets...>
  ```
- 리비전 속성을 수정할 때도 동일하게 인코딩을 지정한다.
  ```bash
  svn propset svn:log --revprop -r <rev> --encoding UTF-8 -F commit_msg.txt <URL>
  ```
- 과거 로그를 조회해 한글 커밋 메시지를 읽을 때는 `svn log --xml` 출력을 사용한다.

## 2. 로컬 변경 보호 (`ignore-on-commit`)

- 수정 전후 `svn status --no-ignore`로 작업 범위를 확인한다.
- 환경설정 파일(`properties`), IDE 설정(`.classpath`, `.project`, `.settings`), 빌드 산출물(`target`, `bin`)이 커밋 대상에 섞이지 않도록 `ignore-on-commit` 체인지리스트 또는 명시적 대상 지정을 유지한다.

## 3. 커밋 단위 및 메시지 템플릿

하나의 목적, 독립 검증 가능 여부, 의존 파일군(예: JSP + 전용 CSS/JS) 완결성을 기준으로 커밋 후보를 묶는다.

```text
[TAG][SITE_OR_SCOPE][ISSUE-ID or 이슈없음] 변경 내용 한 줄 요약

목적: 왜 변경했는지 1줄
수정 파일: 주요 대상 파일 (전체 나열 불필요 시 대표 파일 + 개수)
검증: 실제로 확인한 방법 (정적/브라우저/키보드 등, 한 줄)
```

- 트렁크/메인 동기화 병합 커밋은 `Merge trunk r... into ...` 등 기존 병합 메시지 형식을 유지한다.
