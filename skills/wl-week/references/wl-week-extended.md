# wl-week 확장 레퍼런스 (gstack /retro global 스타일)

> `/wl-week`가 위임하는 상세 산출 규칙. 슬래시 커맨드가 아니라 참조 문서다.
> gstack `/retro global`의 집계·트렌드 사상을 worklog 볼트(`Daily/` 소스)에 맞게 이식한 것.
> 단일 사용자 볼트이므로 retro의 per-person 분해는 **per-project 분해**로 대체한다.

## 소스

- `Daily/YYYY-MM-DD.md` — frontmatter(`total_commits`, `active_repos`, `tags`) + 본문 섹션.
- 프로젝트 매핑: `repo-registry.md` (레포→`Projects/<node>`).
- 이전 주 회고: `Weekly/YYYY-W(NN-1).md` — 트렌드 비교용.

## 섹션별 산출 규칙

### 1. Shipping streak
- **활동일** = 그 날 Daily가 존재하고 (커밋 ≥1 **또는** `## 오프라인 활동` 비어있지 않음)인 날.
- 산출: `활동 X/7일`, `최장 연속 Y일`, `주간 총 커밋 N`(`total_commits` 합).
- 트렌드: 직전 주 대비 활동일·커밋 증감 화살표.

### 2. 프로젝트별 활동
- `active_repos`의 각 레포를 `repo-registry.md`로 `Projects/<node>`에 매핑. **레포명 직박 금지** — 실재 `Projects/<node>.md` 확인 후 위키링크.
- 프로젝트별: 주간 커밋 수 합 + 그 주 핵심 작업 1줄(가장 큰 Daily 항목 요약).
- 커밋 내림차순 정렬. registry 미등록 personal scope 레포는 제외(Daily 작성과 동일 기준).

### 3. 다음 주 포커스
- 각 Daily `## 내일 이어서` 항목 + 미완 Task(`Tasks/` status≠done)를 모음.
- 중복 제거(같은 항목 여러 날 등장 시 1회). 체크박스 `- [ ]`로 출력.
- 가능하면 프로젝트별로 묶음.

### 4. 도구별 사용 (tool usage breakdown)
- 한 주 본문·`tags`에서 워크플로우/스킬/커맨드 사용을 집계:
  autopilot·ralph·ultrawork·advisor(office-hours)·/wl-insights·/wl-lint·gstack(qa/review/ship)·team 등.
- 출력: `<도구> ×N` 빈도 내림차순. 가장 많이 쓴 상위 + 처음 쓴 도구 표시.
- 목적: 한 주 작업 방식의 메타 가시화.

## 트렌드 추적 (주 간 비교)

- 직전 주 `Weekly/` 노트를 읽어 streak·커밋·프로젝트 수를 대조, 증감을 각 섹션에 1줄로 부기.
- 누적 4주 이상이면 간단한 추세(상승/하락/안정) 코멘트 가능.

## 경로·동기화

- 출력: `Weekly/YYYY-WNN.md` (구 `Daily/YYYY-WNN-weekly.md`는 폐기).
- `system-log.md`에 week 항목 append.
- Daily 작성 로직과 중복 구현 금지 — frontmatter/섹션 규칙은 worklog 스킬 참조.
