---
name: wl-concept
description: worklog 볼트 Concepts/ 의 Karpathy식 개념 노트를 생성·갱신한다. 근거 백링크·관련 개념 양방향 위브·sources 카운터 동기화를 관리한다. "이 패턴 개념으로 박제해줘", "Concept 노트 만들어줘", "이 개념 근거 추가해줘" 요청 시 사용.
---

# Concept 노트 관리

`Concepts/`의 개념 노트를 만들거나 갱신한다. 개념 노트는 여러 Daily에서 반복 관찰된 **작업 패턴·교훈**을 박제하는 Karpathy식 second-brain 노드다.

> **경계 (vs wl-insights)**: wl-insights는 최근 Daily를 스윕해 **개념 후보를 제안**(propose)만 한다. wl-concept는 실제 노트를 **생성·편집**(create/edit)한다. 둘 다 `Concepts/`를 건드리므로 역할을 섞지 말 것.

## 환경 사실

- 볼트: `~/Documents/Worklog/Concepts/`.
- Concept 노트 구조는 아래 템플릿이 유일한 규약 원천이다(별도 규약 파일에 의존하지 않는다).

## Concept 노트 구조

```markdown
---
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: N          # 본문 ## 근거의 [[Daily/ 개수와 항상 일치
---

# <개념명>: <한 줄 정의>

## 패턴 설명
[이 패턴이 무엇이고 왜 반복되는지 — 구체 사례 인용]

## 근거
- [[Daily/YYYY-MM-DD]] — 이 Daily가 패턴을 어떻게 예시했는지 1줄
- ... (N개, sources 카운터와 일치)

## 관련 프로젝트
- [[Projects/노드명]]

## 관련 개념
- [[Concepts/다른개념]] — 의미상 가까운 지점 1줄 (양방향)

## 시사점
[이 패턴에서 끌어낼 운영 룰·교훈]
```

---

## 실행 절차

### 1단계: 대상 판별 (생성 vs 갱신)

사용자가 지정한 개념명(또는 갱신 대상)으로 존재 여부를 확인한다.

```bash
ls ~/Documents/Worklog/Concepts/<slug>.md 2>/dev/null
```

- 있으면 → 갱신 모드(hashline_read로 현재 상태 확보).
- 없으면 → 생성 모드(위 템플릿으로 신규). slug는 영문 kebab-case.

### 2단계: 근거 백링크 갱신 (`## 근거`)

- 이 개념을 강하게 예시한 Daily를 `## 근거`에 `[[Daily/YYYY-MM-DD]] — 1줄` 형태로 추가한다.
- **양방향 위브 (핵심)**: 어떤 Daily가 이 개념을 강하게 예시하면, 그 Daily의 `## 개념 연결`에도 `[[Concepts/<slug>]]`를 추가한다. 한쪽만 걸면 허브가 자라지 않는다.
- 깨진 링크 금지: 실재하는 `Daily/` 파일만 링크. 신규 개념을 Daily에서 가리키려면 이 노트를 먼저 만든 뒤 링크.

### 3단계: sources 카운터 동기화

- `frontmatter.sources` == `## 근거`의 `[[Daily/` 개수가 되도록 맞춘다.
- `updated`를 오늘 날짜로 갱신.

### 4단계: 관련 개념 양방향 링크 (`## 관련 개념`)

- 다른 Concept과 의미상 가까우면 `## 관련 개념`에 `[[Concepts/타개념]] — 가까운 지점 1줄`을 추가하고, **상대 Concept에도 역방향 링크를 동시에 추가**한다(양방향 필수).
- 후보 발굴: 공유 Daily 근거 수 / Jaccard 기준으로 가까운 쌍 상위에서 고른다(단발 갱신 시 직접 후보 1~2개 제시로 충분).
- **over-linking 금지**: 자동 대량 생성하지 말고 의미상 명확한 것만. 빈 `## 관련 개념`은 고립 노드로 플래그 대상.

### 5단계: 시사점 정리

- `## 시사점`에 이 패턴의 load-bearing 단언과 운영 룰을 정리. 갱신 시 새 사례가 기존 시사점을 강화/반증하면 반영.

### 6단계: 인덱스·로그

- `index.md`의 Concepts 카운트/목록과 어긋나면 갱신.
- `system-log.md`에 `## YYYY-MM-DD update | Concept <slug> 생성/갱신 ...` 1줄 append.

---

## 검증 체크리스트

- [ ] `frontmatter.sources` == `## 근거`의 `[[Daily/` 개수인가? (drift 0)
- [ ] `## 근거`의 모든 `[[Daily/]]`가 실재 파일인가? (깨진 링크 0)
- [ ] 양방향 위브 완료 — 근거 Daily의 `## 개념 연결`에도 이 개념이 걸렸는가?
- [ ] `## 관련 개념` 링크가 양쪽 Concept에 모두 추가됐는가? (단방향 0)
- [ ] `## 관련 개념`이 비어있지 않은가? (isolation 플래그 회피)
- [ ] wl-insights 영역(후보 제안)을 침범하지 않았는가? (이 스킬은 확정·편집만)
