"""
table_populator.py - Rezultatu lentele pildymas su Performance Guard.
Pagal pyqt6_performance_guard: blockSignals+setUpdatesEnabled + setRowCount(0).
Spalvos pagal failo tipo seima (paveiksliukai/video/dokumentai/archyvai/kita);
grupes tos pacios seimos viduje atskiriamos dvieju atspalviu kaita,
tarp seimu - antrastes eilute su pletiniais. Seimu logika naudoja ir exporter.py.
"""
import json
import os
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidgetItem

from duplicate_engine import pletiniai_kelias
from kalba import t as _t, fam as _famv

FAMILY_ORDER = ["Paveiksliukai", "Video", "Audio", "Dokumentai",
                "Archyvai", "CAD", "Kodas", "Programos", "Kita"]

# (sviesus atspalvis, tamsesnis atspalvis, antrastes teksto spalva)
FAMILY_COLORS = {
    "Paveiksliukai": ("#E6F1FB", "#B5D4F4", "#0C447C"),
    "Video":         ("#EEEDFE", "#CECBF6", "#3C3489"),
    "Audio":         ("#FBEAF0", "#F4C0D1", "#72243E"),
    "Dokumentai":    ("#FAEEDA", "#FAC775", "#633806"),
    "Archyvai":      ("#E1F5EE", "#9FE1CB", "#085041"),
    "CAD":           ("#FAECE7", "#F5C4B3", "#712B13"),
    "Kodas":         ("#EAF3DE", "#C0DD97", "#27500A"),
    "Programos":     ("#FCEBEB", "#F7C1C1", "#791F1F"),
    "Kita":          ("#F1EFE8", "#D3D1C7", "#444441"),
}
SUSPECT_BG = "#ffffcc"  # geltona, ITARINI
SUSPECT_TXT = "#5F5E5A"
# Visi musu fonai sviesus, tad eiluciu tekstas - fiksuotas tamsus. BUTINA:
# nustacius tik fona, teksto spalva lieka sistemos, o tamsios temos sistema
# duoda BALTA -> baltas ant sviesaus (rado fotografas macOS, 2026-08-26).
ROW_TXT = "#1A1A1A"
HEADER_BG = "#FFFFFF"
# Vizualiai panasios nuotraukos: rysk. violetine (skiriasi nuo Video svelnios)
VISUAL_COLORS = ("#E9DDF7", "#CDB4EE", "#3F2B70")

# Pletiniu zinynas is pletiniai.json (salia programos; galima pildyti ranka)
_EXT_INFO = None


def _ext_info():
    global _EXT_INFO
    if _EXT_INFO is None:
        _EXT_INFO = {}
        try:
            # frozen exe rezime __file__ rodo i _MEIPASS - kelias imamas is
            # bendro pagalbininko (salia exe -> bundle fallback)
            p = pletiniai_kelias()
            with open(p, encoding="utf-8") as fh:
                data = json.load(fh)
            _EXT_INFO = {k: v for k, v in data.items()
                         if not k.startswith("_") and isinstance(v, dict)}
        except (OSError, json.JSONDecodeError):
            pass  # be zinyno viskas krenta i "Kita" - programa veikia toliau
    return _EXT_INFO


def family_of(ext):
    """Grazina tipo seimos varda pagal pletini ('.jpg' arba 'jpg')."""
    ext = ext.lower().lstrip(".")
    info = _ext_info().get(ext)
    if info and info.get("seima") in FAMILY_COLORS:
        return info["seima"]
    return "Kita"


def aprasymas_of(ext):
    """Grazina pletinio aprasyma is zinyno arba tuscia eilute."""
    ext = ext.lower().lstrip(".")
    info = _ext_info().get(ext)
    return info.get("aprasymas", "") if info else ""


def _file_row(fp, group_label, grp_type, sizes=None):
    # Vienas os.stat vietoj getsize+getctime poros; dydis - is skeno RAM'o,
    # jei paduotas sizes zodynas (dideliems rezultatams tai daug greiciau)
    try:
        st = os.stat(fp)
        size_b = sizes.get(fp, st.st_size) if sizes else st.st_size
        size_mb = round(size_b / (1024**2), 2)
        ctime = datetime.fromtimestamp(st.st_ctime).strftime("%Y-%m-%d %H:%M")
    except OSError:
        size_mb = 0.0
        ctime = "?"
    return {
        "kind": "file",
        "name": os.path.basename(fp),
        "path": str(Path(fp).resolve()),
        "size_mb": size_mb,
        "ctime": ctime,
        "group": group_label,
        "grp_type": grp_type,
    }


