#!/usr/bin/env python3
"""
Build a book-like single-page website from the Gospel of Jesus markdown sources.

Usage:
    python scripts/build_web.py

Output:
    web/index.html
    web/assets/style.css

Markdown remains the source of truth. Re-run after any content change.
Requires: markdown-it-py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = ROOT / "book"
REFERENCES_DIR = ROOT / "references"
WEB_DIR = ROOT / "web"
ASSETS_DIR = WEB_DIR / "assets"
INDEX_PATH = WEB_DIR / "index.html"
CSS_PATH = ASSETS_DIR / "style.css"

BOOK_FILES = [
    "00-preface.md",
    "01-core-proclamation.md",
    "02-authority.md",
    "03-ethical-teaching.md",
    "04-parables.md",
    "05-encounters.md",
    "06-discipleship.md",
    "07-conflict.md",
    "08-final-days.md",
]

REFERENCE_FILES = [
    "passage-map.md",
    "chronology.md",
    "exclusions.md",
    "red-letter-inventory.md",
    "gap-analysis.md",
]

REPO_URL = "https://github.com/zfifteen/gospel-of-jesus"
LICENSE_URL = "https://github.com/zfifteen/gospel-of-jesus/blob/main/LICENSE"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text[:80] or "section"


def make_unique_id(base: str, used: set[str]) -> str:
    candidate = base
    n = 1
    while candidate in used:
        n += 1
        candidate = f"{base}-{n}"
    used.add(candidate)
    return candidate


def extract_headings(md_text: str) -> list[tuple[int, str]]:
    headings = []
    for line in md_text.splitlines():
        m = re.match(r"^(#{1,2})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            headings.append((level, title))
    return headings


def convert_markdown(md_text: str) -> str:
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    return md.render(md_text)


def inject_heading_ids(html: str, headings: list[tuple[int, str]], used_ids: set[str]) -> str:
    idx = 0

    def replacer(match: re.Match) -> str:
        nonlocal idx
        tag = match.group(1)
        attrs = match.group(2) or ""
        content = match.group(3)
        if idx < len(headings):
            level, title = headings[idx]
            base = slugify(title)
            hid = make_unique_id(base, used_ids)
            idx += 1
            return f'<{tag} id="{hid}"{attrs}>{content}</{tag}>'
        return match.group(0)

    pattern = re.compile(r"<(h[12])([^>]*)>(.*?)</\1>", re.DOTALL | re.IGNORECASE)
    return pattern.sub(replacer, html)


def load_ordered_files(directory: Path, filenames: list[str]) -> list[tuple[str, str, list[tuple[int, str]]]]:
    result = []
    for name in filenames:
        path = directory / name
        if not path.exists():
            print(f"WARNING: missing {path}", file=sys.stderr)
            continue
        raw = path.read_text(encoding="utf-8")
        headings = extract_headings(raw)
        result.append((name, raw, headings))
    return result


def generate_css() -> str:
    return """/* Gospel of Jesus — single-page book stylesheet */
:root {
  --text: #1a1a1a;
  --muted: #555;
  --bg: #faf8f5;
  --paper: #ffffff;
  --accent: #2c3e50;
  --border: #ddd8d0;
  --nav-bg: #2c3e50;
  --nav-text: #f5f5f5;
  --link: #1a5276;
  --max-measure: 42rem;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; font-size: 18px; }

body {
  margin: 0; padding: 0;
  font-family: Georgia, "Times New Roman", Times, serif;
  line-height: 1.65; color: var(--text); background: var(--bg);
}

/* ---- Sticky nav: compact by default, expandable ---- */
.site-nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--nav-bg); color: var(--nav-text);
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 0.85rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.site-nav .nav-bar {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.55rem 1rem;
  max-width: 70rem; margin: 0 auto;
}

.site-nav .nav-label {
  font-weight: 600; opacity: 0.9; white-space: nowrap;
}

.site-nav .nav-toggle {
  margin-left: auto;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.25);
  color: var(--nav-text);
  font: inherit; font-size: 0.8rem;
  padding: 0.3rem 0.7rem;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
}

.site-nav .nav-toggle:hover,
.site-nav .nav-toggle:focus {
  background: rgba(255,255,255,0.22);
  outline: none;
}

