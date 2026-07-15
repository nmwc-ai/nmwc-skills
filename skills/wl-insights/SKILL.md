---
name: wl-insights
description: 최근 30일(또는 사용자가 지정한 기간) Daily를 전수 분석해 크로스커팅 패턴 5가지를 추출하고 Concept 후보·미연결 쌍을 제안한다. "최근 작업에서 패턴 뽑아줘", "인사이트 추출해줘", "Concept 후보 찾아줘" 요청 시 사용.
---

# 30일 크로스커팅 인사이트 추출

최근 ~30일치(사용자가 다른 기간을 지정하면 그 기간) Daily를 전수로 읽어 **개별 일지로는 안 보이는 수평 패턴**을 뽑고,
Concept 노트로 승격할 후보(신규/갱신)와 Concept 그래프의 미연결 쌍을 제안한다.
이 스킬은 **후보를 제안만** 한다 — Concept 노트를 자동 생성하지 않는다(사용자 승인 후 반영).

> ⚠️ **네임스페이스 주의**: 본 스킬과 wl-concept는 둘 다 `Concepts/`를 건드린다.
> 패턴 추출·승격 판단은 wl-insights가, 단건 Concept 작성/편집은 wl-concept가 담당한다.
> 같은 세션에서 둘을 섞어 실행하면 중복 반영이 생길 수 있으니 분리한다.
>
> 부분 중복: Karpathy LLM Wiki "to-do generation"과 패턴 추출 목적이 일부 겹친다.
> worklog는 Concept 승격이 목적이고 to-do 생성은 부수효과 — 혼동하지 말 것.

## 실행 절차

### 1단계: 데이터 수집 (전수 읽기)

기간은 사용자가 지정(기본 30일). 예: "최근 30일 — 2026-03-26~2026-04-25".

- `Daily/` — 기간 내 전 파일 (보통 27~30개). 누락일은 명시.
- `Projects/` 전수 + `OKR/` 전수 + 기존 `Concepts/` 전수.
- (선택) `gbrain query "<패턴 가설>"`로 기간 외 유사 사례 보강 — 임베딩 커버리지는 `gbrain doctor`로 실측 후 신뢰.

추정이 아니라 실제 파일을 읽는다 (개수·날짜 검증).

### 2단계: 5가지 패턴 추출

다음 5개 축으로 각 1개씩, 총 5개 인사이트를 뽑는다(축당 0개면 명시하고 건너뜀):

| 축 | 본다 |
|---|---|
| 반복 의사결정 | 같은 판단 원리가 여러 날 반복 (예: falsification > confirmation, evidence-driven pivot) |
| 기술·도구 | 도구 사용·이관 리듬 (예: autopilot 위임 + advisor 자문, OSS AI 확장) |
| 작업 리듬 | 시간 패턴 (예: 단일 스프린트, weekend warrior, Pre-Phase 0 게이트) |
| 프로젝트 교차 | 서로 다른 프로젝트의 동일 파이프라인 (예: 채용 과제 3건 동일 흐름) |
| 미완성·반복 | 이월·재발 (예: tomorrow-never-comes, skill pre-load 재발) |

각 인사이트는 **Concept 노트로 승격할 가치가 있는 수평 패턴**이어야 한다.

### 단계 2.5: Concept 수평 그래프 점검

기존 `Concepts/` **전체 쌍**에 대해 overlap 점수를 계산한다
(공유 Daily 근거 수 / Jaccard). **Top 5 미연결 쌍**을 "연결 후보"로 출력한다:

```
### Concept 연결 후보 (미연결 쌍)
- [[Concepts/build-then-fix-loop]] ↔ [[Concepts/one-day-sprint-pattern]] — 공유 근거 6건
- [[Concepts/meta-system-investment]] ↔ [[Concepts/skill-as-product-pattern]] — 공유 근거 4건
```

이미 `## 관련 개념`으로 연결된 쌍은 제외.

### 3단계: 검증 (반영 전 필수)

후보를 확정하기 전에 기계 검증을 돌린다:
- **요일 검증**: weekend 등 요일 기반 패턴은 실제 요일을 계산해 확인 (예: 05-22=금 → weekend 제외).
- **프로젝트 귀속**: 단일 프로젝트 사례를 일반 패턴으로 과대 일반화하지 않는다.
- **summary 숫자 대조**: Daily frontmatter/본문 수치 오류는 교정.

### 4단계: 후보 제안 (자동 생성 금지)

리포트로 제안만 한다. 사용자 승인 후에만 반영:
- **신규 Concept**: 제목 + 근거 Daily 목록(sources N) + 1줄 정의.
- **갱신 Concept**: 기존 노트 sources 증가분 + 추가 근거.
- **양방향 링크**: 단계 2.5 연결 후보 중 승인분만 양쪽 `## 관련 개념`에 추가.

### 5단계: 승인분 반영 + 동기화

- 신규 Concept 노트 생성(템플릿) / 기존 노트 sources·근거 갱신.
- `index.md` Concepts 섹션 재동기화 (개수·근거 수 정렬·누락 보충).
- `system-log.md`에 `## YYYY-MM-DD insights | wl-insights 실행 (최근 N일 — 범위)` 항목 append.

## 출력 템플릿

```markdown
## YYYY-MM-DD insights | wl-insights 실행 (최근 30일 — 시작~종료)
- 데이터 수집: Daily N개 + Projects M + OKR K + 기존 Concepts C 전수
- 5가지 패턴: 반복 의사결정(...) / 기술·도구(...) / 작업 리듬(...) / 프로젝트 교차(...) / 미완성·반복(...)
- Concepts 신규 X건: <이름> (sources N) / ...
- Concepts 갱신 Y건: <이름> (기존→신규) / ...

### Concept 연결 후보 (미연결 쌍 — 사용자 승인 대기)
- [[Concepts/A]] ↔ [[Concepts/B]] — 공유 근거 N건

- 검증: 요일 기계검증 / 프로젝트 귀속 / summary 숫자 교정
- 주목 신호: <향후 결정에 영향 줄 신호 1~3건>
```

## 검증 체크리스트

- [ ] 기간 내 Daily를 **전수** 읽었는가? (개수·누락일 확인, 추정 금지)
- [ ] 5개 축 각각에서 패턴을 검토했는가? (0개 축은 명시)
- [ ] 단계 2.5 미연결 쌍을 실제 overlap 계산으로 산출했는가?
- [ ] Concept 노트를 **자동 생성하지 않고** 후보로만 제안했는가?
- [ ] 요일·프로젝트 귀속·숫자 검증을 거쳤는가?
- [ ] `index.md`·`system-log.md` 동기화를 마쳤는가?
- [ ] wl-concept와 중복 반영이 없는지 확인했는가?
