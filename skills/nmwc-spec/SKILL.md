---
name: nmwc-spec
description: NMWC 스펙 주도 개발(Spec-Driven Development) 규격으로 기능 스펙 문서를 작성한다. `.specs/` 폴더에 기능 단위로 spec.md(설계)+PROGRESS.md(진행)를 만들고 INDEX.md를 갱신한다. spec.md에는 개요·데이터 모델·화면 구성·기술 구현을 상세히 담는다. "스펙 써줘", "spec 문서", "기능 설계 문서", ".specs", "스펙 주도 개발", "이 기능 스펙으로 정리" 요청 시 사용. 모호하면 nmwc-plan 인터뷰 게이트를 먼저 거친다.
---

# NMWC 스펙 작성 (nmwc-spec)

기능을 구현하기 전에 **설계를 문서로 먼저 확정**하는 스펙 주도 개발 규격. NMWC 팀 공통이다.
문서가 곧 살아있는 설계서가 되고, AI 코딩 도구가 이 문서를 맥락으로 참조해 일관되게 구현한다.

## 0. 시작 전 — 입력 확정

- `nmwc-plan` 게이트를 거쳐 왔거나 PRD가 있으면 그걸 입력으로 쓴다. Spec은 PRD의 Requirement 하나(또는 기능 하나)를 구현 층위로 상세화하는 것이다.
- 직접 호출됐고 요청이 모호하면(무엇을·어떤 데이터·어떤 화면인지 불명확) 먼저 `nmwc-plan/references/interview-gate.md`로 모호성을 제거한다.
- 모르는 설계 값은 지어내지 말고 `[확인 필요: ...]`로 남긴다 (`nmwc-plan/references/anti-slop.md`).

## 1. 스펙의 범위 (중요)

**1 스펙 = 1 기능 브랜치 = 1 PR** 단위로 잡는다. 너무 넓거나(인게임 전체) 너무 좁으면(버튼 색상) 안 된다.

```
❌ 너무 넓음: spec_dashboard_and_admin_and_settings
❌ 너무 좁음: spec_login_button_color
✅ 적절:     spec_login / spec_admin / spec_slack_messages
```

폴더명: `spec_{기능명}` — 영문 소문자 + 언더스코어만. 목적이 드러나게.

## 2. 폴더 구조 (스캐폴딩)

```
.specs/
├── INDEX.md                    ← 전체 스펙 목록·상태 (단일 현황판)
├── spec_{기능}/
│   ├── spec.md                 ← 설계 (무엇을·어떤 구조로) — 잘 안 변함
│   ├── PROGRESS.md             ← 진행 (어디까지·무엇이 남음) — 수시로 변함
│   └── references/             ← 참고 자료 (선택)
```

처음이거나 폴더가 없으면 스캐폴딩 스크립트로 만든다 (INDEX.md 자동 생성, 스펙 폴더 + 스텁 + INDEX 행 추가):

```bash
python3 scripts/init_specs.py <기능명> --title "<한 줄 제목>" --sprint <sp> --owner <담당자>
# 예: python3 scripts/init_specs.py user_auth --title "사용자 인증" --sprint sp5 --owner 담당자
```

이미 구조가 있으면 스크립트가 INDEX 행만 추가한다. 그다음 생성된 `spec.md`/`PROGRESS.md`를 아래 규격으로 채운다.

## 3. spec.md 작성

구조·섹션·예시는 `references/spec-template.md`를 **읽고** 따른다. 핵심:

