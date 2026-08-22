"""
main_window.py - Smart Duplicate Finder v2 GUI skeleton (FAZE 2.1 + 2.2)
Vertical button bar Kaireje, turinio zona Dešinėje. ~115 eil.
"""
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel, QTableWidget,
    QProgressBar, QMessageBox, QHeaderView, QFrame, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon

from kalba import t

# Rodoma Apie... langelyje; galutini numeri nustatyti leidziant release
# 1.3 (2026-08-22): desinio klaviso meniu, RU/DE kalbos, HEIC/AVIF
VERSIJA = "1.3"

# Saugumo taisykle (aptarta 2026-08-22): siu pletiniu failo NEATIDAROME
# vienu meniu paspaudimu - nezinoma programa nepaleidziama; tik katalogas.
# .py/.pyw Roberto pastaba is gyvo testo: Windows juos sieja su Python
# launcher'iu, tad "atidarymas" faktiskai PALEISTU skripta.
_VYKDOMIEJI = {
    ".exe", ".msi", ".bat", ".cmd", ".ps1", ".vbs", ".vbe", ".js",
    ".jse", ".wsf", ".wsh", ".scr", ".com", ".jar", ".pif", ".hta",
    ".cpl", ".msc", ".reg", ".lnk",
    ".py", ".pyw", ".pyc", ".pyz", ".pyzw",
}


def _res_path(name):
    """Resurso kelias: veikia ir is source, ir is PyInstaller exe (_MEIPASS)."""
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return Path(base) / name
    return Path(__file__).resolve().parent / name


def _app_dir():
    """Katalogas irasymams (ataskaitos numatytoji vieta): salia exe arba .py."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _cache_dir():
    """Darbiniu failu vieta (kesas, veiklos.log, scan_speed.json).

    Nuo 2026-08-06 sprendzia saugykla.py: numatyta
    %LOCALAPPDATA%/SmartDuplicateFinder, o portable rezime (SDF_portable.txt
    salia exe, GUI varnele) - _darbal salia exe. Anksciau buvo %TEMP%,
    bet temp valytuvai kesa istrindavo ir elgsena nesutapo su Temp
    Cleaner dovana (Roberto pastaba 2026-08-06).
    SDF_CACHE_DIR - testu izoliacijai (patikros neperraso tikro keso)."""
    override = os.environ.get("SDF_CACHE_DIR")
    if override:
        d = Path(override)
    else:
        import saugykla
        d = saugykla.data_dir()
    try:
        d.mkdir(parents=True, exist_ok=True)
    except OSError:
        return _app_dir()
    return d


# Modernus mygtuku stilius (2026-08-05, Roberto prasymu): apvalinti kampai,
# svelnus 3D gradientas, ryskus hover; btn_scan - akcentinis (gintarinis,
# deranti prie programos ikonos), btn_export - melynas.
APP_QSS = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ffffff, stop:1 #e4e6ee);
    border: 1px solid #b6bac8;
    border-radius: 10px;
    padding: 9px 14px;
    font-weight: 600;
    color: #2c2f38;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f3f7ff, stop:1 #d6e2f8);
    border: 1px solid #5b8def;
    color: #123a7a;
}
QPushButton:pressed {
    background: #c9d7f0;
    border: 1px solid #3c6fd8;
    padding-top: 11px; padding-bottom: 7px;
}
QPushButton:disabled {
    background: #ededf1; border: 1px solid #d3d3da; color: #a0a0ab;
}
QPushButton#btn_scan {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ffd35c, stop:1 #f0a53a);
    border: 1px solid #d18a1f;
    color: #4a2c00;
}
QPushButton#btn_scan:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ffe08a, stop:1 #f7b551);
    border: 1px solid #b97613;
}
QPushButton#btn_scan:pressed {
    background: #e29a2e; border: 1px solid #a56508;
    padding-top: 11px; padding-bottom: 7px;
}
QPushButton#btn_scan:disabled {
    background: #ededf1; border: 1px solid #d3d3da; color: #a0a0ab;
}
QPushButton#btn_export {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #7fb3f2, stop:1 #3d7bd8);
    border: 1px solid #2b62b5;
    color: #ffffff;
}
QPushButton#btn_export:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #9cc6f8, stop:1 #5590e6);
    border: 1px solid #1f4f9c;
}
QPushButton#btn_export:pressed {
    background: #3568b8; border: 1px solid #1a4485;
    padding-top: 11px; padding-bottom: 7px;
}
QPushButton#btn_help {
    border-radius: 13px;
    padding: 0px;
    font-weight: 700;
}
QPushButton#btn_help::menu-indicator { image: none; width: 0px; }
QProgressBar {
    border: 1px solid #b6bac8; border-radius: 8px;
    background: #eef0f5; text-align: center; height: 16px;
}
QProgressBar::chunk {
    border-radius: 7px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ffd35c, stop:1 #f0a53a);
}
"""


def _title_font():
    return QFont("Segoe UI", 9, QFont.Weight.Bold)


