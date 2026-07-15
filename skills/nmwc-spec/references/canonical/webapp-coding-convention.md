# NMWC 스킬 - 웹 앱 코딩 규약

> NMWC 웹앱(React + TypeScript / Next.js) 코딩 규약을 AI 도구에 스킬로 등록하여,
누가 어떤 AI 도구를 사용하든 동일한 코딩 규약에 맞는 코드를 생성하도록 하기 위한 가이드입니다.
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

웹앱 코딩 규약 스킬은 NMWC의 **React + TypeScript 코딩 규약**을 AI 도구가 코드 작성 시 자동으로 참고하도록 만든 지침 파일입니다.

### 이 스킬의 범위

| 포함 | 미포함 |
| --- | --- |
| 네이밍 표기법 (PascalCase, camelCase, kebab-case, UPPER_SNAKE_CASE) | 폴더 구조 (→ 웹앱 폴더 규약 스킬) |
| 대상별 네이밍 규칙 (컴포넌트, 타입, 훅, 변수, 상수, enum) | Git 브랜치 규약 |
| 컴포넌트 규약 (함수 컴포넌트, Props, export) | 배포 설정 |
| 타입 규약 (type vs interface, any 금지) |  |
| 임포트 순서 |  |

---

## 2. 스킬에 포함된 규칙 요약

### 표기법

| 표기법 | 적용 대상 | 예시 |
| --- | --- | --- |
| PascalCase | 컴포넌트, 타입, 인터페이스, enum | `UserProfile`, `EPaymentStatus` |
| camelCase | 변수, 함수, 훅, 파라미터 | `userName`, `handleClick`, `useAuth` |
| UPPER_SNAKE_CASE | 상수 | `MAX_RETRY_COUNT` |
| kebab-case | 파일명, 폴더명 | `user-profile.tsx` |

### 대상별 규칙

| 대상 | 규칙 |
| --- | --- |
| 컴포넌트 | 함수 컴포넌트만 사용, named export (페이지는 default export) |
| 인터페이스 | I 접두사 사용하지 않음 |
| Props | `{컴포넌트명}Props` 형식, 구조분해 할당 |
| boolean 변수 | `is`, `has`, `can`, `should` 접두사 |
| 이벤트 핸들러 | `handle` 접두사, 콜백 Props는 `on` 접두사 |
| 커스텀 훅 | `use` 접두사 필수 |
| enum | `E` 접두사 + PascalCase, 문자열 enum 기본 |
| 상수 | UPPER_SNAKE_CASE |

---

## 3. 스킬 리소스

### 3-1. SKILL.md (Claude Code / Codex CLI / Claude Projects 공용)

아래 내용을 `SKILL.md`로 저장합니다.

```
# NMWC Web App Coding Convention

## Naming

| Convention | Targets | Example |
|------------|---------|---------|
| PascalCase | Components, Types, Interfaces, Enums | `UserProfile`, `EPaymentStatus` |
| camelCase | Variables, Functions, Hooks, Params | `userName`, `handleClick`, `useAuth` |
| UPPER_SNAKE_CASE | Constants | `MAX_RETRY_COUNT`, `API_BASE_URL` |
| kebab-case | File names, Folder names | `user-profile.tsx`, `use-auth.ts` |

## Component Rules
- Function components only (no class components)
- Named export for components, default export only for Next.js pages
- Props type: `{ComponentName}Props`, use destructuring
- Max 200 lines per component file; split if exceeded

## Naming Details
- Boolean: `is`, `has`, `can`, `should` prefix → `isLoading`, `hasPermission`
- Event handler: `handle` prefix → `handleSubmit`
- Callback props: `on` prefix → `onSubmit`, `onChange`
- Custom hook: `use` prefix → `useAuth`, `useDebounce`
- Interface: NO `I` prefix → `UserProfileProps` (not `IUserProfileProps`)
- Enum: `E` prefix + PascalCase, string enum values → `EUserRole { Admin = 'ADMIN' }`

## Type Rules
- Object shapes → `interface`
- Unions, intersections, utilities → `type`
- NEVER use `any` — use `unknown` with type guards
- All API responses must have defined types

## Import Order
1. React / Next.js
2. External libraries
3. Internal modules (`@/`)
4. Relative imports (same folder)
5. Type imports (`import type`)
Blank line between each group.

## Path Alias
- Use `@/` for absolute imports
- Never use deep relative paths like `../../`

## State Management
- Local: `useState`, `useReducer` (3+ related states)
- Global: Zustand (domain-separated stores)
- Server: React Query wrapped in custom hooks

## Error Handling
- API errors: try-catch with typed errors
- Component errors: Error Boundary / Next.js error.tsx

## Exceptions
- `_` for unused params
- Accepted abbreviations: URL, API, ID, UI, DB
```

