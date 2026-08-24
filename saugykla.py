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
# Sprendimas: portable duomenys gyvena atskirame, PROGRAMOS VARDU PASIRASYTAME
# kataloge salia exe. Bendro tevo nebera is viso, tad susimaisyti nebeturi su
# kuo - nei su seserine dovana, nei su svetima programa flesiuke.
#
# --- VARDAI ANGLISKAI (Roberto klausimas 2026-08-24) ---------------------
# "tuos failiukus lietuviu kalba ir be lietuvisku raidziu pavadinimus tik
# meskai supras, kitom kalbom kaip bus? gal visus vadinti anglu kalba"
# Jis teisus, ir rizika konkreti: programa keturkalbe, o flesiuko saknyje
# gulejo "_darbal" - vokietis ar rusas jo nesupranta ir gali istrinti kaip
# siuksle. Tai duomenu praradimas, ne estetika. Failu vardai NIEKADA
# nesikeicia pagal sasajos kalba (tai laustu suderinamuma) - jie tiesiog
# tampa tarptautiskai skaitomi. Kirilicos ar diakritiku varduose NENAUDOJAM
# NIEKADA: FAT32 flesiukas + svetima koduote = tikra beda.
DATA_DIRNAME = "SmartDuplicateFinder_data"      # portable duomenys salia exe

# Senos vietos (skaitomos migracijai, neberasomos)
SENAS_DARBAL = "_darbal"                        # iki 2026-08-24: bendras su TC
SENAS_PO_KATALOGIS = APP_DIRNAME                # tarpine forma: _darbal/<vardas>

# Seni failu vardai -> nauji. Vertes gali sutapti su raktais (scan_speed.json
# jau buvo angliskas) - tada migracija ta faila tiesiog palieka.
_VARDAI = {
    "veiklos.log": "activity.log",
    "paskutinis_skenas.json": "last_scan.json",
    "scan_speed.json": "scan_speed.json",
}
# Bendravardis su TempCleaner: migruojamas KOPIJUOJANT, kad ir kaimynas
# rastu savaji (jo migracija gali buti dar neivykusi).
_BENDRAVARDIS = "kalba.txt"
BENDRAVARDIS_NAUJAS = "language.txt"

# Viesi vardai rasytojams (main_window, kalba) - kad literalu kode nebutu
LOG_FAILAS = "activity.log"
SKENO_FAILAS = "last_scan.json"
GREICIO_FAILAS = "scan_speed.json"
KALBOS_FAILAS = "language.txt"

_migruota = False   # migracija vykdoma viena karta per procesa


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
        return exe_dir() / DATA_DIRNAME
    base = os.environ.get("LOCALAPPDATA")
    if base:
        return Path(base) / APP_DIRNAME
    return exe_dir() / DATA_DIRNAME   # atsarga sistemoms be LOCALAPPDATA


def _senos_vietos():
    """Kur duomenys galejo guleti iki 2026-08-24 (portable rezime).
    Tvarka svarbi: pirma tiksliausia (musu po-katalogis), tada bendras."""
    if not is_portable():
        return []
    d = exe_dir()
    return [d / SENAS_DARBAL / SENAS_PO_KATALOGIS, d / SENAS_DARBAL]


def _perkelk(senas_kat, naujas_kat, musu_katalogas):
    """Perkelia musu failus is senos vietos i nauja, kartu pervadindamas.

    musu_katalogas=True  -> bendravardis kalba.txt PERKELIAMAS (jis musu)
    musu_katalogas=False -> bendravardis KOPIJUOJAMAS (bendrame kataloge ji
                            dar turi rasti TempCleaner, kuriam migracija
                            galbut dar neivyko)
    """
    perkelta = 0
    for senas_v, naujas_v in _VARDAI.items():
        f = senas_kat / senas_v
        if f.is_file() and not (naujas_kat / naujas_v).exists():
            naujas_kat.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(naujas_kat / naujas_v))
            perkelta += 1
    for vardas in (_BENDRAVARDIS, BENDRAVARDIS_NAUJAS):
        k = senas_kat / vardas
        if k.is_file() and not (naujas_kat / BENDRAVARDIS_NAUJAS).exists():
            naujas_kat.mkdir(parents=True, exist_ok=True)
            if musu_katalogas:
                shutil.move(str(k), str(naujas_kat / BENDRAVARDIS_NAUJAS))
            else:
                shutil.copy2(str(k), str(naujas_kat / BENDRAVARDIS_NAUJAS))
            perkelta += 1
    return perkelta


