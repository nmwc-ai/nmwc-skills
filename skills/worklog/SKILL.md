---
name: worklog
description: 업무일지(Worklog) 작성 스킬. 오늘의 git 커밋을 수집해 Obsidian 볼트(~/Documents/Worklog/)에 Daily 항목을 생성한다. "worklog 써", "오늘 일지", "worklog 작성" 요청 시 사용.
---

# Worklog Skill

업무일지를 작성하는 스킬. 오늘의 git 커밋을 수집하고 Obsidian 볼트(`~/Documents/Worklog/`)에 Daily 항목을 생성한다.

## 호출 방법

사용자가 "worklog 써", "오늘 일지", "worklog 작성" 등을 요청할 때 이 스킬을 따른다.

## 실행 절차

### 1단계: git 커밋 수집

```bash
bash scripts/collect-git.sh
```

스크립트가 오늘 날짜의 모든 커밋을 출력한다.

### 2단계: 오늘 날짜 파일 존재 확인

```bash
ls ~/Documents/Worklog/Daily/$(date +%Y-%m-%d).md 2>/dev/null
```

이미 있으면 내용 읽어 이어서 작성. 없으면 신규 생성.

### 3단계: 사용자에게 비-git 작업 확인

git 커밋이 없거나 오프라인 활동(회의, 외부 미팅, 비-git 작업)이 있을 수 있으니 확인:
- "오늘 git 외에 한 일 있어?"
- 사용자가 내용을 말하면 `## 오프라인 활동` 섹션에 추가

### 4단계: Daily 항목 작성

파일 경로: `~/Documents/Worklog/Daily/YYYY-MM-DD.md`

#### 포맷

```markdown
---
date: YYYY-MM-DD
day: 요일 (월/화/수/목/금/토/일)
type: daily
total_commits: N
active_repos: [repo1, repo2]
tags: [decision/adopt, domain/harness]   # 3축 taxonomy 2-5개, 없으면 생략. Concepts/tags-taxonomy.md 참조
---

# YYYY-MM-DD (요일)

## 요약

**[핵심 작업 1~2문장 볼드 요약].** 이어서 세부 내용을 번호 목록으로.

1. **작업명** — 무엇을 했는지 구체적으로. 결과 포함.
2. ...

## 오늘의 결정

**[결정 1]: 제목**
내용.

## 작업 흐름

<!-- git-start -->
- **repo명** `커밋해시` message — 부연 설명
  - 세부 내용
<!-- git-end -->

## 오프라인 활동
<!-- manual-start -->
- 내용
<!-- manual-end -->

## 프로젝트 연결
- [[Projects/노드파일명]] — 한줄 요약   ← 레포명이 아니라 실재 Projects/ 파일명

## 개념 연결
- [[Concepts/concept-name]] — 오늘 작업이 이 패턴을 어떻게 예시했는지 (해당 시에만)
- [[Tasks/task-name]] · [[OKR/2026-Qn-On]] — 관련 태스크·목표 (해당 시에만)

## 내일 이어서

- 항목
```

#### 작성 규칙

- `total_commits`: 오늘 모든 레포 커밋 합산
- `active_repos`: 오늘 커밋이 있는 레포 이름 목록
- `tags`: `Concepts/tags-taxonomy.md`의 3축(`decision/` `domain/` `learning/`)에서 2-5개. over-tagging 금지, 적합한 게 없으면 생략
- `## 요약`: 첫 줄은 **볼드** 핵심 요약. 이후 번호 목록으로 세부 작업
- `<!-- git-start -->` ~ `<!-- git-end -->`: 커밋 정보 그대로 포맷팅
- **`[[Projects/name]]`은 반드시 실재 노드 파일명으로 링크** — 레포명과 노드명이 다를 수 있다. 쓰기 전 `ls ~/Documents/Worklog/Projects/<name>.md`로 확인. 없으면 repo-registry 매핑 확인 → 그래도 없으면 노드를 먼저 만들고 링크. **레포명을 그대로 박지 말 것**(깨진 링크의 흔한 원인)
- `## 개념 연결`: 그날 작업이 기존 `[[Concepts/]]` 패턴을 강하게 예시할 때만 링크. 새 패턴이면 본문에 `(신규 후보)` 텍스트로만 적고, **링크는 실제 Concept 노드를 만든 뒤에만** 건다(깨진 Concept 링크 금지)
- **양방향 위브(그래프 연결의 핵심)**: 어떤 Concept을 강하게 예시했으면, 그 Concept 노드의 `## 근거`에 `[[Daily/YYYY-MM-DD]]` 한 줄을 추가한다. 일지에서 거는 것만으론 Concept 허브가 안 자란다
- git 커밋이 0개면 `total_commits: 0`, `active_repos: []`, 작업 흐름 섹션은 "git 커밋 없음"으로
- 오프라인 활동 없으면 `<!-- manual-start -->`/`<!-- manual-end -->` 블록 비워둠

### 5단계: 저장 확인

파일 저장 후 경로와 커밋 수를 사용자에게 알린다.

## repo → [[Projects/]] 매핑

`references/repo-registry.md` 참조 — **표 우변(노드 파일명)을 그대로 쓴다.**
매핑에 없는 레포는 `ls ~/Documents/Worklog/Projects/`로 실파일을 확인하고 링크한다. **레포명을 그대로 박으면 깨진 링크가 된다.** 실노드가 없으면 노드를 먼저 생성한다.

## push hook 설치

새 레포를 추가하면:
```bash
bash scripts/install-push-hook.sh
```
