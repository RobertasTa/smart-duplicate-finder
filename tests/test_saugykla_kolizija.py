# Seimos kolizija flesiuke: SDF ir TempCleaner viename kataloge.
# Roberto radinys 2026-08-24: "jei abu tuo paciu pavadinimu pasirasys ta
# failiuka, bedos bus". Ju ir buvo - zr. saugykla.py komentara.
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


def test_portable_duomenys_gyvena_po_katalogyje(flesiukas):
    """Ne bendrame _darbal, o _darbal/SmartDuplicateFinder."""
    assert sg.data_dir() == flesiukas / "_darbal" / "SmartDuplicateFinder"


def test_migracija_pasiima_savus_ir_nelieia_svetimu(flesiukas):
    senas = flesiukas / "_darbal"
    senas.mkdir()
    # musu failai
    (senas / "paskutinis_skenas.json").write_text("{}", encoding="utf-8")
    (senas / "scan_speed.json").write_text("123", encoding="utf-8")
    # bendravardis
    (senas / "kalba.txt").write_text("ru\n", encoding="utf-8")
    # SVETIMAS - TempCleaner valymo zurnalas (auditas!)
    (senas / "valymo_log.txt").write_text("2026-08-24 isvalyta\n", encoding="utf-8")

    perkelta = sg.migruoti_sena_darbal()

    naujas = sg.data_dir()
    assert perkelta == 3
    # savi persikele
    assert (naujas / "paskutinis_skenas.json").exists()
    assert (naujas / "scan_speed.json").exists()
    assert not (senas / "scan_speed.json").exists()
    # bendravardis NUKOPIJUOTAS, ne perkeltas - TempCleaner ji dar ras
    assert (naujas / "kalba.txt").read_text(encoding="utf-8").strip() == "ru"
    assert (senas / "kalba.txt").exists(), "kalba.txt dingo TempCleaner'iui!"
    # svetimas nepaliestas
    assert (senas / "valymo_log.txt").exists(), "pagrobtas TempCleaner zurnalas!"


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


def test_isjungiant_portable_svetimi_failai_lieka(flesiukas, monkeypatch, tmp_path):
    """set_portable(False) issivedza TIK savo kataloga."""
    la = tmp_path / "localappdata"
    la.mkdir()
    monkeypatch.setenv("LOCALAPPDATA", str(la))

    savas = sg.data_dir()
    savas.mkdir(parents=True)
    (savas / "scan_speed.json").write_text("mano", encoding="utf-8")
    # kaimyno duomenys bendrame _darbal
    svetimas = flesiukas / "_darbal" / "TempCleaner"
    svetimas.mkdir(parents=True)
    (svetimas / "valymo_log.txt").write_text("auditas", encoding="utf-8")

    ok, klaida = sg.set_portable(False)

    assert ok, klaida
    assert (la / "SmartDuplicateFinder" / "scan_speed.json").exists()
    assert (svetimas / "valymo_log.txt").exists(), "kaimyno auditas dingo!"
    # bendras _darbal islieka, nes jame dar gyvena kaimynas
    assert (flesiukas / "_darbal").is_dir()
