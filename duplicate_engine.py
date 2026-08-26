# duplicate_engine.py - core scan + duplicate detection, zero Qt imports
import hashlib
import json
import os
import re
import stat as stat_mod
import sys
from collections import defaultdict
from pathlib import Path


def pletiniai_kelias():
    """pletiniai.json vieta. PyInstaller onefile rezime __file__ rodo i
    laikina _MEIPASS aplanka, todel vartotojo redaguojamas failas SALIA EXE
    likdavo nematomas (claude.ai apzvalgos radinys #1, 2026-08-08).
    Paieskos tvarka: (1) salia exe (vartotojo kopija, redaguojama);
    (2) _MEIPASS bundle (gamyklinis fallback); (3) salia .py (dev rezimas)."""
    if getattr(sys, "frozen", False):
        salia_exe = Path(sys.executable).resolve().parent / "pletiniai.json"
        if salia_exe.is_file():
            return salia_exe
        bundle = getattr(sys, "_MEIPASS", None)
        if bundle:
            return Path(bundle) / "pletiniai.json"
        return salia_exe
    return Path(__file__).resolve().parent / "pletiniai.json"

# --- Windows/Mac siuksliu atpazinimas (2026-08-05, Roberto uzsakymas) ---
# Dviguba patikra: vardas + turinio parasas (magic bytes). Failai - gryni
# kesai, OS juos atsikuria; desktop.ini SAMONINGAI neliestas (saugo katalogu
# nustatymus). Papildomi vardai (tik vardo patikra, be paraso) - pletiniai.json
# rakte "_siuksles".
JUNK_NAMES = {"thumbs.db": "OLE2", "ehthumbs.db": "OLE2", ".ds_store": "BUD1"}
_JUNK_MAGIC = {"OLE2": b"\xd0\xcf\x11\xe0", "BUD1": b"\x00\x00\x00\x01Bud1"}
_EXTRA_JUNK = None


def _extra_junk_names():
    """Vartotojo papildyti siuksliu vardai is pletiniai.json '_siuksles'."""
    global _EXTRA_JUNK
    if _EXTRA_JUNK is None:
        _EXTRA_JUNK = set()
        try:
            p = pletiniai_kelias()
            with open(p, encoding="utf-8") as fh:
                data = json.load(fh)
            _EXTRA_JUNK = {str(n).lower() for n in data.get("_siuksles", [])}
        except (OSError, json.JSONDecodeError):
            pass
    return _EXTRA_JUNK


def is_junk_name(path_str):
    name = os.path.basename(path_str).lower()
    return name in JUNK_NAMES or name in _extra_junk_names()


def find_junk(file_list):
    """Siuksliu kandidatai pagal varda (be turinio skaitymo).
    Returns list of (path, size)."""
    return [(p, s) for p, s in file_list if is_junk_name(p)]


def verify_junk(path_str):
    """True TIK jei failas neabejotinai siuksle: zinomas vardas + turinio
    parasas. Vartotojo papildytiems vardams (be zinomo paraso) - vardo uztenka."""
    name = os.path.basename(path_str).lower()
    kind = JUNK_NAMES.get(name)
    if kind is None:
        return name in _extra_junk_names()
    magic = _JUNK_MAGIC[kind]
    try:
        with open(path_str, "rb") as fh:
            return fh.read(len(magic)) == magic
    except OSError:
        return False


