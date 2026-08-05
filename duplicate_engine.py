# duplicate_engine.py - core scan + duplicate detection, zero Qt imports
import hashlib
import json
import os
import re
import stat as stat_mod
from collections import defaultdict
from pathlib import Path

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
            p = Path(__file__).resolve().parent / "pletiniai.json"
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
                    os.chmod(p, stat_mod.S_IWRITE)
                    os.remove(p)
                    deleted += 1
                    freed += s
                except OSError:
                    skipped += 1
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


def hash_groups(candidates, total_files=0, progress_cb=None):
    """2 FAZE (leta): MD5 tik dydzio kandidatu grupese.
    progress_cb(bytes_done, bytes_total) - kvieciamas po kiekvieno failo.

    Returns dict with:
      groups - list of lists, each inner list = identical file paths
      stats  - { total_files, duplicate_groups, duplicated_mb }
    """
    bytes_total = sum(s * len(ps) for s, ps in candidates)
    bytes_done = 0
    groups = []
    dup_bytes = 0
    for size, paths in candidates:
        by_md5 = defaultdict(list)
        for p in paths:
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

    return {
        "groups": groups,
        "stats": {
            "total_files": total_files,
            "duplicate_groups": len(groups),
            "duplicated_mb": round(dup_bytes / (1024.0 * 1024.0), 2),
        },
    }


def _md5(filepath):
    """MD5 hash of file contents. Returns hex string or None on error."""
    h = hashlib.md5()
    try:
        with open(filepath, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
    except (OSError, PermissionError):
        return None
    return h.hexdigest()


def _normalize(name):
    """Remove copy suffixes: ' (1)', '_copy', '- Copy' etc. Lowercase."""
    base, ext = os.path.splitext(name)
    base = re.sub(r'\s*\([^)]*\)', '', base)          # remove (1), (2)...
    base = re.sub(r'[-_]\s*(?:copy|kopija)', '', base, flags=re.IGNORECASE)
    base = base.strip()
    return base.lower() + ext.lower()


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

    Returns list of dicts {file_a, file_b, reason}.
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
    for cand in hash_jobs:
        if len(suspects) >= MAX_SUSPECT_PAIRS:
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
                            break
    return suspects


def find_similar_images(image_files, progress_cb=None, exact_groups=None):
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

    Returns list of groups (list of paths). Neatidaromi failai praleidziami.
    """
    try:
        from PIL import Image
    except ImportError:
        return []

    VIS_DIST = 4  # maks. Hamming atstumas (is 64 bitu), kad laikytume "ta pacia"
                  # (resize/kokybes perspaudimas realiai pajudina 0-2 bitus)

    def _dhash64(img):
        """dHash grynu Pillow (be imagehash/numpy/scipy - exe lieknumui):
        9x8 pilku tasku tinklelis, bitas = ar kairysis taskas sviesesnis
        uz desiniji. Rezultatas - 64 bitu int, atsparus resize/kokybei."""
        g = img.convert("L").resize((9, 8), Image.LANCZOS)
        px = list(g.getdata())
        hv = 0
        for r in range(8):
            for c in range(8):
                hv = (hv << 1) | (1 if px[r * 9 + c] > px[r * 9 + c + 1] else 0)
        return hv

    # 1) dHash kiekvienai nuotraukai; identiski atspaudai suglaudziami is karto
    by_hash = defaultdict(list)
    total = len(image_files)
    for i, (p, s) in enumerate(image_files, 1):
        try:
            with Image.open(p) as img:
                hv = _dhash64(img)
            by_hash[hv].append(p)
        except Exception:
            pass  # sugadinta/neatpazinta nuotrauka - tyliai praleidziama
        if progress_cb:
            progress_cb(i, total)

    # 2) Artimu atspaudu suliejimas be O(n^2): 64 bitai dalinami i 4 gabalus
    # po 16 bitu; jei atstumas <= 3, bent vienas gabalas sutampa (balandides
    # principas) - lyginam tik bendro gabalo kibiruose. VIS_DIST 4-6 pagauna
    # per du gabalus, praktikoje resize/kokybe pajudina vos kelis bitus.
    uniq = list(by_hash.keys())
    parent = list(range(len(uniq)))

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
    for idx, hv in enumerate(uniq):
        for c in range(4):
            buckets[(c, (hv >> (c * 16)) & 0xFFFF)].append(idx)
    for idxs in buckets.values():
        if len(idxs) < 2 or len(idxs) > 300:  # saugiklis nuo isigimusiu kibiru
            continue
        for i in range(len(idxs)):
            for j in range(i + 1, len(idxs)):
                if bin(uniq[idxs[i]] ^ uniq[idxs[j]]).count("1") <= VIS_DIST:
                    _union(idxs[i], idxs[j])

    merged = defaultdict(list)
    for idx, hv in enumerate(uniq):
        merged[_find(idx)].extend(by_hash[hv])

    # 3) Kelio -> tikslios (MD5) grupes id; atmetam grupes be nieko naujo
    exact_gid = {}
    for gid, grp in enumerate(exact_groups or []):
        for fp in grp:
            exact_gid[fp] = gid

    groups = []
    for paths in merged.values():
        if len(paths) < 2:
            continue
        # Unikalus "saltiniai": MD5 grupe = vienas saltinis, laisvas failas -
        # atskiras. >=2 saltiniai -> grupe prideda ka nors naujo.
        sources = set()
        for fp in paths:
            sources.add(exact_gid.get(fp, f"solo:{fp}"))
        if len(sources) >= 2:
            groups.append(sorted(paths))
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
