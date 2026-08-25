"""
atranka.py - "Kuris is dubliu greiciausiai ORIGINALAS?" (v1.4)

KODEL SITAS MODULIS YRA:
Vartotoju noras Nr. 1 (VARTOTOJU_NORAI_dublikatams.md: trys nepriklausomi
saltiniai - dupeGuru #736/#312, Czkawka #1636, AlternativeTo). SDF iki siol
zmogui atiduodavo grupe be jokios uzuominos, kuris failas tos grupes senelis.

KUO SKIRIAMES NUO KONKURENTU (2026-08-24 Duplicate Cleaner 5.27 ardymas):
DC turi "Selection Assistant" - 57 veiksmus, kurie PAZYMI failus TRYNIMUI
pagal 7 kriterijus. Bet DC niekur nepasako, KODEL pazymejo butent ta faila.

!!! RIBA (Roberto priminimas 2026-08-24: "neisijausk") !!!
Sitas modulis NIEKO NESIULO TRINTI ir nieko nezymi salinimui. Jis tik
PASAKO, kuris grupes failas pagal pozymius atrodo esas SENELIS, ir KODEL
butent jis. Tai INFORMACIJA ataskaitos stulpelyje, ne nurodymas.
Sprendzia zmogus. Kai pozymiu nera - saziningai grazinam "neaisku",
o ne spejima. ("Find. Explain. Ask. Never guess.")

Atskirai isiminti: ZYMEJIMAS pacioje SDF (v1.5 tema) reiskia NE "sita
salinti", o atvirksciai - "sitie dubliai man REIKALINGI, laikau tycia".

TAISYKLIU TVARKA (pirma, kuri duoda aiskuma, ta ir lemia):
  1. Failo vardas        - "kopija (1).jpg", "file - Copy.txt" = KOPIJA
  2. Aplanko vardas      - "NAS medziaga kopija", "Atsargine kopija"
  3. Laikinas aplankas   - Downloads/Temp/Cache = greiciau kopija
  4. Kelio gylis         - seklesnis kelias = greiciau originalas
  5. Senesnis mtime      - senesnis = greiciau originalas
Ne viena netiko -> ("", NEAISKU). Spejimo neisradinejam.

Modulis GRYNAS: neliecia disko (mtime paduodamas is isores), nieko netrina,
nieko neraso. Tik skaiciuoja ir paaiskina.
"""
import os
import re

# --- 1 taisykle: vardo pozymiai -------------------------------------------
# Windows/Explorer, narsykles ir failu tvarkykles prideda savo uodegas.
# Raktas: pozymis turi buti PABAIGOJE (pries pletini), kad "Copyright.txt"
# ar "1984.txt" nebutu palaikyti kopijomis.
_KOPIJOS_UODEGOS = [
    r"\s*\(\d+\)$",              # nuotrauka (1).jpg   <- Explorer, Chrome
    r"\s*-\s*[Cc]opy$",          # file - Copy.txt     <- Explorer EN
    r"\s*-\s*[Kk]opija$",        # file - kopija.txt   <- Explorer LT
    # "file - kopija.txt" rusiskai. Kirilica rasoma \u escape'ais TYCIA:
    # higienos sargas (test_hygiene) draudzia kirilica visur, isskyrus
    # kalba_ru.py - o sitas failas turi likti ASCII.
    "\\s*-\\s*[\u041a\u043a]\u043e\u043f\u0438\u044f$",   # "[Kk]opija" rusiskai
    r"\s*-\s*[Kk]opie$",         # file - Kopie.txt    <- Explorer DE
    r"_[Cc]opy$",
    r"_[Kk]opija$",
    # PATAISA 2026-08-25: buvo r"\s*copy\s*\d*$" - o \s* leidzia NULI tarpu,
    # tad kopija tapdavo bet koks zodis, kuris tiesiog BAIGIASI "copy":
    # "Photocopy.jpg", "Hardcopy.pdf", "Recopy.txt". Dabar pries "copy"
    # privalo buti riba - vardo pradzia, tarpas, bruksnys ar pabraukimas.
    r"(?:^|[\s\-_])[Cc]opy\s*\d*$",   # file copy 2.txt  <- macOS/rankinis
    # NE raw string: raw'e \u escape neveiktu ir ieskotume teksto "\u2014"
    "\\s*\u2014\\s*copy$",       # file - copy.txt su ilguoju bruksniu
]
_KOPIJOS_PRIESDELIAI = [
    r"^[Cc]opy of\s+",           # Copy of file.txt
    r"^[Kk]opija\s+-\s+",
]
_UODEGOS_RE = [re.compile(p) for p in _KOPIJOS_UODEGOS]
_PRIESDELIU_RE = [re.compile(p) for p in _KOPIJOS_PRIESDELIAI]


