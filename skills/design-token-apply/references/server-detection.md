# 0단계 — 서버 식별

## 탐지 규칙

세션에 연결된(또는 ToolSearch로 로드 가능한) MCP 도구 이름을 `mcp__<server>__<tool>` 패턴으로 스캔한다. 다음 5개 도구명 중 **최소 4개**가 같은 `<server>` 프리픽스로 존재하면 그 서버를 후보로 삼는다:

```
get_token, get_component, validate_code, suggest_token, scaffold
```

(`search_guidelines`는 있으면 좋지만 필수 카운트에는 넣지 않는다.)

도구가 아직 deferred 상태(system-reminder에 이름만 나열)라면, 먼저 `ToolSearch({query: "select:mcp__<server>__get_token,mcp__<server>__get_component,mcp__<server>__validate_code,mcp__<server>__suggest_token,mcp__<server>__scaffold"})`로 스키마를 로드한 뒤 사용한다.

## 분기

- **후보 서버 1개** — 그대로 사용, 사용자에게 확인받지 않는다.
- **후보 서버 0개** — 중단하고 안내: "MCP 디자인시스템 서버가 안 보입니다. `.mcp.json`에 등록되어 있는지 확인해주세요." static fallback은 만들지 않는다.
- **후보 서버 2개 이상** — `AskUserQuestion`으로 1회 질문("어느 디자인시스템을 기준으로 작업할까요?" + 후보 서버명 옵션). 선택 결과를 프로젝트 메모리에 `type: project`로 저장해(예: `project_memory_write` 도구 또는 `.claude/projects/<cwd>/memory/`) 다음 세션부터 재질문하지 않는다.

## 부분 지원

5개 중 일부만 있는 서버(예: `scaffold` 없음)는 후보에서 제외하지 않되, 사용 불가한 단계는 건너뛰고 어떤 기능이 제한되는지 작업 시작 전에 한 줄로 안내한다.
