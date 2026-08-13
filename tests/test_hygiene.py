# Source hygiene: no stray Cyrillic lookalikes in code or English docs.
# Born 2026-08-13 after the author (an AI that also writes Russian daily)
# typed a Cyrillic 'И' into a Latin word and a human caught it. Lookalike
# letters render fine but silently break search, fonts and string matching.
import re
from pathlib import Path

CYRILLIC = re.compile(r"[Ѐ-ӿ]")
ROOT = Path(__file__).resolve().parents[1]
CHECK_SUFFIXES = {".py", ".md", ".yml", ".yaml", ".json", ".txt", ".spec"}
# Russian-language docs are the one place Cyrillic belongs
ALLOWED_NAMES = {"README-ru.txt", "README-ru.md"}


def test_no_stray_cyrillic():
    lt_failures = []
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
                lt_failures.append(f"{p.relative_to(ROOT)}:{i}: {line.strip()[:60]}")
    assert not lt_failures, "Stray Cyrillic found:\n" + "\n".join(lt_failures[:10])
