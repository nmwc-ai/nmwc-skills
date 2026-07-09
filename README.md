# nmwc-skills

NMWC 팀 Claude Code skill 마켓플레이스.

## 설치

```
/plugin marketplace add nmwc-ai/nmwc-skills
/plugin install <skill-name>@nmwc-skills
```

## 스킬 등록 절차

1. `skills/<skill-name>/SKILL.md`로 원본 스킬 파일을 복사한다.
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
