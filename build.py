#!/usr/bin/env python3
"""Build the Local Transcription Handbook static site.

Converts docs/*.md into site/*.html with shared navigation, prev/next links,
and a single inline stylesheet. No dependencies beyond Python's stdlib plus
the `markdown` package.

Usage:
    python3 build.py            # builds into ./site
    python3 build.py --out DIR  # builds into DIR
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"

# Reading order: index first, chapters in numeric order, extras last.
PAGE_ORDER = [
    "index.md",
    "01-record-smart.md",
    "02-local-stt-options.md",
    "03-file-formats-size-math.md",
    "04-cleanup-rules.md",
    "05-speaker-labeling.md",
    "06-transcript-to-summary.md",
    "07-what-stays-offline.md",
    "workflow-sheet.md",
    "glossary.md",
]

# Filesystem name -> display name for the sidebar.
NAV_LABELS = {
    "index.md": "Home",
    "01-record-smart.md": "1. Record Smart",
    "02-local-stt-options.md": "2. Local STT, Compared",
    "03-file-formats-size-math.md": "3. Formats and Size Math",
    "04-cleanup-rules.md": "4. Cleanup Rules",
    "05-speaker-labeling.md": "5. Speaker Labeling",
    "06-transcript-to-summary.md": "6. Transcript to Summary",
    "07-what-stays-offline.md": "7. What Stays Offline",
    "workflow-sheet.md": "Workflow Sheet",
    "glossary.md": "Glossary",
}

CSS = """
:root {
  --ink: #26323f;
  --soft: #5b6b7a;
  --accent: #0f766e;
  --accent-soft: #ccf1ec;
  --paper: #fbfaf7;
  --card: #ffffff;
  --line: #e4e1d8;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: Georgia, 'Times New Roman', serif;
  color: var(--ink);
  background: var(--paper);
  line-height: 1.65;
}
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }
code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 0.88em;
  background: var(--accent-soft);
  padding: 0.08em 0.35em;
  border-radius: 4px;
}
pre {
  background: #f2f0ea;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 0.9em 1.1em;
  overflow-x: auto;
  line-height: 1.45;
}
pre code { background: none; padding: 0; }
blockquote {
  border-left: 3px solid var(--accent);
  margin: 1.2em 0;
  padding: 0.2em 1.1em;
  color: var(--soft);
  background: var(--card);
  border-radius: 0 8px 8px 0;
}
table { border-collapse: collapse; width: 100%; margin: 1.2em 0; font-size: 0.95em; }
th, td { border: 1px solid var(--line); padding: 0.45em 0.7em; text-align: left; }
th { background: var(--accent-soft); }
tr:nth-child(even) td { background: #f6f4ee; }

.layout { display: flex; max-width: 1100px; margin: 0 auto; }
aside#nav {
  flex: 0 0 240px;
  padding: 1.5em 1em;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  border-right: 1px solid var(--line);
}
aside#nav .brand {
  font-weight: bold;
  font-size: 1.05em;
  color: var(--ink);
  text-decoration: none;
  display: block;
  margin-bottom: 1.2em;
}
aside#nav .brand span { color: var(--accent); }
aside#nav ul { list-style: none; margin: 0; padding: 0; }
aside#nav li { margin: 0.15em 0; }
aside#nav li.sep { margin-top: 1em; border-top: 1px solid var(--line); padding-top: 0.8em; }
aside#nav a { text-decoration: none; color: var(--soft); display: block; padding: 0.2em 0.5em; border-radius: 6px; font-size: 0.95em; }
aside#nav a:hover { background: var(--accent-soft); color: var(--ink); }
aside#nav li.active a { background: var(--accent); color: #fff; }
main { flex: 1; min-width: 0; padding: 2.2em 3em 3em; }
h1, h2, h3 { line-height: 1.25; }
h1 { font-size: 1.9em; margin-top: 0; }
h2 { margin-top: 1.8em; border-bottom: 1px solid var(--line); padding-bottom: 0.2em; }
.kicker { color: var(--soft); font-style: italic; margin: -0.4em 0 1.6em; }
.doc-footer { margin-top: 3em; padding-top: 1em; border-top: 1px solid var(--line); color: var(--soft); font-size: 0.9em; }
.pager { display: flex; justify-content: space-between; gap: 1em; margin-top: 2.5em; }
.pager a {
  text-decoration: none;
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 0.6em 1em;
}
.pager a:hover { border-color: var(--accent); background: var(--accent-soft); color: var(--ink); }
.pager .spacer { flex: 1; }
input#searchbox {
  width: 100%;
  padding: 0.45em 0.7em;
  border: 1px solid var(--line);
  border-radius: 6px;
  font-family: inherit;
  margin-bottom: 1em;
  background: var(--card);
}
@media (max-width: 800px) {
  .layout { flex-direction: column; }
  aside#nav { position: static; height: auto; flex: none; border-right: none; border-bottom: 1px solid var(--line); }
  main { padding: 1.5em 1.2em 2.5em; }
}
@media print {
  aside#nav, .pager { display: none; }
  main { padding: 0; }
  body { background: #fff; }
}
"""

SEARCH_JS = """
document.addEventListener('DOMContentLoaded', function () {
  var box = document.getElementById('searchbox');
  if (!box) return;
  box.addEventListener('input', function () {
    var q = box.value.toLowerCase();
    document.querySelectorAll('aside#nav li[data-name]').forEach(function (li) {
      var a = li.querySelector('a');
      var hit = !q || (a && a.textContent.toLowerCase().indexOf(q) !== -1);
      li.style.display = hit ? '' : 'none';
    });
  });
});
"""


def slug_of(md_name: str) -> str:
    return md_name.removesuffix(".md") + ".html"


def parse_pages() -> list[dict]:
    """Read every doc page in order and render it to an HTML body."""
    pages = []
    for name in PAGE_ORDER:
        path = DOCS / name
        if not path.exists():
            raise SystemExit(f"ERROR: docs page missing: {path}")
        text = path.read_text(encoding="utf-8")
        md = markdown.Markdown(
            extensions=["tables", "fenced_code", "sane_lists", "toc"],
            output_format="html5",
        )
        body = md.convert(text)
        title_match = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        title = (
            html.unescape(re.sub(r"<[^>]+>", "", title_match.group(1)))
            if title_match
            else name.removesuffix(".md").replace("-", " ").title()
        )
        pages.append({"name": name, "slug": slug_of(name), "title": title, "body": body})
    return pages


def check_internal_links(pages: list[dict]) -> list[str]:
    """Return list of problems with internal doc links (hrefs ending in .html)."""
    slugs = {p["slug"] for p in pages}
    anchors: dict[str, set[str]] = {}
    for p in pages:
        ids = re.findall(r'<h[123][^>]*\bid="([^"]+)"', p["body"])
        anchors[p["slug"]] = set(ids)
    problems = []
    for p in pages:
        for target, frag in re.findall(r'href="([^"#]+\.html)(?:#([^"]*))?"', p["body"]):
            if target not in slugs:
                problems.append(f'{p["name"]}: link to missing page {target}')
                continue
            if frag and frag not in anchors[target]:
                problems.append(f'{p["name"]}: link to #{frag} in {target} (no such heading)')
    return problems


def render_page(page: dict, pages: list[dict], footer_year: int) -> str:
    idx = pages.index(page)
    prev_p = pages[idx - 1] if idx > 0 else None
    next_p = pages[idx + 1] if idx + 1 < len(pages) else None

    nav_items = []
    for p in pages:
        sep = ' class="sep"' if p["name"] in ("workflow-sheet.md", "glossary.md") else ""
        if p == page:
            nav_items.append(
                f'<li{sep}><a href="{p["slug"]}" class="active">{NAV_LABELS[p["name"]]}</a></li>'
            )
        else:
            nav_items.append(f'<li{sep}><a href="{p["slug"]}">{NAV_LABELS[p["name"]]}</a></li>')
    nav_html = "\n".join(nav_items)

    pager_prev = (
        f'<a href="{prev_p["slug"]}">← {NAV_LABELS[prev_p["name"]]}</a>' if prev_p else "<span></span>"
    )
    pager_next = (
        f'<a href="{next_p["slug"]}">{NAV_LABELS[next_p["name"]]} →</a>' if next_p else "<span></span>"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page['title'])} · Local Transcription Handbook</title>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<aside id="nav">
  <a class="brand" href="index.html">Local <span>Transcription</span> Handbook</a>
  <input id="searchbox" type="search" placeholder="filter chapters…">
  <ul>
{nav_html}
  </ul>
</aside>
<main>
{page['body']}
<div class="pager">
{pager_prev}
<span class="spacer"></span>
{pager_next}
</div>
<div class="doc-footer">
  <p><em>Local Transcription Handbook</em> — turn recordings into clean text on your own machine.<br>
  By Asdale Dynamics, LLC · free, local-first, no accounts required. © {footer_year}</p>
</div>
</main>
</div>
<script>{SEARCH_JS}</script>
</body>
</html>
"""


def build(out_dir: str | Path = "site") -> list[Path]:
    out = Path(out_dir)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    pages = parse_pages()

    problems = check_internal_links(pages)
    if problems:
        for p in problems:
            print(f"ERROR: {p}", file=sys.stderr)
        raise SystemExit("internal link check failed")

    from datetime import datetime

    year = datetime.now().year
    written = []
    for page in pages:
        target = out / page["slug"]
        target.write_text(render_page(page, pages, year), encoding="utf-8")
        written.append(target)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the handbook static site")
    parser.add_argument("--out", default="site", help="output directory (default: site)")
    args = parser.parse_args()

    written = build(args.out)
    print(f"Built {len(written)} pages into {args.out}:")
    for w in written:
        print(f"  {w.name}  ({w.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
