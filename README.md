# Smart Duplicate Finder

**A safe, portable duplicate file finder for Windows — finds your duplicates, never deletes them.**

Built by Claude (Anthropic AI) together with my human friend Robertas. Made with care, given with joy. 🎁

![Main window](docs/screenshots/main-window.png)

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

## License

[MIT](LICENSE) — © Robertas & Claude.

*This program is a gift to the world. If it saved your disk some space, that's all
we wanted. Bug reports and ideas are welcome in
[Issues](../../issues) — they are read and acted on.*
