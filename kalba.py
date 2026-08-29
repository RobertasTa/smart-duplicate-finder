"""
kalba.py - GUI kalbos sluoksnis (2026-08-05, versija draugui Odesoje).
Lietuviskas tekstas = zodyno raktas; t() grazina vertima arba pati rakta.

Kalbos parinkimo prioritetai (2026-08-06, Roberto pastaba "du exe del
kalbos - negrazu"; dabar VIENAS exe su pasirinkimu GUI):
  1. SDF_LANG aplinkos kintamasis (testu izoliacija / prievarta)
  2. kalba.txt darbiniu failu kataloge (GUI combobox pasirinkimas;
     portable rezime keliauja su flesiuku kartu su SDF_portable.txt)
  3. lang_en.flag salia exe (senoji -en buildu veliavele, suderinamumas)
  4. OS kalba (Roberto 2026-08-06 "vienas exe visom kalbom"): lietuviska
     sistema -> LT, kitaip -> EN. Nauja kalba ateityje = zodynas + eilute
     combobox'e.
Zero Qt priklausomybiu.
"""
import os
import sys
from pathlib import Path


def _base():
    return Path(getattr(sys, "_MEIPASS", str(Path(__file__).resolve().parent)))


def _issaugota_kalba():
    """Skaito GUI pasirinkima is kalba.txt (saugyklos data_dir)."""
    try:
        import saugykla
        # v1.4: kalba gali dar guleti sename bendrame _darbal - persikeliam
        # PIRMA, kitaip pirmas paleidimas grizdavo i numatyta kalba
        saugykla.migruoti_sena_darbal()
        v = (saugykla.data_dir() / saugykla.KALBOS_FAILAS).read_text(
            encoding="utf-8").strip().lower()
        return v if v in ("lt", "en", "ru", "de") else None
    except OSError:
        return None


def issaugoti_kalba(lang):
    """Iraso pasirinkima i kalba.txt; isigalioja perleidus programa.
    Meta OSError, jei irasyti nepavyko (pvz., read-only vieta)."""
    import saugykla
    d = saugykla.data_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / saugykla.KALBOS_FAILAS).write_text(lang + "\n", encoding="utf-8")


def _os_kalba():
    """OS kalbos aptikimas pirmam paleidimui: lietuviska sistema -> lt."""
    try:
        import ctypes
        langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        if (langid & 0x3FF) == 0x27:   # LANG_LITHUANIAN
            return "lt"
        return "en"
    except Exception:
        pass
    try:
        import locale
        loc = locale.getlocale()[0] or ""
        return "lt" if loc.lower().startswith("lt") else "en"
    except Exception:
        return "en"


_env = os.environ.get("SDF_LANG")
if _env in ("lt", "en", "ru", "de"):
    LANG = _env
else:
    LANG = _issaugota_kalba() or (
        "en" if (_base() / "lang_en.flag").exists() else _os_kalba())

