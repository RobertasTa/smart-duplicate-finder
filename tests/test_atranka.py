# Atranka tests - grynas modulis, disko neliecia (keliai tik kaip tekstas).
# Run: pytest tests/
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import atranka as at


# --- 1 taisykle: vardas -----------------------------------------------------

def test_vardas_gaudo_explorer_uodegas():
    assert at.vardas_rodo_kopija(r"C:\foto\nuotrauka (1).jpg")
    assert at.vardas_rodo_kopija(r"C:\foto\ataskaita - Copy.txt")
    assert at.vardas_rodo_kopija(r"C:\foto\ataskaita - kopija.txt")
    assert at.vardas_rodo_kopija(r"C:\foto\Copy of planas.docx")


def test_vardas_NEklysta_su_teisetais_vardais():
    # Sitie NEturi buti palaikyti kopijomis - uodega tik PABAIGOJE
    assert not at.vardas_rodo_kopija(r"C:\doc\Copyright.txt")
    assert not at.vardas_rodo_kopija(r"C:\knygos\1984.txt")
    assert not at.vardas_rodo_kopija(r"C:\foto\IMG (1) galutinis.jpg")
    assert not at.vardas_rodo_kopija(r"C:\dev\copycat.py")


def test_vardas_isskiria_kai_kiti_prisipazino():
    grupe = [r"C:\foto\svente.jpg", r"C:\foto\svente (1).jpg",
             r"C:\foto\svente (2).jpg"]
    kelias, priez = at.greiciausiai_pirminis(grupe)
    assert kelias == r"C:\foto\svente.jpg"
    assert priez == at.PRIEZASTIS_VARDAS


# --- 2 taisykle: laikinas aplankas -----------------------------------------

def test_laikinas_aplankas_tik_pilnas_segmentas():
    assert at.laikinas_aplankas(r"C:\Users\R\Downloads\x.jpg")
    assert at.laikinas_aplankas(r"C:\Users\R\AppData\Local\Temp\x.jpg")
    # NE: 'Templates' nera 'temp', 'MyDownloadsBackup' nera 'downloads'
    assert not at.laikinas_aplankas(r"C:\Users\R\Templates\x.jpg")
    assert not at.laikinas_aplankas(r"C:\Users\R\MyDownloadsBackup\x.jpg")


def test_aplankas_isskiria_kai_kiti_laikinuose():
    grupe = [r"C:\Users\R\Documents\planas.pdf",
             r"C:\Users\R\Downloads\planas.pdf",
             r"C:\Users\R\AppData\Local\Temp\planas.pdf"]
    kelias, priez = at.greiciausiai_pirminis(grupe)
    assert kelias == r"C:\Users\R\Documents\planas.pdf"
    assert priez == at.PRIEZASTIS_APLANKAS


# --- 3 taisykle: gylis ------------------------------------------------------

def test_gylis_isskiria_sekliausia():
    grupe = [r"D:\archyvas\foto.jpg",
             r"D:\archyvas\2020\senos\kopijos\foto.jpg"]
    kelias, priez = at.greiciausiai_pirminis(grupe)
    assert kelias == r"D:\archyvas\foto.jpg"
    assert priez == at.PRIEZASTIS_GYLIS


# --- 4 taisykle: data -------------------------------------------------------

def test_data_lemia_kai_gylis_vienodas():
    a = r"D:\a\foto.jpg"
    b = r"D:\b\foto.jpg"
    kelias, priez = at.greiciausiai_pirminis([a, b], mtimes={a: 1000.0, b: 2000.0})
    assert kelias == a
    assert priez == at.PRIEZASTIS_DATA


def test_be_mtimes_data_nesprendziama():
    a = r"D:\a\foto.jpg"
    b = r"D:\b\foto.jpg"
    kelias, priez = at.greiciausiai_pirminis([a, b])
    assert kelias == ""
    assert priez == at.NEAISKU


# --- SVARBIAUSIAS: nespejam, kai pozymiu nera ------------------------------

def test_lygiaverciai_failai_duoda_NEAISKU():
    """Du vienodo gylio failai be jokiu pozymiu ir be datu - saziningas
    'neaisku'. Cia riba: geriau nieko nepasakyti nei speti."""
    grupe = [r"D:\foto\a\x.jpg", r"D:\foto\b\x.jpg"]
    kelias, priez = at.greiciausiai_pirminis(grupe)
    assert kelias == ""
    assert priez == at.NEAISKU


def test_vienodos_datos_irgi_neaisku():
    a = r"D:\a\foto.jpg"
    b = r"D:\b\foto.jpg"
    kelias, priez = at.greiciausiai_pirminis([a, b], mtimes={a: 500.0, b: 500.0})
    assert kelias == ""
    assert priez == at.NEAISKU


# --- Grupes zyme ------------------------------------------------------------

def test_zyme_kai_visos_kopijos_laikinuose():
    grupe = [r"C:\Users\R\Downloads\x.zip",
             r"C:\Users\R\AppData\Local\Temp\x.zip"]
    assert at.ZYME_VISI_LAIKINI in at.grupes_zymes(grupe)


def test_zymes_nera_kai_bent_vienas_namie():
    grupe = [r"C:\Users\R\Downloads\x.zip", r"D:\archyvas\x.zip"]
    assert at.grupes_zymes(grupe) == []


# --- Kraštiniai atvejai -----------------------------------------------------

def test_tuscia_ir_vienetine_grupe_nelauzia():
    assert at.greiciausiai_pirminis([]) == ("", at.NEAISKU)
    kelias, priez = at.greiciausiai_pirminis([r"D:\x.jpg"])
    assert kelias == r"D:\x.jpg"


def test_visi_vardai_kopijos_nesugriauna_atrankos():
    """Jei VISI grupes failai vardu atrodo kopijos, 1 taisykle nieko
    neisskiria - darbas turi keliauti toliau, ne sustoti."""
    grupe = [r"D:\a\x (1).jpg", r"D:\a\b\c\x (2).jpg"]
    kelias, priez = at.greiciausiai_pirminis(grupe)
    assert kelias == r"D:\a\x (1).jpg"
    assert priez == at.PRIEZASTIS_GYLIS
