# nmwc-skills

NMWC 팀 Claude Code skill 마켓플레이스.

## 설치

```
/plugin marketplace add nmwc-ai/nmwc-skills
/plugin install <skill-name>@nmwc-skills
```

## 스킬 등록 절차

1. `skills/<skill-name>/SKILL.md`로 원본 스킬 파일을 복사한다. 복사한 `SKILL.md`의 frontmatter에 `name`이 있는지 확인한다 (없으면 마켓플레이스 설치 시 스킬 이름이 버전 문자열로 바뀜).
2. `skills/<skill-name>/.claude-plugin/plugin.json`을 만든다:
   ```json
   {
     "name": "<skill-name>",
     "description": "...",
     "version": "1.0.0"
   }
   ```
3. `.claude-plugin/marketplace.json`의 `plugins` 배열에 엔트리를 추가한다:
   ```json
   {
     "name": "<skill-name>",
     "description": "...",
     "version": "1.0.0",
     "source": "./skills/<skill-name>",
     "category": "...",
     "tags": ["..."]
   }
   ```
4. 커밋 · 푸시한다.
5. `nmwc-brand-system` 레포에서 `cd skills-sync && npm run sync`를 실행해 카탈로그를 갱신하고, 결과로 바뀐 `skills-catalog.json`을 커밋한다.

## 벤더링된 스킬 (gstack)

`vendor/gstack/`는 [garrytan/gstack](https://github.com/garrytan/gstack)의 git-tracked 소스를 그대로 복사해 넣은 것이다 (MIT License, Copyright (c) 2026 Garry Tan — 고지는 `vendor/gstack/LICENSE` 참조). `skills/gstack-<name>/SKILL.md`는 이 벤더 트리 안의 원본 파일을 가리키는 심링크이며, 내용을 직접 수정하지 않는다.

**왜 심링크인가**: gstack의 SKILL.md들은 헬퍼 스크립트를 `~/.claude/skills/gstack/bin/...` 같은 **절대경로**로 호출한다 (플러그인 상대경로가 아님). 이 경로 참조가 스킬 46개·SKILL.md 51개 파일에 900개 이상 있어 플러그인 상대경로로 재작성하는 것은 사실상 gstack을 포크하는 것과 같다. 대신 벤더 트리를 그대로 두고, 설치한 사람이 아래 심링크 한 줄로 그 경로를 실제로 채워주는 방식을 쓴다.

**설치 후 필수 1회 설정** (`~/.claude/skills/gstack`가 이미 없는 경우에만):

```bash
ln -s ~/.claude/plugins/marketplaces/nmwc-skills/vendor/gstack ~/.claude/skills/gstack
```

이미 [gstack 공식 설치](https://github.com/garrytan/gstack)(`npx gstack@latest install`)가 되어 있는 PC라면 이 심링크를 만들 필요가 없다 — 기존 설치가 이미 같은 경로를 채우고 있다.

일부 gstack 스킬(bun/node 기반 헬퍼 스크립트)은 `~/.claude/skills/gstack`에서 `bun install`이 필요할 수 있다. bash 전용 스크립트만 쓰는 스킬은 이 단계가 필요 없다.

**신규 gstack 스킬 추가 절차**: 위 "스킬 등록 절차"와 동일하되 1번 단계 대신 심링크를 만든다.

```bash
mkdir -p skills/gstack-<name>/.claude-plugin
ln -s ../../vendor/gstack/<name>/SKILL.md skills/gstack-<name>/SKILL.md
```

`vendor/gstack` 자체를 업데이트하려면 `~/.claude/skills/gstack`의 최신 git-tracked 파일로 다시 복사하고 커밋한다 (현재 벤더 버전: gstack v1.45.0.0, commit `cf50443b`).
