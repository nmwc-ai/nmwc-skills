# NMWC 스킬 - 웹 앱 폴더 규약

> NMWC 웹앱(React + TypeScript / Next.js) 폴더 규약을 AI 도구에 스킬로 등록하여,
AI가 파일 생성이나 구조 변경 시 정해진 폴더 규약을 자동으로 따르도록 하기 위한 가이드입니다.
> 

---

## 목차

1. [이 스킬은 무엇인가?](https://claude.ai/chat/aa33ad0c-5b99-44cd-9944-313310e5f5c7#1-%EC%9D%B4-%EC%8A%A4%ED%82%AC%EC%9D%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80)
2. [스킬에 포함된 규칙 요약](https://claude.ai/chat/aa33ad0c-5b99-44cd-9944-313310e5f5c7#2-%EC%8A%A4%ED%82%AC%EC%97%90-%ED%8F%AC%ED%95%A8%EB%90%9C-%EA%B7%9C%EC%B9%99-%EC%9A%94%EC%95%BD)
3. [스킬 리소스](https://claude.ai/chat/aa33ad0c-5b99-44cd-9944-313310e5f5c7#3-%EC%8A%A4%ED%82%AC-%EB%A6%AC%EC%86%8C%EC%8A%A4)
4. [AI 도구별 사용 방법](https://claude.ai/chat/aa33ad0c-5b99-44cd-9944-313310e5f5c7#4-ai-%EB%8F%84%EA%B5%AC%EB%B3%84-%EC%82%AC%EC%9A%A9-%EB%B0%A9%EB%B2%95)
5. [스킬 인덱스에 등록](https://claude.ai/chat/aa33ad0c-5b99-44cd-9944-313310e5f5c7#5-%EC%8A%A4%ED%82%AC-%EC%9D%B8%EB%8D%B1%EC%8A%A4%EC%97%90-%EB%93%B1%EB%A1%9D)

---

## 1. 이 스킬은 무엇인가?

웹앱 폴더 규약 스킬은 NMWC의 **Next.js App Router 기반 폴더 구조 규약**을 AI 도구가 파일 생성 시 자동으로 참고하도록 만든 지침 파일입니다.

### 이 스킬의 범위

| 포함 | 미포함 |
| --- | --- |
| 프로젝트 루트 구조 | 네이밍 표기법 (→ 웹앱 코딩 규약 스킬) |
| src/ 하위 폴더 역할 및 규칙 | 상태 관리 로직 |
| 파일 네이밍 규칙 (kebab-case) | 배포 설정 |
| app/ 라우팅 구조 규칙 |  |
| 컴포넌트 폴더 승격 기준 |  |

---

## 2. 스킬에 포함된 규칙 요약

### 폴더 구조

| 폴더 | 역할 |
| --- | --- |
| `src/app/` | Next.js App Router (라우팅, 페이지, API 라우트) |
| `src/components/ui/` | 범용 UI 컴포넌트 (비즈니스 로직 없음) |
| `src/components/layout/` | 레이아웃 컴포넌트 (헤더, 사이드바) |
| `src/components/{도메인}/` | 도메인별 컴포넌트 |
| `src/hooks/` | 커스텀 훅 |
| `src/lib/` | 유틸리티, 설정, 외부 라이브러리 래퍼 |
| `src/stores/` | 전역 상태 (Zustand 등) |
| `src/types/` | 공통 타입 정의 |
| `src/constants/` | 공통 상수 |

### 파일 네이밍

| 대상 | 형식 | 예시 |
| --- | --- | --- |
| 컴포넌트 | kebab-case.tsx | `user-card.tsx` |
| 훅 | use-{기능}.ts | `use-auth.ts` |
| Store | {도메인}-store.ts | `auth-store.ts` |
| 타입 | {도메인}.ts | `user.ts` |
| Next.js 특수파일 | Next.js 규약 | `page.tsx`, `layout.tsx`, `error.tsx` |

---

## 3. 스킬 리소스

### 3-1. SKILL.md (Claude Code / Codex CLI / Claude Projects 공용)

아래 내용을 `SKILL.md`로 저장합니다.

```
# NMWC Web App Folder Convention

## Project Structure
```
src/
├── app/                 # Next.js App Router (routing, pages, API routes)
├── components/          # Reusable components
│   ├── ui/              # Generic UI (no business logic)
│   ├── layout/          # Layout (header, sidebar)
│   └── {domain}/        # Domain-specific components
├── hooks/               # Custom hooks (use-{name}.ts)
├── lib/                 # Utilities, configs, library wrappers
├── stores/              # Global state ({domain}-store.ts)
├── types/               # Shared type definitions
├── constants/           # Shared constants
└── styles/              # Global styles
```

## App Router Rules
- Route groups: `(group-name)/` — not included in URL
- Pages: only `page.tsx` is a route entry
- Layouts: `layout.tsx` per route group for shared UI
- API routes: `api/` folder with `route.ts`
- Dynamic routes: `[param]/`
- page.tsx handles data fetching + composition only; no business logic

## File Naming
- All files/folders: kebab-case
- Components: `user-card.tsx`
- Hooks: `use-auth.ts`
- Stores: `auth-store.ts`
- Types: `user.ts`
- Tests: `user-card.test.tsx`
- Next.js special: `page.tsx`, `layout.tsx`, `error.tsx`, `loading.tsx`

## Component Organization
- `components/ui/` — generic, no business logic
- `components/layout/` — header, sidebar, footer
- `components/{domain}/` — domain-specific
- One component per file
- 3+ files in a domain folder → add `index.ts` for re-exports

## Placement Rules
- All source code under `src/`
- Shared types → `src/types/`; component-local types stay in component file
- Props types stay in the component file
- No `utils/` or `helpers/` top-level folder; use `src/lib/`
- Max folder depth: 4 levels from `src/`

## Forbidden
- Source code outside `src/` (config files excluded)
- Page logic inside `components/`
- Deep relative paths (`../../`) — use `@/` alias
```

### 3-2. Cursor용 .mdc 파일

아래 내용을 `.cursor/rules/webapp-folder-convention.mdc`로 저장합니다.

```markdown
---
description: NMWC 웹앱 폴더 규약. 파일 생성, 이동, 구조 변경 시 자동으로 참고됩니다.
globs: src/**/*
alwaysApply: false
---

# NMWC Web App Folder Convention

## Structure
- src/app/ — Next.js App Router (pages, layouts, API routes)
- src/components/ui/ — generic UI, no business logic
- src/components/layout/ — header, sidebar
- src/components/{domain}/ — domain components
- src/hooks/ — custom hooks (use-{name}.ts)
- src/lib/ — utils, configs, library wrappers
- src/stores/ — global state ({domain}-store.ts)
- src/types/ — shared types
- src/constants/ — shared constants

## File Naming: kebab-case
- Components: user-card.tsx
- Hooks: use-auth.ts
- Stores: auth-store.ts
- Next.js: page.tsx, layout.tsx, error.tsx

## Key Rules
- page.tsx = data fetching + composition only
- Route groups: (group-name)/
- One component per file
- 3+ files → add index.ts
- No source outside src/
- No deep relative paths → use @/
- Max 4 folder levels from src/
```

### 3-3. OpenAI (ChatGPT / GPTs)용 프롬프트

아래 내용을 Custom Instructions 또는 GPT Builder Instructions에 추가합니다.

```
## 웹앱 폴더 규약
- src/app/ — Next.js App Router (페이지, 레이아웃, API 라우트)
- src/components/ui/ — 범용 UI (비즈니스 로직 없음)
- src/components/layout/ — 레이아웃 (헤더, 사이드바)
- src/components/{도메인}/ — 도메인별 컴포넌트
- src/hooks/ — 커스텀 훅 (use-{기능}.ts)
- src/lib/ — 유틸리티, 설정, 라이브러리 래퍼
- src/stores/ — 전역 상태 ({도메인}-store.ts)
- src/types/ — 공유 타입
- src/constants/ — 공유 상수
- 파일명은 모두 kebab-case
- page.tsx는 데이터 페칭 + 컴포넌트 조합만 담당
- @/ alias 사용, 깊은 상대 경로 금지
- src/ 바깥에 소스 코드 두지 않음
```

---

## 4. AI 도구별 사용 방법

### 4-1. Claude Code

1. `.claude/skills/nmwc-webapp-folder-convention/SKILL.md`에 3-1 내용을 저장합니다.
2. 파일 생성 시 자동으로 참고됩니다.

### 4-2. Codex CLI

1. `.codex/skills/nmwc-webapp-folder-convention/SKILL.md`에 3-1 내용을 저장합니다.
2. Claude Code와 동일하게 동작합니다.

### 4-3. Cursor

1. `.cursor/rules/webapp-folder-convention.mdc`에 3-2 내용을 저장합니다.
2. `src/**/*` 파일 작업 시 자동으로 적용됩니다.

### 4-4. OpenAI (ChatGPT / GPTs)

1. 3-3 내용을 Custom Instructions 또는 GPT Builder Instructions에 추가합니다.

### 4-5. Claude Projects (claude.ai)

1. 3-1의 SKILL.md 내용을 Project Knowledge에 업로드합니다.

---

## 5. 스킬 인덱스에 등록

스킬 인덱스(INDEX.md)의 스킬 목록 표에 아래 행을 추가합니다.

```markdown
| nmwc-webapp-folder-convention | 웹앱 폴더 구조 및 파일 배치 규약 | ✅ 사용중 | SKILL.md | v1.0 | 2026-05-28 |
```

---

## 개정 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
| --- | --- | --- | --- |
| v1.0 | 2026-05-28 |  | 최초 작성 |