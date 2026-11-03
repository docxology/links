"""Publication guard for scraped page captures.

`cached_data/` holds third-party pages, and those pages embed their own credentials: the
captured YouTube watch page carried five distinct Google keys and a captured article page
carried another. A capture is regenerable cache, so it belongs on disk and not in the index.

Scope is deliberate. This is a publication guard over **tracked** files, not a scan of the
working tree: a developer may keep a local cache, and scanning the tree would fail every
checkout that has one. It detects Google-key-shaped values only — not a general secret
scanner, and it makes no statement about whether a credential is live. Diagnostics are
file and line locators, never matched values.

The `.gitignore` rule and this scan are one control with two halves, and neither half is
sufficient alone. The rule keeps a re-capture out of the index while the cache goes on
being written; this scan reads the index, so it also catches a capture that was force-added
despite the rule. What it cannot see is a key-bearing file that is neither tracked nor
ignored — which is the same file the repository does not publish, so the gap is outside the
surface being asserted.
"""

import subprocess
from pathlib import Path

# Built by joining so this guard does not itself contain the shape it forbids.
GOOGLE_KEY_SHAPE = "".join(["AI", "za"]) + r"[A-Za-z0-9_-]{35}"

REPO_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = REPO_ROOT / "cached_data"


def tracked_capture_paths(root: Path = REPO_ROOT) -> list[Path]:
    """Return the `.html` captures that git tracks under `cached_data/`."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "cached_data"],
        capture_output=True,
        check=True,
        text=False,
    )
    names = [name for name in result.stdout.decode().split("\0") if name.endswith(".html")]
    return [root / name for name in names]


def google_key_locations(paths) -> list[str]:
    """Return `file:line` locators for Google-key-shaped values. Never returns the value."""
    import re

    shape = re.compile(GOOGLE_KEY_SHAPE)
    found = []
    for path in paths:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            if shape.search(line):
                found.append(f"{path}:{number}")
    return found


def test_no_tracked_capture_carries_a_google_key_shaped_value():
    assert google_key_locations(tracked_capture_paths()) == []


def test_guard_detects_a_synthetic_key_without_disclosing_it(tmp_path):
    capture = tmp_path / "capture.html"
    synthetic = "".join(["AI", "za"]) + "A" * 35

    capture.write_text(f"<html>\n<script>cfg.key='{synthetic}';</script></html>", encoding="utf-8")
    assert google_key_locations([capture]) == [f"{capture}:2"]

    capture.write_text("<html>\n<script>cfg.key='';</script></html>", encoding="utf-8")
    assert google_key_locations([capture]) == []
