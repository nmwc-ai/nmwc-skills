# EVAL.md 템플릿

`//`는 지침(문서에 남기지 않음). 판정은 PASS/PARTIAL/FAIL 셋 중 하나만 쓴다. 근거 없는 판정은 `check_eval.py`가 걸러낸다.

```markdown
# EVAL — <feature>

**전체 판정**: 〈PASS | PARTIAL | FAIL〉
**검증일**: 〈YYYY-MM-DD〉
**대상 PRD**: `docs/prd/<feature>/<feature>-PRD.md` 〈또는 "없음 — spec만 검증"〉
**대상 Spec**: `.specs/spec_<feature>/spec.md`

## 1. AC 검증

// PRD의 US 단위로 묶는다. AC-ID는 PRD와 정확히 같은 표기를 쓴다(체크 스크립트가 대조한다).

### US-1.1 〈스토리 제목〉
| ID | 판정 | 근거 |
| --- | --- | --- |
| AC-1 | PASS | `src/app/login/page.tsx:42` — 로그인 성공 시 `/dashboard`로 이동 확인. 브라우저 재현: `eval-screenshots/ac-1-login-success.png` |
| AC-2 | FAIL | 미로그인 상태로 `/dashboard` 직접 접근 시 리다이렉트 없음(`middleware.ts`에 가드 미구현 — 코드 확인). 재현: `eval-screenshots/ac-2-no-redirect.png` |

### US-1.2 〈스토리 제목〉
| ID | 판정 | 근거 |
| --- | --- | --- |

## 2. 정책 준수 (Non-Requirements · Principles)
| 항목 | 판정 | 근거 |
| --- | --- | --- |
| Non-Req: 〈PRD의 Non-Requirements 항목〉 | PASS | 〈코드에 해당 기능 없음을 확인한 방법〉 |
| Principle: 〈PRD의 Principles 항목〉 | PASS | 〈어떻게 지켜지는지〉 |

## 3. 설계 대조 (spec.md)
| 항목 | 판정 | 근거 |
| --- | --- | --- |
| 데이터 모델: 〈타입/필드〉 | PASS | `src/types/user.ts:12` — spec.md §5와 필드 일치 |
| 파일 구성: 〈spec.md 표의 파일〉 | PASS | 실제 존재·역할 일치 확인 |

## 4. 브라우저 검증

- 실행 환경: 〈URL, 날짜〉
- 재현한 User Story: 〈목록〉
- 콘솔/네트워크 에러: 〈없음, 또는 발견 내용〉
- 스크린샷: `.specs/spec_<feature>/eval-screenshots/`
// 생략했다면 아래처럼 사유를 명시한다. "생략"이라고만 쓰고 넘어가지 않는다.
// 브라우저 검증 생략 — 사유: 〈로컬 서버 실행 불가 / claude-in-chrome 미연결 등〉. 관련 AC는 코드 검증만으로 판정.

## 5. 회귀 확인
- 〈실행한 테스트/타입체크/빌드 명령과 결과〉

## 6. 종합
- FAIL 항목: 〈AC-ID 목록, 또는 "없음"〉
- PARTIAL 항목: 〈AC-ID 목록과 부족한 점, 또는 "없음"〉
- 다음 조치: 〈구현자에게 넘길 구체적 지시, PASS면 "없음"〉
```
