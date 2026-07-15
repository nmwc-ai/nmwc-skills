# AI 스킬 가이드

> AI 도구를 팀 전체가 일관된 품질로 활용하기 위한 스킬 작성 및 관리 가이드입니다.
> 

---

## 1. 스킬이란?

스킬(Skill)은 AI 도구에게 특정 작업을 수행할 때 어떻게 행동해야 하는지 사전에 정의해 둔 **`지침 문서`**입니다.

쉽게 말하면 AI에게 주는 "업무 매뉴얼"입니다. 예를 들어 신입 직원에게 "이 작업은 이런 방식으로 해줘"라고 설명하는 것처럼, 스킬은 AI가 특정 작업을 수행할 때마다 참고하는 기준을 정의합니다.

### 스킬이 등장한 배경

AI 도구는 기본적으로 매 대화를 새로 시작합니다. 이전 대화에서 "코딩 규약에 맞게 작성해줘"라고 설명했더라도, 다음 대화에서는 같은 설명을 처음부터 다시 해야 합니다.

개인이 반복적으로 같은 지침을 작성하는 것도 비 효율적이지만, 더 큰 문제는 팀원 마다 AI 에게 다른 지침을 주면 결과물의 품질이 들쭉날쭉 해진다는 점 입니다. 

스킬은 이 문제를 해결하기 위해 등장했습니다.

---

## 2. 왜 스킬을 사용해야 하는가?

### 2-1. 반복 작업 비용 절감

매번 긴 설명을 작성하지 않아도 됩니다. 스킬이 등록되어 있으면 AI는 해당 작업 시 자동으로 스킬을 참고합니다.

```
❌ 스킬 없이 매번 작성해야 하는 것
"NMWC 코딩 규약에 맞게 작성해줘.
 PascalCase, camelCase 규칙 지켜줘.
 멤버 변수는 _ 접두사 붙여줘.
 partial 클래스 쓰지 마. ..."

✅ 스킬이 있을 때
"이 코드 규약에 맞게 리팩토링해줘." (끝)
```

### 2-2. 팀 전체의 AI 활용 품질 통일

같은 스킬을 사용하면 팀원 누가 AI를 사용하든 동일한 기준으로 결과물이 나옵니다.

### 2-3. 노하우의 자산화

개인이 쌓은 `"이렇게 물어봐야 AI가 잘 대답하더라"`는 경험을 스킬로 정리하면 `팀 전체의 자산`이 됩니다. 팀원이 바뀌어도 노하우가 유지됩니다.

### 2-4. 온보딩 속도 향상

신규 입사자가 AI 도구를 처음 사용하더라도 팀의 스킬이 있으면 즉시 팀 수준의 결과물을 낼 수 있습니다.

---

## 3. 스킬의 구성 요소

스킬은 크게 네 가지 요소로 구성됩니다.

| 요소 | 설명 | 예시 |
| --- | --- | --- |
| **역할 (Role)** | AI가 어떤 전문가로서 행동해야 하는지 | "Unity C# 개발자로서 행동하라" |
| **목적 (Goal)** | 이 스킬이 달성해야 하는 결과 | "NMWC 코딩 규약에 맞는 코드를 작성한다" |
| **출력 형식 (Output)** | 결과물의 형태와 구조 | "함수명은 PascalCase, 변수명은 camelCase로 작성" |
| **제약 조건 (Constraints)** | 하지 말아야 할 것들 | "partial 클래스 금지, static 클래스 남용 금지" |

### 좋은 스킬 vs 나쁜 스킬

```
❌ 나쁜 스킬 — 너무 광범위하고 모호함
"좋은 코드를 작성해줘."

✅ 좋은 스킬 — 구체적이고 명확함
"Unity C# 코드를 작성할 때 아래 규칙을 따른다.
- 클래스명: PascalCase (예: PlayerController)
- 멤버 변수: camelCase + _ 접두사 (예: _totalCount)
- 상수: UPPER_SNAKE_CASE (예: MAX_COUNT)
- partial 클래스 선언 금지
- MonoBehaviour 상속 클래스는 static 선언 금지"
```

---

## 4. 스킬 만드는 방법

### 4-1. Claude (claude.ai) — Projects 기능

Claude의 Projects는 특정 프로젝트 내에서 AI가 항상 참고할 지침과 파일을 등록해두는 기능입니다.

