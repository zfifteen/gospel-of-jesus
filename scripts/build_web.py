#!/usr/bin/env python3
"""
Build a book-like single-page website from the Gospel of Jesus markdown sources.

Usage:
    python scripts/build_web.py

Output:
    web/index.html
    web/assets/style.css

Markdown remains the source of truth. Re-run after any content change.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = ROOT / "book"
REFERENCES_DIR = ROOT / "references"
WEB_DIR = ROOT / "web"
ASSETS_DIR = WEB_DIR / "assets"
INDEX_PATH = WEB_DIR / "index.html"
CSS_PATH = ASSETS_DIR / "style.css"

# Ordered book files (preface then chapters 01-08). Skip 00-toc.md.
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

# Ordered reference files
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
    """Create a simple URL-friendly slug from heading text."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text[:80] or "section"


def make_unique_id(base: str, used: set[str]) -> str:
    """Ensure heading IDs are unique across the whole page."""
    candidate = base
    n = 1
    while candidate in used:
        n += 1
        candidate = f"{base}-{n}"
    used.add(candidate)
    return candidate


def extract_headings(md_text: str) -> list[tuple[int, str]]:
    """Return list of (level, title) for H1 and H2 only."""
    headings = []
    for line in md_text.splitlines():
        m = re.match(r"^(#{1,2})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            headings.append((level, title))
    return headings


def convert_markdown(md_text: str) -> str:
    """Convert markdown to HTML with table support."""
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    return md.render(md_text)


def inject_heading_ids(html: str, headings: list[tuple[int, str]], used_ids: set[str]) -> str:
    """Replace <h1> and <h2> with version that carries id attributes."""
    idx = 0

    def replacer(match: re.Match) -> str:
        nonlocal idx
        tag = match.group(1)  # h1 or h2
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
    """Load files in order; return (filename, raw_text, headings)."""
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
    """Book-like, readable, mobile-friendly CSS."""
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

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  font-size: 18px;
}

body {
  margin: 0;
  padding: 0;
  font-family: Georgia, "Times New Roman", Times, serif;
  line-height: 1.65;
  color: var(--text);
  background: var(--bg);
}

/* Sticky top navigation */
.site-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--nav-bg);
  color: var(--nav-text);
  padding: 0.5rem 1rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 0.85rem;
}

.site-nav .nav-inner {
  max-width: 70rem;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 0.75rem;
  align-items: center;
}

.site-nav a {
  color: var(--nav-text);
  text-decoration: none;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  white-space: nowrap;
}

.site-nav a:hover,
.site-nav a:focus {
  background: rgba(255,255,255,0.15);
  outline: none;
}

.site-nav .nav-label {
  font-weight: 600;
  margin-right: 0.5rem;
  opacity: 0.85;
}

.site-nav .nav-sep {
  opacity: 0.4;
  user-select: none;
}

/* Compact mode on small screens: show only top-level */
@media (max-width: 720px) {
  .site-nav a.level-2 {
    display: none;
  }
  .site-nav {
    font-size: 0.8rem;
    padding: 0.4rem 0.6rem;
  }
}

/* Main content */
main {
  max-width: var(--max-measure);
  margin: 0 auto;
  padding: 2rem 1.25rem 4rem;
  background: var(--paper);
  min-height: 80vh;
  box-shadow: 0 0 20px rgba(0,0,0,0.04);
}

/* Frame / header */
.frame {
  border-bottom: 1px solid var(--border);
  padding-bottom: 1.5rem;
  margin-bottom: 2.5rem;
}

