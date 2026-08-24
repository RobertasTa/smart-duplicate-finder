# Seimos kolizija flesiuke + angliski failu vardai.
#
# Roberto radinys 2026-08-24 (I): "jei abu tuo paciu pavadinimu pasirasys ta
# failiuka, bedos bus" - abi dovanos rase i ta pati _darbal.
# Roberto klausimas 2026-08-24 (II): "tuos failiukus lietuviu kalba tik meskai
# supras, kitom kalbom kaip bus?" - vardai pervadinti i angliskus.
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import saugykla as sg


@pytest.fixture
def flesiukas(tmp_path, monkeypatch):
    """Suvaidina flesiuka: abu exe viename kataloge, portable ijungtas."""
    monkeypatch.setattr(sg, "exe_dir", lambda: tmp_path)
    monkeypatch.setattr(sg, "_migruota", False)
    (tmp_path / sg.PORTABLE_MARKER).write_text("portable\n", encoding="utf-8")
    return tmp_path


# --- Vieta ------------------------------------------------------------------

def test_portable_katalogas_pasirasytas_programos_vardu(flesiukas):
    """Bendro tevo nebera: susimaisyti nebeturi su kuo."""
    assert sg.data_dir() == flesiukas / "SmartDuplicateFinder_data"


def test_katalogo_vardas_be_lietuvisku_zodziu(flesiukas):
    """Roberto klausimas: kitakalbis turi suprasti, ka mato flesiuke."""
    vardas = sg.data_dir().name
    assert vardas.isascii(), "varde yra ne-ASCII simboliu"
    assert "darbal" not in vardas.lower()


# --- Migracija is BENDRO _darbal (iki 2026-08-24) ---------------------------

def test_migracija_is_bendro_darbal_pervadina_ir_nelieia_svetimu(flesiukas):
    senas = flesiukas / "_darbal"
    senas.mkdir()
    (senas / "paskutinis_skenas.json").write_text('{"g": 42}', encoding="utf-8")
    (senas / "veiklos.log").write_text("startas\n", encoding="utf-8")
    (senas / "scan_speed.json").write_text("999", encoding="utf-8")
    (senas / "kalba.txt").write_text("ru\n", encoding="utf-8")
    # SVETIMAS - TempCleaner valymo zurnalas (auditas!)
    (senas / "valymo_log.txt").write_text("istrinta 5 GB\n", encoding="utf-8")

    sg.migruoti_sena_darbal()
    naujas = sg.data_dir()

    # savi persikele IR pervadinti
    assert (naujas / "last_scan.json").read_text(encoding="utf-8") == '{"g": 42}'
    assert (naujas / "activity.log").exists()
    assert (naujas / "scan_speed.json").read_text(encoding="utf-8") == "999"
    assert not (naujas / "paskutinis_skenas.json").exists(), "liko senas vardas"
    assert not (naujas / "veiklos.log").exists(), "liko senas vardas"
    # bendravardis: KOPIJUOTAS nauju vardu, senasis paliktas kaimynui
    assert (naujas / "language.txt").read_text(encoding="utf-8").strip() == "ru"
    assert (senas / "kalba.txt").exists(), "kalba.txt dingo TempCleaner'iui!"
    # svetimas nepaliestas
    assert (senas / "valymo_log.txt").exists(), "pagrobtas TempCleaner zurnalas!"


# --- Migracija is TARPINES formos (_darbal/SmartDuplicateFinder) ------------

def test_migracija_is_tarpines_formos(flesiukas):
    """Tokia struktura spejo atsirasti tik Roberto flesiuke (testinis buildas
    2026-08-24 17:43) - bet ji turi persikelti svariai."""
    tarpinis = flesiukas / "_darbal" / "SmartDuplicateFinder"
    tarpinis.mkdir(parents=True)
    (tarpinis / "paskutinis_skenas.json").write_text("{}", encoding="utf-8")
    (tarpinis / "kalba.txt").write_text("de\n", encoding="utf-8")

    sg.migruoti_sena_darbal()
    naujas = sg.data_dir()

    assert (naujas / "last_scan.json").exists()
    # cia katalogas MUSU, tad bendravardis PERKELIAMAS, ne kopijuojamas
    assert (naujas / "language.txt").read_text(encoding="utf-8").strip() == "de"
    assert not tarpinis.exists(), "tuscias tarpinis katalogas neistrintas"
    assert not (flesiukas / "_darbal").exists(), "tuscias _darbal neistrintas"


# --- Vardu pervadinimas VIETOJE (%LOCALAPPDATA% atvejis) --------------------

def test_pervadinimas_vietoje_kai_katalogas_nesikeicia(tmp_path, monkeypatch):
    """Ne portable vartotojui katalogas lieka tas pats - keiciasi tik vardai."""
    la = tmp_path / "localappdata"
    (la / "SmartDuplicateFinder").mkdir(parents=True)
    monkeypatch.setenv("LOCALAPPDATA", str(la))
    monkeypatch.setattr(sg, "exe_dir", lambda: tmp_path / "exe")
    monkeypatch.setattr(sg, "_migruota", False)

    d = la / "SmartDuplicateFinder"
    (d / "veiklos.log").write_text("senas", encoding="utf-8")
    (d / "kalba.txt").write_text("lt\n", encoding="utf-8")

    sg.migruoti_sena_darbal()

    assert (d / "activity.log").read_text(encoding="utf-8") == "senas"
    assert (d / "language.txt").read_text(encoding="utf-8").strip() == "lt"
    assert not (d / "veiklos.log").exists()
    assert not (d / "kalba.txt").exists()


