#!/usr/bin/env python3
"""스펙 주도 개발 스캐폴딩.

- `.specs/` 와 INDEX.md가 없으면 만든다.
- `.specs/spec_{name}/` 에 spec.md + PROGRESS.md 스텁을 만든다 (이미 있으면 건드리지 않음).
- INDEX.md 스펙 목록 표에 새 행을 추가한다 (이미 있으면 생략).

사용:
    python3 init_specs.py <기능명> [--title T] [--sprint SP] [--owner O]
                          [--deps D] [--specs-dir .specs]
    # 기능명은 spec_ 접두사 유무 무관 (자동 정규화)
"""
import argparse
import datetime
import re
from pathlib import Path

INDEX_TEMPLATE = """# 스펙 인덱스

> 전체 스펙 목록 및 상태를 관리합니다.

## 스펙 목록

| 스펙 | 상태 | 스프린트 | 담당자 | 의존성 | 최종 갱신 |
|------|------|---------|--------|--------|----------|

## 상태 범례

| 아이콘 | 상태 | 설명 |
|--------|------|------|
| 🟢 | 진행중 | 현재 개발이 진행 중인 스펙 |
| 🟡 | 보류 | 일시적으로 중단된 스펙 (사유를 PROGRESS.md에 기록) |
| ✅ | 완료 | 개발 및 QA가 완료된 스펙 |
| ❌ | 폐기 | 기획 변경 등으로 폐기된 스펙 (삭제하지 않고 상태만 변경) |

## 갱신 규칙
- 새 스펙을 생성하면 이 파일에 즉시 추가합니다.
- 스펙 상태가 변경되면 이 파일을 함께 갱신합니다.
- 완료 및 폐기된 스펙은 목록 하단으로 이동시킵니다.
"""


def normalize(name):
    """user_auth / spec_user_auth → (folder='spec_user_auth', short='user_auth')"""
    n = re.sub(r"[^a-z0-9_]+", "_", name.strip().lower()).strip("_")
    short = n[5:] if n.startswith("spec_") else n
    return f"spec_{short}", short


def spec_stub(short, title):
    # 가이드 필수 6개 섹션(개요·기술 스택·실행 환경·데이터 구조·파일 구성·변경 이력)을 스캐폴드.
    # 선택 섹션은 references/spec-template.md 참조.
    return f"""# spec_{short}

> {title or "〈이 스펙이 무엇인지 1~2줄〉"}

## 개요
〈무엇을·왜. 핵심 동작 요약.〉

## 기술 스택
〈이 스펙이 쓰는 라이브러리·SDK·프레임워크. 프로젝트 CLAUDE.md에 전역 스택이 있으면 "프로젝트 공통 + 이 스펙 고유: 〈...〉"만.〉

## 실행 환경
〈런타임·플랫폼·버전. 예: Node 20 / 브라우저 / Vercel〉

## 데이터 구조(모델)
〈실제 타입(interface/enum)으로. 모르면 [확인 필요: ...]〉

## 파일(페이지) 구성
| 파일 | 경로 | 설명 |
| --- | --- | --- |
| 〈file〉 | 〈경로〉 | 〈역할〉 |

## 변경 이력
| 날짜 | 변경 내용 |
| --- | --- |
| {today()} | 최초 작성 |

<!-- 선택 섹션(접근 제어·페이지 구성·섹션별 상세·데이터 저장 구조·기술 구현·API·의존성)은
     references/spec-template.md 규격으로 채운다. -->
"""


def progress_stub(short, title):
    return f"""# {title or short} — 진행 상황

## 영역별 진행도
| 영역 | 상태 | 비고 |
|------|------|------|
| 데이터 모델 | ⬜ 미착수 | |

## 작업 히스토리
### {today()}
- spec.md 최초 작성

## 진행중
- [ ] 〈현재 작업〉

## 다음 할일
- [ ] 〈다음 작업〉

## 결정 기록
〈비자명한 기술 선택마다 결정/대안/사유 3줄〉
"""


def today():
    return datetime.date.today().isoformat()


def add_index_row(index_path, folder, short, sprint, owner, deps):
    text = index_path.read_text(encoding="utf-8")
    row = (
        f"| [{short}]({folder}/spec.md) | 🟢 | {sprint or '-'} | "
        f"{owner or '-'} | {deps or '-'} | {today()} |"
    )
    if f"]({folder}/spec.md)" in text:
        return "이미 있음"

    lines = text.splitlines()
    # 스펙 목록 표의 구분선(|---|) 바로 뒤에 삽입
    sep_idx = None
    in_list = False
    for i, ln in enumerate(lines):
        if ln.strip().startswith("## 스펙 목록"):
            in_list = True
        elif in_list and re.match(r"^\|[\s\-|]+\|$", ln.strip()):
            sep_idx = i
            break
    if sep_idx is None:
        # 표를 못 찾으면 끝에 붙임
        lines.append(row)
    else:
        # 구분선 바로 아래의 빈 플레이스홀더 행(| | | |)은 제거
        insert_at = sep_idx + 1
        if insert_at < len(lines) and re.match(
            r"^\|(\s*\|)+\s*$", lines[insert_at].strip()
        ):
            lines.pop(insert_at)
        lines.insert(insert_at, row)
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "추가됨"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="기능명 (spec_ 접두사 유무 무관)")
    ap.add_argument("--title", default="")
    ap.add_argument("--sprint", default="")
    ap.add_argument("--owner", default="")
    ap.add_argument("--deps", default="")
    ap.add_argument("--specs-dir", default=".specs")
    args = ap.parse_args()

    folder, short = normalize(args.name)
    specs = Path(args.specs_dir)
    specs.mkdir(parents=True, exist_ok=True)

    index = specs / "INDEX.md"
    if not index.exists():
        index.write_text(INDEX_TEMPLATE, encoding="utf-8")
        print(f"✓ {index} 생성")

    spec_dir = specs / folder
    created = []
    spec_dir.mkdir(exist_ok=True)
    for fname, content in (
        ("spec.md", spec_stub(short, args.title)),
        ("PROGRESS.md", progress_stub(short, args.title)),
    ):
        fp = spec_dir / fname
        if fp.exists():
            print(f"→ {fp} (이미 존재, 유지)")
        else:
            fp.write_text(content, encoding="utf-8")
            created.append(fname)
    if created:
        print(f"✓ {spec_dir}/ 생성: {', '.join(created)}")

    status = add_index_row(index, folder, short, args.sprint, args.owner, args.deps)
    print(f"✓ INDEX.md 행 {status}: {short}")
    print(f"\n다음: {spec_dir}/spec.md 를 spec-template.md 규격으로 채우세요.")


if __name__ == "__main__":
    main()