.site-nav .nav-links {
  display: none;
  max-height: min(55vh, 28rem);
  overflow-y: auto;
  padding: 0.4rem 1rem 0.75rem;
  border-top: 1px solid rgba(255,255,255,0.12);
  -webkit-overflow-scrolling: touch;
}

.site-nav.is-open .nav-links {
  display: block;
}

.site-nav .nav-links-inner {
  max-width: 70rem; margin: 0 auto;
  display: flex; flex-wrap: wrap; gap: 0.3rem 0.65rem; align-items: center;
}

.site-nav a {
  color: var(--nav-text); text-decoration: none;
  padding: 0.2rem 0.4rem; border-radius: 3px; white-space: nowrap;
}

.site-nav a:hover, .site-nav a:focus {
  background: rgba(255,255,255,0.15); outline: none;
}

.site-nav a.level-1 { font-weight: 600; }

/* On wide screens keep links visible by default, still height-capped */
@media (min-width: 900px) {
  .site-nav .nav-links {
    display: block;
    max-height: 9rem;
  }
  .site-nav .nav-toggle { display: none; }
}

main {
  max-width: var(--max-measure); margin: 0 auto;
  padding: 2rem 1.25rem 4rem; background: var(--paper);
  min-height: 80vh; box-shadow: 0 0 20px rgba(0,0,0,0.04);
}

.frame {
  border-bottom: 1px solid var(--border);
  padding-bottom: 1.5rem; margin-bottom: 2.5rem;
}

.frame h1 {
  font-size: 2rem; margin: 0 0 0.4rem; font-weight: 700; letter-spacing: -0.01em;
}

.frame .purpose { color: var(--muted); font-size: 1.05rem; margin: 0.5rem 0 1rem; }

.frame .meta {
  font-family: system-ui, sans-serif; font-size: 0.85rem; color: var(--muted);
}

.frame .meta a { color: var(--link); }

h1, h2, h3 {
  font-family: Georgia, "Times New Roman", Times, serif;
  line-height: 1.25; color: var(--accent);
  margin-top: 2.2rem; margin-bottom: 0.75rem;
}

h1 { font-size: 1.75rem; border-bottom: 2px solid var(--border); padding-bottom: 0.35rem; }
h2 { font-size: 1.35rem; }
h3 { font-size: 1.15rem; }

p { margin: 0 0 1rem; }

blockquote {
  margin: 1.2rem 0; padding: 0.6rem 1.2rem;
  border-left: 3px solid var(--accent); background: #f7f5f0; font-style: italic;
}

ul, ol { margin: 0 0 1rem; padding-left: 1.5rem; }
li { margin-bottom: 0.35rem; }

table {
  width: 100%; border-collapse: collapse; margin: 1.2rem 0;
  font-size: 0.9rem; font-family: system-ui, -apple-system, sans-serif; line-height: 1.4;
}

th, td {
  border: 1px solid var(--border); padding: 0.45rem 0.6rem;
  text-align: left; vertical-align: top;
}