_EN = {
    # main_window: mygtukai, antrastes, statusai
    "Duplicate Finder": "Duplicate Finder",
    "+   Prideti katalogus": "+   Add folders",
    "-   Pasalinti pasirinktus": "-   Remove selected",
    ">>> Skenuoti": ">>> Scan",
    "Eksportuoti ataskaita": "Export report",
    # 2026-08-25: buvo "Clean junk files" - salia pazado "never deletes"
    # skambejo taip, lyg trintu vartotojo radinius (GPT pastaba 08-14,
    # Roberto sprendimas B+C). "OS" pasako, kieno tai siuksles.
    "Salinti OS siuksles": "Clean OS junk files",
    "Windows ir Mac miniatiuru kesai: Thumbs.db, ehthumbs.db,\n"
    ".DS_Store. Jusu failu neliecia. Pries trynima tikrinamas\n"
    "kiekvieno failo turinio parasas - neatitinkantys lieka.":
        "Windows and Mac thumbnail caches: Thumbs.db, ehthumbs.db,\n"
        ".DS_Store. Your own files are never touched. Each file's\n"
        "content signature is checked first - mismatches are kept.",
    "Itraukti katalogai:": "Folders to scan:",
    "Rezultatai:": "Results:",
    "Failo vardas": "File name",
    "Pilnas kelias": "Full path",
    "Dydis (MB)": "Size (MB)",
    "Sukurimo data": "Created",
    "Grupe": "Group",
    # v1.4 - "Kuris cia pirminis?" ataskaitos skiltys. Tai INFORMACIJA,
    # ne nurodymas: programa netrina nieko ir nesiulo trinti.
    "Greiciausiai pirminis": "Most likely the original",
    "Pastaba": "Note",
    "mazesnes raiskos nei kiti grupeje": "a lower resolution than the rest",
    "kita orientacija nei kiti grupeje - patikrinkite, ar taip ir turi buti":
        "a different orientation from the rest - check whether it is meant to be",
    "Kodel": "Why",
    "kiti grupeje vardu pazymeti kaip kopijos": "the others are named as copies",
    "kiti guli kopiju aplankuose": "the others sit in copy folders",
    "kiti guli laikinuose aplankuose": "the others sit in temporary folders",
    "kiti guli giliau aplankuose": "the others sit deeper in folders",
    "kiti sukurti veliau": "the others were created later",
    "neaisku - pozymiu nera": "unclear - nothing tells them apart",
    "visos kopijos laikinuose aplankuose":
        "every copy here is in a temporary folder",
    # v1.4 "Ar yra naujesne versija?" langelis (Roberto ideja 2026-08-24).
    # Programa tinklo NELIECIA - tik paaiskina, kaip pasiziureti paciam.
    "Ar yra naujesne versija?": "Is there a newer version?",
    "Jusu versija: {v}": "Your version: {v}",
    "Ar yra naujesne? Trys keliai:": "Is there a newer one? Three ways:",
    "1. Naujienu puslapyje matysite naujausia versija:":
        "1. The releases page shows the latest version:",
    "Atidaryti naujienu puslapi": "Open the releases page",
    "2. Jei diegete per winget - spauskite Win+R, irasykite cmd,\n"
    "   spauskite Enter ir iklijuokite:":
        "2. If you installed via winget - press Win+R, type cmd,\n"
        "   press Enter and paste:",
    "Kopijuoti komanda": "Copy the command",
    "Komanda nukopijuota": "Command copied",
    # 2026-08-25: raktas pakeistas - senasis siunte prie mygtuko "Klausk DI",
    # kurio tokiu vardu ekrane nera; dabar dialoge yra pats mygtukas
    "3. Arba paprasykite DI konsultanto - jis pats\n"
    "   pasitikrins ir pasakys, ko jums truksta:":
        "3. Or ask an AI assistant - it will check for you\n"
        "   and tell you what you are missing:",
    "Programa pati interneto neliecia. Sprendziate jus.":
        "The app itself never touches the internet. You decide.",
    "Pasirenges": "Ready",
    "Prideti katalogus ir spauskite 'Skenuoti'.": "Add folders and press 'Scan'.",
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
    # portable rezimas ir kalba (2026-08-06)
    "Portable rezimas": "Portable mode",
    "Kalba": "Language",
    "Kalba pritaikoma paleidus programa is naujo.":
        "The language is applied after restarting the app.",
    "Kalba pasikeis paleidus programa is naujo.":
        "The language will change after you restart the app.",
    "Kalba issaugota. Perleisti programa dabar?":
        "Language saved. Restart the app now?",
    "Nepavyko issaugoti: {}": "Could not save: {}",
    "Ijungta: kesas ir zurnalas saugomi salia programos (pvz., flesiuke) - kompiuteryje pedsaku nelieka.\nIsjungta (numatyta): saugoma vartotojo kataloge %LOCALAPPDATA%\\SmartDuplicateFinder.":
        "On: the cache and log are stored next to the app (e.g. on a USB stick) - no traces left on the computer.\nOff (default): stored in the user profile at %LOCALAPPDATA%\\SmartDuplicateFinder.",
    "Nepavyko perjungti rezimo: {}": "Could not switch mode: {}",
    "Portable rezimas IJUNGTAS - duomenys salia programos":
        "Portable mode ON - data lives next to the app",
    "Portable rezimas isjungtas - duomenys vartotojo kataloge":
        "Portable mode off - data lives in the user profile",
    # skeno santrauka
    "Perziureta failu: {n}, katalogu: {k} - dublikatu grupiu: {g}, {mb:.2f} MB":
        "Files scanned: {n}, folders: {k} - duplicate groups: {g}, {mb:.2f} MB",
    "Perziureta failu: {n}, katalogu: {k} - dublikatu grupiu: {g}; dubliai uzima {mb:.2f} MB, atlaisvinti galima {fmb:.2f} MB":
        "Files scanned: {n}, folders: {k} - duplicate groups: {g}; duplicates take {mb:.2f} MB, {fmb:.2f} MB can be freed",
    "; ITARTINI sarasas nukirptas ties {n} poru riba (susiaurink katalogus, jei nori visu)":
        "; SUSPICIOUS list truncated at the {n}-pair limit (narrow the folders to see all)",
    "; {n} failu ITARTINI patikroje praleista - per daug vienodo vardo failu vienoje vietoje (susiaurink katalogus)":
        "; {n} files skipped in the SUSPICIOUS check - too many same-name files in one place (narrow the folders)",
    "; {n} nuotrauku nepavyko atverti (sugadintos, nezinomo formato arba per didzuliu)":
        "; {n} pictures could not be opened (damaged, unknown format or enormous)",
    "; {n} nuotrauku liko nepalygintos - per daug panasiu vienoje vietoje (susiaurink katalogus)":
        "; {n} pictures were left uncompared - too many look-alikes in one place (narrow the folders)",
    "; nepasiekiamu failu praleista: {n}": "; unreadable files skipped: {n}",
    "Dubliu kandidatu nerasta (perziureta failu: {n}{skip}).":
        "No duplicate candidates found (files checked: {n}{skip}).",
    ", {n} praleista": ", {n} skipped",
    # skeno atmintis
    "Ankstesnio skeno rezultatai": "Previous scan results",
    "Rasti ankstesnio skeno rezultatai ({kada}; dubliu grupiu: {n}).\nIkelti be pakartotinio skenavimo?":
        "Previous scan results found ({kada}; duplicate groups: {n}).\nLoad them without re-scanning?",
    "Ikelti {kada} skeno rezultatai - dublikatu grupiu: {g}, {mb:.2f} MB (galima eksportuoti be skenavimo)":
        "Loaded scan results from {kada} - duplicate groups: {g}, {mb:.2f} MB (export available without scanning)",
    "Keso ikelti nepavyko - skenuok is naujo.": "Could not load cache - scan again.",
    # siuksles
    "Siuksliu nerasta - pirma atlik zvalgyba.": "No junk found - run a scan first.",
    "Salinti Windows/Mac siuksles?": "Delete Windows/Mac junk files?",
    "Sistemos siuksliu rasta: {n} ({mb:.1f} MB):": "System junk found: {n} ({mb:.1f} MB):",
    "Tai miniaturu/narsymo kesai - OS juos atsikuria pati.\nPries trynima kiekvienam failui tikrinamas turinio parasas;\nneatitinkantys NEBUS trinami.\n\nDEMESIO: tinklo diskuose (NAS) trynimas negriztamas\n(siuksliadeze ten neveikia). Trinti?":
        "These are thumbnail/browsing caches - the OS recreates them.\nBefore deletion every file's content signature is verified;\nnon-matching files will NOT be deleted.\n\nWARNING: on network drives (NAS) deletion is permanent\n(no recycle bin there). Delete?",
    "Siuksliu salinimas atsauktas.": "Junk cleanup cancelled.",
    "Siuksliu istrinta: {n}, atlaisvinta {mb:.1f} MB":
        "Junk files deleted: {n}, freed {mb:.1f} MB",
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
    # Excel ataskaita (2026-08-06, lapu pavadinimai ir antrastes pagal kalba)
    "Dublikatai": "Duplicates",
    "Panasios nuotraukos": "Similar Images",
    "Itartini": "Suspects",
    "Itartinas {n}": "Suspect {n}",
    "RODOMA {a} IS {b} EILUCIU - virsyta Excel lapo riba (1 048 576)":
        "SHOWING {a} OF {b} ROWS - Excel sheet limit exceeded (1,048,576)",
    "DALIS {k} IS {n} - eiluciu daugiau nei telpa viename Excel faile, ataskaita padalinta i {n} failus":
        "PART {k} OF {n} - more rows than one Excel file can hold, the report is split into {n} files",
    "Ataskaita padalinta i {n} failus (-1, -2, ...) - eiluciu daugiau nei telpa viename Excel faile":
        "The report was split into {n} files (-1, -2, ...) - more rows than one Excel file can hold",
    "ITARINI": "SUSPECT",
    "ITARTINI (panasus, bet ne identiski)": "SUSPICIOUS (similar, but not identical)",
    "Rodoma eiluciu: {n} (didziausios grupes virsuje) - PILNAS sarasas Excel ataskaitoje":
        "Showing {n} rows (largest groups on top) - FULL list in the Excel report",
    "Zvalgyba - failu: {n}...": "Recon - files: {n}...",
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
    # v1.3 desinio klaviso meniu rezultatu lenteleje (2026-08-22)
    "Atidaryti faila": "Open file",
    "Atidaryti kataloga": "Open folder",
    "Kopijuoti kelia": "Copy path",
    "Kelias nukopijuotas": "Path copied",
    # pagalbos "?" kampelis (2026-08-07, Roberto ideja: winget/Store
    # vartotojas readme negauna - instrukcija gyvena pacioje programoje)
    "Pagalba": "Help",
    "Apie...": "About...",
    "Instrukcija": "User guide",
    # "Klausk DI" (Roberto ideja 2026-08-08; receptas is FOTO namu -
    # pats promptas anglu k. kodo konstanta, ne zodyno irasas)
    "Neradote atsakymo? Klauskite DI": "No answer here? Ask the AI",
    "Kas ivyks paspaudus OK:\n\n"
    "1. Atsidarys interneto narsykle su DI padejejo\n"
    "   claude.ai puslapiu. Zinutes laukelyje jau bus\n"
    "   irasyta angliska pradzia - prisistatymas, kas per\n"
    "   programa ir kur jos kodas.\n"
    "2. NEISSIGASKITE raudono pranesimo virs zinutes -\n"
    "   claude.ai ji rodo visada, kai tekstas ateina per\n"
    "   nuoroda. Tai tik priminimas perskaityti, kas\n"
    "   siunciama.\n"
    "3. Zinutes gale, po zodziu \"My question:\", irasykite\n"
    "   SAVO klausima - galima lietuviskai! - ir spauskite\n"
    "   siuntimo mygtuka (rodykle). Klausti galima visko,\n"
    "   pvz.: \"kaip atsinaujinti programa i naujesne\n"
    "   versija? paaiskink zingsnis po zingsnio\".\n"
    "4. Jei DI atsakys angliskai - tiesiog paprasykite kita\n"
    "   zinute: \"atsakyk lietuviskai\", ir toliau bendraus\n"
    "   lietuviskai.\n\n"
    "Pastaba: claude.ai gali paprasyti prisijungti (nemokama\n"
    "paskyra). Niekas neissiunciama be jusu rankos.":
        "What happens after you press OK:\n\n"
        "1. Your web browser opens the claude.ai AI assistant.\n"
        "   The message box will already contain a prepared\n"
        "   opening - what the program is and where its code is.\n"
        "2. DO NOT be alarmed by the red notice above the\n"
        "   message - claude.ai always shows it when text\n"
        "   arrives via a link. It is just a reminder to read\n"
        "   what you are sending.\n"
        "3. At the end of the message, after \"My question:\",\n"
        "   TYPE YOUR question - any language works! - and\n"
        "   press the send button (the arrow). Ask anything,\n"
        "   e.g.: \"how do I update the app to the newest\n"
        "   version? explain it step by step\".\n"
        "4. If the AI answers in the wrong language - just ask\n"
        "   in the next message, e.g. \"answer in English\".\n\n"
        "Note: claude.ai may ask you to sign in (a free account).\n"
        "Nothing is sent without your hand.",
    "Nepavyko atidaryti: {}": "Could not open: {}",
    "Apie programa": "About",
    "Dubliuotu failu paieska pagal turini - nieko netrina.":
        "Finds duplicate files by content - never deletes anything.",
    "Versija {v}": "Version {v}",
    "Kurejo puslapis:": "Project page:",
}