def test_migracija_neperraso_jau_esamu(flesiukas):
    senas = flesiukas / "_darbal"
    senas.mkdir()
    (senas / "scan_speed.json").write_text("SENAS", encoding="utf-8")
    naujas = sg.data_dir()
    naujas.mkdir(parents=True)
    (naujas / "scan_speed.json").write_text("NAUJAS", encoding="utf-8")

    sg.migruoti_sena_darbal()

    assert (naujas / "scan_speed.json").read_text(encoding="utf-8") == "NAUJAS"


def test_migracija_saugi_kai_nera_ko_migruoti(flesiukas):
    assert sg.migruoti_sena_darbal() == 0


# --- Portable isjungimas ----------------------------------------------------

def test_isjungiant_portable_svetimi_failai_lieka(flesiukas, monkeypatch, tmp_path):
    la = tmp_path / "localappdata"
    la.mkdir()
    monkeypatch.setenv("LOCALAPPDATA", str(la))

    savas = sg.data_dir()
    savas.mkdir(parents=True)
    (savas / "scan_speed.json").write_text("mano", encoding="utf-8")
    # kaimyno duomenys - dabar VISAI atskirame kataloge
    svetimas = flesiukas / "TempCleaner_data"
    svetimas.mkdir()
    (svetimas / "cleaning_log.txt").write_text("auditas", encoding="utf-8")

    ok, klaida = sg.set_portable(False)

    assert ok, klaida
    assert (la / "SmartDuplicateFinder" / "scan_speed.json").exists()
    assert (svetimas / "cleaning_log.txt").exists(), "kaimyno auditas dingo!"
    assert not savas.exists(), "tuscias musu katalogas neistrintas"


# --- Kai NAUJAS vardas jau uzimtas (Roberto gyvas testas 2026-08-24) --------

def test_zurnalai_suliejami_kai_abu_vardai_yra(tmp_path, monkeypatch):
    """Buvo: apsauga nuo perrasymo virsdavo apsauga nuo susitvarkymo -
    veiklos.log likdavo guleti amzinai salia activity.log."""
    la = tmp_path / "localappdata"
    d = la / "SmartDuplicateFinder"
    d.mkdir(parents=True)
    monkeypatch.setenv("LOCALAPPDATA", str(la))
    monkeypatch.setattr(sg, "exe_dir", lambda: tmp_path / "exe")
    monkeypatch.setattr(sg, "_migruota", False)

    (d / "veiklos.log").write_text("SENA ISTORIJA\n", encoding="utf-8")
    (d / "activity.log").write_text("nauja eilute\n", encoding="utf-8")

    sg.migruoti_sena_darbal()

    assert not (d / "veiklos.log").exists(), "senas zurnalas liko guleti"
    turinys = (d / "activity.log").read_text(encoding="utf-8")
    assert "SENA ISTORIJA" in turinys, "sena istorija prarasta!"
    assert "nauja eilute" in turinys
    assert turinys.index("SENA ISTORIJA") < turinys.index("nauja eilute"), \
        "istorija turi buti chronologine - sena pirma"


def test_duomenu_failas_atidedamas_su_priesaga(tmp_path, monkeypatch):
    """Ne zurnalo negalima sulieti - senaji atidedam, bet NETRINAM."""
    la = tmp_path / "localappdata"
    d = la / "SmartDuplicateFinder"
    d.mkdir(parents=True)
    monkeypatch.setenv("LOCALAPPDATA", str(la))
    monkeypatch.setattr(sg, "exe_dir", lambda: tmp_path / "exe")
    monkeypatch.setattr(sg, "_migruota", False)

    (d / "paskutinis_skenas.json").write_text('{"senas": 1}', encoding="utf-8")
    (d / "last_scan.json").write_text('{"naujas": 2}', encoding="utf-8")

    sg.migruoti_sena_darbal()

    assert not (d / "paskutinis_skenas.json").exists()
    assert (d / "paskutinis_skenas.json.old").read_text(encoding="utf-8") == '{"senas": 1}'
    assert (d / "last_scan.json").read_text(encoding="utf-8") == '{"naujas": 2}'


def test_pervadinama_ir_NEAKTYVIOJE_vietoje(flesiukas, monkeypatch, tmp_path):
    """Roberto gyvas testas 2026-08-24: portable rezime profilio katalogas
    likdavo su senais vardais - ir niekada nebebutu sutvarkytas, nes ten
    nebesikreipiam. Migracija turi apziureti ABI musu vietas."""
    la = tmp_path / "localappdata"
    profilis = la / "SmartDuplicateFinder"
    profilis.mkdir(parents=True)
    monkeypatch.setenv("LOCALAPPDATA", str(la))
    (profilis / "veiklos.log").write_text("profilio istorija\n", encoding="utf-8")

    # esam PORTABLE - aktyvi vieta yra flesiukas, ne profilis
    assert sg.data_dir() == flesiukas / "SmartDuplicateFinder_data"
    sg.migruoti_sena_darbal()

    assert not (profilis / "veiklos.log").exists(), \
        "neaktyvioje vietoje liko senas vardas"
    assert (profilis / "activity.log").read_text(encoding="utf-8") == "profilio istorija\n"