.frame h1 {
  font-size: 2rem;
  margin: 0 0 0.4rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.frame .purpose {
  color: var(--muted);
  font-size: 1.05rem;
  margin: 0.5rem 0 1rem;
}

.frame .meta {
  font-family: system-ui, sans-serif;
  font-size: 0.85rem;
  color: var(--muted);
}

.frame .meta a {
  color: var(--link);
}

/* Typography */
h1, h2, h3 {
  font-family: Georgia, "Times New Roman", Times, serif;
  line-height: 1.25;
  color: var(--accent);
  margin-top: 2.2rem;
  margin-bottom: 0.75rem;
}

h1 {
  font-size: 1.75rem;
  border-bottom: 2px solid var(--border);
  padding-bottom: 0.35rem;
}

h2 {
  font-size: 1.35rem;
}

h3 {
  font-size: 1.15rem;
}

p {
  margin: 0 0 1rem;
}

blockquote {
  margin: 1.2rem 0;
  padding: 0.6rem 1.2rem;
  border-left: 3px solid var(--accent);
  background: #f7f5f0;
  font-style: italic;
}

ul, ol {
  margin: 0 0 1rem;
  padding-left: 1.5rem;
}

li {
  margin-bottom: 0.35rem;
}

/* Tables (passage map, inventories, etc.) */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.2rem 0;
  font-size: 0.9rem;
  font-family: system-ui, -apple-system, sans-serif;
  line-height: 1.4;
}

th, td {
  border: 1px solid var(--border);
  padding: 0.45rem 0.6rem;
  text-align: left;
  vertical-align: top;
}

th {
  background: #f0ebe3;
  font-weight: 600;
}

tr:nth-child(even) td {
  background: #faf8f5;
}

/* Section wrappers */
.section {
  margin-bottom: 3rem;
}

.section-group-title {
  font-family: system-ui, sans-serif;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin: 3rem 0 1rem;
  border-top: 1px solid var(--border);
  padding-top: 1.5rem;
}

/* Footer */
footer {
  max-width: var(--max-measure);
  margin: 0 auto;
  padding: 1.5rem 1.25rem 3rem;
  font-family: system-ui, sans-serif;
  font-size: 0.8rem;
  color: var(--muted);
  text-align: center;
  border-top: 1px solid var(--border);
}

footer a {
  color: var(--link);
}

/* Print */
@media print {
  .site-nav {
    position: static;
    box-shadow: none;
    background: #fff;
    color: #000;
    border-bottom: 1px solid #ccc;
  }
  .site-nav a {
    color: #000;
  }
  main {
    box-shadow: none;
    max-width: none;
  }
  a[href]::after {
    content: none;
  }
}
"""


def generate_html(
    nav_items: list[dict],
    book_html_parts: list[str],
    ref_html_parts: list[str],
) -> str:
    """Assemble the full single-page HTML document."""

    # Build nav HTML
    nav_links = []
    for item in nav_items:
        cls = f'class="level-{item["level"]}"'
        nav_links.append(f'<a href="#{item["id"]}" {cls}>{item["title"]}</a>')

    nav_html = "\n          ".join(nav_links)

    # Book sections
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

  <nav class="site-nav" aria-label="Jump navigation">
    <div class="nav-inner">
      <span class="nav-label">Jump:</span>
      {nav_html}
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

</body>
</html>
"""


def main() -> int:
    print("Building web/ single-page companion...")

    # Load sources
    book_data = load_ordered_files(BOOK_DIR, BOOK_FILES)
    ref_data = load_ordered_files(REFERENCES_DIR, REFERENCE_FILES)

    if not book_data:
        print("ERROR: no book files found", file=sys.stderr)
        return 1

    # Convert each file, injecting IDs in the same order the nav will use
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

    # Rebuild nav from the same heading lists (IDs already assigned in used_ids order)
    used_ids_nav: set[str] = set()
    nav_items: list[dict] = []

    for filename, raw, headings in book_data:
        for i, (level, title) in enumerate(headings):
            if level > 2:
                continue
            base = slugify(title)
            hid = make_unique_id(base, used_ids_nav)
            nav_items.append({"id": hid, "title": title, "level": level, "group": "book"})

    for filename, raw, headings in ref_data:
        for i, (level, title) in enumerate(headings):
            if level > 2:
                continue
            base = slugify(title)
            hid = make_unique_id(base, used_ids_nav)
            nav_items.append({"id": hid, "title": title, "level": level, "group": "refs"})

    # Write files
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    CSS_PATH.write_text(generate_css(), encoding="utf-8")
    INDEX_PATH.write_text(
        generate_html(nav_items, book_html_parts, ref_html_parts),
        encoding="utf-8",
    )

    print(f"Wrote {INDEX_PATH.relative_to(ROOT)}")
    print(f"Wrote {CSS_PATH.relative_to(ROOT)}")
    print(f"Nav entries: {len(nav_items)}")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