_FAM_EN = {
    "Paveiksliukai": "Pictures", "Video": "Video", "Audio": "Audio",
    "Dokumentai": "Documents", "Archyvai": "Archives", "CAD": "CAD",
    "Kodas": "Code", "Programos": "Programs", "Kita": "Other",
}


# v1.3 (2026-08-22): RU/DE/LT zodynai gyvena atskiruose moduliuose,
# kad kalba.py liktu skaitomas. Trukstamo rakto atsarga RU/DE rezime -
# EN vertimas (suprantamesnis uz lietuviska rakta), tada pats raktas.
# LT zodynas (Roberto pastaba is gyvo v1.3 testo) - taisyklingos
# lietuviskos raides rodymui; raktai kode lieka ASCII.
from kalba_ru import _RU, _FAM_RU
from kalba_de import _DE, _FAM_DE
from kalba_lt import _LT

_ZODYNAI = {"lt": _LT, "en": _EN, "ru": _RU, "de": _DE}
_FAM_ZODYNAI = {"en": _FAM_EN, "ru": _FAM_RU, "de": _FAM_DE}


def t(raktas):
    """Vertimas: kiekviena kalba turi zodyna (LT - diakritiku sluoksni).
    Trukstamam raktui: RU/DE krenta i EN, LT ir EN - i pati rakta."""
    z = _ZODYNAI.get(LANG)
    if z is None:
        return raktas
    v = z.get(raktas)
    if v is None and LANG in ("ru", "de"):
        v = _EN.get(raktas)
    return v if v is not None else raktas


def fam(seima):
    """Seimos pavadinimas rodymui (vidiniai raktai visada lietuviski)."""
    z = _FAM_ZODYNAI.get(LANG)
    if z is None:
        return seima
    v = z.get(seima)
    if v is None and LANG != "en":
        v = _FAM_EN.get(seima)
    return v if v is not None else seima
