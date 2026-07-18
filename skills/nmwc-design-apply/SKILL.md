---
name: nmwc-design-apply
description: MCP 기반 디자인 토큰/컴포넌트 계약(get_token·get_component·validate_code·suggest_token·scaffold 패턴)을 자동 탐지해 새 UI를 제작하거나 기존 코드를 토큰 규격으로 폴리싱한다. "디자인 폴리싱", "토큰 적용해줘", "디자인 시스템 적용해줘", "이 페이지 토큰화", "apply design tokens", "polish this page to the design system" 요청 시 사용.
---

# 디자인 토큰 적용 (nmwc-design-apply)

MCP로 노출된 디자인 토큰/컴포넌트 계약을 갖춘 프로젝트라면 어디서든 동작하는 범용 스킬이다. 새 UI를 스캐폴딩하거나(제작 모드) 기존 코드의 raw 값을 토큰으로 치환한다(폴리싱 모드). 어느 모드인지는 요청 대상을 보고 스스로 판단한다 — 사용자가 모드를 지정할 필요 없다.

## 전제

세션에 다음 도구 패턴 중 최소 4종(`search_guidelines`는 선택, 카운트에서 제외)을 제공하는 MCP 서버가 연결되어 있어야 한다: `get_token` · `get_component` · `validate_code` · `suggest_token` · `scaffold`. 없으면 0단계에서 중단한다 — 이 스킬은 static bundle(design.json 직접 fetch) 폴백을 제공하지 않는다.

## 흐름

```
0. 서버 식별 → 1. Discover → 2. Reference → 3. Apply → 4. Verify → 5. (선택) Visual QA
```

각 단계 상세는 아래 참고 문서를 **반드시 읽고** 따른다. 요약만 보고 진행하지 않는다.

| 단계 | 문서 | 내용 |
|---|---|---|
| 0. 서버 식별 | `references/server-detection.md` | 도구명 컨벤션 자동탐지, 모호 시 질문+캐시 |
| 1-4. 제작 모드 | `references/build-mode.md` | 신규 파일/컴포넌트 스캐폴딩 |
| 1-4. 폴리싱 모드 | `references/polish-mode.md` | 기존 코드 감사·토큰화 + 검증 게이트 |
| 에러 처리 | `references/edge-cases.md` | 컴포넌트 부재, 부분 지원, 스코프 경계 |

## 스코프 경계

- 색·타이포·radius·spacing·컴포넌트 같은 **시각/토큰 레이어만** 다룬다.
- 카테고리 번호, 네비게이션 구조는 건드리지 않는다 — 프로젝트 CLAUDE.md가 관리하는 영역이다.
- 카피·보이스톤(피해야 할 단어 등)은 건드리지 않는다 — 별도 카피 스킬의 영역이다.
- 브라우저 시각 확인이 필요하면 직접 구현하지 않고 이미 연결된 브라우저 자동화 스킬(예: 세션에 `gstack-browse`나 `webapp-testing`이 있으면 그것)에 위임한다.

## 완료 기준

폴리싱 모드는 `validate_code`/lint violation이 0이거나, 최대 3회 재시도 후에도 남은 항목을 사용자에게 명시적으로 보고했을 때만 "완료"로 본다. 위반이 남아 있는데 완료라고 보고하는 것은 금지.
