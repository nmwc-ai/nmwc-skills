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

## 출처 (단순 복사된 스킬)

아래 스킬들은 원본 저장소의 `SKILL.md`(및 딸린 references/scripts/assets)를 그대로 복사해 등록했다. 절대경로 의존이 없어 vendor+심링크 없이 바로 동작한다.

| 스킬 | 출처 | 라이선스 |
|------|------|----------|
| brainstorming, writing-plans, executing-plans, verification-before-completion, systematic-debugging, using-superpowers | [obra/superpowers](https://github.com/obra/superpowers) | MIT (Jesse Vincent) |
| humanizer | [blader/humanizer](https://github.com/blader/humanizer) | MIT (Siqi Chen) |
| ponytail, ponytail-audit, ponytail-debt, ponytail-gain, ponytail-help, ponytail-review | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | MIT |
| skill-creator, frontend-design, canvas-design, brand-guidelines | [anthropics/skills](https://github.com/anthropics/skills) | Apache License 2.0 |
| obsidian-defuddle, obsidian-markdown, obsidian-bases, obsidian-cli, obsidian-json-canvas | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | MIT (Steph Ango) |

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

## 벤더링된 스킬 (ui-ux-pro-max)

[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)은 저장소 자체에는 `SKILL.md`가 없고, `ui-ux-pro-max-cli`(npx 설치형)가 설치 시점에 SKILL.md + `scripts/`(Python) + `data/`(CSV 데이터셋)를 생성한다. `vendor/ui-ux-pro-max/`는 로컬에 이미 설치되어 있던 산출물을 그대로 복사해 넣은 것이다 (MIT License, Copyright (c) 2024 Next Level Builder — 고지는 `vendor/ui-ux-pro-max/LICENSE` 참조).

**왜 심링크인가**: SKILL.md 안의 스크립트 호출이 `~/.claude/skills/ui-ux-pro-max/scripts/search.py` 같은 **절대경로**를 쓴다 (gstack과 동일한 문제). `skills/ui-ux-pro-max/SKILL.md`는 이 벤더 트리 안의 원본 파일을 가리키는 심링크다.

**설치 후 필수 1회 설정** (`~/.claude/skills/ui-ux-pro-max`가 이미 없는 경우에만):

```bash
ln -s ~/.claude/plugins/marketplaces/nmwc-skills/vendor/ui-ux-pro-max ~/.claude/skills/ui-ux-pro-max
```

이미 공식 CLI(`npx ui-ux-pro-max-cli@latest install` 등)로 설치되어 있는 PC라면 이 심링크는 불필요하다.

## 벤더링된 스킬 (claude-seo)

[AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)는 25개 서브스킬 + 18개 서브에이전트를 하나의 플러그인으로 묶은 대형 SEO 자동화 저장소다. `vendor/claude-seo/`는 이 저장소의 git-tracked 소스를 그대로 복사해 넣은 것이다 (MIT License — 고지는 `vendor/claude-seo/LICENSE` 참조). 이 카탈로그에는 그중 가장 포괄적인 진입점인 `skills/seo`(종합 SEO 감사) 하나만 `claude-seo`라는 이름으로 등록했다.

**왜 심링크인가**: `skills/seo/SKILL.md`는 "Scripts: Located at the plugin root `scripts/` directory"라고 명시한다 — 즉 스크립트가 `skills/seo/` 안이 아니라 벤더 트리의 **저장소 루트** `scripts/`에 있다고 가정한다. `skills/claude-seo/SKILL.md`는 이 가정을 그대로 살리기 위해 `vendor/claude-seo/skills/seo/SKILL.md`를 가리키는 심링크로 등록했다.

**설치 후 필수 1회 설정** (`~/.claude/skills/claude-seo`가 이미 없는 경우에만):

```bash
ln -s ~/.claude/plugins/marketplaces/nmwc-skills/vendor/claude-seo ~/.claude/skills/claude-seo
```

일부 스크립트는 Python 의존성(`vendor/claude-seo/requirements.txt` 또는 `pyproject.toml`)이 필요할 수 있다.
