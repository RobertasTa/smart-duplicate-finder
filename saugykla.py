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

# --- SEIMOS KOLIZIJA, ANTRA DALIS (Roberto radinys 2026-08-24) ------------
# 08-07 buvo prefiksuotas ZYMEKLIS, bet KATALOGAS liko bendras: abi dovanos
# portable rezime rase i ta pati "_darbal" salia exe. Pasekmes flesiuke,
# kur guli abu exe:
#   1) abi rase "kalba.txt" tuo paciu vardu - kalba "nutekedavo" is vienos
#      programos i kita;
#   2) BLOGIAU: set_portable() perkeldavo VISUS is _darbal rastus failus i
#      savo %LOCALAPPDATA% kataloga - t. y. viena dovana issivesdavo kitos
#      dovanos duomenis (SDF kesa arba TC valymo zurnala-audita).
# Sprendimas: portable duomenys gyvena PO-KATALOGE pagal programos varda -
# lygiai taip pat, kaip %LOCALAPPDATA%\\SmartDuplicateFinder. Struktura
# abiem rezimam vienoda, flesiuke lieka vienas tvarkingas _darbal.
DARBAL_DIRNAME = "_darbal"

# Musu darbiniai failai (migracijai is seno bendro _darbal).
# "kalba.txt" TYCIA cia nera - jis bendravardis su TempCleaner, todel
# migruojamas KOPIJUOJANT: abi programos pasiima po kopija ir nuo tada
# viena kitos nebeliecia.
_SAVI_FAILAI = ("veiklos.log", "paskutinis_skenas.json", "scan_speed.json")
_BENDRAVARDIS = "kalba.txt"
_migruota = False   # migracija vykdoma viena karta per procesa


def exe_dir():
    """Katalogas salia exe (frozen) arba salia .py failu (dev)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def is_portable():
    d = exe_dir()
    return (d / PORTABLE_MARKER).exists() or (d / PORTABLE_MARKER_SENAS).exists()


def _senas_darbal():
    """Iki-v1.4 bendra vieta, kuria dalinomes su TempCleaner."""
    return exe_dir() / DARBAL_DIRNAME


def data_dir():
    """Darbiniu failu katalogas pagal rezima (nekuriamas - kuria rasytojai)."""
    if is_portable():
        return exe_dir() / DARBAL_DIRNAME / APP_DIRNAME
    base = os.environ.get("LOCALAPPDATA")
    if base:
        return Path(base) / APP_DIRNAME
    # atsarga sistemoms be LOCALAPPDATA - ta pati po-katalogo struktura
    return exe_dir() / DARBAL_DIRNAME / APP_DIRNAME


def migruoti_sena_darbal():
    """Vienkartinis perkelimas is bendro _darbal i _darbal/SmartDuplicateFinder.

    Kvieciama paleidziant programa. Saugi bet kokioje busenoje:
    - jei seno katalogo nera arba jis jau yra musiskis - nedaro nieko;
    - SAVO failus PERKELIA, bendravardi kalba.txt KOPIJUOJA (kad ir
      TempCleaner ji rastu ir pasiimtu savo kopija);
    - svetimu failu NELIECIA;
    - klaida (read-only flesiukas) nutylima: programa turi startuoti.

    Grazina perkeltu failu skaiciu (0 - nebuvo ko).
    """
    global _migruota
    if _migruota:
        return 0
    _migruota = True
    senas = _senas_darbal()
    naujas = data_dir()
    if senas == naujas or not senas.is_dir():
        return 0
    perkelta = 0
    try:
        for vardas in _SAVI_FAILAI:
            f = senas / vardas
            if f.is_file() and not (naujas / vardas).exists():
                naujas.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), str(naujas / vardas))
                perkelta += 1
        k = senas / _BENDRAVARDIS
        if k.is_file() and not (naujas / _BENDRAVARDIS).exists():
            naujas.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(k), str(naujas / _BENDRAVARDIS))
            perkelta += 1
    except OSError:
        pass
    return perkelta


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
            # Isjungiant portable: nuimam SAVO po-kataloga, o bendra _darbal
            # tik tuomet, jei jame nebeliko nieko - ten gali gyventi kitos
            # dovanos duomenys (Roberto radinys 2026-08-24).
            try:
                (exe_dir() / DARBAL_DIRNAME / APP_DIRNAME).rmdir()
            except OSError:
                pass
            try:
                (exe_dir() / DARBAL_DIRNAME).rmdir()   # tik jei tuscias
            except OSError:
                pass
        return True, ""
    except OSError as e:
        return False, str(e)
