---
name: wl-backfill
description: 누락된 날짜의 Daily 일지를 git 로그 기반으로 백필한다. 커밋이 있으면 정상 일지, 없으면 정직한 최소 placeholder를 생성한다. "며칠 전 일지가 빠졌어", "이 날짜 백필해줘", "누락일 채워줘" 요청 시 사용.
---

# 누락일 일지 백필

갭(누락일)을 발견했을 때 해당 날짜의 Daily 항목을 **사실 기반으로** 채운다.
핵심 원칙: **활동을 지어내지 않는다.** git 로그가 0건이면 0건짜리 정직한 placeholder를 만든다.
백필 항목은 `<!-- auto-backfilled YYYY-MM-DD -->` 센티넬로 표시되어 추후 서사로 재작성 가능하고,
wl-lint·wl-insights·wl-ask가 이 항목의 신뢰도를 디스카운트(confidence 0.5)한다.

## 실행 절차

### 1단계: 날짜 확인 + 중복 확인

사용자가 알려준 날짜(`YYYY-MM-DD`)를 받는다. 불명확하면 날짜를 요청하고 중단.

```bash
DATE="<YYYY-MM-DD>"
ls ~/Documents/Worklog/Daily/$DATE.md 2>/dev/null
```

이미 파일이 존재하면 **덮어쓰지 말고** 그 사실을 알린 뒤 중단(백필은 누락일 전용).

### 2단계: 해당 날짜 git 로그 수집 (KST 00:00~23:59)

`collect-git.sh`는 첫 인자로 날짜를 받아 그날 `00:00:00`~`23:59:59` 윈도우의 커밋만 수집한다.
모든 활성 레포(`~/Documents/Work/<회사>/Project/**` — repo-registry.md 참조)를 고정 깊이 glob으로 열거한다.

```bash
bash scripts/collect-git.sh "$DATE"
```

출력 끝의 `---SUMMARY---` 블록에서 `total_commits` / `active_repos`를 확인한다.

### 3단계: 분기 — 커밋 유무로 결정

#### 3-A. 커밋이 있으면 → 정상 Daily 작성

worklog 스킬의 작성 흐름에 **위임**한다(Daily 로직 중복 구현 금지).
단, 오늘이 아니라 `$DATE` 기준으로 작성하고, frontmatter `date:`/`day:`를 `$DATE`에 맞춘다.
`[[Projects/]]` 링크는 repo-registry.md 우변(노드 파일명)으로만 건다(레포명 직박 금지).

작성 후 **2단계 이하**(센티넬·백필 노트)를 동일하게 적용한다 — 백필은 git 로그 회상이지 실시간 기록이 아니므로 표시한다.

#### 3-B. 커밋이 0건이면 → 정직한 최소 placeholder

활동을 **추측하거나 발명하지 않는다.** git 0건은 "쉰 날" 또는 "비-git 작업일"이며, 후자는 추후 wl-note로 보충한다.
아래 템플릿으로 최소 항목만 생성한다.

```markdown
---
date: YYYY-MM-DD
day: 요일
type: daily
total_commits: 0
active_repos: []
tags: #placeholder/no-activity
---
<!-- auto-backfilled YYYY-MM-DD -->

# YYYY-MM-DD (요일)

## 오늘의 결정

(Git 활동 없음 — 추후 wl-note로 오프라인 활동 보충 가능)

## 작업 흐름

<!-- git-start -->

활성 레포 0개 / 커밋 0건.

<!-- git-end -->

## 오프라인 활동
<!-- manual-start -->

(공란 — 회의·외부 도구 작업·휴식 등은 wl-note로 추가)

<!-- manual-end -->

## 프로젝트 연결

(없음)

## 내일 이어서

(없음 — 다음 작업일 [[Daily/YYYY-MM-DD]] 참조)

---

> ⚙️ 백필 노트: [발견 경위] [[Daily/<직전일>]] → [[Daily/<직후일>]] 갭 발견, wl-backfill YYYY-MM-DD 실행으로 placeholder 생성. 모든 활성 레포 YYYY-MM-DD KST 00:00~23:59 git log 0건 확인 후 최소 일지 형식으로 백필.
```

### 4단계: 정직성 가드 (필수)

- **절대 금지**: git 로그에 없는 작업·결정·커밋을 placeholder에 채워 넣기.
- placeholder는 미래의 wl-ask 답변을 오염시키지 않아야 한다 — 비어 있는 게 거짓보다 낫다.
- 확실하지 않은 활동은 `## 오프라인 활동`을 공란으로 두고 wl-note로 나중에 보충하도록 안내한다.
- `<!-- auto-backfilled YYYY-MM-DD -->` 센티넬을 **반드시** 남긴다(부재 시 lint/insights/ask 디스카운트가 작동하지 않음).

### 5단계: system-log 기록 + 저장 확인

append-only 변경이력에 한 줄 남긴다.

```
## YYYY-MM-DD ingest (backfill) | Daily/YYYY-MM-DD.md 생성
- <직전일> → <직후일> 갭 백필. collect-git <DATE>: total_commits N. <placeholder | 정상 작성>.
```

저장 경로와 커밋 수를 사용자에게 알린다.

## 검증 체크리스트

- [ ] `collect-git.sh "$DATE"`를 **실제 실행**해 해당 날짜 커밋을 수집했는가? (추정 금지)
- [ ] 커밋 0건일 때 활동을 **발명하지 않고** 최소 placeholder만 만들었는가?
- [ ] `<!-- auto-backfilled YYYY-MM-DD -->` 센티넬을 남겼는가?
- [ ] `total_commits` / `active_repos`가 collect-git 실측과 일치하는가?
- [ ] `[[Projects/]]` 링크가 실재 노드 파일명인가? (레포명 직박 아님)
- [ ] 이미 존재하는 Daily를 덮어쓰지 않았는가?
