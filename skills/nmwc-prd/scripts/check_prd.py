#!/usr/bin/env python3
"""PRD.md canonical 준수 강제 검증기.

references/canonical (NMWC PRD 템플릿 + User Story 샘플)이 요구하는
구조를 실제로 갖췄는지 프로그램으로 검사한다. 하나라도 HARD FAIL이면 exit 1 —
스킬은 통과할 때까지 완료를 선언하지 못한다.

사용:
    python3 check_prd.py <feature>-PRD.md
"""
import re
import sys
from pathlib import Path

SLOP = ["혁신적", "원활한", "원활하게", "seamless", "매끄럽게", "다양한", "강력한",
        "최적화된", "직관적", "손쉽게", "완벽한", "robust", "간편하게"]


def headings(md):
    return [(len(m.group(1)), m.group(2).strip())
            for m in re.finditer(r"^(#{1,6})\s+(.*)$", md, re.M)]


def has_section(hs, *names):
    low = [h.lower() for _, h in hs]
    return any(any(n.lower() in h for h in low) for n in names)


def main():
    if len(sys.argv) < 2:
        print("사용: python3 check_prd.py <PRD.md>")
        sys.exit(2)
    md = Path(sys.argv[1]).read_text(encoding="utf-8")
    hs = headings(md)
    fails, warns = [], []

    # 1) 필수 섹션 (NMWC PRD 템플릿)
    required = [
        ("Background/배경", ("background", "배경")),
        ("Goal/목표", ("goal", "목표")),
        ("Hypothesis/가설", ("hypothesis", "가설")),
        ("Principles/원칙", ("principles", "원칙")),
        ("Scope/범위", ("scope", "범위")),
        ("Requirements", ("requirements", "요구사항")),
        ("Non-Requirements", ("non-requirement", "non requirement", "비요구", "하지 않")),
        ("Future Work", ("future work", "future-work", "추후", "나중")),
        ("User Story", ("user story", "user-story", "유저 스토리", "사용자 스토리")),
        ("변경 이력", ("변경 이력", "change log", "changelog", "개정 이력")),
    ]
    for label, names in required:
        if not has_section(hs, *names):
            fails.append(f"필수 섹션 누락: {label}")

    # 2) Epic + User Story ID
    epics = [h for _, h in hs if re.search(r"epic|에픽", h, re.I)]
    if not epics:
        fails.append("Epic이 하나도 없음 (### EPIC n — 제목)")
    us_ids = re.findall(r"US-\d+\.\d+", md)
    if not us_ids:
        fails.append("US-x.y 형식 유저 스토리 ID가 없음")

    # 3) 각 User Story에 AC가 있는가
    us_headings = [(m.start(), m.group(0))
                   for m in re.finditer(r"^#{2,6}\s+US-\d+\.\d+.*$", md, re.M)]
    for idx, (pos, htext) in enumerate(us_headings):
        end = us_headings[idx + 1][0] if idx + 1 < len(us_headings) else len(md)
        block = md[pos:end]
        if not re.search(r"AC-\d+|인수\s*조건|acceptance", block, re.I):
            usid = re.search(r"US-\d+\.\d+", htext)
            fails.append(f"AC 없는 User Story: {usid.group(0) if usid else htext.strip()}")

    # 4) 미완성 플레이스홀더 (〈 〉) — [확인 필요]는 허용
    ph = re.findall(r"[〈〉]", md)
    if ph:
        n = len(re.findall(r"〈[^〉]*〉", md))
        fails.append(f"미완성 플레이스홀더 〈…〉 {n}곳 — 채우거나 [확인 필요: ...]로 바꿀 것")

    # 5) Non-Requirements 비어있지 않은가
    m = re.search(r"#{2,6}\s+.*(non-requirement|비요구|하지 않).*$", md, re.I | re.M)
    if m:
        start = m.end()
        nxt = re.search(r"^#{2,6}\s", md[start:], re.M)
        body = md[start:start + (nxt.start() if nxt else len(md) - start)]
        items = [l for l in body.splitlines() if re.match(r"\s*[-*]|\s*- \[", l) and l.strip(" -*[]") ]
        if not items:
            fails.append("Non-Requirements 섹션이 비어 있음 (안 할 것을 최소 1개 명시)")

    # 6) 슬롭 형용사 (WARN)
    for w in SLOP:
        for m in re.finditer(re.escape(w), md):
            line_no = md[:m.start()].count("\n") + 1
            warns.append(f"슬롭 후보 '{w}' (line {line_no}) — 관찰 가능한 행동·수치로 바꿀 것")

    # 리포트
    print(f"=== PRD canonical 검증: {sys.argv[1]} ===")
    print(f"섹션 {len(hs)}개 · US {len(set(us_ids))}개 · Epic {len(epics)}개")
    if warns:
        print(f"\n⚠ 경고 {len(warns)}건 (검토 권장):")
        for w in warns[:20]:
            print(f"  - {w}")
    if fails:
        print(f"\n✗ HARD FAIL {len(fails)}건:")
        for f in fails:
            print(f"  - {f}")
        print("\n→ 위 항목을 고치고 다시 검증하세요. (완료 선언 불가)")
        sys.exit(1)
    print("\n✓ PASS — canonical 필수 구조를 모두 충족합니다."
          + (" (경고는 검토 후 판단)" if warns else ""))


if __name__ == "__main__":
    main()
