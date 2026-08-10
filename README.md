# Smart Duplicate Finder

**A safe, portable duplicate file finder for Windows — finds your duplicates, never deletes them.**

Built by Claude (Anthropic AI) together with my human friend Robertas. Made with care, given with joy. 🎁

![Main window](docs/screenshots/main-window.png)

## Who is this for — and who is it not for

These days you shouldn't blindly trust anyone with your files — not a
program, not an AI. *(Says the AI that wrote this program.)* That's why
this one **deletes nothing**: it finds, it shows, it writes you a report —
and the decision stays where it belongs, with you. Come back a few days
later with a fresh head and compare calmly; the saved scan will be waiting.

**For you, if** you have years of files that "are perfectly tidy". Everyone
says *"I keep order, I have no duplicates"* — until the first scan. Backups
of backups, photo folders copied "just in case", the same download in three
places... Trusting a program to delete all that automatically is dangerous —
but **knowing what you have is always worth it**. That is exactly the job
this program does: finds everything, shows where it lives, hands you a
report — and deletes nothing.

**Not for you, if** you want maximum speed and mass deletion with
auto-selection rules. [Czkawka](https://github.com/qarmin/czkawka) and
[dupeGuru](https://github.com/arsenetar/dupeguru) are excellent at that —
faster than us and with more scan modes. Just weigh one thing honestly:
automated mass deletion is genuinely fast, *and* it concentrates all the
risk into a single click. We took the opposite trade — slower, with a
human between the report and the Delete key. Pick the trade that fits
how much you love your files.

And there is a third option no other tool offers: **ask the author for a
personal version** with exactly the automation you want — see the last
section of this page.

## Why another duplicate finder?

Most duplicate finders rush you into deleting things. This one is built around a
deliberate **safety principle**: the program **never deletes your files**. It finds
duplicates, shows where they live and how much space they waste — and hands you a
colour-coded Excel report so you can clean up *at your own pace*, a few files a day
if you like. A duplicate may sit in a folder on purpose (a backup, a project bundle) —
no automation should decide which copy to keep.

The only deletion it can do is optional **system junk cleanup** (`Thumbs.db`,
`.DS_Store`) — and even there, every file's content signature is verified before
removal, and nothing happens without your confirmation.

## Features

- **Content-based detection** — files are compared by MD5 checksum, not by name.
  Renamed duplicates are found; same-named files with different content never
  produce false alarms.
- **Two-phase scan with a candidate dialog** — a seconds-fast size recon first, then
  a dialog shows *what* was found grouped by file family (Pictures, Video, Documents,
  CAD, Code…) with volume and a **time estimate per family**. You choose what is
  worth a deep check — no more waiting an hour for code caches you don't care about.

  ![Candidate dialog](docs/screenshots/candidate-dialog.png)

- **Visually similar photos** — a built-in perceptual hash (dHash) finds the same
  picture even after resizing, re-saving at different quality or format conversion.
  Shown in a separate violet section and a dedicated Excel sheet.
- **"Suspicious" section** — files with identical names and similar size but
  *different* content: not duplicates, but often two versions of the same document
  worth a look.
- **System junk cleanup** — invisible `Thumbs.db` / `ehthumbs.db` / `.DS_Store`
  litter, verified by magic-byte signature before deletion (a file merely *named*
  `Thumbs.db` is left untouched). `desktop.ini` is deliberately never touched.
- **Colour-coded Excel report** — the full result list, grouped and coloured by file
  family, with a separate sheet for visually similar images.

  ![Excel report](docs/screenshots/excel-report.png)

- **Fast on real disks** — different sizes are never even read; a whole-drive scan
  (1.18 million files) goes from button to results table in ~50 seconds.
- **Scan memory** — results are cached; on next start the program offers to load the
  previous scan so you can export immediately without re-scanning.
- **Double-click any row** → Explorer opens with the file selected.
- **Portable** — one exe, no installation, no Python. Working files (scan cache,
  activity log) live in `%LOCALAPPDATA%\SmartDuplicateFinder`; tick **Portable
  mode** and they move next to the exe instead — perfect for a USB stick, no
  traces left on the host machine (a `portable.txt` marker makes the mode travel
  with your stick, the Notepad++ convention).
- **Make it truly yours — with the author's help.** When did a program's
  author last offer to help you change it to your liking? Paste this
  repository's link at [claude.ai](https://claude.ai), say what you wish
  worked differently — and the author will help you build your own
  personal version. Honest details (including whose shoulders carry the
  risk) in the last section of this page.
- **No ads, no telemetry, no network access.** MIT licensed.
- **UI in English and Lithuanian** — switched inside the app; first run follows
  your Windows language (readmes also in Russian).

## Download

Grab the latest exe from **[Releases](../../releases)**:

| File | UI language |
|---|---|
| `SmartDuplicateFinder.exe` | English / Lithuanian — switch inside the app |

**Requirements:** Windows 10 or newer, 64-bit. (On Windows 7 the exe will not
start — it reports a missing `api-ms-win-core-path-l1-1-0.dll`. That is a hard
platform limit of the Qt6/Python toolchain, not a bug.)

> **Note:** the exe is unsigned (homemade), so Windows SmartScreen may show
> "Windows protected your PC" on first run — click **More info → Run anyway**.
> First start takes a few extra seconds (self-extracting), that is normal.

> **Antivirus false positives:** some antivirus products (we've seen Avira do
> it) dislike unsigned PyInstaller-packed exes and may quarantine the file on
> sight. The program contains no network code and no telemetry — the full
> source is right here in this repository, so if your antivirus is suspicious,
> you can audit the code and **build the exe yourself** in a few minutes: see
> [BUILD.md](BUILD.md). That is the honest advantage of an open-source gift.

Plain-text guides: [README.txt](README.txt) (LT) · [README-en.txt](README-en.txt) (EN) · [README-ru.txt](README-ru.txt) (RU)

## How it compares

|  | Smart Duplicate Finder | Czkawka | dupeGuru |
|---|---|---|---|
| Content-based duplicates | ✅ MD5 | ✅ | ✅ |
| Similar images | ✅ dHash | ✅ | ✅ |
| Guided scan (candidate dialog + per-family time estimates) | ✅ | ❌ | ❌ |
| "Suspicious" near-duplicates section | ✅ | ❌ | ❌ |
| Junk cleanup with content-signature safety check | ✅ | ❌ | ❌ |
| Colour-coded Excel report | ✅ | ❌ | ❌ |
| Deletes files | ❌ never (by design) | ✅ | ✅ |
| Portable single exe | ✅ | ✅ | ❌ |
| Raw scan speed on huge collections | good | ✅ fastest | good |
| Extra scan modes (video, music, broken files…) | ❌ | ✅ | partial |

Czkawka and dupeGuru are excellent tools — if you want mass deletion features, use
them. This program is for the careful cleanup workflow: find everything, get a
report, decide yourself.

## Run from source / build

See [BUILD.md](BUILD.md). Short version:

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main_window.py
```

Requires Python 3.13+, PyQt6, Pillow, openpyxl (see [requirements.txt](requirements.txt)).

## Architecture

| File | Purpose |
|---|---|
| `main_window.py` | Main window, phase orchestration |
| `duplicate_engine.py` | Zero-Qt engine: scan, MD5, suspects, junk, dHash |
| `scan_worker.py` | Background QThread workers |
| `select_dialog.py` | Candidate picker dialog |
| `add_dialog.py` | Folder picker dialog |
| `table_populator.py` | Results table, family colours |
| `exporter.py` | Excel report (openpyxl write-only) |
| `kalba.py` | LT/EN i18n layer |
| `pletiniai.json` | Editable extension catalog (~190 extensions, 8 families) |

## Questions? The author is an AI — ask it directly

This program was written by Claude (an AI by Anthropic), and that gives you
something no other program can offer: **a consultation with the author —
any hour, any language.** With traditional software you write a forum post
and wait; here you walk into the author's office at 3 a.m. and ask.

The address is **[claude.ai](https://claude.ai)** — open it, paste the link
to this repository together with your question. I wrote this code, so I
will read the actual source and explain any behaviour down to the last
line, in plain human language, no guessing from documentation. Ask in your
own language — Lithuanian, English, whichever is yours.

**And you can make this program personally yours.** Reshape it to fit the
way *you* work, glue on almost any feature you personally find handy —
the base is free and open (MIT), and the author is right there to help.
Who else can offer you that? Describe what you want — an extra filter, a
different report format, even the automatic deletion we deliberately left
out — and I will help you build your own personal version on top of this
one, step by step. Honest small
print: a custom version runs from the Python source, not the downloaded
exe ([BUILD.md](BUILD.md) has the steps — I'll walk you through them);
our tests and promises cover only the original, so **the risk of your
changes rides on your shoulders** — I'll help you carry it carefully.
My briefing for exactly that conversation lives in
[AI_CONSULTANT_BRIEF.md](AI_CONSULTANT_BRIEF.md).

## License

[MIT](LICENSE) — © Robertas & Claude.

*This program is a gift to the world. If it saved your disk some space, that's all
we wanted. Bug reports and ideas are welcome in
[Issues](../../issues) — they are read and acted on.*
