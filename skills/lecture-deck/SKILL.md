---
name: lecture-deck
description: 스크롤형 강의·발표 슬라이드 덱을 만드는 스킬. 다크 OKLCH 그레이스케일 + Geist + scroll-snap 풀스크린 섹션 + reveal 애니메이션의 일관된 디자인 언어로 렉쳐 덱을 생성한다. 두 가지 모드 — (A) Next.js route 스캐폴드, (B) 단일 self-contained HTML. "렉쳐 덱", "강의 덱", "슬라이드 덱", "발표 덱", "스크롤 덱", "lecture deck", "덱 만들어", "슬라이드 만들어" 요청 시 사용.
---

# Lecture Deck Skill

스크롤형 강의·발표 덱을 **일관된 디자인 언어**로 만드는 스킬. `ai-coding-deck` repo의 3개 덱(deck / agents-2026 / health-research)에서 추출한 검증된 패턴이다.

핵심은 두 가지 — **디자인 스타일**(다크 그레이스케일, Geist, 글라스 카드)과 **표현 방식**(풀스크린 scroll-snap 섹션, reveal 애니메이션, 넘버링 카드 그리드, 우측 점 네비). 이 둘을 그대로 재현한다.

---

## 0. 모드 선택 (먼저 결정)

두 가지 산출물 형태를 지원한다. 요청 맥락으로 판단하되 애매하면 사용자에게 1개 질문으로 확정한다.

| 모드 | 언제 | 산출물 |
|------|------|--------|
| **A. Next.js route** (기본) | Next.js(App Router) repo 안에서 작업 중 · `src/app/` 존재 · "이 repo에 덱 추가" | `src/app/<slug>/` 폴더 (page.tsx + sections/ + 필요 시 hooks/shell) |
| **B. 단일 HTML** | Next.js가 아닌 곳 · "혼자 열리는 파일" · 빠른 공유·이메일 첨부 · 아무 데서나 | self-contained `<slug>.html` 1개 (인라인 CSS/JS) |

판단 규칙: cwd에 `next.config.*` + `src/app/`이 있으면 → A 기본. 없으면 → B 기본. 사용자가 "HTML로", "혼자 열리게"라고 하면 B. "route로", "repo에 추가"면 A.

---

## 1. 디자인 언어 (두 모드 공통 — 절대 바꾸지 말 것)

### 팔레트 — 다크 OKLCH 그레이스케일
| 토큰 | 값 | 용도 |
|------|-----|------|
| background | `oklch(0.145 0 0)` | 페이지 배경 (near-black) |
| foreground | `oklch(0.985 0 0)` | 본문 텍스트 (near-white) |
| card | `oklch(0.205 0 0)` | 카드 배경 |
| muted / secondary / accent | `oklch(0.269 0 0)` | 보조 표면 |
| muted-foreground | `oklch(0.708 0 0)` | 서브텍스트·부제 (회색) |
| primary | `oklch(0.922 0 0)` | 강조 (밝은 회백) |
| destructive | `oklch(0.704 0.191 22.216)` | 경고·부정 (빨강) |
| border | `oklch(1 0 0 / 10%)` | 카드 테두리 |
| radius | `0.625rem` (카드는 `rounded-2xl`) | |

무채색이 원칙. 컬러는 의미 신호로만 아껴 쓴다 — 성공/체크 = `green-500` 계열(`text-green-400 bg-green-500/10 border-green-500/40`), 경고/부정 = destructive 빨강. 색으로 예쁘게 하려 하지 말 것.

### 타이포그래피 — Geist Sans + Geist Mono
- **본문/제목**: Geist Sans (`--font-geist-sans`)
- **모노**: Geist Mono (`--font-geist-mono`) — eyebrow 라벨, 넘버링(01·02), 코드/프롬프트에만
- 스케일:
  - 타이틀 h1: `text-5xl font-bold tracking-tight sm:text-7xl` (2번째 줄은 `<span className="text-muted-foreground">`로 톤다운)
  - 섹션 h2: `text-3xl font-bold tracking-tight sm:text-5xl` (또는 `sm:text-6xl`)
  - eyebrow: `font-mono text-xs tracking-widest text-muted-foreground uppercase` (예: `Part 1 · The Filter`)
  - 부제: `text-base text-muted-foreground` (또는 `text-lg`)
  - 카드 본문: `text-sm text-muted-foreground leading-relaxed`, 작은 건 `text-xs`

### 카드 (핵심 표현 단위)
```
rounded-2xl border border-border/40 bg-card/80 p-4 shadow-sm backdrop-blur-sm
```
- 넘버링 카드: 좌측에 `<span className="font-mono text-sm text-primary shrink-0 mt-0.5">01</span>` (또는 `text-muted-foreground/50`로 dim) + 우측 `title`(`text-sm font-semibold`) + `desc`
- 그리드: `grid grid-cols-1 sm:grid-cols-2 gap-3`, 마지막 홀수 항목은 `sm:col-span-2`로 풀폭

