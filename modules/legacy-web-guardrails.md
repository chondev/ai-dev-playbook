# 모듈: 레거시 웹 시스템 AI 안전 가드레일

- 적용: Java 8 / Spring MVC / JSP·JSTL / Apache Tiles / jQuery 1.12.x 등 레거시 웹 환경
- 상위 지침: [`../AGENTS.md`](../AGENTS.md)

## 1. 기술 환경 유지 원칙

- 기존 기술 스택(Java 8, Spring MVC, JSP/JSTL, Tiles, jQuery 1.12.x, 기존 DB 방언)을 유지한다.
- 새로운 프레임워크(Spring Boot, React/Vue 등)나 불필요한 의존성(`pom.xml` 등)을 임의로 추가하지 않는다.
- 파일이 최근에 작성됐다는 이유만으로 ES6+ 문법을 프로젝트 표준으로 단정하지 않는다.

## 2. 절대 피해야 할 4대 고위험 패턴

### 2.1. 레거시 런타임 비호환 문법 생성
- **위험**: 화살표 함수(`() => {}`), `let`/`const`, `async`/`await`, `Promise`, 옵셔널 체이닝(`?.`), 널 병합(`??`) 등
- **장애 결과**: 구버전 브라우저 및 jQuery 1.12.x 환경에서 `SyntaxError`가 발생해 페이지 스크립트 전체가 멈춘다.
- **규칙**: 기존 `var` 및 `function()` 선언 방식과 호환 API를 유지한다.

### 2.2. 동기식 폼 검증 파괴 (`return false;` 무력화)
- **위험**: `<form onsubmit="return validate();">` 또는 `onclick="if(!check()) return false;"` 구조의 검증 함수를 `async`로 변경하는 경우
- **장애 결과**: `async` 함수는 항상 truthy인 `Promise` 객체를 반환하므로, 입력값 검증에 실패해도 폼이 즉시 서버로 전송되는 장애가 발생한다.
- **규칙**: 기존 동기식 반환(`return false;`) 흐름을 임의로 비동기로 바꾸지 않는다. 커스텀 알림 모달로 전환할 때도 호출 순서를 조정해 동기 반환을 보존한다.

### 2.3. 코어 비즈니스 로직 과잉 리팩터링 (Scope Creep)
- **위험**: 화면 품질/접근성 수정 중 Controller 매핑, SQL 호출, 폼 파라미터명(`name`, `id`, `hidden`), `onclick` 비즈니스 로직까지 임의 변경
- **장애 결과**: 서버 측 `CommandMap`·DTO 매핑이 깨져 데이터 누락이나 결제·신청 오류가 발생한다.
- **규칙**: 요청된 결함 요소만 외과수술식으로 최소 변경하고, `form action`, `name`, `id`, `value`, submit 방식, 서버 전송 파라미터를 유지한다.

### 2.4. Tiles 및 다중 레이아웃 오판
- Controller가 반환하는 View 이름만 보고 실제 JSP 경로를 단정하지 않는다.
- 레이아웃 정의 파일(`tiles-defs.xml` 등)의 와일드카드·suffix 치환 규칙을 확인해 실제 렌더링되는 `body`, `header`, `footer` 파일을 특정한 뒤 수정한다.
