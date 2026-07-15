---
name: nmwc-prd
description: NMWC 팀 공통 규격의 PRD(제품 요구사항 문서)를 작성한다. Background·Goal·Hypothesis·Principles·Scope에 더해, 핵심인 Epic → User Story(US-x.y) → 인수 조건(AC)을 상세히 만들고, 공유용 렌더 HTML 뷰까지 생성한다. "PRD 써줘", "제품 요구사항 문서", "기획서 작성", "에픽/유저 스토리/인수 조건 정리", "requirements 문서" 요청 시 사용한다. 모호한 요청이면 nmwc-plan의 인터뷰 게이트를 먼저 거친다.
---

# NMWC PRD 작성 (nmwc-prd)

NMWC 팀이 **같은 규격**으로 PRD를 쓰게 하는 스킬. 다른 회사 PRD와의 차이는 두 가지다.
- **Epic → User Story → 인수 조건(AC)** 이 문서의 심장이고, 상세하게 쓴다.
- 마크다운 정본에 더해, 팀 공유·리뷰용 **렌더 HTML 뷰**를 함께 낸다 (레퍼런스: "커머스 예시 — User Story").

## 0. 시작 전 — 입력 확정

- `nmwc-plan`의 인터뷰 게이트를 거쳐 왔다면, 넘겨받은 **인터뷰 확정 요약**을 입력으로 쓴다. 같은 걸 다시 묻지 않는다.
- 이 스킬이 직접 호출됐고 요청이 모호하면(목표·대상·범위 중 2개+ 불명확), 먼저 `nmwc-plan`의 `references/interview-gate.md`를 읽어 **모호성을 제거**한 뒤 작성한다. 구체적이면 바로 작성한다.
- 못 채운 값은 절대 지어내지 말고 문서에 `[확인 필요: ...]`로 남긴다 (`nmwc-plan/references/anti-slop.md`).

## 1. 산출물

기본 저장 위치는 `docs/prd/<feature>/` (없으면 만든다; 팀 관례가 다르면 그 위치로).

| 파일 | 역할 |
|------|------|
| `<feature>-PRD.md` | **정본(단일 출처)**. 아래 §2 구조 전체 (Background~Documents). Git 커밋 대상 |
| `<feature>-PRD.html` | 공유용 렌더 HTML 뷰 — **PRD 전체**를 정본 .md에서 그대로 렌더. `scripts/render_doc.py`로 생성 |
| `<feature>-user-story.json` + `-user-story.html` | (선택) User Story 슬라이스만 카드형으로 강조한 뷰. `scripts/render_user_story.py`. 에픽/스토리/AC만 빠르게 공유할 때 |

## 2. PRD 구조 (정본 .md)

`references/prd-template.md`의 템플릿을 그대로 따른다. 섹션 순서와 의미:

1. **메타** — 소요 기간 · 문서 생성일 · 담당자
2. **Background** — 왜 하는지 설득한다. 문제/기회를 구체적으로. 형용사 슬롭 금지.
3. **Goal** — 어떤 지표를 개선할지. 가능하면 현재값→목표값 표. 측정 지표가 없으면 "정성 목표"로 명시(지어내지 않음).
4. **Hypothesis** — 핵심 가설. "X를 하면 Y가 될 것이다" 형태로.
5. **Principles** — 기획·디자인·개발이 지킬 약속(제약).
6. **Scope** — **Requirements**(할 것) / **Non-Requirements**(안 할 것) / **Future Work**(나중). 세 개 다 채운다. 안 할 것을 비우지 않는다.
7. **User Story** — 이 문서의 심장. §3 참조. Requirements에 해당하지 않는 Epic은 생략.
8. **Flow Chart / Wireframe / Documents** — 있으면 링크·이미지·설명, 없으면 `[확인 필요]` 또는 "해당 없음".

## 3. User Story — Epic · Story · AC (핵심)

작성 규율·품질 기준·예시는 `references/user-story-craft.md`를 **반드시 읽고** 따른다. 요지:

- **Epic**: 큰 기능 묶음. 번호 + 제목 (예: `1. 계정·팀·로그인`). Scope의 Requirements에서 도출한다.
- **User Story**: `US-{epic}.{n}` ID + 제목 + **한 문장** "[역할]은 [행동]한다" (예: "셀러는 이메일과 비밀번호로 로그인하고, 끝나면 로그아웃한다").
- **AC(인수 조건)**: 각 스토리의 검증 가능한 조건 목록. pass/fail 판정 가능해야 하고, **정상 경로 + 엣지·네거티브 케이스**를 담는다. 정본 .md에서는 NMWC 표준 AC 표 형식(AC-1/AC-2/... + Prototype or Design + Additional Details)을 쓴다.

AC까지 다 쓴 정본 `<feature>-PRD.md`가 완성되면, 공유용 HTML 뷰를 정본에서 그대로 렌더한다 (단일 출처 — .md 하나가 원본):

```bash
python3 scripts/render_doc.py <feature>-PRD.md <feature>-PRD.html
```

`render_doc.py`는 PRD 전체(Background~Documents)를 레퍼런스와 같은 디자인 토큰으로 렌더하고, User Story의 `US-x.y`·"> 역할은…" 인용·AC 표를 자연스럽게 카드처럼 보여준다. 표·코드블록(mermaid·와이어프레임)·체크박스를 지원한다.

**(선택) User Story만 카드형으로 강조**해 빠르게 공유하려면, `references/user-story-craft.md`의 "JSON 스키마"로 `<feature>-user-story.json`을 만들고:
```bash
python3 scripts/render_user_story.py <feature>-user-story.json <feature>-user-story.html
```
이건 에픽/스토리/AC만 담은 슬라이스 뷰다 (상단 통계 배지 자동 집계). 전체 PRD 공유가 기본이고, 이건 옵션이다.

## 4. 검증 게이트 (필수 — 통과 전 완료 금지)

정본 `<feature>-PRD.md`를 다 쓰면, **완료를 선언하기 전에 반드시** 검증기를 통과시킨다. 선택이 아니라 강제 단계다.

```bash
python3 scripts/check_prd.py <feature>-PRD.md
```

이 검증기는 canonical(`references/canonical/NMWC-PRD-템플릿.md`)이 요구하는 구조를 프로그램으로 검사한다:
- 필수 섹션(Background·Goal·Hypothesis·Principles·Scope·Requirements·Non-Requirements·Future Work·User Story·변경 이력)
- Epic·`US-x.y` 존재, **AC 없는 User Story 적발**, 미완성 `〈…〉` 플레이스홀더, 빈 Non-Requirements, 슬롭 형용사(경고)

**exit 0 (PASS)가 나올 때까지 완료하지 않는다.** FAIL 항목을 고치고 재실행한다. 검증기가 못 잡는 질(質)은 사람이 확인한다 — 경고로 뜬 슬롭 후보를 관찰 가능한 문장으로, AC가 정말 pass/fail 판정 가능한지, 엣지·네거티브 케이스가 있는지 (`nmwc-plan/references/anti-slop.md` 셀프 체크).

**PASS 후에만** §3의 HTML 뷰를 렌더하고 완료를 선언한다.

## 5. 마무리 — 다음 단계

완료 후 사용자에게: 정본 `.md`·뷰 `.html` 위치 안내 + **"이 PRD의 Requirements를 기능 단위 Spec으로 이어서 설계할까요?"** → 예이면 `nmwc-spec`으로 넘긴다 (PRD를 참조 입력으로).
