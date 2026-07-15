#!/usr/bin/env python3
"""마크다운 문서(.md) → 공유용 스타일 HTML (단일 출처: .md 하나가 정본).

PRD.md / spec.md 등 팀 기획 문서를 그대로 렌더한다. 표준 라이브러리만 사용.
지원: 헤딩(#~####), 문단, 인용(>), 목록(-,*,1., 체크박스 - [ ]),
      표(| |), 코드펜스(```), 수평선(---), 인라인(**bold** *em* `code` [txt](url)).
User Story 섹션의 "> 역할은 …" 인용과 AC 표가 자연스럽게 카드처럼 렌더된다.
라이트/다크 자동. 레퍼런스(NMWC 커머스 User Story)와 같은 디자인 토큰.

사용:
    python3 render_doc.py <input.md> [output.html] [--title "제목"]
"""
import html
import re
import sys
from pathlib import Path

CSS = """
  :root{--bg:#fff;--fg:#1f2328;--muted:#656d76;--faint:#8b949e;--line:#e6e8eb;
    --card:#f8f9fa;--accent:#2563eb;--accent-soft:#eff4ff;--quote-bg:#f0f6ff;
    --quote-bar:#2563eb;--code-bg:#f3f4f6;}
  @media (prefers-color-scheme:dark){:root{--bg:#0f1216;--fg:#e6e9ec;--muted:#9aa4ae;
    --faint:#6e7a86;--line:#262c33;--card:#171c22;--accent:#6ea8fe;--accent-soft:#16233c;
    --quote-bg:#14202f;--quote-bar:#6ea8fe;--code-bg:#171c22;}}
  *{box-sizing:border-box;}
  body{margin:0;background:var(--bg);color:var(--fg);
    font-family:Pretendard,"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",system-ui,sans-serif;
    font-size:16px;line-height:1.75;word-break:keep-all;overflow-wrap:break-word;}
  .wrap{max-width:860px;margin:0 auto;padding:56px 28px 96px;}
  h1{font-size:32px;line-height:1.3;letter-spacing:-.02em;margin:0 0 24px;padding-bottom:14px;border-bottom:2px solid var(--line);}
  h2{font-size:23px;letter-spacing:-.01em;margin:44px 0 16px;padding-bottom:10px;border-bottom:1px solid var(--line);}
  h3{font-size:18.5px;margin:30px 0 12px;}
  h4{font-size:16px;margin:22px 0 8px;color:var(--fg);}
  h4 .usid,.usid{display:inline-block;font-size:12.5px;font-weight:700;color:var(--accent);
    background:var(--accent-soft);border-radius:6px;padding:2px 8px;margin-right:8px;font-variant-numeric:tabular-nums;}
  p{margin:10px 0;}
  a{color:var(--accent);text-decoration:none;}a:hover{text-decoration:underline;}
  blockquote{margin:14px 0;padding:12px 18px;background:var(--quote-bg);
    border-left:4px solid var(--quote-bar);border-radius:0 10px 10px 0;font-weight:600;}
  blockquote p{margin:4px 0;}
  ul,ol{margin:10px 0;padding-left:26px;}li{margin:5px 0;}
  ul.task{list-style:none;padding-left:4px;}
  ul.task li{position:relative;padding-left:28px;}
  ul.task li::before{content:"";position:absolute;left:2px;top:.5em;width:15px;height:15px;
    border:1.5px solid var(--faint);border-radius:4px;}
  ul.task li.done::before{background:var(--accent);border-color:var(--accent);}
  code{background:var(--code-bg);border-radius:4px;padding:1px 6px;font-size:.88em;
    font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;}
  pre{background:var(--card);border:1px solid var(--line);border-radius:12px;
    padding:16px 18px;overflow-x:auto;margin:14px 0;}
  pre code{background:none;padding:0;font-size:13px;line-height:1.6;white-space:pre;}
  table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14.5px;display:block;overflow-x:auto;}
  th,td{border:1px solid var(--line);padding:8px 12px;text-align:left;vertical-align:top;}
  th{background:var(--card);font-weight:700;}
  hr{border:0;border-top:1px solid var(--line);margin:32px 0;}
  .doc-meta{color:var(--muted);font-size:14px;margin:-12px 0 24px;}
"""

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
EM = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
USID = re.compile(r"^(US-\d+\.\d+)\s+(.*)$")


def esc(s):
    return html.escape(s, quote=False)


def inline(text):
    # 코드 조각을 먼저 뽑아 자리표시자로 보호(내부는 이스케이프만)
    spans = []

    def stash(m):
        spans.append("<code>" + esc(m.group(1)) + "</code>")
        return f"\x00{len(spans)-1}\x00"

    text = INLINE_CODE.sub(stash, text)
    text = esc(text)
    text = LINK.sub(lambda m: f'<a href="{html.escape(m.group(2),quote=True)}">{m.group(1)}</a>', text)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = EM.sub(r"<em>\1</em>", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)
    return text


def render(md):
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # 코드펜스
        m = re.match(r"^```(\w*)\s*$", line)
        if m:
            buf = []
            i += 1
            while i < n and not re.match(r"^```\s*$", lines[i]):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + esc("\n".join(buf)) + "</code></pre>")
            continue
        # 수평선
        if re.match(r"^---+\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        # 헤딩
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            content = m.group(2).strip()
            um = USID.match(content)
            if lvl >= 4 and um:
                content = f'<span class="usid">{um.group(1)}</span>{inline(um.group(2))}'
            else:
                content = inline(content)
            tag = f"h{min(lvl,4)}"
            out.append(f"<{tag}>{content}</{tag}>")
            i += 1
            continue
        # 표
        if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s\-:|]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in header)
            trs = []
            for r in rows:
                tds = "".join(f"<td>{inline(c)}</td>" for c in r)
                trs.append(f"<tr>{tds}</tr>")
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table>")
            continue
        # 인용
        if line.strip().startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = "".join(f"<p>{inline(b)}</p>" for b in buf if b.strip())
            out.append(f"<blockquote>{inner}</blockquote>")
            continue
        # 목록(순서/비순서/체크박스)
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            items = []
            is_task = False
            while i < n and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                item = re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i])
                cls = ""
                cm = re.match(r"^\[( |x|X)\]\s+(.*)$", item)
                if cm:
                    is_task = True
                    cls = ' class="done"' if cm.group(1).lower() == "x" else ""
                    item = cm.group(2)
                items.append(f"<li{cls}>{inline(item)}</li>")
                i += 1
            tag = "ol" if ordered else "ul"
            klass = ' class="task"' if is_task else ""
            out.append(f"<{tag}{klass}>{''.join(items)}</{tag}>")
            continue
        # 빈 줄
        if not line.strip():
            i += 1
            continue
        # 문단
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|>|\s*([-*]|\d+\.)\s|```|---+\s*$|\|)", lines[i]
        ):
            buf.append(lines[i])
            i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    inp = Path(sys.argv[1])
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    out = Path(args[0]) if args else inp.with_suffix(".html")
    title = None
    if "--title" in sys.argv:
        title = sys.argv[sys.argv.index("--title") + 1]
    md = inp.read_text(encoding="utf-8")
    if not title:
        m = re.search(r"^#\s+(.*)$", md, re.M)
        title = m.group(1).strip() if m else inp.stem
    body = render(md)
    doc = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style></head>
<body><div class="wrap">
{body}
</div></body></html>
"""
    out.write_text(doc, encoding="utf-8")
    print(f"✓ {out}")


if __name__ == "__main__":
    main()
