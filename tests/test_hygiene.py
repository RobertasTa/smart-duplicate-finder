# Source hygiene: no stray Cyrillic lookalikes in code or English docs.
# Born 2026-08-13 after the author (an AI that also writes Russian daily)
# typed a Cyrillic capital I (U+0418) into a Latin word and a human caught
# it. Lookalikes render fine but silently break search and string matching.
# (This file itself is pure ASCII - the guard must not trip on its own net.)
import re
from pathlib import Path

CYRILLIC = re.compile("[\\u0400-\\u04ff]")
ROOT = Path(__file__).resolve().parents[1]
CHECK_SUFFIXES = {".py", ".md", ".yml", ".yaml", ".json", ".txt", ".spec"}
# Russian-language docs are the one place Cyrillic belongs
ALLOWED_NAMES = {"README-ru.txt", "README-ru.md"}


def test_no_stray_cyrillic():
    failures = []
    for p in ROOT.rglob("*"):
        if (not p.is_file() or p.suffix.lower() not in CHECK_SUFFIXES
                or p.name in ALLOWED_NAMES
                or ".venv" in p.parts or ".git" in p.parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if CYRILLIC.search(line):
                failures.append(f"{p.relative_to(ROOT)}:{i}: {line.strip()[:60]}")
    assert not failures, "Stray Cyrillic found:\n" + "\n".join(failures[:10])
