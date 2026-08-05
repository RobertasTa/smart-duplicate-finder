"""
select_dialog.py - Kandidatu pasirinkimo dialogas (2 faziu schema, 2026-08-05)
Po greitos zvalgybos rodo, kokiu seimu vienodo dydzio kandidatu rasta,
su varnelemis ka tikrinti giliai (MD5). Laiko prognoze pagal disko greiti.
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)

from kalba import t, fam


def fmt_bytes(n):
    """1234567 -> '1.2 MB'"""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{int(n)} B"
        n /= 1024


def fmt_time(seconds):
    """95 -> '~2 min'"""
    if seconds < 5:
        return t("akimirka")
    if seconds < 90:
        return f"~{int(seconds)} s"
    if seconds < 5400:
        return f"~{int(round(seconds / 60))} min"
    return f"~{seconds / 3600:.1f} val"


class SelectFamiliesDialog(QDialog):
    """Lentele: [varna] Seima | Grupiu | Failu | Apimtis | ~Laikas.
    get_selected_families() grazina pazymetu seimu set'a."""

    def __init__(self, fam_summary, speed_mbs=150.0, parent=None,
                 visual_count=0):
        # fam_summary: list of {family, groups, files, bytes} (rusiuota)
        # visual_count: paveiksliuku kiekis vizualiam lyginimui (papildoma
        # eilute su NUIMTA varnele - lyginimas letas, tegul zmogus renkasi)
        super().__init__(parent)
        self.setWindowTitle(t("Rasti kandidatai i dublius"))
        self.setMinimumWidth(560)
        self._summary = fam_summary
        self._visual_count = visual_count

        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(t(
            "Vienodo dydzio failu grupes (kandidatai). Pazymekite,\n"
            "kurias seimas tikrinti giliai (MD5 pagal turini):")))

        extra = 1 if visual_count else 0
        self.table = QTableWidget(len(fam_summary) + extra, 5)
        self.table.setObjectName("tbl_families")
        self.table.setHorizontalHeaderLabels(
            [t("Seima"), t("Grupiu"), t("Failu"), t("Apimtis"), t("~Laikas")])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch)

        total_bytes = 0
        for i, fs in enumerate(fam_summary):
            # Rodomas isverstas pavadinimas, vidinis raktas - UserRole
            it_fam = QTableWidgetItem(fam(fs["family"]))
            it_fam.setData(Qt.ItemDataRole.UserRole, fs["family"])
            it_fam.setFlags(Qt.ItemFlag.ItemIsEnabled
                            | Qt.ItemFlag.ItemIsUserCheckable)
            it_fam.setCheckState(Qt.CheckState.Checked)
            self.table.setItem(i, 0, it_fam)
            secs = fs["bytes"] / (speed_mbs * 1024 * 1024) if speed_mbs else 0
            for col, txt in ((1, str(fs["groups"])), (2, str(fs["files"])),
                             (3, fmt_bytes(fs["bytes"])), (4, fmt_time(secs))):
                it = QTableWidgetItem(txt)
                it.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(i, col, it)
            total_bytes += fs["bytes"]

        if visual_count:
            # Vizualus lyginimas: varnele UZDETA kaip ir kitos (Roberto
            # sprendimas 2026-08-05) - dideliems archyvams galima nusiimti,
            # nes kiekviena nuotrauka atveriama (~40 nuotr./s)
            i = len(fam_summary)
            it_v = QTableWidgetItem(t("Panasios nuotraukos (vizualiai)"))
            it_v.setData(Qt.ItemDataRole.UserRole, "_VIZUALAS")
            it_v.setFlags(Qt.ItemFlag.ItemIsEnabled
                          | Qt.ItemFlag.ItemIsUserCheckable)
            it_v.setCheckState(Qt.CheckState.Checked)
            self.table.setItem(i, 0, it_v)
            for col, txt in ((1, "-"), (2, str(visual_count)), (3, "-"),
                             (4, fmt_time(visual_count / 40))):
                it = QTableWidgetItem(txt)
                it.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(i, col, it)

        lay.addWidget(self.table)
        total_secs = total_bytes / (speed_mbs * 1024 * 1024) if speed_mbs else 0
        lay.addWidget(QLabel(
            t("Is viso pazymejus viska: {mb} skaitymo, {t} (disko greitis "
              "~{v} MB/s)").format(mb=fmt_bytes(total_bytes),
                                   t=fmt_time(total_secs), v=int(speed_mbs))))

        btns = QHBoxLayout()
        btns.addStretch()
        b_ok = QPushButton(t("Tikrinti pazymetus"))
        b_ok.setObjectName("btn_deep_ok")
        b_ok.clicked.connect(self.accept)
        b_cancel = QPushButton(t("Atsaukti"))
        b_cancel.setObjectName("btn_deep_cancel")
        b_cancel.clicked.connect(self.reject)
        btns.addWidget(b_ok)
        btns.addWidget(b_cancel)
        lay.addLayout(btns)

    def get_selected_families(self):
        chosen = set()
        for i in range(self.table.rowCount()):
            it = self.table.item(i, 0)
            if it is not None and it.checkState() == Qt.CheckState.Checked:
                # Vidinis seimos raktas (UserRole), ne isverstas tekstas
                chosen.add(it.data(Qt.ItemDataRole.UserRole) or it.text())
        return chosen