def vardas_rodo_kopija(kelias):
    """True, jei failo VARDAS pats prisipazista esas kopija."""
    saknis = os.path.splitext(os.path.basename(kelias))[0]
    for r in _UODEGOS_RE:
        if r.search(saknis):
            return True
    for r in _PRIESDELIU_RE:
        if r.search(saknis):
            return True
    return False


# --- 2 taisykle: aplanko vardas prisipazista ------------------------------
# Roberto gyvas testas 2026-08-24: "NAS medziaga kopija\irankis.exe" ir
# "Atsargine kopija\receptas.jfif" - zmogus perskaito per sekunde, o
# programa graibstesi silpniausiu taisykliu, nes tikrino TIK failo varda.
# Aplanku vardai kelyje yra toks pat prisipazinimas kaip failo vardas.
#
# PATAISA 2026-08-25: cia buvo paprasta poeiluciu paieska ("kopij" in vardas),
# ir ji apkaltindavo nekaltus aplankus - "Copyright materials" (nes turi
# "copy") ir "Mikroskopija" (nes turi "kopij"). Ta pati klaida, nuo kurios
# 3 taisykle jau buvo apsaugota ("Templates" nera "temp"), tik cia liko
# nepataisyta. Dabar zyme turi buti ATSKIRAS ZODIS (\b riba is abieju pusiu),
# o galunes leidziamos: "kopija", "kopijos", "kopiju", "copies", "backups".
# Saziningai pripazistam ka PRARANDAM: "Fotokopijos" nebebus atpazintas.
# Tokia kryptis pasirinkta tycia - modulio doktrina sako, kad geriau
# nieko nepasakyti, nei apkaltinti nekalta ("Never guess").
_KOPIJU_APLANKU_RE = re.compile(
    r"\b("
    r"kopij\w*"                   # kopija, kopijos, kopiju, "NAS medziaga kopija"
    r"|copy|copies"
    r"|backup|backups"
    r"|kopie|kopien"              # DE
    # Kirilica - \u escape'ais, kad sitas failas liktu ASCII (zr. 1 taisykle)
    r"|\u043a\u043e\u043f\u0438\w*"          # RU "kopi(ja/i)"
    r"|\u0440\u0435\u0437\u0435\u0440\u0432\w*"   # RU "rezerv(as/naja)"
    r")\b",
    re.UNICODE,
)


def aplankas_rodo_kopija(kelias):
    """True, jei bent vienas aplankas kelyje vadinasi kopiju aplanku.
    Tikrinam TIK aplankus, ne pati faila - failo varda tvarko 1 taisykle."""
    dalys = os.path.normpath(kelias).replace("/", "\\").split("\\")[:-1]
    for aplankas in dalys:
        if _KOPIJU_APLANKU_RE.search(aplankas.lower()):
            return True
    return False


# --- 3 taisykle: laikini aplankai -----------------------------------------
# Aplankai, kuriuose failas gyvena "pakeliui", o ne namie.
_LAIKINI = (
    "downloads", "atsisiuntimai", "\u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438",
    "temp", "tmp", "laikini",
    "cache", "kesas",
    "$recycle.bin", "recycler", "siuksliadeze",
    "appdata\\local\\temp",
    "windows\\temp",
)


def laikinas_aplankas(kelias):
    """True, jei kelyje yra bent vienas 'pakeliui' aplankas.
    Lyginam PILNUS kelio segmentus, ne poeilutes - kitaip 'Templates'
    virstu 'temp', o 'MyDownloadsBackup' - 'downloads'."""
    z = os.path.normpath(kelias).lower()
    segmentai = set(z.replace("/", "\\").split("\\"))
    for zyme in _LAIKINI:
        if "\\" in zyme:
            if zyme in z:
                return True
        elif zyme in segmentai:
            return True
    return False


