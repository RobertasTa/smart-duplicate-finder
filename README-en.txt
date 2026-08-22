=====================================================================
  SMART DUPLICATE FINDER v2 — duplicate file finder
=====================================================================

WHAT IT IS
----------
The program finds duplicate (identical content) files in selected
folders or whole drives and shows how much space they waste.
Files are compared by CONTENT (MD5 checksum), not by name — renamed
duplicates are found, while same-named files with different content
are never reported as duplicates.

It can also find and clean INVISIBLE system junk files (Thumbs.db
etc.) — see the section below.

IMPORTANT: the program does NOT delete your duplicates — it only
finds and shows them; you decide what to do. The only deletion is
the system-junk cleanup, and that runs only after your confirmation.

Ask anyone who has used duplicate finders for years and you will
hear the same story: one day the program deleted the wrong files.
That is not a bug in one particular tool — it is the limit of every
algorithm. NO ALGORITHM CAN DECIDE WHAT MATTERS TO YOU: what is
junk to one person is the only surviving backup to another.

So this is a DELIBERATE SAFETY PRINCIPLE, not a limitation: no
automation should decide which copy to keep — a duplicate may sit
in a folder on purpose (a backup, a project bundle). The program
will never delete what you wanted to keep, so it is safe to scan
even your most precious archives.

That is also what the Excel report is for: cleaning up AT YOUR OWN
PACE. Nothing forces you to act immediately — the report is a file
you can open a week later, sort, colour-mark what is done, and work
through a few duplicates a day until the drive is clean. And if
after the review you decide you want to keep every single copy —
that is a perfectly good outcome too. The goal here is not
gigabytes deleted; it is you knowing exactly what you have and
making the call yourself.

HOW TO RUN
----------
1. You only need one file: SmartDuplicateFinder-en.exe
   No installation, no Python — runs straight from a USB stick.
2. The first start takes a few extra seconds — that is normal.
3. If Windows shows a blue "Windows protected your PC" screen,
   click "More info" -> "Run anyway". The program is unsigned
   (homemade), but safe.

HOW TO USE (step by step)
-------------------------
1. "+ Add folders" — pick where to search (a whole drive like D:\
   works fine). You can also paste paths from Explorer.
2. ">>> Scan" — a fast RECON runs first (only file sizes are read,
   takes seconds).
3. A "Duplicate candidates found" window appears — candidates are
   grouped by type (Pictures, Video, Documents, CAD, Code, ...)
   with volume and a TIME ESTIMATE for each row.
   TIP: usually untick "Code" and "Other" — thousands of tiny
   program files nobody needs to clean, but slowest to check.
4. "Check selected" — deep content check runs. The bottom-right
   corner shows live progress: files done, speed (MB/s), time left.
5. Results are colour-grouped by type; the BIGGEST duplicates are
   on top. Hover a row to see the file-type description.
6. DOUBLE-CLICK a row to open Explorer with the file selected.
   RIGHT-CLICK (since v1.3) offers: open file / open folder /
   copy path (opening executables is disabled for safety).
7. "Export report" — the full list is saved to a colour-coded
   Excel file (you choose where; Documents is suggested).

SYSTEM JUNK CLEANUP ("Clean junk files" button)
-----------------------------------------------
Windows and macOS litter folders with INVISIBLE cache files that
Explorer normally hides:
  * Thumbs.db, ehthumbs.db — Windows thumbnail cache
  * .DS_Store — macOS Finder browsing litter (common on NAS shares)
Harmless but messy — and hard to delete by hand since you can't
see them.

How it works:
1. After the recon, if junk was found, the "Clean junk files (N)"
   button lights up.
2. Click it — you get a summary by type and a confirmation prompt.
3. SAFETY: before deleting, EVERY file's content signature (magic
   bytes) is verified. A file merely NAMED Thumbs.db whose content
   differs is left untouched. In doubt = never deleted.
4. Afterwards you see how many files were removed and how much
   space was freed. The OS recreates these caches when needed.
WARNING: on network drives (NAS) deletion is permanent — there is
no recycle bin there. That is exactly why signatures are verified.

Note: desktop.ini files are deliberately NEVER touched — they store
folder customisations.

SIMILAR PHOTOS (visual comparison)
----------------------------------
The candidates window has an extra row "Similar photos (visual)"
(ticked by default, like the others). With it photos are compared VISUALLY —
the same picture is found even if it was resized, re-saved at a
different quality or converted to another format (MD5 cannot see
those, since the bytes differ). Works across everyday image formats
(JPG, PNG, GIF, BMP, TIFF, WebP) and, since v1.3, the iPhone formats
HEIC/AVIF; phone photos stored "rotated" (EXIF orientation) are
matched correctly too. Such groups appear in violet
("VISUALLY SIMILAR") and on a separate "Similar Images" sheet in
the Excel report.
A note on time: this comparison must open EVERY photo (~40 photos/s),
so large archives (tens of thousands of photos) take a while — untick
it when in a hurry. Groups where all files are byte-identical (already
reported as duplicates) are not repeated here — only genuinely
"hidden" copies are shown.

GOOD TO KNOW
------------
* SCAN MEMORY THAT SURVIVES ANYTHING: results are saved to disk the
  moment scanning finishes, BEFORE the table is even drawn. If the
  program gets killed or crashes right after a long scan, the
  results are still there: on next start it offers to load the
  previous scan so you can review and export immediately, without
  re-scanning. A scan that took hours is never lost.
* The table shows up to 2,000 rows (largest groups); the FULL list
  is always in the Excel report.
* SUSPICIOUS section (yellow) — files with identical names and
  similar size but DIFFERENT content. Not duplicates, but worth a
  look (e.g. two versions of the same document).
* Different file size = guaranteed not a duplicate, so such files
  are never even read — that is why scans are fast on big drives.
* Empty (0-byte) files are skipped on purpose.

WHERE THINGS ARE STORED
-----------------------
* Excel reports — wherever you choose (Documents suggested).
* Service files — in %LOCALAPPDATA%\SmartDuplicateFinder\:
    paskutinis_skenas.json  - scan memory
    scan_speed.json         - disk speed for time estimates
    veiklos.log             - activity log (useful if something
                              ever gets stuck)
* PORTABLE MODE (checkbox at the bottom of the left bar): when ON,
  service files are stored in a _darbal folder NEXT TO the app
  (e.g. on a USB stick) and no traces are left on the computer —
  the app even removes its previously created %LOCALAPPDATA% folder.
  The choice is remembered by a portable.txt file next to the exe
  (the Notepad++ / VS Code convention) - it travels with your stick.
* All service files can be deleted at any time — the program simply
  starts fresh.
* LANGUAGE (Lietuviu / English / Russian / German) can be switched
  in the dropdown at the bottom of the left bar; the choice is
  remembered and applied after a restart.

---------------------------------------------------------------------
Created by: Robertas + Claude (Anthropic AI) + local AI assistant
2026-08-05        Version: v2 (English UI)
=====================================================================
