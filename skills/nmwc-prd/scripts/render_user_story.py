#!/usr/bin/env python3
"""User Story JSON → styled HTML view.

"NMWC 커머스 — User Story" 레퍼런스와 동일한 디자인 언어로 렌더한다.
- 상단 통계 배지(에픽/유저 스토리/인수 조건 수)는 입력에서 자동 집계.
- 목차(에픽→스토리 링크), 에픽 섹션, 스토리 카드, AC 체크리스트.
- 표준 라이브러리만 사용(의존성 없음). 라이트/다크 자동.

사용:
    python3 render_user_story.py <input.json> [output.html]
    # output 생략 시 input과 같은 이름의 .html
입력 스키마: references/user-story-craft.md "JSON 스키마" 참조.
"""
import html
import json
import re
import sys
from pathlib import Path

CSS = """
  :root {
    --bg: #ffffff; --fg: #1f2328; --muted: #656d76; --faint: #8b949e;
    --line: #e6e8eb; --card: #f8f9fa; --accent: #2563eb; --accent-soft: #eff4ff;
    --quote-bg: #f0f6ff; --quote-bar: #2563eb; --check: #c9ced4;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0f1216; --fg: #e6e9ec; --muted: #9aa4ae; --faint: #6e7a86;
      --line: #262c33; --card: #171c22; --accent: #6ea8fe; --accent-soft: #16233c;
      --quote-bg: #14202f; --quote-bar: #6ea8fe; --check: #3a434d;
    }
  }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0; background: var(--bg); color: var(--fg);
    font-family: Pretendard, "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", system-ui, sans-serif;
    font-size: 16px; line-height: 1.75; word-break: keep-all; overflow-wrap: break-word;
  }
  .wrap { max-width: 860px; margin: 0 auto; padding: 56px 28px 96px; }
  header.doc h1 { font-size: 34px; line-height: 1.3; margin: 0 0 8px; letter-spacing: -0.02em; }
  .doc-sub { color: var(--muted); margin: 0 0 20px; font-size: 15px; }
  .stats { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 36px; }
  .stat { background: var(--accent-soft); color: var(--accent); border-radius: 999px; padding: 4px 14px; font-size: 13px; font-weight: 600; }
  nav.toc { border: 1px solid var(--line); border-radius: 14px; padding: 22px 26px; margin-bottom: 48px; }
  nav.toc > p { margin: 0 0 12px; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--faint); }
  .toc-epic { margin-bottom: 12px; }
  .toc-epic:last-child { margin-bottom: 0; }
  .toc-epic-title { font-weight: 700; color: var(--fg); text-decoration: none; display: inline-flex; align-items: center; gap: 8px; }
  .toc-epic-title:hover { color: var(--accent); }
  .toc-epic ul { list-style: none; margin: 6px 0 0; padding: 0 0 0 30px; display: grid; gap: 3px; }
  .toc-epic a { color: var(--muted); text-decoration: none; font-size: 14.5px; }
  .toc-epic ul a:hover { color: var(--accent); }
  .toc-id { color: var(--faint); font-size: 12.5px; font-weight: 600; font-variant-numeric: tabular-nums; margin-right: 2px; }
  .epic { margin-bottom: 56px; }
  .epic > h2 {
    display: flex; align-items: center; gap: 12px; font-size: 24px; letter-spacing: -0.01em;
    margin: 0 0 22px; padding-bottom: 14px; border-bottom: 2px solid var(--line);
  }
  .epic-num {
    display: inline-grid; place-items: center; width: 30px; height: 30px; flex: none;
    background: var(--accent); color: #fff; border-radius: 9px; font-size: 15px; font-weight: 800;
  }
  nav .epic-num { width: 22px; height: 22px; font-size: 12px; border-radius: 7px; }
  .story { border: 1px solid var(--line); border-radius: 14px; padding: 24px 26px 20px; margin-bottom: 18px; }
  .story h3 { display: flex; align-items: center; gap: 10px; font-size: 18px; margin: 0 0 14px; }
  .story-id {
    flex: none; font-size: 12.5px; font-weight: 700; color: var(--accent);
    background: var(--accent-soft); border-radius: 6px; padding: 2px 8px; font-variant-numeric: tabular-nums;
  }
  .story-sentence {
    margin: 0 0 18px; padding: 12px 18px; background: var(--quote-bg);
    border-left: 4px solid var(--quote-bar); border-radius: 0 10px 10px 0;
    font-size: 16.5px; font-weight: 600;
  }
  .criteria-label { margin: 0 0 8px; font-size: 12.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--faint); }
  ul.criteria { list-style: none; margin: 0; padding: 0; }
  ul.criteria li {
    position: relative; padding: 7px 0 7px 32px; color: var(--fg);
    border-bottom: 1px dashed var(--line); font-size: 15.5px;
  }
  ul.criteria li:last-child { border-bottom: 0; }
  ul.criteria li::before {
    content: ""; position: absolute; left: 4px; top: 13px; width: 15px; height: 15px;
    border: 1.5px solid var(--check); border-radius: 4px;
  }
  .story-details { margin: 14px 0 0; font-size: 14px; color: var(--muted); }
  footer.doc { margin-top: 64px; padding-top: 20px; border-top: 1px solid var(--line); color: var(--faint); font-size: 13px; }
  @media print {
    body { font-size: 12px; }
    .wrap { max-width: none; padding: 0; }
    nav.toc { display: none; }
    .story { break-inside: avoid; }
  }
"""


