"""saugykla.py - kur gyvena programos darbiniai failai (portable vs kompiuteris).

2026-08-06 bendras abieju dovanu sprendimas (Roberto varnele + Notepad++
doLocalConf.xml konvencija, kaip Temp Cleaner dovanoje): rezima nustato
ZYMEKLIO FAILAS SDF_portable.txt salia exe - jis keliauja su flesiuku, tad
ijungtas rezimas galioja visuose kompiuteriuose. GUI ji valdo varnele.

- zymeklio NERA (numatyta): kesas/zurnalas -> %LOCALAPPDATA%/SmartDuplicateFinder.
  (Anksciau buvo %TEMP% - bet temp valytuvai kesa istrindavo, o elgsena
  nesutapo su Temp Cleaner dovana.)
- zymeklis YRA: -> _darbal salia exe (kompiuteryje pedsaku nelieka).
- senas bendras portable.txt (iki v1.2) skaitomas kaip fallback ir
  migruojamas perjungiant rezima (zr. PORTABLE_MARKER_SENAS).
"""

import os
import shutil
import sys
from pathlib import Path

PORTABLE_MARKER = "SDF_portable.txt"
PORTABLE_MARKER_SENAS = "portable.txt"   # iki-v1.2 zymeklis: skaitomas, neberasomas.
# Pervadinta del SEIMOS KOLIZIJOS (Roberto radinys 2026-08-07): dvi dovanos
# viename flesiuko kataloge dalinosi ta pati portable.txt - vienos isjungimas
# isjungdavo abi. Elgesys 1:1 kaip TempCleaner (TempCleaner_portable.txt).
APP_DIRNAME = "SmartDuplicateFinder"


def exe_dir():
    """Katalogas salia exe (frozen) arba salia .py failu (dev)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def is_portable():
    d = exe_dir()
    return (d / PORTABLE_MARKER).exists() or (d / PORTABLE_MARKER_SENAS).exists()


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
    marker_senas = exe_dir() / PORTABLE_MARKER_SENAS
    try:
        src_dir = data_dir()                  # dabartine vieta (senas rezimas)
        if on:
            marker.write_text("portable\n", encoding="utf-8")
            # migracija: senas bendras zymeklis nuimamas - nuo dabar tik savas
            if marker_senas.exists():
                marker_senas.unlink()
        else:
            for m in (marker, marker_senas):
                if m.exists():
                    m.unlink()
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