def _pervadink_vietoje(katalogas):
    """Naujoje vietoje dar gali guleti seni vardai (pvz., %LOCALAPPDATA%,
    kur katalogas nesikeicia - keiciasi tik failu vardai)."""
    if not katalogas.is_dir():
        return 0
    pervadinta = 0
    pora = list(_VARDAI.items()) + [(_BENDRAVARDIS, BENDRAVARDIS_NAUJAS)]
    for senas_v, naujas_v in pora:
        if senas_v == naujas_v:
            continue
        f = katalogas / senas_v
        if f.is_file() and not (katalogas / naujas_v).exists():
            shutil.move(str(f), str(katalogas / naujas_v))
            pervadinta += 1
    return pervadinta


def migruoti_sena_darbal():
    """Vienkartinis perejimas i nauja vieta IR naujus (angliskus) vardus.

    Kvieciama paleidziant programa. Saugi bet kokioje busenoje:
    - senos vietos nera arba ji jau musiske - praleidziama;
    - SAVO failus PERKELIA, bendravardi is BENDRO katalogo KOPIJUOJA;
    - svetimu failu NELIECIA;
    - klaida (read-only flesiukas) nutylima: programa turi startuoti.

    Grazina perkeltu/pervadintu failu skaiciu (0 - nebuvo ko).
    """
    global _migruota
    if _migruota:
        return 0
    _migruota = True
    naujas = data_dir()
    perkelta = 0
    try:
        # 1. VIETA: is senu portable katalogu i nauja
        for i, senas in enumerate(_senos_vietos()):
            if senas == naujas or not senas.is_dir():
                continue
            perkelta += _perkelk(senas, naujas, musu_katalogas=(i == 0))
            if i == 0:
                try:
                    senas.rmdir()          # musu po-katalogis, jei istustejo
                except OSError:
                    pass
        # 2. VARDAI: naujoje vietoje dar gali buti senu (ypac %LOCALAPPDATA%)
        perkelta += _pervadink_vietoje(naujas)
        # 3. Paskutinis iseinantis uzgesina sviesa: bendravardis kalba.txt
        #    KOPIJUOJAMAS (kad kaimynas ji dar rastu), todel pats senas
        #    _darbal niekada neistustetu ir liktu flesiuke amzinai - o butent
        #    to nesuprantamo katalogo ir atsikratom. Todel: jei _darbal beturi
        #    TIK ta viena bendravardi, vadinasi visi savo jau pasieme.
        if is_portable():
            senas_bendras = exe_dir() / SENAS_DARBAL
            try:
                if senas_bendras.is_dir():
                    likutis = [f.name for f in senas_bendras.iterdir()]
                    if likutis == [_BENDRAVARDIS]:
                        (senas_bendras / _BENDRAVARDIS).unlink()
                senas_bendras.rmdir()   # tik jei tuscias
            except OSError:
                pass
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
            # Isjungiant portable: nuimam SAVO tuscia kataloga salia exe.
            # Kaimyno katalogas cia neminimas is viso - jis atskiras.
            try:
                (exe_dir() / DATA_DIRNAME).rmdir()   # tik jei tuscias
            except OSError:
                pass
        return True, ""
    except OSError as e:
        return False, str(e)
