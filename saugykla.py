"""saugykla.py - kur gyvena programos darbiniai failai (portable vs kompiuteris).

2026-08-06 bendras abieju dovanu sprendimas (Roberto varnele + Notepad++
doLocalConf.xml konvencija, kaip Temp Cleaner dovanoje): rezima nustato
ZYMEKLIO FAILAS portable.txt salia exe - jis keliauja su flesiuku, tad
ijungtas rezimas galioja visuose kompiuteriuose. GUI ji valdo varnele.

- portable.txt NERA (numatyta): kesas/zurnalas -> %LOCALAPPDATA%/SmartDuplicateFinder.
  (Anksciau buvo %TEMP% - bet temp valytuvai kesa istrindavo, o elgsena
  nesutapo su Temp Cleaner dovana.)
- portable.txt YRA: -> _darbal salia exe (kompiuteryje pedsaku nelieka).
"""

import os
import shutil
import sys
from pathlib import Path

PORTABLE_MARKER = "portable.txt"
APP_DIRNAME = "SmartDuplicateFinder"


def exe_dir():
    """Katalogas salia exe (frozen) arba salia .py failu (dev)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def is_portable():
    return (exe_dir() / PORTABLE_MARKER).exists()


def data_dir():
    """Darbiniu failu katalogas pagal rezima (nekuriamas - kuria rasytojai)."""
    if is_portable():
        return exe_dir() / "_darbal"
    base = os.environ.get("LOCALAPPDATA")
    if base:
        return Path(base) / APP_DIRNAME
    return exe_dir() / "_darbal"   # atsarga sistemoms be LOCALAPPDATA


def set_portable(on):
    """Perjungia rezima: zymeklis + darbiniai failai persikelia + pedsaku valymas.

    Grazina (ok, klaidos_tekstas) - pvz., read-only flesiukas -> (False, ...).
    """
    marker = exe_dir() / PORTABLE_MARKER
    try:
        src_dir = data_dir()                  # dabartine vieta (senas rezimas)
        if on:
            marker.write_text("portable\n", encoding="utf-8")
        elif marker.exists():
            marker.unlink()
        dst_dir = data_dir()                  # nauja vieta (rezimas jau naujas)
        if src_dir != dst_dir and src_dir.is_dir():
            dst_dir.mkdir(parents=True, exist_ok=True)
            for f in src_dir.iterdir():
                if f.is_file():
                    shutil.move(str(f), str(dst_dir / f.name))
        if on:
            # Pedsaku valymas: kompiuteryje likes katalogas istrinamas
            base = os.environ.get("LOCALAPPDATA")
            if base:
                shutil.rmtree(Path(base) / APP_DIRNAME, ignore_errors=True)
        else:
            try:
                (exe_dir() / "_darbal").rmdir()   # tik jei tuscias
            except OSError:
                pass
        return True, ""
    except OSError as e:
        return False, str(e)
