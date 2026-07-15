---
name: wl-ask
description: worklog 볼트에 과거 작업·결정·회사 간 맥락을 gbrain 의미검색으로 질의하고, 출처를 위키링크로 인용해 답한다. 질문이 없으면 세션 종료 자동 파일링 모드(opt-out)로 이번 세션 작업을 오늘 Daily에 기록한다. "예전에 왜 그렇게 결정했지", "저번에 뭐 했더라", "worklog에 물어봐", 또는 세션을 마무리하며 "오늘 일지에 남겨줘" 요청 시 사용.
---

# Worklog 질의 + 세션 종료 자동 파일링

사용자의 질문이 있으면 **질의 모드**, 질문 없이 세션을 마무리하는 맥락이면 **세션 종료 자동 파일링 모드**로 동작한다.

## 환경 사실

- 볼트: `~/Documents/Worklog/` — `Daily/` `Projects/` `Concepts/` `Tasks/` `OKR/` `Plans/`, 루트 `index.md` `system-log.md`.
- gbrain CLI: `gbrain search <q>`(키워드 정확매칭) · `gbrain query <q>`(하이브리드 의미검색). 임베딩은 조건부 자동(silent-skip)이므로 커버리지는 `gbrain doctor`로 실측. 임베딩 부재 시 `query`가 빈약하면 `search`로 폴백.
- Daily 작성 로직은 worklog 스킬에 위임 — 여기서 중복 구현하지 않는다.

---

## 모드 A: 질의 (질문이 있을 때)

> 과거 작업·결정·진행상황·회사 간 맥락을 묻는다. 기억·추정이 아니라 **볼트 + gbrain 실데이터**로 답한다.

### 1단계: 의미검색 실행

```bash
gbrain query "<사용자 질문>"        # 하이브리드 의미검색 (1차)
gbrain search "<핵심 키워드>"        # 정확매칭 보강 (2차, 고유명사·날짜·레포명)
```

- 결과가 빈약하면 질문을 키워드로 분해해 `search` 재실행.
- gbrain이 죽어있거나 0건이면 `index.md` 진입 후 `grep -rn` 볼트 직접 탐색으로 폴백.

### 2단계: 후보 노트 읽기 + 검증

- 검색이 가리킨 `Daily/` `Projects/` `Concepts/` 노트를 실제로 Read.
- **auto-backfilled 디스카운트**: 본문에 `<!-- auto-backfilled YYYY-MM-DD -->` 마커가 있는 entry는 자동 합성된 placeholder다. 1차 사실로 인용하지 말고 **신뢰도 0.5로 디스카운트**한다. 답변에 쓸 수밖에 없으면 "(자동 백필 항목, 미검증)"으로 명시 플래그한다.
- 마커 없는 직접 작성 entry > backfilled entry. 충돌 시 직접 작성·최신 날짜 우선.

### 3단계: 답변 합성 (출처 인용)

```
[질문에 대한 직접적 답변 — 2~4문장]

**근거**
- [[Daily/YYYY-MM-DD]] — 이 노트가 뒷받침하는 사실 1줄
- [[Projects/노드명]] — 진행상황/결정 1줄
- [[Concepts/패턴명]] — 관련 패턴 (해당 시)

**불확실/플래그**
- (자동 백필 항목 인용 시) [[Daily/YYYY-MM-DD]] — auto-backfilled, 미검증
- (검색 0건/추정 시) 볼트에 직접 근거 없음 — 추정임을 명시
```

- 모든 사실 주장에 위키링크 출처를 단다. 출처 없는 단언 금지.
- 회사 간 맥락 질문은 여러 Project를 교차 인용한다.

---

## 모드 B: 세션 종료 자동 파일링 (질문 없음)

> 세션 종료 시, 이번 세션에서 한 작업을 **오늘 Daily에 자동 파일링**한다. **opt-out** — 사용자가 거부하면 건너뛴다.

### 1단계: opt-out 확인

```
이번 세션 작업을 오늘 Daily([[Daily/YYYY-MM-DD]])에 파일링할까요? (기본: 진행 / "스킵"이면 건너뜀)
```

- 사용자가 "스킵"·"아니"·"하지마"면 즉시 종료. 그 외에는 진행(opt-out 기본 동작).

### 2단계: 오늘 Daily에 반영

- worklog 스킬의 Daily 작성 흐름에 위임한다.
- 오늘 파일 있으면 이어쓰기, 없으면 신규 생성. git 커밋은 `collect-git.sh`로 수집, 비-git 작업은 `## 오프라인 활동`에 추가.
- 자동 추론으로 채운 항목(직접 확인 못 한 것)은 `<!-- auto-backfilled YYYY-MM-DD -->` 마커를 단다 → 이후 모드 A 질의에서 디스카운트 대상이 된다.

### 3단계: 기록

- 파일링 완료 후 `system-log.md`에 `## YYYY-MM-DD update | ...` 1줄 append.

---

## 검증 체크리스트

- [ ] (모드 A) `gbrain query`/`search`를 실제로 실행했는가? (기억으로 답하지 않음)
- [ ] (모드 A) 모든 사실 주장에 `[[Daily/]]`/`[[Projects/]]` 출처를 달았는가?
- [ ] (모드 A) `<!-- auto-backfilled -->` 마커 항목을 디스카운트/플래그했는가?
- [ ] (모드 A) gbrain 0건일 때 볼트 grep 폴백을 시도했는가?
- [ ] (모드 B) opt-out 확인 후 진행했는가?
- [ ] (모드 B) Daily 작성을 worklog 스킬에 위임했는가? (로직 중복 구현 금지)