th { background: #f0ebe3; font-weight: 600; }
tr:nth-child(even) td { background: #faf8f5; }

.section { margin-bottom: 3rem; }

.section-group-title {
  font-family: system-ui, sans-serif; font-size: 0.75rem;
  text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted);
  margin: 3rem 0 1rem; border-top: 1px solid var(--border); padding-top: 1.5rem;
}

footer {
  max-width: var(--max-measure); margin: 0 auto;
  padding: 1.5rem 1.25rem 3rem;
  font-family: system-ui, sans-serif; font-size: 0.8rem; color: var(--muted);
  border-top: 1px solid var(--border);
}

footer a { color: var(--link); }

@media (max-width: 600px) {
  html { font-size: 16px; }
  main { padding: 1.25rem 1rem 3rem; }
  .frame h1 { font-size: 1.6rem; }
}
"""


def generate_html(nav_items: list[dict], book_html_parts: list[str], ref_html_parts: list[str]) -> str:
    nav_links = []
    for item in nav_items:
        cls = f'class="level-{item["level"]}"'
        nav_links.append(f'<a href="#{item["id"]}" {cls}>{item["title"]}</a>')
    nav_html = "\n          ".join(nav_links)
    book_body = "\n".join(book_html_parts)
    ref_body = "\n".join(ref_html_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gospel of Jesus — Full Companion</title>
  <meta name="description" content="A single-page, book-like presentation of the lifetime teachings and actions of Jesus of Nazareth together with the full companion references.">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>

  <nav class="site-nav" id="site-nav" aria-label="Jump navigation">
    <div class="nav-bar">
      <span class="nav-label">Jump to section</span>
      <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="nav-links">
        Show navigation
      </button>
    </div>
    <div class="nav-links" id="nav-links">
      <div class="nav-links-inner">
        {nav_html}
      </div>
    </div>
  </nav>

  <main>
    <header class="frame">
      <h1>Gospel of Jesus</h1>
      <p class="purpose">A self-contained record of the teachings and actions of Jesus of Nazareth restricted exclusively to the period of his lifetime.</p>
      <p class="meta">
        <a href="{REPO_URL}">Repository</a>
        ·
        License: <a href="{LICENSE_URL}">CC0 1.0 Universal</a>
      </p>
    </header>

    <div class="section-group-title">The Book</div>
    {book_body}

    <div class="section-group-title">Companion References</div>
    {ref_body}
  </main>

  <footer>
    Generated from the markdown sources in the
    <a href="{REPO_URL}">gospel-of-jesus</a> repository.
    Content remains under <a href="{LICENSE_URL}">CC0 1.0</a>.
    Re-run <code>python scripts/build_web.py</code> after any source change.
  </footer>

  <script>
  (function () {{
    var nav = document.getElementById('site-nav');
    var btn = document.getElementById('nav-toggle');
    var links = document.getElementById('nav-links');
    if (!nav || !btn) return;

    function setOpen(open) {{
      nav.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Hide navigation' : 'Show navigation';
    }}

    btn.addEventListener('click', function () {{
      setOpen(!nav.classList.contains('is-open'));
    }});

    // Close after choosing a link (mobile-friendly)
    links.addEventListener('click', function (e) {{
      if (e.target.tagName === 'A' && window.matchMedia('(max-width: 899px)').matches) {{
        setOpen(false);
      }}
    }});
  }})();
  </script>

</body>
</html>
"""


def main() -> int:
    print("Building web/ single-page companion...")
    book_data = load_ordered_files(BOOK_DIR, BOOK_FILES)
    ref_data = load_ordered_files(REFERENCES_DIR, REFERENCE_FILES)

    if not book_data:
        print("ERROR: no book files found", file=sys.stderr)
        return 1

    used_ids: set[str] = set()
    book_html_parts: list[str] = []
    for filename, raw, headings in book_data:
        html = convert_markdown(raw)
        html = inject_heading_ids(html, headings, used_ids)
        book_html_parts.append(f'<section class="section" data-source="{filename}">\n{html}\n</section>')

    ref_html_parts: list[str] = []
    for filename, raw, headings in ref_data:
        html = convert_markdown(raw)
        html = inject_heading_ids(html, headings, used_ids)
        ref_html_parts.append(f'<section class="section" data-source="{filename}">\n{html}\n</section>')

    used_ids_nav: set[str] = set()
    nav_items: list[dict] = []
    for filename, raw, headings in book_data:
        for level, title in headings:
            if level > 2:
                continue
            base = slugify(title)
            hid = make_unique_id(base, used_ids_nav)
            nav_items.append({"id": hid, "title": title, "level": level, "group": "book"})

    for filename, raw, headings in ref_data:
        for level, title in headings:
            if level > 2:
                continue
            base = slugify(title)
            hid = make_unique_id(base, used_ids_nav)
            nav_items.append({"id": hid, "title": title, "level": level, "group": "refs"})

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    CSS_PATH.write_text(generate_css(), encoding="utf-8")
    INDEX_PATH.write_text(generate_html(nav_items, book_html_parts, ref_html_parts), encoding="utf-8")

    print(f"Wrote {INDEX_PATH.relative_to(ROOT)}")
    print(f"Wrote {CSS_PATH.relative_to(ROOT)}")
    print(f"Nav entries: {len(nav_items)}")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