def _hdr(txt):
    l = QLabel(txt); l.setFont(_title_font()); return l


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Duplicate Finder v2")
        ico = _res_path("app.ico")
        if ico.exists():
            self.setWindowIcon(QIcon(str(ico)))
        # Stilius visai programai (galioja ir dialogams)
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(APP_QSS)
        self.setMinimumSize(1100, 700)
        self.folders = []
        self.scan_results = None
        self.suspect_results = None
        self._all_files = []
        self._skipped = 0
        self.visual_results = []
        # Thread guards (pyqt6_threading_guard)
        self._worker = None
        self._thread = None

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(self._build_left_bar())
        root.addWidget(self._build_right_area(), stretch=1)
        self.statusBar().showMessage(t("Pasirenges"))
        # Gyvas skaitliukas apatiniame desiniame kampe (programistu kampelis):
        # [veikia MM:SS] [darbininko statistika]
        self.elapsed_label = QLabel("")
        self.elapsed_label.setStyleSheet("color: #5a5e6b; font-size: 8pt;")
        self.statusBar().addPermanentWidget(self.elapsed_label)
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("color: #5a5e6b; font-size: 8pt;")
        self.statusBar().addPermanentWidget(self.stats_label)
        self._build_scan_overlay()
        self._log("PROGRAMA paleista")
        self._offer_restore()

    def _log(self, msg):
        """Veiklos zurnalas (%TEMP%\\SmartDuplicateFinder\\veiklos.log) -
        faziu laikai diagnostikai; veikia ir is exe, ir is python."""
        try:
            with open(_cache_dir() / "veiklos.log", "a", encoding="utf-8") as fh:
                fh.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
        except OSError:
            pass

    # ---- Paskutinio skeno atmintis (%TEMP% kesas; Roberto ideja 2026-08-05) ----
    def _cache_file(self):
        return _cache_dir() / "paskutinis_skenas.json"

    def _save_cache(self):
        """Po gilaus skeno - rezultatai i %TEMP%, kad nulusus/uzdarius neprapultu."""
        import json
        try:
            data = {
                "kada": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "folders": self.folders,
                "stats": self.scan_results["stats"],
                "groups": self.scan_results["groups"],
                "suspects": self.suspect_results or [],
                "visual": self.visual_results or [],
                "sizes": self._sizes,
            }
            with open(self._cache_file(), "w", encoding="utf-8") as fh:
                json.dump(data, fh)
        except (OSError, TypeError, KeyError):
            pass  # kesas - patogumas, ne butinybe

    def _offer_restore(self):
        """Paleidus programa: jei yra ankstesnio skeno kesas - pasiulyti ikelti."""
        import json
        try:
            with open(self._cache_file(), encoding="utf-8") as fh:
                data = json.load(fh)
            kada = data["kada"]; n_groups = len(data["groups"])
        except (OSError, ValueError, KeyError):
            return
        atsakymas = QMessageBox.question(
            self, t("Ankstesnio skeno rezultatai"),
            t("Rasti ankstesnio skeno rezultatai ({kada}, {n} dubliu grupiu).\n"
              "Ikelti be pakartotinio skenavimo?").format(kada=kada, n=n_groups))
        if atsakymas != QMessageBox.StandardButton.Yes:
            return
        try:
            self.scan_results = {"stats": data["stats"], "groups": data["groups"]}
            self.suspect_results = data.get("suspects") or []
            self.visual_results = data.get("visual") or []
            self._sizes = data.get("sizes") or {}
            for fp in data.get("folders") or []:
                if fp not in self.folders:
                    self.folders.append(fp)
                    self.folder_list.addItem(QListWidgetItem(fp))
            from table_populator import populate_table
            populate_table(self.results_table, self.scan_results,
                           self.suspect_results, self._sizes,
                           visual=self.visual_results)
            st = self.scan_results["stats"]
            self.status_label.setText(
                t("Ikelti {kada} skeno rezultatai: {g} dublikatu grupes, "
                  "{mb:.2f} MB (galima eksportuoti be skenavimo)")
                .format(kada=kada, g=st['duplicate_groups'],
                        mb=st['duplicated_mb']))
        except (KeyError, TypeError):
            self.status_label.setText(t("Keso ikelti nepavyko - skenuok is naujo."))

    # ---- "Vyksta skenavimas" overlay (pagal Temp SIUKSLIU valymas sablona) ----
    # Modeless: NE dialogas, NE exec() - tik virsutinis QFrame vaikas.
    def _build_scan_overlay(self):
        self._scan_overlay = QFrame(self)
        self._scan_overlay.setObjectName("scan_overlay")
        self._scan_overlay.setStyleSheet(
            "QFrame#scan_overlay { background-color: #ffffff;"
            " border: 3px solid #b0b0b0; border-radius: 14px; }"
        )
        ov_lay = QHBoxLayout(self._scan_overlay)
        ov_lay.setContentsMargins(28, 18, 28, 18)
        ov_lay.setSpacing(12)
        ov_text = QLabel(t("Vyksta skenavimas"))
        ov_text.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #222; border: none;")
        self._overlay_text = ov_text
        self._overlay_spin = QLabel("|")
        self._overlay_spin.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #3c4e99; border: none;")
        ov_lay.addWidget(ov_text)
        ov_lay.addWidget(self._overlay_spin)
        self._scan_overlay.hide()
        self._work_t0 = None
        self._spin_frames = "|/-\\"
        self._spin_idx = 0
        self._spin_timer = QTimer(self)
        self._spin_timer.setInterval(120)
        self._spin_timer.timeout.connect(self._spin_tick)

    def _spin_tick(self):
        self._spin_idx = (self._spin_idx + 1) % len(self._spin_frames)
        self._overlay_spin.setText(self._spin_frames[self._spin_idx])
        # Fazes laikrodis kampe - tiksi visada, net kai darbininkas tyli
        if self._work_t0:
            el = int(time.time() - self._work_t0)
            self.elapsed_label.setText(
                f"{t('veikia')} {el // 60:02d}:{el % 60:02d} •")

    def _position_scan_overlay(self):
        self._scan_overlay.adjustSize()
        w = self._scan_overlay.width()
        h = self._scan_overlay.height()
        # 1/6 aukscio - katalogu saraso zonoje, kad neuzdengtu progreso juostos
        self._scan_overlay.move((self.width() - w) // 2,
                                (self.height() - h) // 6)

    def _show_scan_overlay(self, text=None):
        self._overlay_text.setText(text or t("Vyksta skenavimas"))
        self._work_t0 = time.time()
        self._position_scan_overlay()
        self._scan_overlay.show()
        self._scan_overlay.raise_()
        self._spin_timer.start()

    def _hide_scan_overlay(self):
        self._spin_timer.stop()
        self._scan_overlay.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        ov = getattr(self, "_scan_overlay", None)
        if ov is not None and ov.isVisible():
            self._position_scan_overlay()

    # ---- Kaire: vertikali mygtuku juosta ----
    def _build_left_bar(self):
        bar = QWidget(); bar.setFixedWidth(180)
        lay = QVBoxLayout(bar)
        lay.setSpacing(12)
        la = QLabel("Duplicate Finder")
        la.setFont(_title_font()); lay.addWidget(la); lay.addSpacing(8)

        def _add_buttons(defs):
            for txt, cb, name in defs:
                b = QPushButton(txt); b.setMinimumHeight(38)
                b.setObjectName(name)
                setattr(self, name, b)
                b.clicked.connect(cb); lay.addWidget(b)

        # Virsuje - katalogu sarasa valdantys mygtukai
        _add_buttons([
            (t("+   Prideti katalogus"), self._on_add, "btn_add"),
            (t("-   Pasalinti pasirinktus"), self._on_remove, "btn_remove"),
        ])
        # Zemiau - ties rezultatu lentele
        lay.addStretch(1)
        _add_buttons([
            (t(">>> Skenuoti"), self._on_scan, "btn_scan"),
            (t("Eksportuoti ataskaita"), self._on_export, "btn_export"),
            (t("Salinti siuksles"), self._on_junk, "btn_junk"),
        ])
        self.btn_junk.setEnabled(False)
        lay.addStretch(2)

        # Portable varnele (2026-08-06, bendras abieju dovanu sprendimas:
        # Roberto ideja + SDF_portable.txt zymeklis salia exe, zr. saugykla.py)
        import saugykla
        self.chk_portable = QCheckBox(t("Portable rezimas"))
        self.chk_portable.setObjectName("chk_portable")
        self.chk_portable.setChecked(saugykla.is_portable())
        self.chk_portable.setToolTip(t(
            "Ijungta: kesas ir zurnalas saugomi salia programos (pvz., "
            "flesiuke) - kompiuteryje pedsaku nelieka.\n"
            "Isjungta (numatyta): saugoma vartotojo kataloge "
            "%LOCALAPPDATA%\\SmartDuplicateFinder."))
        self.chk_portable.toggled.connect(self._on_portable_toggled)
        lay.addWidget(self.chk_portable)

        # Kalbos pasirinkimas (2026-08-06, Roberto pastaba "du exe del
        # kalbos - negrazu"): vienas exe, pasirinkimas kalba.txt faile,
        # isigalioja perleidus programa.
        from PyQt6.QtWidgets import QComboBox
        from kalba import LANG as _dabartine_kalba
        self.cmb_kalba = QComboBox()
        self.cmb_kalba.setObjectName("cmb_kalba")
        self.cmb_kalba.addItem("Lietuvi\u0173", "lt")   # rodo "Lietuviu" su u-nosine
        self.cmb_kalba.addItem("English", "en")
        # v1.3 (2026-08-22): RU (viesas "Ernis" pazadas Telegram 08-13)
        # ir DE (Vokietijos rinka); UA atideta Roberto verdiktu 08-22.
        self.cmb_kalba.addItem(
            "\u0420\u0443\u0441\u0441\u043a\u0438\u0439", "ru")  # "Russkij" kirilica
        self.cmb_kalba.addItem("Deutsch", "de")
        _idx = self.cmb_kalba.findData(_dabartine_kalba)
        self.cmb_kalba.setCurrentIndex(_idx if _idx >= 0 else 0)
        self.cmb_kalba.setToolTip(t(
            "Kalba pritaikoma paleidus programa is naujo."))
        self.cmb_kalba.currentIndexChanged.connect(self._on_kalba_changed)
        lay.addWidget(self.cmb_kalba)
        return bar

    def _perleisti_programa(self):
        """Paleidzia nauja programos kopija ir uzdaro sia (kalbos keitimui).

        PyInstaller onefile SPASTAS (Roberto gyvas testas 2026-08-06):
        vaikas paveldi _PYI*/_MEIPASS2 env ir naudoja TEVO _MEI kataloga;
        tevas ji istrina -> kitas restartas luzta 'Failed to start
        embedded python interpreter'. Env isvalomas - vaikas issipakuoja
        SAVO kopija.
        """
        import subprocess
        env = {k: v for k, v in os.environ.items()
               if k != "_MEIPASS2" and not k.startswith("_PYI")}
        if getattr(sys, "frozen", False):
            subprocess.Popen(
                [sys.executable], env=env,
                cwd=str(Path(sys.executable).resolve().parent))
        else:
            subprocess.Popen([sys.executable] + sys.argv, env=env)
        QApplication.instance().quit()

    def _on_kalba_changed(self, _idx):
        """Kalbos pasirinkimas: irasomas i kalba.txt + pasiulomas perleidimas.

        Roberto pastaba 2026-08-06: "gal geriau pati restartuotu, painiavos
        maziau" - Taip perleidzia is karto, Ne pritaiko kita karta.
        """
        from kalba import issaugoti_kalba
        try:
            issaugoti_kalba(self.cmb_kalba.currentData())
        except OSError as e:
            QMessageBox.warning(
                self, t("Kalba"), t("Nepavyko issaugoti: {}").format(e))
            return
        reply = QMessageBox.question(
            self, t("Kalba"),
            t("Kalba issaugota. Perleisti programa dabar?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self._perleisti_programa()

    def _on_portable_toggled(self, on):
        """Portable varnele: saugyklos perjungimas (zr. saugykla.py).

        Nepavykus (pvz., read-only flesiukas) - varnele grazinama atgal
        (blockSignals, kad atstatymas nesuktu antro perjungimo).
        """
        import saugykla
        ok, err = saugykla.set_portable(on)
        if not ok:
            QMessageBox.warning(
                self, t("Portable rezimas"),
                t("Nepavyko perjungti rezimo: {}").format(err))
            self.chk_portable.blockSignals(True)
            self.chk_portable.setChecked(not on)
            self.chk_portable.blockSignals(False)
            return
        self.status_label.setText(
            t("Portable rezimas IJUNGTAS - duomenys salia programos") if on
            else t("Portable rezimas isjungtas - duomenys vartotojo kataloge"))

    # ---- "?" pagalbos kampelis (2026-08-07, Roberto ideja: winget/Store
    # vartotojas readme negauna, tad instrukcija gyvena pacioje programoje) ----
    def _build_help_button(self):
        from PyQt6.QtWidgets import QMenu
        b = QPushButton("?")
        b.setObjectName("btn_help")
        b.setFixedSize(26, 26)
        b.setToolTip(t("Pagalba"))
        meniu = QMenu(b)
        meniu.addAction(t("Apie..."), self._on_apie)
        meniu.addAction(t("Instrukcija"), self._on_instrukcija)
        meniu.addAction(t("Neradote atsakymo? Klauskite DI"),
                        self._on_klausk_di)
        b.setMenu(meniu)
        return b

    def _on_klausk_di(self):
        """Atidaro claude.ai su paruostu promptu (Roberto ideja
        2026-08-08, receptas is FOTO namu spr. 40): programa rase
        Claude, tad claude.ai atsakys tiksliausiai. claude.ai/new?q=
        tik UZPILDO lauka - siuncia pats vartotojas; pries narsykle -
        paaiskinamasis langas su logotipu ('mociuciu instrukcija':
        raudona juosta, kur rasyti klausima, kaip pakeisti kalba).
        Promptas VISADA anglu k. su TIKSLIA repo nuoroda (gyvo testo
        pamoka: is profilio nuorodos DI programos nerado). Tinklas
        TIK vartotojui paspaudus OK."""
        import urllib.parse
        import webbrowser
        dlg = QMessageBox(self)
        dlg.setWindowTitle(t("Neradote atsakymo? Klauskite DI"))
        ico = _res_path("app.ico")
        if ico.exists():
            dlg.setIconPixmap(QIcon(str(ico)).pixmap(64, 64))
        dlg.setText(t(
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
            "paskyra). Niekas neissiunciama be jusu rankos."))
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok
                               | QMessageBox.StandardButton.Cancel)
        if dlg.exec() != QMessageBox.StandardButton.Ok:
            return
        # 2026-08-22 gyvo testo pamoka: be tiesioginio paminejimo debesinis
        # skaito TIK README ir brief'o (antihaliucinacinio protokolo)
        # neatranda - todel jis ivardijamas PIRMAS.
        promptas = (
            'Hi! I am using the app "Smart Duplicate Finder" - a'
            " duplicate file finder. Its source code is public:"
            " https://github.com/RobertasTa/smart-duplicate-finder."
            " Please FIRST read the file AI_CONSULTANT_BRIEF.md in that"
            " repository - it is your briefing from the author - then the"
            " program's code and README, and answer my question in plain,"
            " human language - no programmer jargon."
            " My question: ")
        webbrowser.open("https://claude.ai/new?q="
                        + urllib.parse.quote(promptas))

    def _on_apie(self):
        """Apie... langelis (Roberto dizainas 2026-08-07): logo,
        pavadinimas, aprasas, versija, GitHub nuoroda apacioje.
        Tinklas TIK vartotojui paspaudus nuoroda (offline DNR)."""
        from PyQt6.QtWidgets import QDialog, QDialogButtonBox
        dlg = QDialog(self)
        dlg.setWindowTitle(t("Apie programa"))
        lay = QVBoxLayout(dlg)
        virsus = QHBoxLayout()
        logo = QLabel()
        ico = _res_path("app.ico")
        if ico.exists():
            logo.setPixmap(QIcon(str(ico)).pixmap(64, 64))
        virsus.addWidget(logo, alignment=Qt.AlignmentFlag.AlignTop)
        info = QVBoxLayout()
        pavadinimas = QLabel("Smart Duplicate Finder")
        pavadinimas.setStyleSheet("font-size: 14pt; font-weight: bold;")
        info.addWidget(pavadinimas)
        info.addWidget(QLabel(
            t("Dubliuotu failu paieska pagal turini - nieko netrina.")))
        info.addWidget(QLabel(t("Versija {v}").format(v=VERSIJA)))
        autoriai = QLabel("Robertas & Claude")
        autoriai.setStyleSheet("color: #5a5e6b;")
        info.addWidget(autoriai)
        virsus.addLayout(info)
        lay.addLayout(virsus)
        # Ryski melyna + bold, kad matytusi jog spaudziama (Roberto
        # pastaba 2026-08-07: numatytoji nuorodos spalva per tamsi)
        nuoroda = QLabel(
            t("Kurejo puslapis:") + ' <a href="https://github.com/'
            'RobertasTa/smart-duplicate-finder" style="color:#2f7ce0;'
            'font-weight:bold;">GitHub</a>')
        nuoroda.setOpenExternalLinks(True)
        lay.addWidget(nuoroda)
        mygtukai = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        mygtukai.rejected.connect(dlg.reject)
        lay.addWidget(mygtukai)
        dlg.exec()

    def _on_instrukcija(self):
        """Instrukcija: exe viduje ikeptas README (LT/EN pagal GUI kalba)
        rodomas pacios programos lange su slinktimi (Roberto pastaba
        2026-08-07: Notepad atsidarydavo tuscias - jokiu isoriniu
        programu ir jokiu failu kopiju diske)."""
        from PyQt6.QtWidgets import QDialog, QPlainTextEdit, QDialogButtonBox
        from kalba import LANG
        vardas = {"lt": "README.txt", "ru": "README-ru.txt",
                  "de": "README-de.txt"}.get(LANG, "README-en.txt")
        kelias = _res_path(vardas)
        if not kelias.exists():
            # Senas buildas be ru/de zinyno - atsarga EN
            kelias = _res_path("README-en.txt")
        try:
            tekstas = kelias.read_text(
                encoding="utf-8", errors="replace")
        except OSError as e:
            QMessageBox.warning(
                self, t("Pagalba"), t("Nepavyko atidaryti: {}").format(e))
            return
        dlg = QDialog(self)
        dlg.setWindowTitle(t("Instrukcija"))
        lay = QVBoxLayout(dlg)
        rodinys = QPlainTextEdit(tekstas)
        rodinys.setReadOnly(True)
        # Monospace - kad README ASCII antrastes lygiuotusi
        rodinys.setFont(QFont("Consolas", 10))
        lay.addWidget(rodinys)
        mygtukai = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        mygtukai.rejected.connect(dlg.reject)
        lay.addWidget(mygtukai)
        dlg.resize(780, 560)
        dlg.exec()

    # ---- Desineje: katalogu sarasas + lentele ----
    def _build_right_area(self):
        w = QWidget(); lay = QVBoxLayout(w)
        virsus = QHBoxLayout()
        virsus.addWidget(_hdr(t("Itraukti katalogai:")))
        virsus.addStretch(1)
        virsus.addWidget(self._build_help_button())
        lay.addLayout(virsus)
        self.folder_list = QListWidget()
        self.folder_list.setMinimumHeight(80); lay.addWidget(self.folder_list)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False); lay.addWidget(self.progress_bar)
        self.status_label = QLabel(t("Prideti katalogus ir spauskite 'Skenuoti'."))
        self.status_label.setWordWrap(True); lay.addWidget(self.status_label)
        lay.addWidget(_hdr(t("Rezultatai:")))
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            t("Failo vardas"), t("Pilnas kelias"), t("Dydis (MB)"),
            t("Sukurimo data"), t("Grupe")])
        # Pradiniai plociai; "Pilnas kelias" tempiasi per likusi plota
        self.results_table.setColumnWidth(0, 220)
        self.results_table.setColumnWidth(2, 90)
        self.results_table.setColumnWidth(3, 140)
        self.results_table.setColumnWidth(4, 90)
        self.results_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch)
        # 2026-08-06: ilgi keliai buvo rodomi "C:..." (Roberto laptopo
        # skrinas) - numatytas wordWrap=True lauzo kelia ties '\' ir
        # isjungia elidinima; be wrap ElideMiddle rodo pradzia...galas
        # (patikrinta izoliuotu testu Temp Cleaner dovanoje).
        self.results_table.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.results_table.setWordWrap(False)
        self.results_table.cellDoubleClicked.connect(self._on_open_folder)
        # v1.3 desinio klaviso meniu (Roberto sprendimas 2026-08-22;
        # receptas is TC v2 "Kas tai?" meniu). Double-click nekeiciamas.
        self.results_table.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.results_table.customContextMenuRequested.connect(
            self._on_context_menu)
        lay.addWidget(self.results_table, 1); return w

    # ---- Mygtuku veiksmai ----
    def _on_add(self):
        from add_dialog import AddFoldersDialog as Dialog
        d = Dialog(self)
        if d.exec() == Dialog.DialogCode.Accepted:
            for fp in d.get_selected_paths():
                if fp not in self.folders:
                    self.folders.append(fp)
                    self.folder_list.addItem(QListWidgetItem(fp))

    def _on_remove(self):
        for item in self.folder_list.selectedItems():
            fp = item.text()
            if fp in self.folders: self.folders.remove(fp)
            self.folder_list.takeItem(self.folder_list.row(item))

    # ---- Skenavimas: 2 fazes (zvalgyba -> dialogas -> gilus MD5) ----
    def _start_worker(self, worker, connections):
        """Bendras QThread paleidimas (pyqt6_threading_guard)."""
        if self._thread is not None and self._thread.isRunning():
            self._thread.quit(); self._thread.wait(1000)
        from scan_worker import create_scan_thread
        self._worker = worker
        for sig, slot in connections:
            sig.connect(slot, Qt.ConnectionType.QueuedConnection)
        thread = create_scan_thread(worker)
        self._thread = thread
        thread.started.connect(worker.run)
        thread.start()

    def _on_scan(self):
        from scan_worker import SizeScanWorker

        if not self.folders:
            self.status_label.setText(t("Pirma prideti bent viena kataloga.")); return
        self._log(f"ZVALGYBA start: {self.folders}")
        self.progress_bar.setVisible(True); self.progress_bar.setValue(0)
        self.status_label.setText(t("Zvalgyba: renkami failu dydziai..."))
        self.results_table.setRowCount(0)
        self.btn_scan.setEnabled(False)
        self._show_scan_overlay()

        worker = SizeScanWorker(self.folders)
        self._start_worker(worker, [
            (worker.sizeScanDone, self._on_candidates),
            (worker.updateStats, self.stats_label.setText),
            (worker.scanError, self._on_scan_error),
        ])

    def _scan_idle(self, msg):
        """Grazina UI i ramybes busena su zinute."""
        self.status_label.setText(msg)
        self.progress_bar.setVisible(False)
        self._hide_scan_overlay()
        self.btn_scan.setEnabled(True)
        if self._thread is not None:
            self._thread.quit()

    def _on_scan_error(self, exc):
        self._log(f"KLAIDA: {exc}")
        self._scan_idle(f"{t('Klaida:')} {exc}")

    def _on_candidates(self, data):
        """Po 1 fazes: sugrupuoja kandidatus pagal seimas ir rodo dialoga."""
        from collections import Counter, defaultdict
        from table_populator import family_of, FAMILY_ORDER
        from select_dialog import SelectFamiliesDialog

        if self._thread is not None:
            self._thread.quit()
        self._hide_scan_overlay()

        self._all_files = data["files"]
        self._skipped = data["skipped"]
        candidates = data["candidates"]
        # Windows/Mac siuksles - aktyvuojam mygtuka (veikia ir atsaukus dialoga)
        self._junk = data.get("junk") or []
        junk_mb = sum(s for _, s in self._junk) / 1048576
        self.btn_junk.setText(f"{t('Salinti siuksles')} ({len(self._junk)})"
                              if self._junk else t("Salinti siuksles"))
        self.btn_junk.setEnabled(bool(self._junk))
        self._log(f"ZVALGYBA done: {len(self._all_files)} failu, "
                  f"{self._skipped} praleista, {len(candidates)} kandidatu grupiu, "
                  f"{len(self._junk)} siuksliu ({junk_mb:.1f} MB)")
        skip_txt = (t(", {n} praleista").format(n=self._skipped)
                    if self._skipped else "")
        # Vizualiam lyginimui - VISI paveiksliukai (skaiciuojama anksti, nes
        # dialogas rodomas NET be MD5 kandidatu, jei yra nuotrauku)
        vis_files_early = [fl for fl in self._all_files
                           if family_of(Path(fl[0]).suffix) == "Paveiksliukai"]
        if not candidates and not vis_files_early:
            self._scan_idle(t("Dubliu kandidatu nerasta ({n} failu perziureta{skip}).")
                            .format(n=len(self._all_files), skip=skip_txt))
            return

        # Grupes seima - pagal nariu dauguma (grupeje gali but skirtingi pletiniai)
        grouped = defaultdict(lambda: {"groups": 0, "files": 0,
                                       "bytes": 0, "cands": []})
        for size, paths in candidates:
            fam = Counter(family_of(Path(p).suffix)
                          for p in paths).most_common(1)[0][0]
            g = grouped[fam]
            g["groups"] += 1
            g["files"] += len(paths)
            g["bytes"] += size * len(paths)
            g["cands"].append((size, paths))

        summary = [{"family": f, "groups": grouped[f]["groups"],
                    "files": grouped[f]["files"], "bytes": grouped[f]["bytes"]}
                   for f in FAMILY_ORDER if f in grouped]

        # Vizualiam lyginimui - VISI paveiksliukai (ne tik dydzio kandidatai:
        # sumazintos kopijos dydziu nesutampa!)
        vis_files = vis_files_early

        dlg = SelectFamiliesDialog(summary, self._load_speed(), self,
                                   visual_count=len(vis_files))
        if dlg.exec() != SelectFamiliesDialog.DialogCode.Accepted:
            self._scan_idle(t("Skenavimas atsauktas."))
            return
        chosen = dlg.get_selected_families()
        vizualas = "_VIZUALAS" in chosen
        chosen.discard("_VIZUALAS")
        # Galima tikrinti VIEN vizuala (pvz. kataloge nera MD5 kandidatu)
        if not chosen and not vizualas:
            self._scan_idle(t("Nepazymeta ne viena seima - skenavimas atsauktas."))
            return
        self._log(f"DIALOGAS: pasirinkta {sorted(chosen)}"
                  + (" + VIZUALAS" if vizualas else ""))
        sel_cands = [c for f in chosen for c in grouped[f]["cands"]]
        # ITARTINI ieskoma tik pasirinktu seimu failuose
        sel_files = [fl for fl in self._all_files
                     if family_of(Path(fl[0]).suffix) in chosen]
        self._start_deep_scan(sel_cands, sel_files,
                              vis_files if vizualas else [])

    def _start_deep_scan(self, candidates, suspect_files, visual_files=None):
        from scan_worker import DeepScanWorker

        gb = sum(s * len(ps) for s, ps in candidates) / 1024**3
        self._log(f"GILUS start: {len(candidates)} grupiu ({gb:.2f} GB), "
                  f"ITARTINI baze {len(suspect_files)} failu, "
                  f"vizualas {len(visual_files or [])} nuotrauku")
        self.status_label.setText(t("Gilus tikrinimas (MD5 pagal turini)..."))
        self._show_scan_overlay()
        worker = DeepScanWorker(candidates, suspect_files,
                                len(self._all_files), visual_files)
        self._start_worker(worker, [
            (worker.updateProgress, self.progress_bar.setValue),
            (worker.updateStats, self.stats_label.setText),
            (worker.scanDone, self._on_deep_done),
            (worker.scanError, self._on_scan_error),
        ])

    def _on_deep_done(self, data):
        self.scan_results = {
            "stats": data["stats"],
            "groups": data["groups"]
        }
        self.suspect_results = data["suspects"]
        self.visual_results = data.get("visual") or []
        self._sizes = data.get("sizes") or {}
        st0 = data["stats"]
        self._log(f"GILUS done: {st0['duplicate_groups']} grupiu, "
                  f"{st0['duplicated_mb']:.0f} MB dubliu "
                  f"(atlaisvinama {st0.get('freeable_mb', 0):.0f} MB), "
                  f"{len(self.suspect_results)} ITARTINI poru"
                  f"{' (NUKIRPTA)' if data.get('suspects_truncated') else ''}, "
                  f"{len(self.visual_results)} vizualiu grupiu, "
                  f"greitis {data.get('speed_mbs', 0)} MB/s")
        # Kesas PRIES lentele: jei vartotojas nudobtu programa lentelei pildantis,
        # rezultatai jau issaugoti
        if data.get("speed_mbs"):
            self._save_speed(data["speed_mbs"])
        self._save_cache()
        t_populate = time.time()
        from table_populator import populate_table
        populate_table(self.results_table,
                       self.scan_results, self.suspect_results, self._sizes,
                       visual=self.visual_results)
        self._log(f"LENTELE: {self.results_table.rowCount()} eiluciu "
                  f"per {time.time() - t_populate:.1f} s")
        st = data["stats"]
        msg = t("Skeniruota {n} failu is {k} katalogu - {g} dublikatu grupes: "
                "dubliai uzima {mb:.2f} MB, atlaisvinti galima {fmb:.2f} MB"
                ).format(n=st['total_files'], k=len(self.folders),
                         g=st['duplicate_groups'],
                         mb=st['duplicated_mb'],
                         fmb=st.get('freeable_mb', 0.0))
        if self._skipped:
            msg += t("; praleista {n} nepasiekiamu failu").format(n=self._skipped)
        if self.visual_results:
            msg += t("; vizualiai panasiu grupiu: {n}").format(
                n=len(self.visual_results))
        if data.get("suspects_truncated"):
            from duplicate_engine import MAX_SUSPECT_PAIRS
            msg += t("; ITARTINI sarasas nukirptas ties {n} poru riba "
                     "(susiaurink katalogus, jei nori visu)").format(
                n=MAX_SUSPECT_PAIRS)
        self._scan_idle(msg)

    # ---- Disko greicio prisiminimas laiko prognozei (scan_speed.json) ----
    def _load_speed(self):
        import json
        try:
            with open(_cache_dir() / "scan_speed.json", encoding="utf-8") as fh:
                return float(json.load(fh).get("mbs", 150.0))
        except (OSError, ValueError, TypeError):
            return 150.0

    def _save_speed(self, mbs):
        import json
        if not mbs or mbs <= 0:
            return
        try:
            with open(_cache_dir() / "scan_speed.json", "w", encoding="utf-8") as fh:
                json.dump({"mbs": mbs}, fh)
        except OSError:
            pass

    def _on_open_folder(self, row, col):
        """Dvigubas klikas ant dublio eilutes - atidaro kataloga Explorer'yje
        su pazymetu failu. Antrasciu eilutes neturi kelio - ignoruojamos."""
        item = self.results_table.item(row, 0)
        if item is None:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        if not path:
            return
        path = os.path.normpath(path)
        if os.path.exists(path):
            # Viena eilute su kabutemis TIK aplink kelia - su sarasu subprocess
            # apkabintu visa '/select,kelia' ir Explorer atidarytu ne ta kataloga
            subprocess.Popen(f'explorer /select,"{path}"')
        else:
            self.status_label.setText(f"{t('Failas neberastas:')} {path}")

    def _on_context_menu(self, pos):
        """v1.3 desinio klaviso meniu ant dublio eilutes (receptas is TC v2
        "Kas tai?" meniu; Roberto sprendimas 2026-08-22).

        "Atidaryti faila" - numatyta programa (os.startfile), vykdomiesiems
        pletiniams punktas NEAKTYVUS (zr. _VYKDOMIEJI). "Atidaryti kataloga"
        = tas pats, kaip dvigubas klikas. "Kopijuoti kelia" - konsultacijoms
        (pvz., "Klausk DI"). Antrasciu eilutes kelio neturi - ignoruojamos.
        """
        row = self.results_table.rowAt(pos.y())
        if row < 0:
            return
        item = self.results_table.item(row, 0)
        if item is None:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        if not path:
            return
        path = os.path.normpath(path)
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction
        menu = QMenu(self)
        act_file = QAction(t("Atidaryti faila"), self)
        act_file.setEnabled(
            os.path.splitext(path)[1].lower() not in _VYKDOMIEJI)
        act_dir = QAction(t("Atidaryti kataloga"), self)
        act_copy = QAction(t("Kopijuoti kelia"), self)
        menu.addAction(act_file)
        menu.addAction(act_dir)
        menu.addSeparator()
        menu.addAction(act_copy)
        chosen = menu.exec(self.results_table.viewport().mapToGlobal(pos))
        if chosen is act_file:
            if not os.path.exists(path):
                self.status_label.setText(f"{t('Failas neberastas:')} {path}")
                return
            try:
                os.startfile(path)
            except OSError as e:
                self.status_label.setText(f"{t('Klaida:')} {e}")
        elif chosen is act_dir:
            self._on_open_folder(row, 0)
        elif chosen is act_copy:
            QApplication.clipboard().setText(path)
            self.status_label.setText(t("Kelias nukopijuotas"))

    # ---- Windows/Mac siuksliu salinimas (Thumbs.db, .DS_Store ir pan.) ----
    def _on_junk(self):
        junk = getattr(self, "_junk", None)
        if not junk:
            self.status_label.setText(t("Siuksliu nerasta - pirma atlik zvalgyba."))
            return
        from collections import Counter
        mb = sum(s for _, s in junk) / 1048576
        pagal_varda = Counter(os.path.basename(p) for p, _ in junk)
        israsas = "\n".join(f"   {n}: {c}"
                            for n, c in pagal_varda.most_common(6))
        atsakymas = QMessageBox.question(
            self, t("Salinti Windows/Mac siuksles?"),
            t("Rasta {n} sistemos siuksliu ({mb:.1f} MB):").format(n=len(junk), mb=mb)
            + f"\n{israsas}\n\n"
            + t("Tai miniaturu/narsymo kesai - OS juos atsikuria pati.\n"
                "Pries trynima kiekvienam failui tikrinamas turinio parasas;\n"
                "neatitinkantys NEBUS trinami.\n\n"
                "DEMESIO: tinklo diskuose (NAS) trynimas negriztamas\n"
                "(siuksliadeze ten neveikia). Trinti?"))
        if atsakymas != QMessageBox.StandardButton.Yes:
            self.status_label.setText(t("Siuksliu salinimas atsauktas."))
            return
        from scan_worker import JunkWorker
        self._log(f"SIUKSLES start: {len(junk)} failu ({mb:.1f} MB)")
        self.btn_junk.setEnabled(False)
        self._show_scan_overlay(t("Salinamos siuksles"))
        worker = JunkWorker(junk)
        self._start_worker(worker, [
            (worker.updateStats, self.stats_label.setText),
            (worker.junkDone, self._on_junk_done),
            (worker.scanError, self._on_scan_error),
        ])

    def _on_junk_done(self, data):
        freed_mb = data["freed"] / 1048576
        self._log(f"SIUKSLES done: istrinta {data['deleted']}, "
                  f"praleista {data['skipped']}, atlaisvinta {freed_mb:.1f} MB")
        self._hide_scan_overlay()
        self._junk = []
        self.btn_junk.setText(t("Salinti siuksles"))
        msg = t("Istrinta {n} siuksliu, atlaisvinta {mb:.1f} MB").format(
            n=data['deleted'], mb=freed_mb)
        if data["skipped"]:
            msg += t("; praleista {n} (parasas nesutapo arba failas uzrakintas)"
                     ).format(n=data['skipped'])
        if self._thread is not None:
            self._thread.quit()
        self.status_label.setText(msg)

    def _on_export(self):
        from PyQt6.QtCore import QStandardPaths
        from PyQt6.QtWidgets import QFileDialog

        # Eksportuoti galima, kai yra BET KOKIU rezultatu: MD5 dubliu,
        # ITARTINI arba vizualiu (pvz. demo kataloge MD5 grupiu 0)
        turi_rezultatu = (self.scan_results and self.scan_results.get("groups")) \
            or getattr(self, "suspect_results", None) \
            or getattr(self, "visual_results", None)
        if not turi_rezultatu:
            self.status_label.setText(t("Pirma atlikti skana.")); return
        if not self.scan_results:
            self.scan_results = {"groups": [], "stats": {}}
        # "Kur issaugoti?" dialogas (is flekes/Program Files salia exe rasyti negalima)
        docs = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation) or str(_app_dir())
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        siulomas = os.path.join(docs, f"duplicate_report_{ts}.xlsx")
        target, _ = QFileDialog.getSaveFileName(
            self, t("Kur issaugoti ataskaita?"), siulomas,
            t("Excel failai (*.xlsx)"))
        if not target:
            self.status_label.setText(t("Eksportas atsauktas.")); return
        # Fone - kad GUI nesustingtu su dideliais rezultatais
        from scan_worker import ExportWorker
        self._log(f"EKSPORTAS start: {target}")
        self._export_t0 = time.time()
        self.status_label.setText(t("Exportuojama..."))
        self.btn_export.setEnabled(False)
        self._show_scan_overlay(t("Formuojama ataskaita"))
        worker = ExportWorker(self.scan_results,
                              self.suspect_results if hasattr(self, 'suspect_results') else [],
                              target, getattr(self, "_sizes", None),
                              getattr(self, "visual_results", None))
        self._start_worker(worker, [
            (worker.exportDone, self._on_export_done),
            (worker.scanError, self._on_export_error),
        ])

    def _on_export_done(self, p):
        self._log(f"EKSPORTAS done per "
                  f"{time.time() - getattr(self, '_export_t0', time.time()):.1f} s: {p}")
        self._hide_scan_overlay()
        self.btn_export.setEnabled(True)
        self.status_label.setText(f"{t('Ataskaita sukurta:')} {Path(p).name}")
        if self._thread is not None:
            self._thread.quit()
        QMessageBox.information(self, t("Eksportas sekmingas"),
                                f"{t('Ataskaita sukurta:')}\n{p}")

    def _on_export_error(self, exc):
        self._hide_scan_overlay()
        self.btn_export.setEnabled(True)
        self.status_label.setText(f"{t('Exporto klaida:')} {exc}")
        if self._thread is not None:
            self._thread.quit()

    # ---- Thread cleanup on close (pyqt6_threading_guard) ----
    def closeEvent(self, event):
        if self._thread is not None and getattr(self._thread, 'isRunning', lambda: False)():
            self._thread.quit(); self._thread.wait(1000)
        super().closeEvent(event)


# === Entry point (GUARD: app.exec() tik cia) ===
if __name__ == "__main__":
    app = QApplication.instance() or QApplication([])
    win = MainWindow(); win.show(); app.exec()