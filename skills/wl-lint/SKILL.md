---
name: wl-lint
description: worklog 볼트 건강도를 점검한다. 깨진 링크·frontmatter·고아 Daily·Concept drift 등 a~j 10개 항목 검사 후 점수(예 B 78/100)와 자동 수정 후보를 보고한다. 사용자가 자동 수정을 요청하면 기계적으로 고칠 수 있는 항목만 실제로 수정한다. "worklog 건강도 점검해줘", "볼트 lint 돌려줘", "깨진 링크 있는지 확인해줘" 요청 시 사용.
---

# Worklog 볼트 Lint (건강도 점검)

볼트(`~/Documents/Worklog/`)의 정합성을 a~j 10개 항목으로 검사하고
점수 리포트를 낸다. 사용자가 자동 수정을 요청하면 **자동 수정 가능 항목만** 실제로 고친다.

> 검사 a~f는 기존 항목, g~j는 이후 추가된 항목. **태그(tags)는 의도적으로 검사하지 않는다** — 강제 시 over-tagging drift를 유발하기 때문.

## 실행 절차

### 0단계: 볼트 스캔

```bash
ls ~/Documents/Worklog/Daily/ ~/Documents/Worklog/Projects/ ~/Documents/Worklog/Concepts/ ~/Documents/Worklog/Tasks/ ~/Documents/Worklog/OKR/
```
- Daily / Projects / Concepts / Tasks / OKR 파일 목록과 frontmatter, 본문 섹션, 위키링크를 수집한다.
- 추정 금지 — 실제 파일을 읽어 카운트한다.

### 1단계: 기존 검사 a~f

| # | 검사 | 위반 조건 | 통과(whitelist) |
|---|------|-----------|------------------|
| **a** | OKR 연결 | Project frontmatter `okr` 빈 문자열/빈 배열 | `okr: 2026-Qn-On` 또는 sentinel `external`·`personal` |
| **b** | 비활성/stale | `status: in-progress`인데 Project 14일+·Task 21일+ 무활동 | 활동 있음, `status: done/on-hold` |
| **c** | Daily 일지 품질 | Daily에 `## 오늘의 결정` 섹션 없음(현행 템플릿 채택 이후 작성분만) | 구형 템플릿 작성분은 제외 |
| **d** | git 마커 정합 | `<!-- git-start/end -->`·`<!-- manual-start/end -->` 짝 깨짐 | 마커 짝 정합 |
| **e** | frontmatter 카운트 정합 | `total_commits`/`active_repos`가 실제 `## 작업 흐름` 블록과 불일치 | 일치 |
| **f** | 깨진 위키링크 | raw `[[slug]]` placeholder·미생성 노드·삭제된 Project 참조 | 백틱 감싼 예시 `` `[[slug]]` ``, archive prefix |

### 2단계: 추가 검사 g~j

> **g. 고아 Daily 감지**
> - 어느 Project `## 최근 활동`에도, 어느 Concept `## 근거`에도 링크되지 않은 Daily
> - **권장**: 해당 Daily 본문의 `## 프로젝트 연결`을 재확인하고 Project "최근 활동"을 소급 업데이트
> - 예외: `total_commits: 0` 빈 일지(주말/휴식)는 통과 — false positive 회귀 방지

> **h. Daily `## 프로젝트 연결` 섹션 검사**
> - 템플릿 필수 섹션(`## 프로젝트 연결`, `## 내일 이어서`) 누락 파일
> - **자동 수정 가능**: git 데이터 있으면 Project 추론 후 섹션 생성

> **i. Concept sources counter drift**
> - `frontmatter.sources != 본문 ## 근거의 [[Daily/ 개수`
> - **자동 수정**: frontmatter 갱신

> **j. Concept isolation 감지**
> - `## 관련 개념` 섹션이 없거나 비어있는 Concept
> - **플래그만**(자동 수정 금지, 의미 판단 필요). wl-insights에서 후보 제안으로 이어짐

### 3단계: 자동 수정 vs 플래그 분류

각 위반을 **자동 수정**(기계적)과 **플래그**(사람 판단 필요)로 분류한다:

| 항목 | 행동 | 이유 |
|------|------|------|
| 고아 Daily (g) | **플래그** | Project/Concept 할당 판단 필요 |
| Daily 섹션 누락 (h) | **자동 수정** | git 활동 기반 추론 가능 |
| Concept sources drift (i) | **자동 수정** | 기계적 count |
| Concept isolation (j) | **플래그** | 의미상 연결 판단 필요 |

- 자동 수정: e(카운트 재계산), f(명백한 placeholder 백틱 감싸기)
- 플래그: a(OKR 매핑 결정), b(stale status 판단), c·d(템플릿/마커 — 맥락 확인 후 보강)

### 4단계: 건강도 리포트

```
## 🩺 Worklog Lint 리포트  (YYYY-MM-DD)

| # | 검사 | 위반 | 자동수정 | 플래그 |
|---|------|------|----------|--------|
| a | OKR 연결          | N | - | N |
| b | 비활성/stale      | N | - | N |
| c | Daily 일지 품질   | N | - | N |
| d | git 마커 정합     | N | N | - |
| e | 카운트 정합       | N | N | - |
| f | 깨진 위키링크     | N | N | N |
| g | 고아 Daily        | N | - | N |
| h | Daily 섹션 누락   | N | N | - |
| i | Concept drift     | N | N | - |
| j | Concept isolation | N | - | N |

종합 점수: **B (78/100)**
- 자동 수정 가능: N건  →  자동 수정 요청 시 일괄 처리
- 사람 판단 필요(플래그): N건
```

점수 기준: A 90+ / B 80-89 / C 70-79 / D 60-69 / F 60 미만.

### 5단계: 자동 수정 모드 (사용자가 요청했을 때만)

사용자가 자동 수정을 요청하면 **자동 수정 분류 항목만** 실제로 편집한다:
- h: 누락 템플릿 섹션을 git 활동 기반으로 backfill
- i: Concept frontmatter `sources`를 본문 `## 근거` 개수로 재계산
- e: `total_commits`/`active_repos` 재계산
- f: 명백한 placeholder `[[slug]]`를 백틱으로 감쌈

플래그 항목(a, b, c, g, j)은 자동 수정으로도 건드리지 않고 리포트에만 남긴다.
Daily 작성/섹션 backfill 로직은 worklog 스킬(4단계)을 참조·위임한다.

수정 후 1줄 요약:
```
> 자동 수정: h N건 · i N건 · e N건 · f N건. 플래그 N건은 수동 검토 필요.
```

## 검사하지 않는 것 (의도적 제외)

- **태그(tags)**: 강제 시 over-tagging drift 유발 → 검사 제외(설계 결정)
- gbrain 임베딩 커버리지: lint 범위 밖(`gbrain doctor`로 별도 확인)

## 검증 체크리스트

- [ ] 실제 파일을 `ls`/Read로 스캔했는가? (추정 금지)
- [ ] a~j 10개 항목을 모두 검사했는가?
- [ ] 위키링크 검사 시 백틱 감싼 예시를 whitelist 했는가? (false positive 방지)
- [ ] 고아 Daily 검사에서 `total_commits: 0` 빈 일지를 예외 처리했는가?
- [ ] 플래그 항목을 자동 수정으로 건드리지 않았는가?
- [ ] 태그는 검사하지 않았는가?
