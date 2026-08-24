"""
exporter.py - Excel ataskaita (FAZE 5.2; perrasyta 2026-08-05 greiciui)
Ta pati logika kaip GUI lenteleje: tipo seimu antrastes, grupes atskirtos
dvieju atspalviu kaita. Stulpeliu plociai - automatiskai.

GREICIO sprendimai (dideliems rezultatams, pvz. viso disko skenui):
- write_only Workbook: eilutes srautu i diska, RAM nelaiko viso failo
  (OKF_openpyxl_changelog: write-only rezimas palaiko stilius, plocius,
  bet ws.column_dimensions privalo buti nustatyti PRIES appendinant eilutes);
- sizes zodynas is skeno (RAM) vietoj pakartotiniu os.path.getsize;
- stiliu objektai sukuriami po VIENA karta ir perpanaudojami.
"""
import os
from datetime import datetime
from pathlib import Path

import atranka
from kalba import fam as _famv, t as _t
from table_populator import family_of, FAMILY_ORDER, FAMILY_COLORS


def _rgb(hex_color):
    return "FF" + hex_color.lstrip("#").upper()


MAX_COL_WIDTH = 60  # per placiu stulpeliu lentele istampo; ilgesni tekstai
                    # lauzomi langelio viduje (wrap_text)

# Roberto gyvo testo pastaba 2026-08-24: v1.4 "Kodel" stulpelis nukrisdavo
# UZ EKRANO krasto - matesi tik pirmoji raide. Paaiskinimo, del kurio visa
# funkcija ir daryta, zmogus paprastai net nepamatydavo. Todel du siauresni
# rezimai: kelias 45 vietoj 60, o "Kodel" 26 su lauzymu (eilute paaugsta
# pati, nes Excel su wrap_text auksti pritaiko automatiskai).
KELIO_WIDTH = 45
PRIEZASTIES_WIDTH = 26
# Stulpeliu indeksai (0-based) dublikatu lape
STULP_KELIAS = 2
STULP_KODEL = 5


def _autofit(sheet, rows, headers):
    """Nustato plocius pagal jau paruostus duomenis (vienas praejimas RAM'e).
    Plotis ribojamas - likusi dali sutvarko wrap_text (eilute paaugsta pati)."""
    from openpyxl.utils import get_column_letter
    ribos = {STULP_KELIAS: KELIO_WIDTH, STULP_KODEL: PRIEZASTIES_WIDTH}
    # Antrastes lauziamos (wrap_text), tad joms uztenka ILGIAUSIO ZODZIO -
    # kitaip "Greiciausiai pirminis" istemptu placia stulpeli varnelei
    widths = [max((len(z) for z in h.split()), default=len(h)) for h in headers]
    for r in rows:
        for i, v in enumerate(r):
            l = len(str(v))
            if l > widths[i]:
                widths[i] = l
    for i, w in enumerate(widths, start=1):
        riba = ribos.get(i - 1, MAX_COL_WIDTH)
        sheet.column_dimensions[get_column_letter(i)].width = min(w + 3, riba)