### 레이아웃·표현 방식
- **풀스크린 scroll-snap 섹션** — 한 슬라이드 = 한 화면. 컨테이너 `h-screen overflow-y-auto snap-y sm:snap-mandatory`
- **뷰포트를 채운다 (fill) — 콘텐츠가 중앙에 작게 몰리면 안 된다.** 콘텐츠가 세로로 ~70% 이상을 차지하게 만든다. 핵심 레버는 폰트 크기가 아니라 **세로 여백(gap·padding·margin)**: 카드 padding·그리드 gap·요소 간 margin을 넉넉히 준다. 단일 HTML(모드 B)은 `html{font-size:120~128%}`로 루트 스케일을 올려 rem 기반 타입·여백·wrap을 한 번에 키운다(콘텐츠가 여전히 작으면 130%까지). 차트 막대·이미지 등 px 고정 요소는 별도로 키운다. 슬라이드가 밀도 낮으면(카드 3개 등) 억지로 늘리지 말고 여백 균형을 유지.
- **홀짝 배경 교차** — 홀수 섹션 `bg-muted/20`로 미묘한 리듬
- **reveal 애니메이션** — 섹션 진입 시 `opacity-0 translate-y-6` → `opacity-100 translate-y-0` (`duration-700 ease-out`). 요소별 `style={{ transitionDelay: "80ms" | "150ms" | "300ms" }}`로 stagger
- **우측 점 네비게이션** — fixed, 모바일 숨김(`hidden sm:flex`), 현재 섹션 점은 글로우
- **키보드 네비** — ↑/↓/Space로 섹션 이동
- 타이틀 슬라이드 하단에 `SCROLL ↓` (`animate-bounce`)

---

## 2. 슬라이드 컴포넌트 계약 (Route 모드)

모든 슬라이드는 이 형태를 지킨다:
```tsx
"use client";
import { forwardRef } from "react";
import SectionShell from "./section-shell";   // 같은 덱 폴더 기준
import { cn } from "@/lib/utils";

interface P { anim: (i: number) => string; index: number; }

const S = forwardRef<HTMLElement, P>(({ anim, index }, ref) => (
  <SectionShell ref={ref} index={index}>
    {/* eyebrow → h2 → 부제 → 카드 그리드 */}
  </SectionShell>
));
S.displayName = "S02FiveFilters";
export default S;
```
- 표시하고 싶은 모든 요소에 `className={cn("...", anim(index))}` 를 걸어 reveal 대상으로 만든다.
- 데이터는 컴포넌트 상단 `const items = [...]` 배열로 두고 `.map()` 렌더.
- 파일당 1 슬라이드, 200줄 이하.

`page.tsx`는 `sectionLabels`(우측 네비 라벨) + `sectionComponents`(순서) 두 배열로 조립한다. 템플릿: `references/route-page.tsx`.

---

## 3. 실행 절차

### 모드 A — Next.js route
1. **덱 slug 확정** (예: `agents-2026`). 대상 = `src/app/<slug>/`.
2. **공유 인프라 확인**: 같은 repo에 이미 덱이 있고 `hooks.ts`/`section-shell.tsx`가 있으면 **재사용**(import 경로만 상대경로로). 없으면 `references/hooks.ts`·`references/section-shell.tsx`를 `src/app/<slug>/`에 복사.
3. **`@/lib/utils`의 `cn` 확인** — 없으면 생성: `import { clsx, type ClassValue } from "clsx"; import { twMerge } from "tailwind-merge"; export function cn(...i: ClassValue[]) { return twMerge(clsx(i)); }` (deps: `clsx tailwind-merge`).
4. **디자인 토큰 확인** — `globals.css`에 위 OKLCH 토큰 + `@theme inline` 매핑이 없으면 `references/design-tokens.css` 내용을 병합. Geist 폰트를 `layout.tsx`에서 `next/font/google`로 로드.
5. **슬라이드 작성** — 콘텐츠 아웃라인을 슬라이드 단위로 쪼개, `references/slide-template.tsx`를 복제해 각 `sections/NN-name.tsx` 생성. 00은 항상 타이틀.
6. **page.tsx 조립** — `references/route-page.tsx`에서 import·`sectionLabels`·`sectionComponents`·`SECTION_COUNT` 채움.
7. **검증** — `pnpm lint` + `pnpm dev`로 `/<slug>` 확인. (이 repo는 로컬 `pnpm build` 금지 — repo CLAUDE.md 참조. 프로덕션 검증은 Vercel 배포 URL.)

### 모드 B — 단일 HTML
1. `references/standalone.html`을 복제.
2. `<title>`, 타이틀 슬라이드, 각 `<section>` 슬라이드를 콘텐츠로 채움. CSS 토큰·scroll-snap·IntersectionObserver reveal·점 네비가 이미 인라인으로 들어있음.
3. Geist는 CSP 안전을 위해 시스템 폰트 폴백 사용(외부 폰트 로드 불가 환경 대비). 필요 시 `<link>` 추가.
4. 브라우저로 열어 확인 후 파일 전달.

---

## 4. 콘텐츠 표현 원칙 (강의 덱다움)

- **한 슬라이드 한 메시지.** h2로 결론을 먼저, 카드로 근거를 편다.
- **넘버링 카드 그리드**가 기본 표현. 3~7개 항목을 2열로. 텍스트 벽 금지.
- **eyebrow로 파트 구분** (`Part 1 · ...`). 긴 덱은 recap 슬라이드를 중간에.
- **부제 1줄로 슬라이드 맥락** — "흔한 실수 7가지 — 미리 알면 절반은 피한다"처럼 구어체 요약.
- 카피는 짧고 단정적으로. 회색(muted-foreground)이 정보 위계의 90%를 처리한다 — 강조는 흰색/primary로 아껴서.
- 프롬프트·코드 예시는 mono + `whitespace-pre-wrap` 카드. 복사 버튼 필요하면 `references/`의 template-card 패턴 참고.

## 5. 참조 파일
- `references/route-page.tsx` — page.tsx 조립 템플릿 (점 네비 + snap 컨테이너)
- `references/hooks.ts` — useRevealAnimation / useSectionObserver / useKeyboardNav
- `references/section-shell.tsx` — SectionShell (snap·홀짝배경·max-w-6xl)
- `references/slide-template.tsx` — 슬라이드 1개 시작점 (eyebrow+h2+카드그리드)
- `references/design-tokens.css` — globals.css에 병합할 OKLCH 토큰
- `references/standalone.html` — 모드 B 전체 self-contained 템플릿