**설정 방법**

1. claude.ai에서 프로젝트를 생성합니다.
2. 프로젝트 설정에서 **Custom Instructions**에 스킬 내용을 작성합니다.
3. 프로젝트에 파일(코딩 규약 문서, 폴더 규약 문서 등)을 업로드하면 AI가 해당 파일을 참고합니다.

**스킬 파일 구조 (SKILL.md)**

Claude에서는 스킬을 SKILL.md 파일로 관리합니다. Claude Code의 SKILL.md와 동일한 형식을 사용합니다.

```markdown
---
name: nmwc-coding-convention
description: NMWC C# 코딩 규약을 적용할 때 사용합니다.
             Unity 코드 작성, 리팩토링, 코드 리뷰 시 자동으로 참고됩니다.
---

# NMWC 코딩 규약 스킬

## 역할
Unity C# 시니어 개발자로서 NMWC 코딩 규약에 맞는 코드를 작성한다.

## 규칙
- 클래스명: PascalCase
- 멤버 변수: camelCase + _ 접두사
- 상수: UPPER_SNAKE_CASE
...
```

### 4-2. Claude Code — Skills

Claude Code는 터미널에서 동작하는 AI 코딩 에이전트로, `SKILL.md` 파일을 기반으로 스킬을 관리합니다. claude.ai의 스킬과 동일한 SKILL.md 형식을 사용하지만, 터미널 환경에 맞게 스크립트 실행, 파일 조작 등 더 강력한 자동화를 지원합니다.

### 스킬 저장 위치

| 범위 | 경로 | 설명 |
| --- | --- | --- |
| **개인 전역** | `~/.claude/skills/{스킬명}/SKILL.md` | 내 모든 프로젝트에서 사용 |
| **프로젝트 공유** | `{프로젝트루트}/.claude/skills/{스킬명}/SKILL.md` | 해당 프로젝트 팀원 전체 공유 (Git 포함) |

### 스킬 설치 방법

Anthropic 공식 스킬 저장소에서 제공하는 스킬은 아래 명령어로 설치할 수 있습니다.

```bash
# Claude Code 내에서 플러그인 형태로 설치
/plugin install document-skills@anthropic-agent-skills
```

### 스킬 폴더 구조

```
.claude/skills/nmwc-coding-convention/
├── SKILL.md          # 필수 — 스킬 진입점 (YAML frontmatter + 지침)
├── scripts/          # 선택 — 반복 실행할 자동화 스크립트
├── references/       # 선택 — 참고 문서 (규약서, API 문서 등)
└── assets/           # 선택 — 템플릿, 아이콘 등 출력에 사용하는 파일
```

> SKILL.md만 있어도 스킬로 동작합니다. 나머지 폴더는 필요한 경우에만 생성합니다.
> 

### 스킬 작성 예시

```markdown
---
name: nmwc-coding-convention
description: NMWC C# 코딩 규약을 적용합니다.
             Unity 코드 작성, 리팩토링, 코드 리뷰 요청 시 자동으로 참고됩니다.
---

# NMWC 코딩 규약 스킬

## 역할
Unity C# 시니어 개발자로서 NMWC 코딩 규약에 맞는 코드를 작성한다.

## 규칙
- 클래스명: PascalCase (예: PlayerController)
- 멤버 변수: camelCase + _ 접두사 (예: _totalCount)
- 상수: UPPER_SNAKE_CASE (예: MAX_COUNT)
- partial 클래스 선언 금지
- MonoBehaviour 상속 클래스는 static 선언 금지
```

### 스킬 호출 방법

Claude Code에서는 두 가지 방식으로 스킬을 사용합니다.

```bash
# 1. 직접 호출 — /스킬명 으로 명시적으로 실행
/nmwc-coding-convention

# 2. 자동 감지 — 관련 작업을 요청하면 Claude가 스킬을 자동으로 로드
"이 코드를 규약에 맞게 리팩토링해줘"
```

> description에 작성한 내용이 자동 감지의 기준이 됩니다. description을 구체적으로 작성할수록 스킬이 더 정확하게 자동 호출됩니다.
> 

### 빌트인 스킬

Claude Code에는 기본 제공되는 스킬이 있습니다. 별도 설치 없이 바로 사용할 수 있습니다.