- **가이드 필수 6개 (항상 포함)**: 개요 · 기술 스택 · 실행 환경 · 데이터 구조(모델) · 파일(페이지) 구성 · 변경 이력. 이 목록은 canonical 원본 `references/canonical/spec-driven-development.md` §4-3 이 규정한다. 하나라도 빠뜨리면 규격 미달이다.
- **기능 성격에 따라(선택)**: 라우팅·접근 제어·화면 구성(ASCII 와이어프레임)·섹션별 UI·데이터 저장 구조·기술 구현(컴포넌트/서버 액션)·API·의존성.
- **역할 분리**: 프로젝트 전역 스택·실행 환경이 프로젝트 CLAUDE.md에 이미 있으면, spec.md에는 "프로젝트 공통 + 이 스펙 고유: 〈...〉"만 한 줄로 적어 중복을 피한다. 프로젝트 문서가 없으면 spec.md에 명시한다.
- **단일 출처 원칙**: 설계 정보는 spec.md에만. 진행 상황은 PROGRESS.md에만. 전체 현황은 INDEX.md에만. 겹쳐 쓰지 않는다.
- 데이터 모델은 실제 타입(TypeScript interface / enum 등)으로. 화면은 ASCII 와이어프레임으로 배치를 보여준다 (레퍼런스 spec_admin 참조).

> **canonical 출처**: 이 스킬의 규격은 `references/canonical/`에 보관된 팀 원본 가이드(spec-driven-development.md·webapp-*-convention.md 등)에서 왔다. 규격 판단이 애매하면 canonical 원본이 최종 기준이다.

## 4. PROGRESS.md 작성

`references/progress-template.md` 참조. 영역별 진행도 · 작업 히스토리(날짜별) · 진행중/다음 할일 · **결정 기록**(무엇을 왜 그렇게 정했는지 — 대안 포함). 결정 기록은 "왜 이렇게 구현했지?"에 답하는 자산이다.

## 5. INDEX.md 갱신

`scripts/init_specs.py`가 새 행을 추가한다. 이후 상태가 바뀌면(진행중🟢→완료✅) 직접 갱신한다. 완료·폐기 스펙은 삭제하지 않고 상태만 바꾸며 목록 하단으로 옮긴다.

| 상태 | 아이콘 |
|------|--------|
| 진행중 | 🟢 |
| 보류 | 🟡 |
| 완료 | ✅ |
| 폐기 | ❌ |

## 6. HTML 뷰 (선택)

스펙 정본은 repo 안의 `.md`다(에디터·GitHub에서 읽음). 비개발 이해관계자와 공유하려면 정본에서 그대로 렌더한다 (단일 출처):

```bash
python3 scripts/render_doc.py .specs/spec_<기능>/spec.md spec_<기능>.html
```

표·TS 코드블록·ASCII 와이어프레임을 살려 `nmwc-prd`와 같은 디자인 토큰으로 낸다. 기본 산출은 `.md`이고, HTML은 공유가 필요할 때만 만든다.

## 7. 검증 게이트 (필수 — 통과 전 완료 금지)

spec.md를 다 쓰면 **완료를 선언하기 전에 반드시** 검증기를 통과시킨다. 강제 단계다.

```bash
python3 scripts/check_spec.py .specs/spec_<기능>/spec.md
```

이 검증기는 canonical(`references/canonical/spec-driven-development.md` §4-3)이 요구하는 구조를 검사한다:
- **가이드 필수 6개 섹션**(개요·기술 스택·실행 환경·데이터 구조·파일 구성·변경 이력)
- 미완성 `〈…〉` 플레이스홀더, `PROGRESS.md` 형제 존재, `INDEX.md` 등록, 단일 출처 위반(경고)

**exit 0 (PASS)가 나올 때까지 완료하지 않는다.** FAIL 항목을 고치고 재실행한다. 그다음 anti-slop 셀프 체크(`nmwc-plan/references/anti-slop.md`): 지어낸 설계 없음(`[확인 필요]`), 데이터 모델 구체적, 단일 출처 원칙.

## 8. 마무리
- 민감 정보(API 키·서버 주소·매출) 금지 — 스펙은 Git에 커밋되고 AI 도구에 전달된다.
- 스펙 문서 변경은 관련 코드 변경과 같은 커밋/PR에 포함시킨다.
