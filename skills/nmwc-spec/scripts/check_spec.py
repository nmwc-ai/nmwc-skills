#!/usr/bin/env python3
"""spec.md canonical(spec-driven-development.md §4-3) 준수 강제 검증기.

가이드 필수 6개 섹션 + 단일 출처 구조(PROGRESS.md·INDEX 등록)를 검사한다.
하나라도 HARD FAIL이면 exit 1 — 스킬은 통과할 때까지 완료를 선언하지 못한다.

사용:
    python3 check_spec.py <.specs/spec_기능/spec.md>
"""
import re
import sys
from pathlib import Path


def headings(md):
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.*)$", md, re.M)]


def has(hs, *names):
    low = [h.lower() for h in hs]
    return any(any(n.lower() in h for h in low) for n in names)


def main():
    if len(sys.argv) < 2:
        print("사용: python3 check_spec.py <spec.md>")
        sys.exit(2)
    spec_path = Path(sys.argv[1])
    md = spec_path.read_text(encoding="utf-8")
    hs = headings(md)
    fails, warns = [], []

    # 1) 가이드 필수 6개 섹션
    required = [
        ("개요", ("개요", "overview")),
        ("기술 스택", ("기술 스택", "tech stack", "기술스택")),
        ("실행 환경", ("실행 환경", "실행환경", "runtime", "환경")),
        ("데이터 구조(모델)", ("데이터 구조", "데이터 모델", "data model", "데이터모델")),
        ("파일(페이지) 구성", ("파일", "파일 구성", "파일(페이지)", "file")),
        ("변경 이력", ("변경 이력", "change log", "개정 이력", "changelog")),
    ]
    for label, names in required:
        if not has(hs, *names):
            fails.append(f"가이드 필수 섹션 누락: {label}")

    # 2) 미완성 플레이스홀더 (〈 〉) — [확인 필요]는 허용
    if re.search(r"[〈〉]", md):
        n = len(re.findall(r"〈[^〉]*〉", md))
        fails.append(f"미완성 플레이스홀더 〈…〉 {n}곳 — 채우거나 [확인 필요: ...]로")

    # 3) 단일 출처 구조: PROGRESS.md 형제 존재
    folder = spec_path.parent
    if not (folder / "PROGRESS.md").exists():
        fails.append(f"PROGRESS.md 없음 ({folder}/PROGRESS.md) — 진행/결정 기록 분리 필요")

    # 4) INDEX.md 등록 확인
    index = folder.parent / "INDEX.md"
    if not index.exists():
        warns.append(f"INDEX.md를 찾지 못함 ({index}) — 전체 현황판 등록 확인 필요")
    else:
        if folder.name not in index.read_text(encoding="utf-8"):
            fails.append(f"INDEX.md에 '{folder.name}' 행이 없음 — 스펙 목록 등록 필요")

    # 5) 단일 출처 위반: spec.md 안에 진행률/체크박스 진행표가 섞였는가 (WARN)
    if re.search(r"진행\s*상황|진행도|작업\s*히스토리|다음\s*할일", md):
        warns.append("spec.md에 진행 상황 표현이 보임 — 진행/결정은 PROGRESS.md로 (단일 출처)")

    # 리포트
    print(f"=== spec canonical 검증: {spec_path} ===")
    print(f"섹션 {len(hs)}개 · 폴더 {folder.name}")
    if warns:
        print(f"\n⚠ 경고 {len(warns)}건:")
        for w in warns:
            print(f"  - {w}")
    if fails:
        print(f"\n✗ HARD FAIL {len(fails)}건:")
        for f in fails:
            print(f"  - {f}")
        print("\n→ 위 항목을 고치고 다시 검증하세요. (완료 선언 불가)")
        sys.exit(1)
    print("\n✓ PASS — 가이드 필수 6개 섹션 + 단일 출처 구조를 충족합니다."
          + (" (경고는 검토 후 판단)" if warns else ""))


if __name__ == "__main__":
    main()