| 스킬 | 설명 |
| --- | --- |
| `/debug` | 오류 원인 분석 및 수정 |
| `/simplify` | 코드 간결화 |
| `/batch` | 여러 파일에 동일 작업 일괄 적용 |
| `/loop` | 반복 작업 자동화 |
| `/run` | 앱 실행 및 변경 사항 확인 |
| `/verify` | 코드 변경 사항 검증 |

### 4-3. Cursor — Rules for AI

Cursor는 코드 에디터에 통합된 AI 기능으로, `.cursorrules` 파일 또는 Settings의 Rules for AI를 통해 스킬을 등록합니다.

**설정 방법 (전역 규칙)**

1. Cursor Settings → General → Rules for AI에 규칙을 작성합니다.
2. 모든 프로젝트에서 공통으로 적용됩니다.

**설정 방법 (프로젝트별 규칙)**

1. 프로젝트 루트에 `.cursorrules` 파일을 생성합니다.
2. 해당 프로젝트에만 적용됩니다.

```
# .cursorrules 예시

You are a Unity C# developer following NMWC's coding conventions.

## Naming Rules
- Classes: PascalCase
- Member variables: camelCase with _ prefix (e.g. _totalCount)
- Constants: UPPER_SNAKE_CASE (e.g. MAX_COUNT)

## Forbidden
- Do not use partial classes
- Do not declare static MonoBehaviour classes
```

> **참고:** Cursor 1.0 이후부터는 `.cursorrules` 대신 `.cursor/rules/` 폴더 하위에 `.mdc` 파일로 관리하는 방식을 권장합니다.
> 

### 4-4. OpenAI (ChatGPT) — GPTs / Custom Instructions

OpenAI에서는 두 가지 방법으로 스킬을 등록할 수 있습니다.

**Custom Instructions (개인 설정)**

- ChatGPT 프로필 → Custom Instructions에 작성합니다.
- 모든 대화에 자동으로 적용됩니다.

**GPTs (팀 공유용)**

- 특정 목적에 맞는 AI를 별도로 만드는 기능입니다.
- 시스템 프롬프트, 참고 파일, 사용 가능한 기능 등을 설정할 수 있습니다.
- 팀 구성원과 공유하거나 내부에서만 사용하도록 설정할 수 있습니다.

### 4-5. NMWC 스킬 작성 단계

| 단계 | 내용 |
| --- | --- |
| 1 | 이 스킬이 어떤 작업에 사용될지 목적을 정한다 |
| 2 | 해당 작업의 기준 문서(코딩 규약, 폴더 규약 등)를 참고한다 |
| 3 | 역할 / 목적 / 출력 형식 / 제약 조건 순으로 작성한다 |
| 4 | 실제로 AI에게 적용하여 결과물을 확인한다 |
| 5 | 예상과 다른 결과가 나오는 경우 스킬을 수정한다 |
| 6 | 팀 채널에 공유하고 피드백을 받는다 |

---

## 5. 스킬 작성 시 주의사항

### 5-1. 범위를 적절히 설정하기

너무 광범위한 스킬은 AI가 판단하기 어렵고, 너무 좁은 스킬은 활용 빈도가 낮아집니다.

```
❌ 너무 광범위
"좋은 Unity 개발자처럼 행동해줘."

❌ 너무 좁음
"PlayerController 클래스에서 _speed 변수 작성 시 float 타입 사용."

✅ 적절한 범위
"Unity C# 코드 작성 시 NMWC 코딩 규약(네이밍, 접근 한정자, enum 규약)을 따른다."
```

### 5-2. 민감 정보 포함 금지

스킬 파일에는 아래 정보를 포함하지 않습니다.

- API 키, 토큰, 비밀번호 등 인증 정보
- 내부 서버 주소, 개발 서버 URL
- 미출시 게임 콘텐츠나 내부 사업 정보

> 외부 AI 서비스(ChatGPT, Claude 등)에 입력된 내용은 서버에 전송됩니다.
민감 정보가 포함된 스킬을 외부 AI에 등록하지 않도록 주의하세요.
자세한 내용은 **NMWC 소스코드 및 내부자료 보안** 문서를 참고하세요.
> 

### 5-3. 충돌하는 규칙 작성 금지

