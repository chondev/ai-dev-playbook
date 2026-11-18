# 모듈: 웹 접근성(KWCAG / WCAG) 구현·검증 기준

- 적용: 웹 접근성 품질인증 및 KWCAG / WCAG / WAI-ARIA 기반 화면 개선 작업
- 상위 지침: [`../AGENTS.md`](../AGENTS.md)

## 1. 구현 판단 순서

1. 기본 HTML 요소만으로 해결 가능한지 먼저 확인한다.
2. 의미에 맞는 시맨틱 요소와 문서 구조를 적용한다.
3. 키보드 동작(`Tab`, `Shift+Tab`, `Enter`, `Space`, `ESC`, 방향키)을 확인한다.
4. 초점 순서·표시(Focus Ring)·이동·복귀를 확인한다.
5. 스크린리더에 이름·역할·상태·값이 전달되는지 확인한다.
6. 기본 HTML만으로 부족할 때만 WAI-ARIA를 적용한다.
7. JavaScript 화면 상태와 ARIA 상태(`aria-expanded`, `aria-selected`, `aria-hidden`, `aria-invalid`, `aria-current`, `aria-checked`, `aria-disabled`)를 동기화한다.

- `div`나 `span`에 클릭 이벤트와 `role`을 붙이기 전에 `<button>`, `<a>`, `<input>` 같은 기본 요소를 사용할 수 있는지 먼저 확인한다.
- 자동 검사 도구(axe 등) 오류 0건만을 목표로 삼지 않고, 실제 키보드 조작 가능성과 정보 이해를 기준으로 판단한다.

## 2. 주요 점검 항목

- 페이지별 고유 `<title>`, 올바른 Heading 계층, 랜드마크, 스킵 내비게이션
- 링크 목적 및 새 창 열림 안내
- 이미지·아이콘 대체텍스트 (`alt`)
- Form `<label>` 연결, `fieldset`/`legend`, 필수 입력 및 오류 메시지 연결
- Modal 초점 이동·내부 순환·닫기 후 호출 요소로 초점 복귀
- Tab / Accordion / Menu / Datepicker / Carousel 키보드 조작 및 상태 전달
- Ajax 처리 결과 및 동적 상태 알림
- 데이터 표 Header 관계 (`th`, `scope`, `caption`)
- 명도 대비, 색상 비의존성, 콘텐츠 선형화
- 200% 확대 및 400% 좁은 화면(반응형) 대응

## 3. 최소 변경 원칙

- 접근성 기준 충족에 필요한 변경 외에는 기존 UI/UX와 비즈니스 로직을 유지한다.
- 심사 필수기준·권고기준·프로젝트 기존 결정 사항을 구분한다.
- 자동 검사 결과만으로 최종 통과(Pass)를 단정하지 않고, 수동 검증 여부와 미수행 항목을 분리 보고한다.
