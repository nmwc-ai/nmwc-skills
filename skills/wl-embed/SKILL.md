---
name: wl-embed
description: gbrain 임베딩 인프라를 수동 유지보수한다. preflight 8실패모드 검진 → sync(import+embed) → 커버리지/quota 리포트. "gbrain 임베딩 충전해줘", "worklog 검색이 안 잡혀", "gbrain 커버리지 점검해줘" 요청 시 사용.
---

# gbrain 임베딩 수동 유지보수

자동화(데몬·cron)는 소비자(검증자) 부재 시 조용히 죽는 특성(silent-failure)이 있어, 임베딩은 사람이 직접 매번 **검진 → 동기화 → 리포트**의 3단계로 충전하는 것을 기본으로 한다. 임베딩은 조건부 자동(Ollama+idle)이고 silent-skip이라, 이 수동 top-up이 커버리지를 보장하는 유일한 경로다.

## 실행 절차

### 1단계: preflight — 8실패모드 검진

임베딩을 시도하기 **전에** 알려진 8개 실패모드를 먼저 검진한다. 하나라도 FAIL이면 그 항목을 먼저 복구하고, 2단계로 넘어가지 않는다.

| # | 실패모드 | 검진 방법 | 정상값 | 복구 |
|---|----------|-----------|--------|------|
| 1 | **pg_trgm ABI 깨짐** (postgres **서버 엔진 한정**) | 1차: `gbrain doctor` brain 체크. 서버 엔진이면 `command -v psql && psql -d gbrain -c "SELECT similarity('a','ab')"` (PGLite 엔진은 psql 없음 — doctor로 갈음) | doctor brain OK / similarity 값 반환 (예: 0.375) | `brew services restart postgresql@18` |
| 2 | **bun PATH 누락** (launchd `bun: not found` 원인) | `command -v bun` | `~/.bun/bin/bun` 해소 | 셸 프로파일/`~/.bun/bin` PATH 확인 |
| 3 | **launchd 데몬 잔존** (autopilot은 KeepAlive→respawn) | `launchctl list \| grep -i gbrain` | **0건** (수동 전환 후 정상) | `launchctl unload` + plist 삭제 |
| 4 | **embedding 키/모델 도달 불가** | `~/.gbrain/env`에 `GOOGLE_API_KEY` 존재(chmod 600) | 키 존재·`gemini-embedding-001` 응답 | AI Studio 새 GCP 프로젝트 키 발급 |
| 5 | **API quota 소진** (무료 1000 RPD 일일카운터) | 단일 embed 시도 시 HTTP 429 여부 | 429 아님 | **~16:00 KST 리셋** 대기 후 충전 (데몬 무관) |
| 6 | **stale sync 백로그** (sync_failures WARN) | `gbrain doctor` sync_failures | OK | `gbrain sync --skip-failed`로 acknowledge |
| 7 | **NULL 임베딩 청크** (커버리지 갭) | `gbrain doctor` embeddings 커버리지 / `embedding IS NULL` 카운트 | 100% / 0건 | 2단계 `embed --stale` |
| 8 | **gbrain doctor 종합 FAIL** (resolver·pgvector·RLS·skills) | `gbrain doctor --json` | Health 양호·FAIL 0 | 항목별 doctor 안내 따름 |

```
## 🔎 preflight (8실패모드)

| # | 실패모드        | 결과 | 실측값                    |
|---|-----------------|------|---------------------------|
| 1 | pg_trgm         | [✅/❌] | similarity()=[값]         |
| 2 | bun PATH        | [✅/❌] | [경로]                    |
| 3 | launchd 데몬    | [✅/❌] | [N]건 (정상=0)            |
| 4 | embedding 키    | [✅/❌] | GOOGLE_API_KEY [존재/없음] |
| 5 | quota           | [✅/❌] | [정상 / 429 소진]         |
| 6 | sync 백로그     | [✅/❌] | sync_failures [N]         |
| 7 | NULL 임베딩     | [⚠️/✅] | [N] chunks NULL           |
| 8 | doctor 종합     | [✅/❌] | Health [N]                |

판정: [전부 PASS → 2단계 진행 / FAIL 있음 → 해당 항목 복구 먼저]
```

> 5번(quota)이 FAIL이면 — 데몬을 다 제거했어도 quota는 일일 카운터라 직전 사용분으로 소진될 수 있다. **~16:00 KST 리셋 후** 재실행한다. 그 사이에도 키워드 검색(`gbrain search`, tsvector)은 임베딩과 무관하게 정상 동작한다.

### 2단계: sync — import + embed --stale

preflight PASS 후 git→brain 증분 동기화와 누락 임베딩 충전을 수행한다. `--stale`는 `embedding`(또는 `embed_at`)이 NULL인 청크만 처리한다 — 멱등하며 이미 임베딩된 청크는 건드리지 않는다.

```bash
gbrain sync --skip-failed          # git→brain 증분 import (실패분은 ack)
gbrain embed --stale               # NULL 임베딩 청크만 충전
```

- 페이지 단위 atomic — 큰 페이지(예: daily 71KB ≈ 82청크)는 한 번에 끝낼 quota window가 필요하다. quota가 빠듯하면 리셋 직후 full 1000에서 실행한다.
- 도중 429가 뜨면 그 시점까지 충전된 만큼만 커밋되고 나머지는 다음 회차로 이월된다(다시 `embed --stale`).

```
## 🔄 sync 결과

- import: [N] pages / [M] chunks ([K] skip-failed ack)
- embed --stale: [P]/[Q] embedded (~[T]분)
- 이월(미충전): [R] chunks → 다음 quota 리셋 후 재실행
```

### 3단계: 커버리지 / quota 리포트

`gbrain doctor`로 임베딩 커버리지와 헬스를 실측 보고한다(추정 금지 — silent-skip 특성상 반드시 실측).

```bash
gbrain doctor --json
```

```
## 📊 임베딩 리포트

- 커버리지: [N]/[M] ([%]) — 목표 100%
- NULL 잔여: [K] chunks ([어느 페이지])
- doctor Health: [점수] (sync_failures [OK/WARN])
- quota: [정상 / 소진 — ~16:00 KST 리셋 대기]
- 검색 상태: 키워드(`gbrain search`) 정상 / 하이브리드(`gbrain query`)는 임베딩 [N%]에 비례

[100% 미만 시] → 미충전 [K]건은 quota 리셋 후 wl-embed 재실행으로 충전
```

> 임베딩 100%일 때 하이브리드 검색(`gbrain query` = 키워드+벡터+멀티쿼리+reranker)이 최고 성능. 임베딩 누락분만큼 하이브리드 품질이 떨어지지만, 키워드 검색은 항상 정상이다.

---

## 검증 체크리스트

- [ ] preflight 8모드를 **실제 명령으로** 검진했는가? (기억·추정 금지)
- [ ] FAIL 항목을 2단계 전에 복구했는가? (특히 #3 launchd 데몬 0건, #1 pg_trgm)
- [ ] `embed --stale`로 NULL 청크만 처리했는가? (전체 재임베딩 아님 — 멱등)
- [ ] 커버리지를 `gbrain doctor`로 **실측**했는가? (silent-skip이라 추정 불가)
- [ ] quota 429면 ~16:00 KST 리셋 후 재실행으로 안내했는가?
- [ ] launchd에 gbrain 잡이 다시 생기지 않았는가? (KeepAlive respawn 감시)
