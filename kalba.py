"""
kalba.py - GUI kalbos sluoksnis (2026-08-05, versija draugui Odesoje).
Lietuviskas tekstas = zodyno raktas; t() grazina vertima arba pati rakta.
Kalba parenkama: exe su isiutu lang_en.flag failu -> EN; kitaip pagal
SDF_LANG aplinkos kintamaji; kitaip LT. Zero Qt priklausomybiu.
"""
import os
import sys
from pathlib import Path


def _base():
    return Path(getattr(sys, "_MEIPASS", str(Path(__file__).resolve().parent)))


if (_base() / "lang_en.flag").exists() or os.environ.get("SDF_LANG") == "en":
    LANG = "en"
else:
    LANG = "lt"

_EN = {
    # main_window: mygtukai, antrastes, statusai
    "Duplicate Finder": "Duplicate Finder",
    "+   Prideti katalogus": "+   Add folders",
    "-   Pasalinti pasirinktus": "-   Remove selected",
    ">>> Skenuoti": ">>> Scan",
    "Eksportuoti ataskaita": "Export report",
    "Salinti siuksles": "Clean junk files",
    "Ivriniti katalogai:": "Folders to scan:",
    "Rezultatai:": "Results:",
    "Failo vardas": "File name",
    "Pilnas kelias": "Full path",
    "Dydis (MB)": "Size (MB)",
    "Sukurimo data": "Created",
    "Grupe": "Group",
    "Pasiirenges": "Ready",
    "Prideti katalogus ir spauskite 'Skelnuoti'.": "Add folders and press 'Scan'.",
    "Pirma prideti bent viena kataloga.": "Add at least one folder first.",
    "Zvalgyba: renkami failu dydziai...": "Recon: collecting file sizes...",
    "Gilus tikrinimas (MD5 pagal turini)...": "Deep check (MD5 by content)...",
    "Skenavimas atsauktas.": "Scan cancelled.",
    "Nepazymeta ne viena seima - skenavimas atsauktas.":
        "No family selected - scan cancelled.",
    "Vyksta skenavimas": "Scanning",
    "Formuojama ataskaita": "Building report",
    "Salinamos siuksles": "Cleaning junk",
    "Pirma atlikti skana.": "Run a scan first.",
    "Exportuojama...": "Exporting...",
    "Eksportas atsauktas.": "Export cancelled.",
    "Kur issaugoti ataskaita?": "Where to save the report?",
    "Excel failai (*.xlsx)": "Excel files (*.xlsx)",
    "Eksportas sekmingas": "Export finished",
    "Ataskaita sukurta:": "Report created:",
    "Failas neberastas:": "File no longer exists:",
    "Klaida:": "Error:",
    "Exporto klaida:": "Export error:",
    "veikia": "running",
    # skeno santrauka
    "Skeniruota {n} failu is {k} katalogu - {g} dublikatu grupes, {mb:.2f} MB":
        "Scanned {n} files in {k} folder(s) - {g} duplicate groups, {mb:.2f} MB",
    "; praleista {n} nepasiekiamu failu": "; {n} unreadable files skipped",
    "Dubliu kandidatu nerasta ({n} failu perziureta{skip}).":
        "No duplicate candidates found ({n} files checked{skip}).",
    ", {n} praleista": ", {n} skipped",
    # skeno atmintis
    "Ankstesnio skeno rezultatai": "Previous scan results",
    "Rasti ankstesnio skeno rezultatai ({kada}, {n} dubliu grupiu).\nIkelti be pakartotinio skenavimo?":
        "Previous scan results found ({kada}, {n} duplicate groups).\nLoad them without re-scanning?",
    "Ikelti {kada} skeno rezultatai: {g} dublikatu grupes, {mb:.2f} MB (galima eksportuoti be skenavimo)":
        "Loaded scan results from {kada}: {g} duplicate groups, {mb:.2f} MB (export available without scanning)",
    "Keso ikelti nepavyko - skenuok is naujo.": "Could not load cache - scan again.",
    # siuksles
    "Siuksliu nerasta - pirma atlik zvalgyba.": "No junk found - run a scan first.",
    "Salinti Windows/Mac siuksles?": "Delete Windows/Mac junk files?",
    "Rasta {n} sistemos siuksliu ({mb:.1f} MB):": "Found {n} system junk files ({mb:.1f} MB):",
    "Tai miniaturu/narsymo kesai - OS juos atsikuria pati.\nPries trynima kiekvienam failui tikrinamas turinio parasas;\nneatitinkantys NEBUS trinami.\n\nDEMESIO: tinklo diskuose (NAS) trynimas negriztamas\n(siuksliadeze ten neveikia). Trinti?":
        "These are thumbnail/browsing caches - the OS recreates them.\nBefore deletion every file's content signature is verified;\nnon-matching files will NOT be deleted.\n\nWARNING: on network drives (NAS) deletion is permanent\n(no recycle bin there). Delete?",
    "Siuksliu salinimas atsauktas.": "Junk cleanup cancelled.",
    "Istrinta {n} siuksliu, atlaisvinta {mb:.1f} MB":
        "Deleted {n} junk files, freed {mb:.1f} MB",
    "; praleista {n} (parasas nesutapo arba failas uzrakintas)":
        "; {n} skipped (signature mismatch or file locked)",
    # select_dialog
    "Rasti kandidatai i dublius": "Duplicate candidates found",
    "Vienodo dydzio failu grupes (kandidatai). Pazymekite,\nkurias seimas tikrinti giliai (MD5 pagal turini):":
        "Groups of same-size files (candidates). Tick the\nfamilies to deep-check (MD5 by content):",
    "Seima": "Family",
    "Grupiu": "Groups",
    "Failu": "Files",
    "Apimtis": "Volume",
    "~Laikas": "~Time",
    "Tikrinti pazymetus": "Check selected",
    "Atsaukti": "Cancel",
    "Is viso pazymejus viska: {mb} skaitymo, {t} (disko greitis ~{v} MB/s)":
        "All selected: {mb} to read, {t} (disk speed ~{v} MB/s)",
    "akimirka": "instant",
    # add_dialog
    "Prideti katalogus": "Add folders",
    "Iklijuokite kelius is Explorer (Ctrl+V) arba pasirinkite paspausdami mygtuka:":
        "Paste paths from Explorer (Ctrl+V) or pick with the button:",
    "C:\\Ap1\nD:\\Ap2\nF:\\Ap3  (kiekvienas - naujoje eiluteje)":
        "C:\\Folder1\nD:\\Folder2\nF:\\Folder3  (one per line)",
    "Pasirinkti katalogus": "Browse folders",
    "Pasirinkti kataloga": "Pick a folder",
    "Prideti": "Add",
    "Atstatyti": "Cancel",
    # table_populator / worker
    "Grupe {idx}": "Group {idx}",
    "ITARINI": "SUSPECT",
    "ITARTINI (panasus, bet ne identiski)": "SUSPICIOUS (similar, but not identical)",
    "Rodoma {n} eiluciu (didziausios grupes virsuje) - PILNAS sarasas Excel ataskaitoje":
        "Showing {n} rows (largest groups on top) - FULL list in the Excel report",
    "Zvalgyba: {n} failu...": "Recon: {n} files...",
    "Panasios nuotraukos (vizualiai)": "Similar photos (visual)",
    "VIZUALIAI PANASUS (skirtinga rezoliucija/kokybe)":
        "VISUALLY SIMILAR (different resolution/quality)",
    "Vaizdas {idx}": "Image {idx}",
    "Vizualus lyginimas: {a}/{b} nuotrauku": "Visual compare: {a}/{b} photos",
    "; vizualiai panasiu grupiu: {n}": "; visually similar groups: {n}",
    "ITARTINI paieska: {a}/{b} failu": "Suspicious search: {a}/{b} files",
    "Salinamos siuksles: {a}/{b}": "Cleaning junk: {a}/{b}",
    "{f}/{ft} failu": "{f}/{ft} files",
    "liko": "left",
}

_FAM_EN = {
    "Paveiksliukai": "Pictures", "Video": "Video", "Audio": "Audio",
    "Dokumentai": "Documents", "Archyvai": "Archives", "CAD": "CAD",
    "Kodas": "Code", "Programos": "Programs", "Kita": "Other",
}


def t(raktas):
    """Vertimas: LT rezime grazina rakta, EN - vertima (arba rakta, jei nera)."""
    if LANG == "en":
        return _EN.get(raktas, raktas)
    return raktas


def fam(seima):
    """Seimos pavadinimas rodymui (vidiniai raktai visada lietuviski)."""
    if LANG == "en":
        return _FAM_EN.get(seima, seima)
    return seima
