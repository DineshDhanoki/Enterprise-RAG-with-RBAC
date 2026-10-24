"""Dependency-free checks for the static NexusVault prototype."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
required = [
    "index.html",
    "styles.css",
    "result.css",
    "animations.css",
    "app.js",
    "favicon.svg",
    "README.md",
    "LICENSE",
]

for filename in required:
    path = ROOT / filename
    assert path.is_file(), f"missing required file: {filename}"
    assert path.stat().st_size > 0, f"empty required file: {filename}"

html = (ROOT / "index.html").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")

assert '<html lang="en">' in html
assert '<meta name="viewport"' in html
assert 'id="query-input"' in html
assert 'id="ask-button"' in html
assert 'aria-label="Primary navigation"' in html
assert re.search(r"<title>[^<]+</title>", html)
assert "CONTRIBUTING.md" in readme
assert "SECURITY.md" in readme
assert "good first issue" in readme
assert "github.io/Enterprise-RAG-with-RBAC" in readme

print(f"smoke checks passed ({len(required)} required files, {len(html)} HTML characters)")