def delete_junk(junk_list, progress_cb=None):
    """Trina TIK verify_junk patvirtintas siukles (abejone -> praleidziama).
    Returns (deleted_count, skipped_count, freed_bytes)."""
    deleted = skipped = freed = 0
    for i, (p, s) in enumerate(junk_list, 1):
        if verify_junk(p):
            try:
                os.remove(p)
                deleted += 1
                freed += s
            except PermissionError:
                # hidden/system/readonly atributai - nuimam ir bandom dar karta
                try:
                    senas_mode = os.stat(p).st_mode
                except OSError:
                    senas_mode = None
                try:
                    os.chmod(p, stat_mod.S_IWRITE)
                    os.remove(p)
                    deleted += 1
                    freed += s
                except OSError:
                    skipped += 1
                    # trinti nepavyko - grazinam atributus, kokie buvo
                    # (claude.ai apzvalgos radinys #5, 2026-08-08)
                    if senas_mode is not None:
                        try:
                            os.chmod(p, stat_mod.S_IMODE(senas_mode))
                        except OSError:
                            pass
            except OSError:
                skipped += 1
        else:
            skipped += 1
        if progress_cb:
            progress_cb(i, len(junk_list))
    return deleted, skipped, freed


def scan_folders_stats(folders, progress_cb=None):
    """Recursively collect files from given folders.
    Returns (list of [absolute_path_str, size_int], skipped_count).
    skipped_count - failai, kuriu nepavyko nuskaityti (uzrakinti/be teisiu).
    progress_cb(found_count) - kvieciamas kas 1000 rastu failu (gyvas skaitliukas).

    PERFORMANCE 2026-08-05: os.scandir vietoj pathlib.rglob+resolve -
    Windows'e DirEntry.stat() dydi grazina be papildomo syscall'o (3-5x
    greiciau dideliems medziams). follow_symlinks=False - junction'ai
    nesekami, tad nebera ir ciklu rizikos."""
    result = []
    skipped = 0
    for folder in folders:
        root = os.path.abspath(folder)
        if not os.path.isdir(root):
            continue
        stack = [root]
        while stack:
            d = stack.pop()
            try:
                with os.scandir(d) as it:
                    for entry in it:
                        try:
                            if entry.is_dir(follow_symlinks=False):
                                stack.append(entry.path)
                            elif entry.is_file(follow_symlinks=False):
                                result.append(
                                    [entry.path,
                                     entry.stat(follow_symlinks=False).st_size])
                                if progress_cb and (len(result) + skipped) % 1000 == 0:
                                    progress_cb(len(result) + skipped)
                        except OSError:
                            skipped += 1
            except OSError:
                skipped += 1
    return result, skipped


def scan_folders(folders):
    """Senasis API: tik failu sarasas, be praleistu skaiciaus."""
    return scan_folders_stats(folders)[0]


def size_candidates(file_list):
    """1 FAZE (greita, be turinio skaitymo): grupuoja pagal dydi.
    0 baitu failai atmetami (ju MD5 vienodas, bet tai ne dubliai, o triuksmas).
    Returns list of (size, [paths]) kur grupeje >= 2 failai."""
    by_size = defaultdict(list)
    for path_str, size in file_list:
        if size > 0:
            by_size[size].append(path_str)
    return [(s, ps) for s, ps in by_size.items() if len(ps) >= 2]


def _fiziniu_failu_kiekis(paths):
    """Kiek FIZISKAI skirtingu failu tarp keliu (hardlink'ai = tas pats
    failas, st_dev+st_ino sutampa). Hardlink'o istrynimas vietos neatlaisvina,
    tad 'atlaisvinama' skaiciuojama nuo fiziniu kopiju (claude.ai apzvalgos
    radinys #3, 2026-08-08). Neperskaitomi keliai laikomi atskirais failais."""
    inodes = set()
    extra = 0
    for p in paths:
        try:
            st = os.stat(p)
            inodes.add((st.st_dev, st.st_ino))
        except OSError:
            extra += 1
    return len(inodes) + extra


