---
name: wl-setup
description: worklog 시스템을 부트스트랩하고 진단·복구한다. 볼트 구조·쓰기 스킬 배선·푸시 훅·gbrain·wl-* 커맨드 패밀리를 점검하고 빠진 조각을 설치한다. 새 머신에 worklog를 처음 설치했거나 "worklog 셋업해줘", "worklog 진단해줘", "볼트가 제대로 안 깔린 것 같아" 요청 시 사용.
---

# worklog 셋업 & 닥터

새 머신/최초 설치 직후 worklog 시스템이 제대로 깔리고 배선됐는지 점검하고, 빠진 조각을 설치한다.
각 조각을 **확인 → 빠진 것 보고 → 사용자 승인 후 수정**의 순서로 다룬다. 파괴적 동작은 승인 없이 하지 않는다.

## 실행 절차

### 0단계: 머신 식별 (읽기 전용)

```bash
hostname; git config user.email
```

어느 머신인지 기록만 한다(이전 시 양 머신 상태가 다를 수 있음). 이하 모든 단계는 먼저 **읽기**로 상태를 수집한 뒤 판정한다.

### 1단계: 볼트 존재·구조 확인

```bash
ls -d ~/Documents/Worklog/{Daily,Projects,Concepts,Tasks,OKR,Plans,Offline} \
      ~/Documents/Worklog/{index.md,system-log.md,Dashboard.md} 2>&1
```

빠진 하위 폴더/진입점 파일을 표로 보고한다(`Offline/` 등 일부는 선택적일 수 있으니 "없음=경고"가 아니라 "없음=확인 필요"로 표기).

볼트 자체가 없으면(`Daily/` 등 전부 없음) 최초 설치로 판단하고, 사용자 승인 후 기본 폴더 구조(`Daily/ Projects/ Concepts/ Tasks/ OKR/ Plans/`)와 진입점 파일(`index.md`)을 생성한다.

### 2단계: 쓰기 스킬 + 커맨드 배선 확인

```bash
ls -la ~/.claude/skills/worklog/SKILL.md \
       ~/.claude/skills/worklog/scripts/{collect-git.sh,install-push-hook.sh} \
       ~/.claude/skills/worklog/references/repo-registry.md 2>&1
# wl-* 커맨드/스킬 패밀리 잔존 여부
ls ~/.claude/commands/wl-*.md 2>&1
```

- worklog 스킬(SKILL.md·scripts·references)이 없으면 → 마켓플레이스에서 재설치(`/plugin install worklog@nmwc-skills`) 안내.
- wl-* 커맨드/스킬이 비었으면 → 마켓플레이스에서 필요한 것만 선택 설치(`/plugin install wl-ask@nmwc-skills` 등) 안내.

### 3단계: 푸시 훅 설치 상태 확인

```bash
# Work 하위 레포에 post-push 훅이 깔렸는지 표본 점검
find "${WORK_DIR:-$HOME/Documents/Work}" -maxdepth 7 -type d -name .git 2>/dev/null \
  | while read g; do [ -f "$g/hooks/post-push" ] && echo "✓ ${g%/.git}" || echo "✗ ${g%/.git}"; done | head -40
```

미설치 레포가 있으면 설치 제안:

```bash
bash ~/.claude/skills/worklog/scripts/install-push-hook.sh
```

(이 스크립트는 기존 훅이 있으면 건너뛰므로 재실행 안전.)

### 4단계: gbrain 설치·brain 초기화 확인

```bash
command -v gbrain >/dev/null && echo "gbrain 설치됨" || echo "gbrain 미설치"
gbrain doctor --json 2>/dev/null || gbrain doctor 2>/dev/null
```

- CLI 미설치면 → 설치 안내(머신 글로벌 `~/.gbrain`).
- brain 미초기화면 → 초기화 + `gbrain import ~/Documents/Worklog` 제안.
- `doctor`로 resolver/skills/pgvector/RLS/embeddings 상태를 읽고, 임베딩 커버리지가 낮으면(silent-skip 특성) wl-embed 실행을 제안.

### 5단계: 자동화(launchd/cron) 상태 확인

```bash
launchctl list 2>/dev/null | grep -i "gbrain\|worklog" || echo "등록된 worklog/gbrain job 없음"
crontab -l 2>/dev/null | grep -i "gbrain\|worklog" || echo "cron 항목 없음"
```

등록된 게 없고 사용자가 주기 동기화(gbrain refresh 등)를 원하면 등록을 제안한다. **기본은 제안만** — 자동 등록하지 않는다.

### 6단계: 진단 리포트 출력

```
## worklog 시스템 진단 — <hostname> (<date>)

| 조각 | 상태 | 조치 |
|------|------|------|
| 볼트 구조 | ✓/✗ | … |
| 쓰기 스킬(SKILL.md) | ✓/✗ | … |
| wl-* 커맨드/스킬 패밀리 | N개 존재/유실 | … |
| 푸시 훅 | N/M 레포 | install-push-hook.sh |
| gbrain CLI + brain | ✓/✗ | … |
| 임베딩 커버리지 | …% | wl-embed |
| 자동화 job | 있음/없음 | (선택) |

### 빠진 조각 / 권장 조치
1. [우선순위] …
```

### 7단계: 승인 후 수정

리포트의 "빠진 조각"마다 사용자에게 수정 여부를 묻고(`AskUserQuestion` 가용 시 사용), 승인된 항목만 실행한다.
수정 후 해당 점검을 **재실행해 ✓로 바뀌었는지 실측**한다(주장 금지).

## 검증 체크리스트

- [ ] 모든 상태를 추정이 아니라 실제 명령(`ls`/`grep`/`gbrain doctor`)으로 측정했는가?
- [ ] 파괴적 동작 전 사용자 승인을 받았는가?
- [ ] 수정 후 같은 점검을 재실행해 통과를 실측했는가?
- [ ] wl-* 커맨드/스킬 유실을 탐지했는가?