서로 모순되는 규칙이 있으면 AI가 어느 쪽을 따를지 알 수 없습니다.

```
❌ 충돌하는 규칙
"코드를 최대한 간결하게 작성해줘."
"모든 함수에 반드시 주석을 추가해줘."
```

### 5-4. 스킬은 하나의 목적에 집중하기

하나의 스킬에 너무 많은 목적을 담으면 관리가 어려워집니다.
목적이 다른 경우 별도 스킬로 분리합니다.

```
❌ 하나의 스킬에 너무 많은 내용
코딩 규약 + 폴더 구조 + Git 커밋 메시지 + 코드 리뷰 기준 (모두 한 스킬에)

✅ 목적별로 분리
- nmwc-coding-convention (코딩 규약)
- nmwc-folder-convention (폴더 규약)
- nmwc-git-convention (Git 규약)
```

---

## 6. AI 별 스킬 비교

| 항목 | Claude (claude.ai) | Claude Code | Cursor | OpenAI (GPTs) |
| --- | --- | --- | --- | --- |
| **스킬 파일 형식** | SKILL.md | SKILL.md | `.cursor/rules/*.mdc` | 시스템 프롬프트 (텍스트) |
| **적용 범위** | 프로젝트 단위 | 전역 또는 프로젝트 단위 | 전역 또는 프로젝트 단위 | 전역 또는 GPT 단위 |
| **파일 첨부** | 가능 (문서, 코드 등) | 가능 (스크립트, 참고 문서 등) | 가능 (코드베이스 자동 참조) | 가능 (GPTs에 파일 업로드) |
| **팀 공유** | 프로젝트 공유로 가능 | `.claude/skills/` 폴더를 Git으로 공유 | `.cursor/rules/` 폴더를 Git으로 공유 | GPT 공유 링크 또는 팀 플랜 |
| **스킬 자동 호출** | O (description 기반) | O (description 기반) | O (파일 패턴 기반) | X (직접 GPT 선택) |
| **스크립트 실행** | X | O (bash, python 등) | X | X |
| **코드 에디터 통합** | X | 터미널 기반 | VS Code 기반 | X |
| **주요 사용 목적** | 문서 작업, 범용 대화 | 코드 자동화, 반복 작업 | 코드 작성, 리팩토링 | 범용 대화, 자동화 |
| **무료 사용 여부** | 제한적 무료 | 제한적 무료 | 제한적 무료 | 제한적 무료 |

### NMWC 권장 사용 방법

| 작업 | 권장 도구 |
| --- | --- |
| 코딩 규약에 맞는 코드 작성 / 리팩토링 | Cursor 또는 Claude Code |
| 여러 파일에 걸친 반복 작업 자동화 | Claude Code |
| 문서 작성, 기획 검토, 범용 질의응답 | Claude |
| 코드 이외 업무 자동화, 데이터 분석 | ChatGPT 또는 Claude |

---

## 7. 스킬 공유 방법

### 7-1. 팀 내 공유

**Claude Projects 스킬**

- 작성한 SKILL.md 파일을 팀 Notion 또는 사내 Git 저장소에 업로드합니다.
- 팀원이 해당 파일을 자신의 Claude Project에 추가하여 사용합니다.

**Claude Code 스킬**

- 프로젝트 루트의 `.claude/skills/` 폴더를 Git 저장소에 포함시킵니다.
- 팀원이 저장소를 Clone하면 자동으로 스킬이 적용됩니다.

**Cursor 스킬**

- `.cursor/rules/` 폴더를 프로젝트 Git 저장소에 포함시킵니다.
- 팀원이 저장소를 Clone하면 자동으로 적용됩니다.

**OpenAI GPTs**

- GPT 설정에서 공유 링크를 생성하여 팀원에게 전달합니다.
- 또는 팀 플랜 사용 시 조직 내부 공유로 설정합니다.

### 7-2. 외부 공유 시 주의사항

스킬을 외부(타사, 커뮤니티 등)에 공유할 때는 아래 사항을 반드시 확인합니다.

| 확인 | 항목 |
| --- | --- |
| ☐ | 스킬 내용에 내부 기술 정보나 프로젝트 명칭이 포함되어 있지 않은가? |
| ☐ | 리더의 승인을 받았는가? |
| ☐ | 회사 자산으로 분류되는 내용이 포함되어 있지 않은가? |