def export_excel(scan_results, suspect_results, output_dir=".", out_path=None,
                 sizes=None, visual=None):
    """Export Excel ataskaita su openpyxl (write_only srautas).
    Sheet 'Duplicates': Group | File Name | Full Path | Size (MB),
    rusiuota seima -> grupe, su seimu antrastemis (kaip GUI lenteleje).
    Sheet 'Suspects': same format for suspects.
    Ispejimai: raudona >1GB, geltona >100MB.
    out_path - pilnas tikslo kelias (is 'Kur issaugoti?' dialogo).
    sizes - {kelias: dydis_baitais} is skeno (kad nereiketu getsize is disko)."""

    try:
        from openpyxl import Workbook
        from openpyxl.cell import WriteOnlyCell
        from openpyxl.styles import PatternFill, Font, Alignment
    except ImportError:
        print("openpyxl nepasiekiamas")
        return None

    # Ilgi keliai lauzomi langelio viduje (Excel auksti pritaiko pats)
    wrap_align = Alignment(wrap_text=True, vertical="top")

    sizes = sizes or {}

    def _size_of(fp):
        s = sizes.get(fp)
        if s is not None:
            return s
        try:
            return os.path.getsize(fp)
        except OSError:
            return 0

    # --- Stiliai: po viena objekta, perpanaudojami ---
    def _fill(hex_color):
        rgb = _rgb(hex_color)
        return PatternFill(start_color=rgb, end_color=rgb, fill_type="solid")

    header_fill = _fill("#4CAF50")
    bold_font = Font(bold=True)
    warn_red = _fill("#FFCDD2")     # >1GB
    warn_yellow = _fill("#FFF9C4")  # >100MB
    fam_fills = {f: (_fill(c[0]), _fill(c[1])) for f, c in FAMILY_COLORS.items()}
    fam_hdr_fonts = {f: Font(bold=True, color=_rgb(c[2]))
                     for f, c in FAMILY_COLORS.items()}
    sus_fills = (_fill("#FFFFCC"), _fill("#FFF3CD"))

    # Roberto klausimas 2026-08-06: lapu pavadinimai ir antrastes - pagal
    # pasirinkta kalba (ataskaita yra dokumentas zmogui), tie patys raktai
    # kaip GUI lenteleje. Failo pavadinimas lieka angliskas (techninis).
    headers = [_t("Grupe"), _t("Failo vardas"),
               _t("Pilnas kelias"), _t("Dydis (MB)")]

    # v1.4: du papildomi stulpeliai TIK dublikatu lape. Tai INFORMACIJA
    # ("kuris cia senelis ir kodel"), NE nurodymas trinti - programa
    # netrina nieko ir siulymo nedaro. Kur pozymiu nera - "neaisku".
    dup_headers = headers + [_t("Greiciausiai pirminis"), _t("Kodel")]

    # Priezasciu kodai -> tekstai (raktai verciami iprastu keliu)
    _PRIEZ_TEKSTAI = {
        atranka.PRIEZASTIS_VARDAS: _t("kiti grupeje vardu pazymeti kaip kopijos"),
        atranka.PRIEZASTIS_APLANKAS: _t("kiti guli laikinuose aplankuose"),
        atranka.PRIEZASTIS_GYLIS: _t("sekliausias kelias"),
        atranka.PRIEZASTIS_DATA: _t("seniausias failas"),
        atranka.NEAISKU: _t("neaisku - pozymiu nera"),
    }

    def _pirminis_ir_kodel(grp):
        """Grazina (zyme_siai_eilutei_dict, kodel_tekstas_grupei).
        mtime is disko imamas TIK jei pirmos trys taisykles neisspreze -
        taip dazniausiu atveju disko neliecia is viso."""
        kelias, priez = atranka.greiciausiai_pirminis(grp)
        if priez == atranka.NEAISKU and len(grp) > 1:
            mt = {}
            for fp in grp:
                try:
                    mt[fp] = os.stat(fp).st_mtime
                except OSError:
                    pass
            if mt:
                kelias, priez = atranka.greiciausiai_pirminis(grp, mtimes=mt)
        return kelias, _PRIEZ_TEKSTAI.get(priez, "")

    # --- 1. Paruosiam eiluciu duomenis RAM'e (tik dubliai - nedidele apimtis) ---
    # (vals, fill, font) - fill/font None = paprastas tekstas
    dup_rows = []
    groups = scan_results.get("groups", [])
    fam_groups = {}
    for gid, grp in enumerate(groups, 1):
        if not grp:
            continue
        fam = family_of(Path(grp[0]).suffix)
        fam_groups.setdefault(fam, []).append((gid, grp))

    for fam in FAMILY_ORDER:
        if fam not in fam_groups:
            continue
        exts = sorted({Path(fp).suffix.lower()
                       for _, g in fam_groups[fam] for fp in g})
        # Antraste be fono - tik paryskintas spalvotas tekstas (kaip GUI)
        dup_rows.append(([f"{_famv(fam)} ({', '.join(exts)})", "", "", "", "", ""],
                         None, fam_hdr_fonts[fam]))
        for shade_i, (gid, grp) in enumerate(fam_groups[fam]):
            group_fill = fam_fills[fam][shade_i % 2]
            pirminis, kodel = _pirminis_ir_kodel(grp)
            # Grupes lygio ispejimas (DC "warning all marked" atitikmuo musu
            # kalba): visos sios grupes kopijos guli laikinuose aplankuose
            if atranka.ZYME_VISI_LAIKINI in atranka.grupes_zymes(grp):
                zyme = _t("visos kopijos laikinuose aplankuose")
                kodel = f"{kodel}; {zyme}" if kodel else zyme
            pirma_eilute = True
            for fp in grp:
                size_bytes = _size_of(fp)
                if size_bytes > 1_073_741_824:
                    active = warn_red
                elif size_bytes > 104_857_600:
                    active = warn_yellow
                else:
                    active = group_fill
                # "Kodel" rasom VIENA karta grupeje: prie pazymeto failo,
                # o jei nepazymeta nieko - prie pirmos grupes eilutes
                yra_pirminis = bool(pirminis) and fp == pirminis
                if yra_pirminis or (not pirminis and pirma_eilute):
                    kodel_langelis = kodel
                else:
                    kodel_langelis = ""
                dup_rows.append(([_t("Grupe {idx}").format(idx=gid),
                                  os.path.basename(fp),
                                  str(Path(fp).resolve()),
                                  round(size_bytes / 1048576, 2),
                                  "✓" if yra_pirminis else "",
                                  kodel_langelis],
                                 active, None))
                pirma_eilute = False

    # Vizualiai panasios nuotraukos - atskiras lapas (violetiniai atspalviai)
    vis_fills = (_fill("#E9DDF7"), _fill("#CDB4EE"))
    vis_rows = []
    for vidx, grp in enumerate(visual or [], 1):
        fill = vis_fills[(vidx - 1) % 2]
        for fp in grp:
            vis_rows.append(([_t("Vaizdas {idx}").format(idx=vidx),
                              os.path.basename(fp),
                              str(Path(fp).resolve()),
                              round(_size_of(fp) / 1048576, 2)],
                             fill, None))

    sus_rows = []
    suspects = suspect_results if isinstance(suspect_results, list) else []
    for sid, pair in enumerate(suspects):
        fill = sus_fills[sid % 2]
        for fp, sz_key in ((pair.get("file_a"), "size_a"),
                           (pair.get("file_b"), "size_b")):
            if not fp:
                continue
            # Dydis is variklio (size_a/size_b) - be disko uzklausu
            sz = pair.get(sz_key)
            if sz is None:
                sz = _size_of(fp)
            sus_rows.append(([_t("Itartinas {n}").format(n=sid + 1),
                              os.path.basename(fp),
                              str(Path(fp).resolve()),
                              round(sz / 1048576, 2)],
                             fill, None))

    # --- 2. write_only srautas: plociai PRIES eilutes, tada liejam ---
    # Excel KIETA riba - 1 048 576 eiluciu lape; virsijus Excel "remontuoja"
    # faila ismesdamas lapo turini. Apsauga: apkerpam su pastaba.
    SAFE_ROWS = 1_000_000
    wb = Workbook(write_only=True)

    def _write_sheet(title, rows, lapo_headers=None):
        # lapo_headers: dublikatu lapas turi dvi papildomas skiltis, kiti - ne
        lapo_headers = lapo_headers or headers
        ws = wb.create_sheet(title)
        notice = None
        if len(rows) > SAFE_ROWS:
            notice = _t("RODOMA {a} IS {b} EILUCIU - virsyta Excel lapo riba (1 048 576)").format(
                a=SAFE_ROWS, b=len(rows))
            rows = rows[:SAFE_ROWS]
        # Antrasciu i eiluciu sarasa NEDEDAM - jos jau ateina atskiru
        # argumentu ir skaiciuojamos pagal ilgiausia ZODI (nes lauziamos);
        # idejus dukart laimedavo pilnas ilgis ir stulpelis likdavo platus
        _autofit(ws, [r[0] for r in rows], lapo_headers)
        hdr = []
        for h in lapo_headers:
            c = WriteOnlyCell(ws, value=h)
            c.fill = header_fill
            c.font = bold_font
            # Ilgas antrastes lauziam - kitaip "Greiciausiai pirminis"
            # isteptu 27 simboliu ploti stulpeliui, kuriame tik varnele
            c.alignment = wrap_align
            hdr.append(c)
        ws.append(hdr)
        for vals, fill, font in rows:
            cells = []
            for ci, v in enumerate(vals):
                c = WriteOnlyCell(ws, value=v)
                if fill is not None:
                    c.fill = fill
                if font is not None:
                    c.font = font
                # Ilgus tekstus lauziam langelio viduje - Excel eilutes
                # auksti tada pritaiko pats (Roberto prasymas 2026-08-24)
                if isinstance(v, str) and (
                        (ci == STULP_KELIAS and len(v) > KELIO_WIDTH)
                        or (ci == STULP_KODEL and len(v) > PRIEZASTIES_WIDTH)):
                    c.alignment = wrap_align
                cells.append(c)
            ws.append(cells)
        if notice:
            c = WriteOnlyCell(ws, value=notice)
            c.font = bold_font
            ws.append([c])

    _write_sheet(_t("Dublikatai"), dup_rows, dup_headers)
    if vis_rows:
        _write_sheet(_t("Panasios nuotraukos"), vis_rows)
    _write_sheet(_t("Itartini"), sus_rows)

    if out_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(output_dir, f"duplicate_report_{ts}.xlsx")
    wb.save(out_path)
    return out_path