def esc(s):
    return html.escape(str(s), quote=True)


def story_anchor(story_id):
    """US-1.1 → us-1-1"""
    return re.sub(r"[^a-z0-9]+", "-", str(story_id).lower()).strip("-")


def render(data):
    epics = data.get("epics", [])
    n_epics = len(epics)
    n_stories = sum(len(e.get("stories", [])) for e in epics)
    n_ac = sum(len(s.get("criteria", [])) for e in epics for s in e.get("stories", []))

    title = esc(data.get("title", "User Story"))
    subtitle = data.get("subtitle")
    footer = esc(data.get("footer", "NMWC · User Story"))

    # 목차
    toc = []
    for e in epics:
        eid = esc(e.get("id", ""))
        etitle = esc(e.get("title", ""))
        items = []
        for s in e.get("stories", []):
            sa = story_anchor(s.get("id", ""))
            items.append(
                f'<li><a href="#{sa}"><span class="toc-id">{esc(s.get("id",""))}</span> '
                f'{esc(s.get("title",""))}</a></li>'
            )
        toc.append(
            f'<div class="toc-epic">\n'
            f'  <a class="toc-epic-title" href="#epic-{eid}">'
            f'<span class="epic-num">{eid}</span> {etitle}</a>\n'
            f'  <ul>{"".join(items)}</ul>\n</div>'
        )

    # 본문
    sections = []
    for e in epics:
        eid = esc(e.get("id", ""))
        etitle = esc(e.get("title", ""))
        arts = []
        for s in e.get("stories", []):
            sa = story_anchor(s.get("id", ""))
            crit = "".join(f"      <li>{esc(c)}</li>\n" for c in s.get("criteria", []))
            details = s.get("details")
            details_html = (
                f'    <p class="story-details">{esc(details)}</p>\n' if details else ""
            )
            arts.append(
                f'  <article class="story" id="{sa}">\n'
                f'    <h3><span class="story-id">{esc(s.get("id",""))}</span>'
                f'{esc(s.get("title",""))}</h3>\n'
                f'    <p class="story-sentence">{esc(s.get("sentence",""))}</p>\n'
                f'    <p class="criteria-label">인수 조건</p>\n'
                f'    <ul class="criteria">\n{crit}    </ul>\n'
                f"{details_html}"
                f"  </article>"
            )
        sections.append(
            f'<section class="epic" id="epic-{eid}">\n'
            f'  <h2><span class="epic-num">{eid}</span>{etitle}</h2>\n'
            + "\n".join(arts)
            + "\n</section>"
        )

    sub_html = f'    <p class="doc-sub">{esc(subtitle)}</p>\n' if subtitle else ""

    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="doc">
    <h1>{title}</h1>
{sub_html}    <div class="stats">
      <span class="stat">에픽 {n_epics}</span>
      <span class="stat">유저 스토리 {n_stories}</span>
      <span class="stat">인수 조건 {n_ac}</span>
    </div>
  </header>
  <nav class="toc">
    <p>목차</p>
{chr(10).join(toc)}
  </nav>
{chr(10).join(sections)}
  <footer class="doc">{footer}</footer>
</div>
</body></html>
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else inp.with_suffix(".html")
    data = json.loads(inp.read_text(encoding="utf-8"))
    out.write_text(render(data), encoding="utf-8")
    n_epics = len(data.get("epics", []))
    n_stories = sum(len(e.get("stories", [])) for e in data.get("epics", []))
    n_ac = sum(
        len(s.get("criteria", []))
        for e in data.get("epics", [])
        for s in e.get("stories", [])
    )
    print(f"✓ {out}  (에픽 {n_epics} · 스토리 {n_stories} · AC {n_ac})")


if __name__ == "__main__":
    main()