---

## 8. 스킬 관리 및 유지보수

### 8-1. 스킬 품질 검증

스킬을 작성한 후 아래 방법으로 품질을 확인합니다.

1. **테스트 케이스 작성** — 스킬이 의도한 대로 동작하는지 확인할 질문 3~5개를 미리 준비합니다.
2. **결과물 확인** — 스킬 적용 전/후 결과물을 비교합니다.
3. **팀원 피드백** — 동료에게 스킬을 사용해보도록 요청하고 피드백을 받습니다.

```
테스트 케이스 예시 (코딩 규약 스킬)

Q1. 아래 코드를 규약에 맞게 수정해줘.
    public int count = 0;
    → 기대 결과: private int _count = 0; 으로 수정

Q2. 상점 아이템 타입 enum을 작성해줘.
    → 기대 결과: E 접두사, 클래스 내부 선언, PascalCase 멤버

Q3. 플레이어 이동 기능을 partial 클래스로 분리해줘.
    → 기대 결과: partial 클래스 대신 PlayerMoveController 분리 제안
```

### 8-2. 스킬 갱신 기준

아래 상황이 발생하면 스킬을 갱신합니다.

- NMWC 코딩 규약 또는 폴더 규약이 개정된 경우
- AI 도구가 업데이트되어 기존 스킬이 잘 동작하지 않는 경우
- 팀원 피드백을 통해 개선이 필요한 내용이 발견된 경우
- 스킬이 의도와 다른 결과를 반복적으로 낼 경우

### 8-3. 효과 없는 스킬 판단 기준

아래 증상이 반복된다면 스킬을 수정하거나 폐기합니다.

- AI가 스킬을 무시하고 다른 방식으로 답변하는 경우
- 같은 스킬을 써도 결과물의 품질이 일관되지 않은 경우
- 스킬 규칙이 서로 충돌하여 AI가 혼란스러운 결과를 낼 경우

### 8-4. 스킬 파일 네이밍 규칙

스킬 파일명은 아래 형식을 따릅니다.

```
nmwc_{스킬목적}.md

예시:
nmwc_coding_convention.md
nmwc_folder_convention.md
nmwc_git_convention.md
nmwc_pr_review.md
```

---

## 9. 공식 문서 링크

각 AI 도구별 스킬 관련 공식 문서입니다. 본 가이드에서 다루지 않은 심화 내용은 아래 문서를 참고하세요.

### Claude

| 문서 | 링크 | 설명 |
| --- | --- | --- |
| Agent Skills 개요 | [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | 스킬의 개념, 구조, 동작 방식 |
| Agent Skills 퀵스타트 | [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart) | 첫 번째 스킬 만들기 단계별 가이드 |
| Agent Skills 베스트 프랙티스 | [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | 스킬 작성 모범 사례 |
| Anthropic 공식 스킬 저장소 | [github.com/anthropics/skills](https://github.com/anthropics/skills) | Anthropic이 제공하는 예시 스킬 모음 |

### Claude Code

| 문서 | 링크 | 설명 |
| --- | --- | --- |
| Extend Claude with skills | [code.claude.com](https://code.claude.com/docs/en/skills) | Claude Code에서 스킬을 만들고 관리하는 방법 |

### Cursor

| 문서 | 링크 | 설명 |
| --- | --- | --- |
| Rules | [docs.cursor.com](https://docs.cursor.com/context/rules) | 프로젝트 규칙 및 전역 규칙 작성 방법 |

### OpenAI (ChatGPT)

| 문서 | 링크 | 설명 |
| --- | --- | --- |
| GPTs in ChatGPT | [help.openai.com](https://help.openai.com/en/articles/8554407-gpts-in-chatgpt) | GPT란 무엇인지, 어떻게 사용하는지 |
| Creating and editing GPTs | [help.openai.com](https://help.openai.com/en/articles/8554397-creating-a-gpt) | GPT 생성 및 설정 방법 |
| Custom Instructions | [help.openai.com](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions) | 개인 커스텀 인스트럭션 설정 방법 |
| Writing Instructions for GPTs | [help.openai.com](https://help.openai.com/en/articles/9358033-key-guidelines-for-writing-instructions-for-custom-gpts) | GPT 지침 작성 가이드라인 |