def hash_groups(candidates, total_files=0, progress_cb=None):
    """2 FAZE (leta): MD5 tik dydzio kandidatu grupese.
    progress_cb(bytes_done, bytes_total) - kvieciamas po kiekvieno failo.

    Returns dict with:
      groups - list of lists, each inner list = identical file paths
      stats  - { total_files, duplicate_groups, duplicated_mb, freeable_mb }
        duplicated_mb - bendras dubliu uzimamas turis (VISOS kopijos kartu);
        freeable_mb   - kiek atsilaisvintu palikus po viena FIZINE kopija
                        (size*(n-1), hardlink'ai neskaiciuojami; GPT radinys
                        (a) + claude.ai #3, 2026-08-08).
    """
    bytes_total = sum(s * len(ps) for s, ps in candidates)
    bytes_done = 0
    groups = []
    dup_bytes = 0
    freeable_bytes = 0
    for size, paths in candidates:
        # Dideliems failams - 64 KB prefikso filtras: pilnas MD5 tik toms
        # pogrupemis, kuriu prefiksai sutampa (skirtingi failai atkrenta
        # perskaicius pirmus baitus, ne visa turini)
        pogrupes = [paths]
        if size > _PREFIX_RIBA:
            by_pref = defaultdict(list)
            for p in paths:
                pm = _md5_prefiksas(p)
                if pm is None:
                    # pilnas MD5 irgi luztu - failas praleidziamas, progresas juda
                    bytes_done += size
                    if progress_cb:
                        progress_cb(bytes_done, bytes_total)
                else:
                    by_pref[pm].append(p)
            pogrupes = []
            for ps in by_pref.values():
                if len(ps) >= 2:
                    pogrupes.append(ps)
                else:
                    # prefiksas unikalus - dublio nebus, pilno skaitymo nereikia
                    bytes_done += size
                    if progress_cb:
                        progress_cb(bytes_done, bytes_total)
        by_md5 = defaultdict(list)
        for ps in pogrupes:
            for p in ps:
                m = _md5(p)
                bytes_done += size
                if m is not None:
                    by_md5[m].append(p)
                if progress_cb:
                    progress_cb(bytes_done, bytes_total)
        for md, members in by_md5.items():
            if len(members) >= 2:
                groups.append(sorted(members))
                dup_bytes += size * len(members)
                freeable_bytes += size * max(0, _fiziniu_failu_kiekis(members) - 1)

    return {
        "groups": groups,
        "stats": {
            "total_files": total_files,
            "duplicate_groups": len(groups),
            "duplicated_mb": round(dup_bytes / (1024.0 * 1024.0), 2),
            "freeable_mb": round(freeable_bytes / (1024.0 * 1024.0), 2),
        },
    }


# Nuo kokio failo dydzio apsimoka pirmas 64 KB "prefikso" perskaitymas:
# dideliems failams skirtingas turinys demaskuojamas is pirmu baitu ir
# pilno skaitymo nebereikia (claude.ai apzvalgos radinys #6, 2026-08-08)
_PREFIX_RIBA = 4 * 1024 * 1024
_PREFIX_KIEK = 65536


def _md5_prefiksas(filepath):
    """MD5 tik pirmu 64 KB - pigus filtras pries pilna skaityma."""
    h = hashlib.md5(usedforsecurity=False)
    try:
        with open(filepath, "rb") as fh:
            h.update(fh.read(_PREFIX_KIEK))
    except (OSError, PermissionError):
        return None
    return h.hexdigest()