# --- Priezasciu kodai (i teksta verciami kalba.py, ne cia) ----------------
PRIEZASTIS_VARDAS = "vardas"        # kiti grupes failai vardu prisipazino
PRIEZASTIS_KOPIJU_APLANKAS = "kopiju_aplankas"  # kiti guli kopiju aplanke
PRIEZASTIS_APLANKAS = "aplankas"    # kiti guli laikinuose aplankuose
PRIEZASTIS_GYLIS = "gylis"          # sekliausias kelias
PRIEZASTIS_DATA = "data"            # seniausias
NEAISKU = "neaisku"                 # pozymiu nera - nespejam

# Grupes lygio ispejimas (Duplicate Cleaner "warning all marked" atitikmuo,
# perverstas i musu kalba: mes netrinam, bet zmogus ataskaita skaito ir
# trina rankomis - jei VISOS kopijos laikinos, jam verta tai pasakyti)
ZYME_VISI_LAIKINI = "visi_laikini"


def _gylis(kelias):
    return len(os.path.normpath(kelias).replace("/", "\\").split("\\"))


def greiciausiai_pirminis(grupe, mtimes=None):
    """Kuris grupes failas pagal pozymius atrodo esas PIRMINIS (senelis).
    Vardas sako, ka funkcija daro: ji SPEJA IR PAAISKINA, o ne nurodo.

    grupe   - failu keliu sarasas (>=2)
    mtimes  - {kelias: mtime} arba None (tada 4 taisykle praleidziama;
              disko neliecia PATS modulis - datas paduoda kvieciantysis)

    Grazina (kelias, priezasties_kodas). Nieko neaisku -> ("", NEAISKU).
    """
    if not grupe:
        return "", NEAISKU
    if len(grupe) == 1:
        return grupe[0], NEAISKU

    # 1. Vardas. Jei DALIS failu prisipazino kopijomis - likusieji laimi.
    nekopijos = [p for p in grupe if not vardas_rodo_kopija(p)]
    if len(nekopijos) == 1:
        return nekopijos[0], PRIEZASTIS_VARDAS
    kandidatai = nekopijos if nekopijos else list(grupe)

    # 2. Aplanko vardas. "NAS medziaga kopija", "Atsargine kopija" - toks
    #    pat prisipazinimas kaip failo vardas, tik vienu lygiu auksciau.
    ne_kopiju_aplanke = [p for p in kandidatai if not aplankas_rodo_kopija(p)]
    if len(ne_kopiju_aplanke) == 1:
        return ne_kopiju_aplanke[0], PRIEZASTIS_KOPIJU_APLANKAS
    if ne_kopiju_aplanke:
        kandidatai = ne_kopiju_aplanke

    # 3. Laikinas aplankas. Ta pati logika: jei lieka lygiai vienas "namie".
    namie = [p for p in kandidatai if not laikinas_aplankas(p)]
    if len(namie) == 1:
        return namie[0], PRIEZASTIS_APLANKAS
    if namie:
        kandidatai = namie

    # 4. Kelio gylis. Tik jei sekliausias yra VIENAS - kitaip neaisku.
    gyliai = [(_gylis(p), p) for p in kandidatai]
    min_gylis = min(g for g, _ in gyliai)
    sekliausi = [p for g, p in gyliai if g == min_gylis]
    if len(sekliausi) == 1:
        return sekliausi[0], PRIEZASTIS_GYLIS
    kandidatai = sekliausi

    # 5. Data. Be mtimes nespejam.
    if mtimes:
        turintys = [(mtimes[p], p) for p in kandidatai if p in mtimes]
        if turintys:
            min_data = min(d for d, _ in turintys)
            seniausi = [p for d, p in turintys if d == min_data]
            if len(seniausi) == 1:
                return seniausi[0], PRIEZASTIS_DATA

    return "", NEAISKU


def grupes_zymes(grupe):
    """Grupes lygio ispejimai. Grazina kodu sarasa (dazniausiai tuscia)."""
    zymes = []
    if grupe and all(laikinas_aplankas(p) for p in grupe):
        zymes.append(ZYME_VISI_LAIKINI)
    return zymes
