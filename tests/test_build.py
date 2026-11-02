import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build as build_mod

EXPECTED_PAGES = [
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


# ---------- docs coverage ----------

def test_all_expected_docs_exist():
    for name in EXPECTED_PAGES:
        assert (ROOT / "docs" / name).is_file(), f"missing docs page: {name}"


def test_index_toc_links_every_chapter():
    text = (ROOT / "docs" / "index.md").read_text()
    for name in EXPECTED_PAGES[1:]:
        assert Path(name).stem in text, f"index never mentions {name}"


def test_no_untodo_placeholders():
    for name in EXPECTED_PAGES:
        text = (ROOT / "docs" / name).read_text()
        assert "TODO" not in text and "TBD" not in text, name


def test_no_secrets_in_repo_files():
    pattern = re.compile(r"sk-[A-Za-z0-9]{10,}|api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}", re.I)
    for path in list(ROOT.glob("docs/*.md")) + list(ROOT.glob("scripts/*.py")) + [ROOT / "README.md"]:
        assert not pattern.search(path.read_text(errors="replace")), f"possible secret in {path}"


# ---------- build script ----------

def test_build_produces_all_site_pages(tmp_path):
    out = tmp_path / "site"
    written = build_mod.build(out)
    names = {p.name for p in written}
    assert names == {Path(n).with_suffix(".html").name for n in EXPECTED_PAGES}


def test_build_overwrites_stale_output(tmp_path):
    out = tmp_path / "site"
    out.mkdir()
    stale = out / "stale.html"
    stale.write_text("old", encoding="utf-8")
    build_mod.build(out)
    assert not stale.exists()


@pytest.mark.parametrize(
    "page,label",
    [
        ("01-record-smart.html", "1. Record Smart"),
        ("workflow-sheet.html", "Workflow Sheet"),
        ("glossary.html", "Glossary"),
    ],
)
def test_nav_labels_appear(page, label, tmp_path):
    out = tmp_path / "site"
    build_mod.build(out)
    html = (out / page).read_text()
    assert label in html


def test_prev_next_pager(tmp_path):
    out = tmp_path / "site"
    build_mod.build(out)
    ch1 = (out / "01-record-smart.html").read_text()
    assert "index.html" in ch1 and "02-local-stt-options.html" in ch1
    last = (out / "glossary.html").read_text()
    assert "workflow-sheet.html" in last


def test_internal_links_resolve_in_built_site(tmp_path):
    out = tmp_path / "site"
    build_mod.build(out)
    for page in out.glob("*.html"):
        html_text = page.read_text()
        for href in re.findall(r'href="([^"#]+\.html)(?:#[^"]*)?"', html_text):
            assert href.startswith("http") or (out / href).is_file(), f"{page.name} -> {href}"


def test_broken_internal_link_fails_build(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# X\n\n[dead link](missing-page.html)\n")
    monkeypatch.setattr(build_mod, "DOCS", docs)
    monkeypatch.setattr(build_mod, "PAGE_ORDER", ["index.md"])
    with pytest.raises(SystemExit, match="internal link check failed"):
        build_mod.build(tmp_path / "site")


def test_missing_doc_page_fails_build(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# X")
    monkeypatch.setattr(build_mod, "DOCS", docs)
    with pytest.raises(SystemExit, match="docs page missing"):
        build_mod.build(tmp_path / "site")


def test_cli_build_runs(tmp_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--out", str(tmp_path / "out")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "out" / "index.html").is_file()
    assert "Built 10 pages" in result.stdout


# ---------- repo meta files ----------

def test_license_copyright_line_exact():
    text = (ROOT / "LICENSE").read_text()
    assert "Copyright (c) 2026 Asdale Dynamics, LLC" in text


def test_readme_credits_asdale():
    text = (ROOT / "README.md").read_text()
    assert "Asdale Dynamics, LLC" in text
