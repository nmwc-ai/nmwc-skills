#!/usr/bin/env python3
"""EVAL.md canonical 준수 강제 검증기.

PRD의 모든 AC가 EVAL.md에 빠짐없이 등장하는지, FAIL/PARTIAL 판정에 근거가
있는지, 전체 판정이 하위 판정과 모순되지 않는지, 브라우저 검증 섹션이
비어있지 않은지를 프로그램으로 검사한다. 하나라도 HARD FAIL이면 exit 1 —
스킬은 통과할 때까지 완료를 선언하지 못한다.

사용:
    python3 check_eval.py <EVAL.md> [<feature>-PRD.md]
    (PRD.md를 생략하면 AC 커버리지 검사는 건너뛰고 구조만 검사한다)
"""
import re
import sys
from pathlib import Path

VERDICTS = ("PASS", "PARTIAL", "FAIL")


def headings(md):
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.*)$", md, re.M)]


def has(hs, *names):
    low = [h.lower() for h in hs]
    return any(any(n.lower() in h for h in low) for n in names)


def us_blocks(md):
    """US-x.y 헤딩 기준으로 문서를 블록 단위로 쪼갠다."""
    marks = [(m.start(), m.group(0)) for m in re.finditer(r"^#{2,6}\s+.*US-\d+\.\d+.*$", md, re.M)]
    blocks = {}
    for idx, (pos, htext) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(md)
        usid = re.search(r"US-\d+\.\d+", htext).group(0)
        blocks[usid] = md[pos:end]
    return blocks


def ac_ids(block):
    return set(re.findall(r"AC-\d+", block))


def eval_ac_rows(block):
    """EVAL.md 블록에서 `| AC-n | 판정 | 근거 |` 행을 파싱한다."""
    rows = {}
    for m in re.finditer(r"\|\s*(AC-\d+)\s*\|\s*(\S+)\s*\|\s*(.*?)\s*\|\s*$", block, re.M):
        acid, verdict, evidence = m.group(1), m.group(2), m.group(3)
        rows[acid] = (verdict, evidence)
    return rows


def main():
    if len(sys.argv) < 2:
        print("사용: python3 check_eval.py <EVAL.md> [<PRD.md>]")
        sys.exit(2)

    eval_path = Path(sys.argv[1])
    md = eval_path.read_text(encoding="utf-8")
    hs = headings(md)
    fails, warns = [], []

    # 1) 필수 섹션
    required = [
        ("AC 검증", ("ac 검증", "인수 조건")),
        ("정책 준수", ("정책 준수", "non-requirement", "principles")),
        ("설계 대조", ("설계 대조", "spec")),
        ("브라우저 검증", ("브라우저 검증",)),
        ("회귀 확인", ("회귀 확인", "regression")),
        ("종합", ("종합", "summary")),
    ]
    for label, names in required:
        if not has(hs, *names):
            fails.append(f"필수 섹션 누락: {label}")

    # 2) 전체 판정 필드
    m_overall = re.search(r"전체\s*판정\**\s*[:：]\s*[〈\[]?\s*(PASS|PARTIAL|FAIL)", md, re.I)
    if not m_overall:
        fails.append("'전체 판정' 필드가 없거나 PASS/PARTIAL/FAIL 중 하나가 아님")
    overall = m_overall.group(1).upper() if m_overall else None

    # 3) EVAL.md 내 AC 행 파싱 (US 블록 단위)
    eval_blocks = us_blocks(md)
    all_row_verdicts = []
    for usid, block in eval_blocks.items():
        for acid, (verdict, evidence) in eval_ac_rows(block).items():
            all_row_verdicts.append((usid, acid, verdict, evidence))

    if not all_row_verdicts:
        fails.append("AC 판정 행을 하나도 찾지 못함 (`| AC-n | PASS|PARTIAL|FAIL | 근거 |` 형식 확인)")

    # 4) 판정 형식 + 근거 확인
    for usid, acid, verdict, evidence in all_row_verdicts:
        if verdict.upper() not in VERDICTS:
            fails.append(f"판정 형식 오류: {usid} {acid} = '{verdict}' (PASS/PARTIAL/FAIL만 허용)")
        elif verdict.upper() in ("FAIL", "PARTIAL") and (not evidence or evidence.strip() in ("-", "")):
            fails.append(f"근거 없는 {verdict.upper()}: {usid} {acid} — 근거 칸이 비어 있음")

    # 5) PRD 대비 AC 커버리지 (PRD 인자가 있을 때만)
    if len(sys.argv) >= 3:
        prd_path = Path(sys.argv[2])
        if prd_path.exists():
            prd_md = prd_path.read_text(encoding="utf-8")
            prd_blocks = us_blocks(prd_md)
            for usid, block in prd_blocks.items():
                expected = ac_ids(block)
                if not expected:
                    continue
                if usid not in eval_blocks:
                    fails.append(f"EVAL.md에 US 전체 누락: {usid}")
                    continue
                got = set(eval_ac_rows(eval_blocks[usid]).keys())
                missing = expected - got
                if missing:
                    fails.append(f"AC 누락: {usid} — {', '.join(sorted(missing))} 가 EVAL.md에 없음")
        else:
            warns.append(f"PRD 경로를 찾지 못함 ({prd_path}) — AC 커버리지 검사 생략")
    else:
        warns.append("PRD.md 인자 없음 — AC 커버리지 검사 생략 (구조만 검사)")

    # 6) 전체 판정과 하위 판정 일관성
    if overall and all_row_verdicts:
        verdicts_upper = [v.upper() for _, _, v, _ in all_row_verdicts if v.upper() in VERDICTS]
        if verdicts_upper:
            expected_overall = "FAIL" if "FAIL" in verdicts_upper else (
                "PARTIAL" if "PARTIAL" in verdicts_upper else "PASS")
            if overall != expected_overall:
                fails.append(
                    f"'전체 판정'이 {overall}이지만 하위 판정 기준으로는 {expected_overall}이어야 함")

    # 7) 브라우저 검증 섹션 내용
    m_browser = re.search(r"^#{2,6}\s+.*브라우저 검증.*$", md, re.M)
    if m_browser:
        nxt = re.search(r"^#{2,6}\s", md[m_browser.end():], re.M)
        body = md[m_browser.end():m_browser.end() + (nxt.start() if nxt else len(md) - m_browser.end())]
        stripped = re.sub(r"\s|//.*", "", body)
        if len(stripped) < 10:
            fails.append("'브라우저 검증' 섹션이 비어 있음 — 수행 내용 또는 생략 사유를 적을 것")
        elif re.search(r"생략", body) and not re.search(r"생략(?:이|은)?\s*아니", body) and "사유" not in body:
            warns.append("브라우저 검증을 생략했다면 사유를 명시할 것")

    # 8) 미완성 플레이스홀더
    ph = re.findall(r"[〈〉]", md)
    if ph:
        n = len(re.findall(r"〈[^〉]*〉", md))
        fails.append(f"미완성 플레이스홀더 〈…〉 {n}곳 — 채우거나 명시적으로 뺄 것")

    # 리포트
    print(f"=== EVAL canonical 검증: {eval_path} ===")
    print(f"섹션 {len(hs)}개 · AC 판정 행 {len(all_row_verdicts)}개 · 전체 판정 {overall or '(없음)'}")
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
    print("\n✓ PASS — EVAL.md가 canonical 필수 구조를 모두 충족합니다."
          + (" (경고는 검토 후 판단)" if warns else ""))


if __name__ == "__main__":
    main()