def build_rows(scan_results, suspect_results, sizes=None, max_rows=None,
               visual=None):
    """Eiliu sarasas lentelei: rusiuota seima -> grupe, su antrasciu eilutemis.
    Gale - ITARTINI sekcija (panasus, bet ne identiski failai).
    sizes - {kelias: dydis} is skeno (nebutinas; taupo disko stat'us).
    max_rows - nutraukti formavima PRIES disko stat'us likusioms eilutems
    (dideliems rezultatams; +1 kad populate_table atpazintu apkirpima)."""
    entries = []
    limit = (max_rows + 1) if max_rows else None
    groups = (scan_results or {}).get("groups") or []

    fam_groups = {}
    for idx, grp in enumerate(groups, 1):
        if not grp:
            continue
        fam = family_of(Path(grp[0]).suffix)
        fam_groups.setdefault(fam, []).append((idx, grp))

    for fam in FAMILY_ORDER:
        if fam not in fam_groups:
            continue
        exts = sorted({Path(fp).suffix.lower() for _, g in fam_groups[fam] for fp in g})
        entries.append({"kind": "header", "family": fam,
                        "label": f"{_famv(fam)} ({', '.join(exts)})"})
        if sizes:
            # Riebiausi dubliai virsuje: grupes rusiuojamos pagal bendra dydi
            fam_groups[fam].sort(
                key=lambda ig: -sum(sizes.get(fp, 0) for fp in ig[1]))
        for shade_i, (idx, grp) in enumerate(fam_groups[fam]):
            if limit and len(entries) >= limit:
                return entries
            for fp in grp:
                r = _file_row(fp, _t("Grupe {idx}").format(idx=idx), "dup", sizes)
                r["family"] = fam
                r["shade"] = shade_i % 2
                entries.append(r)

    if visual:
        entries.append({"kind": "header", "family": "_VIZUALAS",
                        "label": _t("VIZUALIAI PANASUS (skirtinga rezoliucija/kokybe)")})
        for vidx, grp in enumerate(visual, 1):
            if limit and len(entries) >= limit:
                return entries
            for fp in grp:
                r = _file_row(fp, _t("Vaizdas {idx}").format(idx=vidx), "visual",
                              sizes)
                r["family"] = "_VIZUALAS"
                r["shade"] = (vidx - 1) % 2
                entries.append(r)

    if suspect_results:
        entries.append({"kind": "header", "family": None,
                        "label": _t("ITARTINI (panasus, bet ne identiski)")})
        for s in suspect_results:
            if limit and len(entries) >= limit:
                return entries
            for fp in (s["file_a"], s["file_b"]):
                r = _file_row(fp, _t("ITARINI"), "suspect")
                r["family"] = None
                r["shade"] = 0
                entries.append(r)
    return entries


def row_bg_color(row):
    """Grazina eilutes fono QColor pagal seima ir atspalvio indeksa."""
    if row.get("grp_type") == "suspect":
        return QColor(SUSPECT_BG)
    if row.get("grp_type") == "visual":
        return QColor(VISUAL_COLORS[1] if row.get("shade") else VISUAL_COLORS[0])
    fam = row.get("family") or "Kita"
    light, dark, _ = FAMILY_COLORS.get(fam, FAMILY_COLORS["Kita"])
    return QColor(dark if row.get("shade") else light)


MAX_TABLE_ROWS = 2000  # lentele - perziurai; pilnas sarasas Excel ataskaitoje


def populate_table(table_widget, scan_results, suspect_results, sizes=None,
                   max_rows=MAX_TABLE_ROWS, visual=None):
    """Populate QTableWidget with results. Performance guard applied.
    Virs max_rows lentele apkerpama (QTableWidget nuo desimciu tukstanciu
    eiluciu stingdo GUI); gale prisegama pastaba apie Excel ataskaita."""
    entries = build_rows(scan_results, suspect_results, sizes, max_rows, visual)

    notice = None
    if max_rows and len(entries) > max_rows:
        notice = _t("Rodoma eiluciu: {n} (didziausios grupes virsuje) - "
                    "PILNAS sarasas Excel ataskaitoje").format(n=max_rows)
        entries = entries[:max_rows]

    # pyqt6_performance_guard: disable signals + updates during fill
    table_widget.blockSignals(True)
    table_widget.setUpdatesEnabled(False)

    table_widget.clearSpans()
    table_widget.setRowCount(0)
    table_widget.clearContents()
    table_widget.setRowCount(len(entries) + (1 if notice else 0))
    ncols = table_widget.columnCount()

    if notice:
        item = QTableWidgetItem(notice)
        item.setForeground(QColor("#5F5E5A"))
        item.setBackground(QColor(HEADER_BG))
        f = item.font(); f.setBold(True); item.setFont(f)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        table_widget.setItem(len(entries), 0, item)
        table_widget.setSpan(len(entries), 0, 1, ncols)

    for i, e in enumerate(entries):
        if e["kind"] == "header":
            if e["family"] == "_VIZUALAS":
                txt = VISUAL_COLORS[2]
            elif e["family"]:
                _, _, txt = FAMILY_COLORS.get(e["family"], FAMILY_COLORS["Kita"])
            else:
                txt = SUSPECT_TXT
            # Antraste baltu fonu (kaip Excel) - geriau issiskiria tarp spalvotu eiluciu
            item = QTableWidgetItem(e["label"])
            item.setForeground(QColor(txt))
            item.setBackground(QColor(HEADER_BG))
            f = item.font(); f.setBold(True); item.setFont(f)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            table_widget.setItem(i, 0, item)
            table_widget.setSpan(i, 0, 1, ncols)
            continue

        vals = (e["name"], e["path"], str(e["size_mb"]),
                e["ctime"], e["group"])
        bg = row_bg_color(e)
        ext = Path(e["name"]).suffix
        desc = aprasymas_of(ext)
        tooltip = f"{desc} ({ext.lower()})" if desc else ""
        for col, val in enumerate(vals):
            item = QTableWidgetItem(val)
            item.setBackground(bg)
            item.setForeground(QColor(ROW_TXT))
            # Pilnas kelias - dvigubam klikui (atidaro kataloga Explorer'yje)
            item.setData(Qt.ItemDataRole.UserRole, e["path"])
            if tooltip:
                item.setToolTip(tooltip)
            table_widget.setItem(i, col, item)

    # Numeracija kaireje: TIK failams; antrastems/pastabai - tuscia
    # (kitaip antraste gauna numeri ir skaiciavimas meluoja)
    labels = []
    n = 0
    for e in entries:
        if e["kind"] == "header":
            labels.append("")
        else:
            n += 1
            labels.append(str(n))
    if notice:
        labels.append("")
    table_widget.setVerticalHeaderLabels(labels)

    # Re-enable
    table_widget.setUpdatesEnabled(True)
    table_widget.blockSignals(False)
