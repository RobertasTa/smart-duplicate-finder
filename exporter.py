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

from kalba import fam as _famv
from table_populator import family_of, FAMILY_ORDER, FAMILY_COLORS


def _rgb(hex_color):
    return "FF" + hex_color.lstrip("#").upper()


MAX_COL_WIDTH = 60  # per placiu stulpeliu lentele istampo; ilgesni tekstai
                    # lauzomi langelio viduje (wrap_text)


def _autofit(sheet, rows, headers):
    """Nustato plocius pagal jau paruostus duomenis (vienas praejimas RAM'e).
    Plotis ribojamas MAX_COL_WIDTH - likusi dali sutvarko wrap_text."""
    from openpyxl.utils import get_column_letter
    widths = [len(h) for h in headers]
    for r in rows:
        for i, v in enumerate(r):
            l = len(str(v))
            if l > widths[i]:
                widths[i] = l
    for i, w in enumerate(widths, start=1):
        sheet.column_dimensions[get_column_letter(i)].width = min(w + 3, MAX_COL_WIDTH)


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

    headers = ["Group", "File Name", "Full Path", "Size (MB)"]

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
        dup_rows.append(([f"{_famv(fam)} ({', '.join(exts)})", "", "", ""],
                         None, fam_hdr_fonts[fam]))
        for shade_i, (gid, grp) in enumerate(fam_groups[fam]):
            group_fill = fam_fills[fam][shade_i % 2]
            for fp in grp:
                size_bytes = _size_of(fp)
                if size_bytes > 1_073_741_824:
                    active = warn_red
                elif size_bytes > 104_857_600:
                    active = warn_yellow
                else:
                    active = group_fill
                dup_rows.append(([f"Group {gid}", os.path.basename(fp),
                                  str(Path(fp).resolve()),
                                  round(size_bytes / 1048576, 2)],
                                 active, None))

    # Vizualiai panasios nuotraukos - atskiras lapas (violetiniai atspalviai)
    vis_fills = (_fill("#E9DDF7"), _fill("#CDB4EE"))
    vis_rows = []
    for vidx, grp in enumerate(visual or [], 1):
        fill = vis_fills[(vidx - 1) % 2]
        for fp in grp:
            vis_rows.append(([f"Image {vidx}", os.path.basename(fp),
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
            sus_rows.append(([f"Suspect {sid+1}", os.path.basename(fp),
                              str(Path(fp).resolve()),
                              round(sz / 1048576, 2)],
                             fill, None))

    # --- 2. write_only srautas: plociai PRIES eilutes, tada liejam ---
    # Excel KIETA riba - 1 048 576 eiluciu lape; virsijus Excel "remontuoja"
    # faila ismesdamas lapo turini. Apsauga: apkerpam su pastaba.
    SAFE_ROWS = 1_000_000
    wb = Workbook(write_only=True)

    def _write_sheet(title, rows):
        ws = wb.create_sheet(title)
        notice = None
        if len(rows) > SAFE_ROWS:
            notice = (f"RODOMA {SAFE_ROWS} IS {len(rows)} EILUCIU - "
                      f"virsyta Excel lapo riba (1 048 576)")
            rows = rows[:SAFE_ROWS]
        _autofit(ws, [r[0] for r in rows] + [headers], headers)
        hdr = []
        for h in headers:
            c = WriteOnlyCell(ws, value=h)
            c.fill = header_fill
            c.font = bold_font
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
                if ci == 2 and isinstance(v, str) and len(v) > MAX_COL_WIDTH:
                    c.alignment = wrap_align  # Full Path lauzymas
                cells.append(c)
            ws.append(cells)
        if notice:
            c = WriteOnlyCell(ws, value=notice)
            c.font = bold_font
            ws.append([c])

    _write_sheet("Duplicates", dup_rows)
    if vis_rows:
        _write_sheet("Similar Images", vis_rows)
    _write_sheet("Suspects", sus_rows)

    if out_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(output_dir, f"duplicate_report_{ts}.xlsx")
    wb.save(out_path)
    return out_path
