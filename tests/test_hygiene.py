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
# Russian-language docs and the RU dictionary are where Cyrillic belongs
# (kalba_ru.py added v1.3, 2026-08-22 - RU UI language)
ALLOWED_NAMES = {"README-ru.txt", "README-ru.md", "kalba_ru.py"}
# Live-test checklists for the author quote the exact on-screen strings in
# all four UI languages - that is the point of them (added 2026-08-25 when
# the guard caught ROBERTO_TESTAS_v1.4.md). Internal documents, not code.
ALLOWED_PREFIXES = ("ROBERTO_TESTAS",)
# The language dropdown is quoted verbatim in LT/DE readmes ("Russkij"
# in Cyrillic); that exact token is deliberate, not a stray lookalike.
# Escapes keep this file itself pure ASCII (see the header rule).
ALLOWED_TOKEN = "\u0420\u0443\u0441\u0441\u043a\u0438\u0439"


def test_no_stray_cyrillic():
    failures = []
    for p in ROOT.rglob("*"):
        if (not p.is_file() or p.suffix.lower() not in CHECK_SUFFIXES
                or p.name in ALLOWED_NAMES
                or p.name.startswith(ALLOWED_PREFIXES)
                or ".venv" in p.parts or ".git" in p.parts
                # _darbal - darbine medziaga (pvz., dukrytes RU vertimu
                # archyvas), ne programos kodas
                or "_darbal" in p.parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if CYRILLIC.search(line.replace(ALLOWED_TOKEN, "")):
                failures.append(f"{p.relative_to(ROOT)}:{i}: {line.strip()[:60]}")
    assert not failures, "Stray Cyrillic found:\n" + "\n".join(failures[:10])
