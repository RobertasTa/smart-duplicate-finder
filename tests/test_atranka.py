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
    # PASTABA 2026-08-24: cia TYCIA nera aplanko su zodziu "kopij" - nuo
    # aplanko taisykles atsiradimo toks kelias butu isspresta anksciau,
    # ir sitas testas tikrintu ne ta, ka teigia
    grupe = [r"D:\archyvas\foto.jpg",
             r"D:\archyvas\2020\senos\gilyn\foto.jpg"]
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


# --- Aplanko vardas (Roberto gyvas testas 2026-08-24) ----------------------

def test_aplanko_vardas_prisipazista():
    """"NAS medziaga kopija", "Atsargine kopija" - zmogus perskaito per
    sekunde; programa turi irgi."""
    assert at.aplankas_rodo_kopija(r"D:\t\NAS medziaga kopija\irankis.exe")
    assert at.aplankas_rodo_kopija(r"D:\t\Atsargine kopija\receptas.jfif")
    assert at.aplankas_rodo_kopija(r"D:\t\Backup\a.jpg")
    assert at.aplankas_rodo_kopija(r"D:\t\Kopie\a.jpg")


def test_aplanko_taisykle_NEklysta_su_normaliais():
    assert not at.aplankas_rodo_kopija(r"D:\t\Dokumentai\a.txt")
    assert not at.aplankas_rodo_kopija(r"D:\t\Nuotraukos\2025\a.jpg")
    # failo vardas su "copy" NEturi suveikti kaip APLANKO taisykle
    assert not at.aplankas_rodo_kopija(r"D:\t\foto\copy of a.jpg")


def test_kopiju_aplankas_isskiria_ir_paaiskina():
    grupe = [r"D:\t\NAS medziaga\irankis.exe",
             r"D:\t\NAS medziaga kopija\irankis.exe"]
    kelias, priez = at.greiciausiai_pirminis(grupe)
    assert kelias == r"D:\t\NAS medziaga\irankis.exe"
    assert priez == at.PRIEZASTIS_KOPIJU_APLANKAS


def test_failo_vardas_pirmesnis_uz_aplanka():
    """Failo vardas yra tikslesnis pozymis nei aplanko - jis pirmas."""
    grupe = [r"D:\t\Backup\svente.jpg", r"D:\t\foto\svente (1).jpg"]
    kelias, priez = at.greiciausiai_pirminis(grupe)
    assert kelias == r"D:\t\Backup\svente.jpg"
    assert priez == at.PRIEZASTIS_VARDAS


# --- Nekaltuju gynyba (2026-08-25) -----------------------------------------
# Sitie testai gime is patikros, kuri parode, kad 37 zali testai nesugavo
# dvieju vietu, kur ataskaita sakydavo netiesa. Abi klaidos vienodos:
# pozymio ieskota kaip POEILUTES, be zodzio ribos.

def test_vardas_NEklysta_su_zodziais_kurie_baigiasi_copy():
    """"Photocopy", "Hardcopy", "Recopy" NERA kopijos - "copy" ten yra
    zodzio dalis, ne Explorer'io uodega."""
    assert not at.vardas_rodo_kopija(r"C:\skenai\Photocopy.jpg")
    assert not at.vardas_rodo_kopija(r"C:\doc\Hardcopy.pdf")
    assert not at.vardas_rodo_kopija(r"C:\skenai\Recopy.txt")
    # o tikros uodegos turi likti pagaunamos
    assert at.vardas_rodo_kopija(r"C:\foto\planas copy 2.docx")
    assert at.vardas_rodo_kopija(r"C:\foto\planas_copy.docx")
    assert at.vardas_rodo_kopija(r"C:\foto\planas - Copy.docx")


