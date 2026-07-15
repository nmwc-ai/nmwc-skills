---
name: wl-week
description: 이번 주(또는 지정한 ISO week) Daily를 모아 주간 회고 노트(shipping streak·프로젝트별 활동·다음 주 포커스·도구별 사용)를 작성한다. "이번 주 회고 작성해줘", "주간 정리해줘", "wl-week 돌려줘" 요청 시 사용.
---

# 주간 회고 롤업

이번 주(또는 사용자가 지정한 ISO week) Daily 항목을 모아 **운영 회고**를 만든다.
`Daily/`를 소스로 롤업한다.

> **wl-insights와 구분**: 이 스킬은 *이번 주 운영 롤업*(무엇을 shipped/얼마나 꾸준히).
> wl-insights는 *30일 패턴·Concept 추출*(왜·어떤 원리). 둘을 섞지 않는다.

## 실행 절차

### 1단계: 주간 범위 산정

- 지정 없으면 이번 주(ISO week, 월~일). 사용자가 `YYYY-WNN`을 지정하면 해당 주.
- 범위 내 `Daily/YYYY-MM-DD.md` 전부 수집 (없는 날은 "활동 없음"으로 streak 계산에 반영).

### 2단계: 4개 섹션 생성

Daily frontmatter(`total_commits`, `active_repos`, `tags`)와 본문을 롤업한다:

1. **Shipping streak** — 한 주 중 활동(커밋/오프라인 작업)이 있던 날 연속/총합. 예: `5/7일 활동, 최장 연속 4일`.
2. **프로젝트별 활동** — `active_repos`를 `repo-registry.md`로 `Projects/<node>`에 매핑(레포명 직박 금지). 프로젝트별 커밋 수·핵심 작업 1줄.
3. **다음 주 포커스** — 각 Daily `## 내일 이어서` + 미완 Task를 모아 다음 주 할 일로 정리.
4. **도구별 사용 (tool usage)** — 한 주간 사용한 워크플로우/스킬/커맨드 빈도 (예: autopilot N회, advisor N회, wl-insights, gstack qa 등). `tags`와 본문에서 집계.

상세 산출 규칙(섹션별 집계 방법·트렌드 비교)은 `references/wl-week-extended.md`에 위임한다.

### 3단계: Weekly 노트 작성

경로: `~/Documents/Worklog/Weekly/YYYY-WNN.md`
(구 형식 `Daily/YYYY-WNN-weekly.md`는 폐기됨 — `Weekly/` 사용.)

### 4단계: system-log 기록

`system-log.md`에 `## YYYY-MM-DD week | wl-week YYYY-WNN 주간 회고` 항목 append.

## 출력 템플릿

```markdown
---
week: YYYY-WNN
type: weekly
range: YYYY-MM-DD ~ YYYY-MM-DD
total_commits: N
active_projects: [project1, project2]
---

# YYYY-WNN 주간 회고 (MM-DD ~ MM-DD)

## Shipping streak
- 활동 X/7일 · 최장 연속 Y일 · 총 커밋 N
- (지난 주 대비 ↑/↓ — wl-week-extended 트렌드)

## 프로젝트별 활동
- [[Projects/<node>]] — N commits · <핵심 작업 1줄>

## 다음 주 포커스
- [ ] <Daily 「내일 이어서」/미완 Task에서 모은 항목>

## 도구별 사용
- autopilot ×N · advisor ×N · wl-insights ×N · <기타>
```

## 검증 체크리스트

- [ ] 주간 범위를 ISO week로 정확히 산정했는가?
- [ ] `active_repos`를 `repo-registry.md`로 매핑해 실재 `Projects/<node>`에 위키링크했는가? (레포명 직박 금지)
- [ ] 4개 섹션(streak·프로젝트별·다음 주·도구별)을 모두 채웠는가?
- [ ] `Weekly/YYYY-WNN.md` 경로에 썼는가? (구 `Daily/...-weekly.md` 아님)
- [ ] `system-log.md`에 기록했는가?