### 3-2. Cursor용 .mdc 파일

아래 내용을 `.cursor/rules/webapp-coding-convention.mdc`로 저장합니다.

```markdown
---
description: NMWC 웹앱 코딩 규약. TypeScript/React 코드 작성, 리팩토링, 리뷰 시 자동으로 참고됩니다.
globs: src/**/*.{ts,tsx}
alwaysApply: false
---

# NMWC Web App Coding Convention

## Naming
- PascalCase: Components, Types, Interfaces, Enums
- camelCase: Variables, Functions, Hooks, Params
- UPPER_SNAKE_CASE: Constants
- kebab-case: File/folder names

## Key Rules
- Function components only, named export (default only for pages)
- Props: `{Component}Props`, destructure
- Boolean: `is/has/can/should` prefix
- Handlers: `handle` prefix, callback props: `on` prefix
- Hooks: `use` prefix
- Enum: `E` prefix, string values
- Interface: NO `I` prefix
- Object shapes → interface, unions → type
- No `any`, use `unknown`
- Import order: React → External → @/ → Relative → Types
- `@/` alias, no deep relative paths
```

### 3-3. OpenAI (ChatGPT / GPTs)용 프롬프트

아래 내용을 Custom Instructions 또는 GPT Builder Instructions에 추가합니다.

```
## 웹앱 코딩 규약
- PascalCase: 컴포넌트, 타입, 인터페이스, enum
- camelCase: 변수, 함수, 훅, 파라미터
- UPPER_SNAKE_CASE: 상수
- kebab-case: 파일명, 폴더명
- 함수 컴포넌트만 사용, named export (페이지만 default export)
- Props는 {컴포넌트명}Props 형식, 구조분해 할당
- boolean 변수는 is/has/can/should 접두사
- 이벤트 핸들러는 handle 접두사, 콜백 Props는 on 접두사
- 커스텀 훅은 use 접두사 필수
- 인터페이스에 I 접두사 사용하지 않음
- enum은 E 접두사 + PascalCase, 문자열 값 사용
- any 사용 금지, unknown + 타입 가드 사용
- @/ alias로 절대 경로 임포트, 깊은 상대 경로 금지
```

---

## 4. AI 도구별 사용 방법

### 4-1. Claude Code

1. `.claude/skills/nmwc-webapp-coding-convention/SKILL.md`에 3-1 내용을 저장합니다.
2. 코드 작성 시 자동으로 참고됩니다.

### 4-2. Codex CLI

1. `.codex/skills/nmwc-webapp-coding-convention/SKILL.md`에 3-1 내용을 저장합니다.
2. Claude Code와 동일하게 동작합니다.

### 4-3. Cursor

1. `.cursor/rules/webapp-coding-convention.mdc`에 3-2 내용을 저장합니다.
2. `src/**/*.{ts,tsx}` 파일 작업 시 자동으로 적용됩니다.

### 4-4. OpenAI (ChatGPT / GPTs)

1. 3-3 내용을 Custom Instructions 또는 GPT Builder Instructions에 추가합니다.

### 4-5. Claude Projects (claude.ai)

1. 3-1의 SKILL.md 내용을 Project Knowledge에 업로드합니다.

---

## 5. 스킬 인덱스에 등록

스킬 인덱스(INDEX.md)의 스킬 목록 표에 아래 행을 추가합니다.

```markdown
| nmwc-webapp-coding-convention | 웹앱 코딩 규약 (React+TS 네이밍, 컴포넌트, 타입) | ✅ 사용중 | SKILL.md | v1.0 | 2026-05-28 |
```

---

## 개정 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
| --- | --- | --- | --- |
| v1.0 | 2026-05-28 |  | 최초 작성 |