def test_aplankas_NEklysta_su_zodziais_kuriuose_slypi_zyme():
    """"Copyright materials" turi "copy", "Mikroskopija" turi "kopij" -
    bet nei vienas nera kopiju aplankas."""
    assert not at.aplankas_rodo_kopija(r"D:\t\Copyright materials\a.txt")
    assert not at.aplankas_rodo_kopija(r"D:\mokslas\Mikroskopija\vaizdas.tif")
    # o tikri kopiju aplankai turi likti pagaunami
    assert at.aplankas_rodo_kopija(r"D:\t\Kopijos\a.jpg")
    assert at.aplankas_rodo_kopija(r"D:\t\Backup 2024\a.jpg")
    assert at.aplankas_rodo_kopija(r"D:\t\Copies\a.jpg")
    assert at.aplankas_rodo_kopija(r"D:\t\Kopien\a.jpg")


def test_kopiju_aplankai_veikia_ir_kirilica():
    """RU vartotojui "Kopii" / "Rezervnaja kopija" (rasoma kirilica) yra
    toks pat prisipazinimas kaip lietuviui "Kopijos".
    Patys vardai rasomi \\u escape'ais - sitas failas lieka ASCII, kaip
    reikalauja test_hygiene (jis mane cia ir pagavo 2026-08-25)."""
    assert at.aplankas_rodo_kopija("D:\\t\\\u041a\u043e\u043f\u0438\u0438\\a.jpg")
    assert at.aplankas_rodo_kopija(
        "D:\\t\\\u0420\u0435\u0437\u0435\u0440\u0432\u043d\u0430\u044f "
        "\u043a\u043e\u043f\u0438\u044f\\a.jpg")
    # "Mikroskopija" rusiskai - irgi neturi buti palaikyta kopija
    assert not at.aplankas_rodo_kopija(
        "D:\\t\\\u041c\u0438\u043a\u0440\u043e\u0441\u043a\u043e\u043f\u0438\u044f\\a.jpg")


def test_mikroskopijos_grupe_duoda_saziniga_neaisku():
    """Pilnas scenarijus: kai vienintelis "pozymis" buvo klaidingas,
    atsakymas turi buti "neaisku", o ne pasufleruotas ne tas failas."""
    grupe = [r"D:\mokslas\Mikroskopija\vaizdas.tif",
             r"D:\mokslas\archyvas\vaizdas.tif"]
    kelias, priez = at.greiciausiai_pirminis(grupe)
    assert kelias == ""
    assert priez == at.NEAISKU


def test_year_in_brackets_is_not_a_copy_number():
    """A four-digit number in brackets is a year, not a copy number.

    Explorer and browsers number copies as (1), (2), (3) - short. Names like
    "Report (2024).pdf" or "Budget (2026).xlsx" merely carry the year, and
    reading them as copies is the same mistake as reading "Photocopy.jpg"
    as a copy: the marking looked right but was not there.
    """
    for vardas in ("Ataskaita (2024).pdf", "Nuotrauka (2019).jpg",
                   "Biudzetas (2026).xlsx"):
        assert not at.vardas_rodo_kopija(vardas), vardas
    # short numbers stay copies
    for vardas in ("daina (1).mp3", "file (12).txt", "Kaina (100).xlsx"):
        assert at.vardas_rodo_kopija(vardas), vardas


def test_copy_suffix_stripping_covers_all_four_languages():
    """The suspects search must know copies in every language the app speaks.

    Windows names a copy "- Copy", "- kopija", "- kopiya" (Cyrillic) or
    "- Kopie" depending on its own language, and macOS uses "Copy of ...".
    Until 2026-08-26 only the first two were recognised - three pairs out of
    five slipped through unnoticed.
    """
    RU = "\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442"
    KOPIJA_RU = "\u043a\u043e\u043f\u0438\u044f"
    poros = [("report", "report - Copy"),
             ("ataskaita", "ataskaita - kopija"),
             (RU, RU + " - " + KOPIJA_RU),
             ("Bericht", "Bericht - Kopie"),
             ("plan", "Copy of plan"),
             ("file", "file (1)"),
             ("foto", "foto_copy")]
    for svarus, kopija in poros:
        assert at.be_kopijos_pozymio(kopija) == svarus, kopija
    # and names that only look like copies must be left alone
    for vardas in ("Photocopy", "Ataskaita (2024)", "daina (remix)", "1984"):
        assert at.be_kopijos_pozymio(vardas) == vardas, vardas