def _md5(filepath):
    """MD5 hash of file contents. Returns hex string or None on error.

    usedforsecurity=False: MD5 cia tik turinio sutapimo raktas, ne
    kriptografija - be sito FIPS rezimo Windows (imoniu/valstybines
    masinos) hashlib.md5() meta ValueError ir programa luzta
    (claude.ai apzvalgos radinys #2, 2026-08-08)."""
    h = hashlib.md5(usedforsecurity=False)
    try:
        with open(filepath, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
    except (OSError, PermissionError):
        return None
    return h.hexdigest()


def _normalize(name):
    """Vardas be kopijos pozymio, mazosiomis raidemis.

    2026-08-26: anksciau cia gyveno SAVO, siauresne taisykle, ir ji darė dvi
    klaidas vienu metu:
      (a) mokejo tik "- Copy" ir "- kopija" - o programa keturkalbe, tad
          rusiskas "- kopija", vokiskas "- Kopie" ir "Copy of ..." likdavo
          neatpazinti (isMATUOTA: 3 poros is 5 nepatekdavo i ITARTINUS);
      (b) salino BET KOKI skliaustu turini, todel "Ataskaita (2024)" ir
          "Ataskaita (2025)" tapdavo tuo paciu vardu - lygiai ta pati klaidos
          rusis, kaip v1.4 "Photocopy" ir "Mikroskopija".
    Dabar naudojamas tas pats atranka.py zinynas, kuri jau turi programa -
    ne naujos taisykles, o esamu panaudojimas vienoje vietoje.
    """
    base, ext = os.path.splitext(name)
    import atranka
    return atranka.be_kopijos_pozymio(base).strip().lower() + ext.lower()


def find_duplicates(file_list):
    """Senasis API: abi fazes vienu ypu (size_candidates + hash_groups)."""
    return hash_groups(size_candidates(file_list), total_files=len(file_list))


# ITARTINI lubos: daugiau poru zmogus neperziuretu, o simtai tukstanciu
# poru (pvz. vienavardes ikoneles) stingdo lentele, kesa ir Excel eksporta
MAX_SUSPECT_PAIRS = 10_000


def find_suspects(file_list, progress_cb=None):
    """Suspect files: normalized name match + size within +-10% but DIFF MD5.

    PERFORMANCE FIX 2026-08-05: (a) grupuojama pagal normalizuota varda;
    (b) DYDZIU PREFILTRAS - hash'uojami TIK tie vardo sutapimo failai, kurie
    turi dydzio partneri +-10% (dydziai jau RAM'e - disko skaityt nereikia).
    Be prefiltro visam diskui buvo hash'uojami visi vienavardziai failai.
    progress_cb(done, total) - kvieciamas po kiekvieno suhash'uoto failo.

    Returns (suspects, truncated):
      suspects  - list of dicts {file_a, file_b, size_a, size_b, reason}
      truncated - True, jei pasiekta MAX_SUSPECT_PAIRS lubos ir dalis poru
                  NEPARODYTA (anksciau kirpdavo TYLIAI - claude.ai apzvalgos
                  radinys #4, 2026-08-08; vartotojui rodyti ispejima).
    """
    by_name = defaultdict(list)
    for path_str, size in file_list:
        nname = _normalize(os.path.basename(path_str))
        by_name[nname].append((path_str, size))

    # Dydziu prefiltras (be jokio disko skaitymo)
    hash_jobs = []
    for nname, items in by_name.items():
        if len(items) < 2:
            continue
        cand = []
        for i, (p, s) in enumerate(items):
            for j, (p2, s2) in enumerate(items):
                if i == j:
                    continue
                ref = max(s, s2)
                if ref > 0 and abs(s - s2) / ref <= 0.10:
                    cand.append((p, s))
                    break
        if len(cand) >= 2:
            hash_jobs.append(cand)

    total = sum(len(c) for c in hash_jobs)
    done = 0
    seen = set()
    suspects = []
    truncated = False
    for cand in hash_jobs:
        if len(suspects) >= MAX_SUSPECT_PAIRS:
            truncated = True
            break
        enriched = []
        for p, s in cand:
            m = _md5(p)
            done += 1
            if progress_cb:
                progress_cb(done, total)
            if m is not None:
                enriched.append((p, s, m))
        for i in range(len(enriched)):
            if len(suspects) >= MAX_SUSPECT_PAIRS:
                truncated = True
                break
            pa, sa, ma = enriched[i]
            for j in range(i + 1, len(enriched)):
                pb, sb, mb = enriched[j]
                if ma == mb:
                    continue
                ref = max(sa, sb)
                if ref > 0 and abs(sa - sb) / ref <= 0.10:
                    key = tuple(sorted([pa, pb]))
                    if key not in seen:
                        seen.add(key)
                        # size_a/size_b - kad eksportui/lentelei nereiketu
                        # klausti disko (dydziai jau zinomi cia)
                        suspects.append({
                            "file_a": pa,
                            "file_b": pb,
                            "size_a": sa,
                            "size_b": sb,
                            "reason": "norm name match + similar size +-10%, diff content",
                        })
                        if len(suspects) >= MAX_SUSPECT_PAIRS:
                            truncated = True
                            break
    return suspects, truncated


# Apkrovos lubos vienam atspaudu kibirui (zr. find_similar_images).
# Kibire lyginama kiekvienas su kiekvienu, tad kaina auga kvadratu:
# 10 000 atspaudu = 50 mln. poru ~ 15 s (isMATUOTA 2026-08-26: 3,3 mln.
# poru/s). Buvusi riba 300 nukirsdavo jau prie ~20 000 unikaliu atspaudu -
# t. y. prie EILINIO namu archyvo: gyvas matavimas ant Roberto NAS
# (66 537 nuotraukos) rado kibira su 334 atspaudais, ir jie is paieskos
# iskrito TYLIAI. Ribos dydis rezultatu TEISINGUMO nekeicia (balandides
# principo garantija su 4x16 bitu lieka ta pati) - tik tai, kiek darbo
# sutinkame padaryti.
MAX_BUCKET = 10_000


def find_similar_images(image_files, progress_cb=None, exact_groups=None,
                        stats_out=None, max_bucket=None):
    """VIZUALIAI panasiu nuotrauku paieska (2026-08-05 vakaras, Roberto
    uzsakymas 'kad luzeriu neisvadintu').

    dHash (imagehash): nuotrauka sumazinama iki 9x8 pilku tasku -> 64 bitu
    vizualinis pirstu atspaudas, nepriklausantis nuo rezoliucijos, formato
    ar suspaudimo kokybes. Grupuojama pagal IDENTISKA atspauda - taip
    randamos sumazintos/perspaustos tos pacios nuotraukos kopijos.

    image_files - [(path, size), ...] (tik paveiksliukai; filtruoja worker'is).
    exact_groups - tiksliuju (MD5) dubliu grupes: vizualines grupes, kurios
    nieko naujo neprideda (visi nariai jau vienoje MD5 grupeje), atmetamos.
    progress_cb(done, total) - po kiekvienos nuotraukos.
    stats_out - neprivalomas zodynas; jei paduotas, uzpildomas raktais
    "skipped_buckets" ir "skipped_pictures" (kiek kibiru virsijo apkrovos luba
    ir kiek atspaudu del to liko VISAI nepalyginti). Kvieteju, kurie jo
    neduoda, elgsena nesikeicia.
    max_bucket - apkrovos lubos perrasymas (numatyta MAX_BUCKET); tik testams.

    Returns list of groups (list of paths). Neatidaromi failai praleidziami.
    """
    try:
        from PIL import Image, ImageOps
    except ImportError:
        return []
    # HEIC/HEIF (iPhone numatytasis formatas): Pillow pats ju neatidaro -
    # pillow-heif registruoja atidarytuvus (dupeGuru #455, 17 balsu; v1.3,
    # gyvas testas 2026-08-22: HEIC+AVIF+JPEG kopijos suguli i viena grupe).
    # AVIF nuo Pillow 11.2+ atidaromas natyviai. Priedo nesant elgsena
    # kaip iki siol - tokie failai tyliai praleidziami (except zemiau).
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except ImportError:
        pass

    VIS_DIST = 3  # maks. Hamming atstumas (is 64 bitu), kad laikytume "ta pacia"
                  # (resize/kokybes perspaudimas realiai pajudina 0-2 bitus).
                  # BUVO 4, bet 4x16 bitu skirstymas zemiau GARANTUOJA tik <=3
                  # (balandides principas: 4 skirtingi bitai gali pataikyti i
                  # visus 4 gabalus) - riba suvienodinta su garantija, kad
                  # nebutu tyliu praleidimu (GPT (b) + claude.ai #7, 2026-08-08)

    def _dhash64(img):
        """dHash grynu Pillow (be imagehash/numpy/scipy - exe lieknumui):
        9x8 pilku tasku tinklelis, bitas = ar kairysis taskas sviesesnis
        uz desiniji. Rezultatas - 64 bitu int, atsparus resize/kokybei."""
        g = img.convert("L").resize((9, 8), Image.LANCZOS)
        # getdata() nyksta Pillow 14 (2027) - naujas API naudojamas kai yra,
        # senas paliktas suderinamumui su Pillow <12.3
        if hasattr(g, "get_flattened_data"):
            px = list(g.get_flattened_data())
        else:
            px = list(g.getdata())
        hv = 0
        for r in range(8):
            for c in range(8):
                hv = (hv << 1) | (1 if px[r * 9 + c] > px[r * 9 + c + 1] else 0)
        return hv

    # Astuonios padetys: 4 pasukimai x 2 (su veidrodziu). PIRMOJI (indeksas 0)
    # yra TIESIOGINE - jos atspaudas sutampa su tuo, kuris buvo skaiciuojamas
    # iki 2026-08-26, tad senas elgesys nesikeicia.
    # Kodel reikia: exif_transpose isgelbeja tik tas nuotraukas, kurias
    # PAZYMEJO fotoaparatas. Kai pikselius perraso redaktorius, pokalbiu
    # programa ar skeneris, zymes nebelieka ir atspaudas pasidaro visai kitas.
    # Gyvas matavimas 2026-08-26: originalas + fiziskai pasukta 90 laipsniu +
    # veidrodine davė NULI grupiu. dupeGuru tokias randa (8 orientacijos) -
    # is jos ir perimta IDEJA (ne kodas).
    _POZOS = (None,
              getattr(Image, "ROTATE_90", 2),
              getattr(Image, "ROTATE_180", 3),
              getattr(Image, "ROTATE_270", 4),
              getattr(Image, "FLIP_LEFT_RIGHT", 0))

    _KVADRATAS = 32     # tarpine sumazinta kopija, is kurios sukama

    def _visos_padetys(img):
        """8 atspaudai: tiesioginis, 3 pasukimai, veidrodinis ir jo 3 pasukimai.

        GREICIO ESME (isMATUOTA 2026-08-26 ant 200 tikru nuotrauku):
          1 padetis (kaip buvo)      71,1 nuotr./s
          8 sukant DIDELI vaizda      9,8 nuotr./s   <- 7 kartus letesne
          8 per maza KVADRATA        65,4 nuotr./s   <- si versija
        Pirma vienas sumazinimas i 32x32, o sukama jau ta smulkme - tad
        pasukimu palaikymas kainuoja apie desimtadali greicio, ne kartus.
        Kvadratas butinas: 9x8 tinklelis pasuktas 90 laipsniu virstu 8x9
        ir nebutu su kuo lyginti.
        """
        maz = img.convert("L").resize((_KVADRATAS, _KVADRATAS), Image.LANCZOS)
        rez = [_dhash64(maz)]
        for tr in _POZOS[1:4]:
            rez.append(_dhash64(maz.transpose(tr)))
        veidrodis = maz.transpose(_POZOS[4])
        rez.append(_dhash64(veidrodis))
        for tr in _POZOS[1:4]:
            rez.append(_dhash64(veidrodis.transpose(tr)))
        return rez

    # 1) Atspaudai kiekvienai nuotraukai (po 8; [0] - tiesioginis)
    keliai = []
    atspaudai = []
    neatidaryti = []      # nuotraukos, kuriu nepavyko atverti (zr. zemiau)
    total = len(image_files)
    for i, (p, s) in enumerate(image_files, 1):
        try:
            with Image.open(p) as img:
                # JPEG: draft dekoduoja is karto sumazinta - keliskart greiciau
                # (miniatiurai 9x8 pilnos rezoliucijos nereikia)
                img.draft("L", (9, 8))
                # EXIF Orientation: telefonu "pasukta" kopija be sito gautu
                # KITA atspauda ir dublio nerastume (claude.ai radinys, 2026-08-08;
                # pillow_foto_guard taisykle #1)
                img = ImageOps.exif_transpose(img)
                hs = _visos_padetys(img)
            keliai.append(p)
            atspaudai.append(hs)
        except Exception:
            # 2026-08-26: anksciau cia buvo "pass" - nuotrauka dingdavo TYLIAI.
            # Priezastys tikros: sugadintas failas, nezinomas formatas, be
            # teisiu, o milziniskoms (virs 2 x Pillow MAX_IMAGE_PIXELS =
            # 179 mln. taskeliu) Pillow meta DecompressionBombError. Gyvi
            # matavimai: 240 ir 285 tokiu nuotrauku dviejuose Roberto
            # archyvuose. Vartotojas apie jas nesuzinodavo NIEKO.
            neatidaryti.append(p)
        if progress_cb:
            progress_cb(i, total)

    # 2) Artimu atspaudu suliejimas be O(n^2): 64 bitai dalinami i 4 gabalus
    # po 16 bitu; jei atstumas <= 3, bent vienas gabalas sutampa (balandides
    # principas) - lyginam tik bendro gabalo kibiruose. Garantija galioja
    # butent <=3, todel VIS_DIST=3 (zr. aukciau).
    # Jungiam FAILUS (ne atspaudus): viena nuotrauka dabar turi 8 atspaudus,
    # ir sutapti gali bet kuri jos padetis su bet kuria kito failo padetimi.
    parent = list(range(len(keliai)))

    def _find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def _union(a, b):
        ra, rb = _find(a), _find(b)
        if ra != rb:
            parent[rb] = ra

    buckets = defaultdict(list)
    for idx, hs in enumerate(atspaudai):
        for poz, hv in enumerate(hs):
            for c in range(4):
                buckets[(c, (hv >> (c * 16)) & 0xFFFF)].append((idx, poz))
    riba = MAX_BUCKET if max_bucket is None else max_bucket
    per_dideli = set()     # failai, kuriuos kibiras atmete
    palyginti = set()      # failai, kurie bent viename kibire buvo lyginti
    praleista_kibiru = 0
    for items in buckets.values():
        if len(items) < 2:
            continue
        if len(items) > riba:     # saugiklis nuo isigimusiu kibiru
            praleista_kibiru += 1
            per_dideli.update(fi for fi, _ in items)
            continue
        palyginti.update(fi for fi, _ in items)
        for i in range(len(items)):
            fi, pi = items[i]
            hi = atspaudai[fi][pi]
            for j in range(i + 1, len(items)):
                fj, pj = items[j]
                if fi == fj:
                    continue      # ta pati nuotrauka kita padetimi
                # BENT VIENAS turi buti TIESIOGINEJE padetyje.
                # Jei B yra pasukta A versija, tai A tiesioginis atspaudas
                # sutaps su kuria nors B padetimi - lyginti dvieju PASUKTU
                # tarpusavyje nereikia, ir butent ten gimdavo atsitiktiniai
                # pataikymai: sukant prarandama dalis informacijos, tad du
                # skirtingi vaizdai gali netycia suartėti.
                # Gyvas matavimas 2026-08-26 (Roberto testo katalogas):
                #   tikras pasukimas / veidrodis / 180 / sumazinta -> 0..2 bitai
                #   atsitiktinis (dvi skirtingos nuotraukos)       -> 4 bitai
                # Priedo 8 kartus maziau lyginimu.
                if pi and pj:
                    continue
                if bin(hi ^ atspaudai[fj][pj]).count("1") <= VIS_DIST:
                    _union(fi, fj)
    if stats_out is not None:
        # Failas nukenteja tik tada, kai NE VIENAS jo kibiras nebuvo
        # palygintas - kitaip ji isgelbejo kitas gabalas ar kita padetis.
        stats_out["skipped_buckets"] = praleista_kibiru
        stats_out["skipped_pictures"] = len(per_dideli - palyginti)

    merged = defaultdict(list)
    for idx in range(len(keliai)):
        merged[_find(idx)].append(idx)

    # 3) Kelio -> tikslios (MD5) grupes id; atmetam grupes be nieko naujo
    exact_gid = {}
    for gid, grp in enumerate(exact_groups or []):
        for fp in grp:
            exact_gid[fp] = gid

    def _nukrype_nuo_normos(idxs):
        """Kurie grupes nariai guli KITAIP pasukti nei dauguma?

        Robertas 2026-08-26: verta pasakyti ne "grupeje kazkas pasukta", o
        KURIE failai - nes tai daznai ne kopija, o BROKAS ("pasuko ir pamirso
        grazinti"), matomas pries issiunciant krūva klientui.

        Norma = didziausias pogrupis, kurio TIESIOGINIAI atspaudai tarpusavyje
        panasus. Visi likusieji ir yra pasukti/veidrodiniai variantai.
        """
        # mazas union-find grupes viduje, TIK pagal tiesiogini atspauda
        tevas = list(range(len(idxs)))

        def _f(a):
            while tevas[a] != a:
                tevas[a] = tevas[tevas[a]]
                a = tevas[a]
            return a

        for i in range(len(idxs)):
            hi = atspaudai[idxs[i]][0]
            for j in range(i + 1, len(idxs)):
                if bin(hi ^ atspaudai[idxs[j]][0]).count("1") <= VIS_DIST:
                    ra, rb = _f(i), _f(j)
                    if ra != rb:
                        tevas[rb] = ra
        pogrupiai = defaultdict(list)
        for i in range(len(idxs)):
            pogrupiai[_f(i)].append(i)
        if len(pogrupiai) < 2:
            return []          # visi vienodai pasukti - nera ka sakyti
        dydziai = sorted((len(v) for v in pogrupiai.values()), reverse=True)
        if len(dydziai) > 1 and dydziai[0] == dydziai[1]:
            # NERA daugumos (dazniausiai grupe is dvieju: vienas pries viena).
            # Roberto gyvas testas 2026-08-26: tada zyme prilipdavo ATSITIKTINIAM
            # nariui - kartais originalui. Spejimas, kurio mes nedarome: kai
            # negalima pasakyti, KURIS pasuktas, sakom apie abu ir sprendima
            # paliekam zmogui.
            return [keliai[i] for i in idxs]
        norma = max(pogrupiai.values(), key=len)
        normos = set(norma)
        return [keliai[idxs[i]] for i in range(len(idxs)) if i not in normos]

    groups = []
    pasukti_failai = []
    for idxs in merged.values():
        if len(idxs) < 2:
            continue
        paths = [keliai[i] for i in idxs]
        # Unikalus "saltiniai": MD5 grupe = vienas saltinis, laisvas failas -
        # atskiras. >=2 saltiniai -> grupe prideda ka nors naujo.
        sources = set()
        for fp in paths:
            sources.add(exact_gid.get(fp, f"solo:{fp}"))
        if len(sources) >= 2:
            pasukti_failai.extend(_nukrype_nuo_normos(idxs))
            groups.append(sorted(paths))
    if stats_out is not None:
        stats_out["rotated_files"] = pasukti_failai
        stats_out["unreadable_pictures"] = neatidaryti
    return groups


def get_extension_stats(file_list):
    """Categorize files by extension for pie chart.

    Returns dict {category: count}.
    """
    cat_map = {
        "Foto": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Video": [".mp4", ".avi", ".mov", ".mkv"],
        "Dokumentai": [".docx", ".doc", ".txt", ".pdf", ".xlsx", ".pptx", ".csv"],
        "Archyvai": [".zip", ".rar", ".7z", ".tar", ".gz"],
    }
    counts = {}
    other = 0
    for path_str, _sz in file_list:
        ext = os.path.splitext(path_str)[1].lower()
        found = False
        for cat, exts in cat_map.items():
            if ext in exts:
                counts[cat] = counts.get(cat, 0) + 1
                found = True
                break
        if not found:
            other += 1
    if other > 0:
        counts["Kita"] = other
    return counts
