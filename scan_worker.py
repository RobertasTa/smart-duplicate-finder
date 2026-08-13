"""
scan_worker.py - Foniniai skeneriai (2 faziu schema, 2026-08-05)
Ploni QObject'ai, nekopijuoja duplicate_engine logikos.
QThread on demand (PYQT6_THREADING_GUARD).

1 faze: SizeScanWorker - greita zvalgyba (tik metaduomenys, be turinio).
2 faze: DeepScanWorker - MD5 pasirinktu seimu kandidatams + ITARTINI.
"""
import time

from PyQt6.QtCore import QObject, pyqtSignal

from kalba import t as _t


def _fmt_gb(nbytes):
    if nbytes >= 1024**3:
        return f"{nbytes / 1024**3:.2f} GB"
    return f"{nbytes / 1024**2:.0f} MB"


def _fmt_eta(seconds):
    if seconds < 90:
        return f"~{int(seconds)} s"
    if seconds < 5400:
        return f"~{int(round(seconds / 60))} min"
    return f"~{seconds / 3600:.1f} val"


class SizeScanWorker(QObject):
    """1 FAZE: failu sarasas + grupavimas pagal dydi. Sekundes, ne minutes."""

    sizeScanDone = pyqtSignal(dict)   # {files, skipped, candidates}
    updateStats = pyqtSignal(str)     # gyvas skaitliukas statusbar kampe
    scanError = pyqtSignal(str)

    def __init__(self, folders):
        super().__init__()
        self.folders = list(folders)

    def run(self):
        try:
            from duplicate_engine import (scan_folders_stats, size_candidates,
                                          find_junk, is_junk_name)

            def _cb(found):
                self.updateStats.emit(
                    _t("Zvalgyba: {n} failu...")
                    .format(n=f"{found:,}").replace(",", " "))

            files, skipped = scan_folders_stats(self.folders, progress_cb=_cb)
            # Windows/Mac siuksles (Thumbs.db ir pan.) - atskirai: i dubliu
            # rezultatus nepatenka, bet siulomos isvalymui
            junk = find_junk(files)
            if junk:
                files = [fl for fl in files if not is_junk_name(fl[0])]
            candidates = size_candidates(files)
            self.sizeScanDone.emit({
                "files": files,
                "skipped": skipped,
                "candidates": candidates,
                "junk": junk,
            })
        except Exception as exc:
            self.scanError.emit(str(exc))


class DeepScanWorker(QObject):
    """2 FAZE: MD5 kandidatu grupese + ITARTINI paieska pasirinktiems failams.
    Progresas pagal perskaitytus baitus; matuojamas disko greitis (MB/s)."""

    updateProgress = pyqtSignal(int)  # progress % 0-100
    updateStats = pyqtSignal(str)     # gyvas skaitliukas statusbar kampe
    scanDone = pyqtSignal(dict)       # {stats, groups, suspects, speed_mbs}
    scanError = pyqtSignal(str)

    def __init__(self, candidates, suspect_files, total_files, visual_files=None):
        super().__init__()
        self.candidates = list(candidates)
        self.suspect_files = list(suspect_files)
        self.total_files = total_files
        # Vizualus lyginimas (dHash) - tik jei vartotojas pazymejo dialoge
        self.visual_files = list(visual_files or [])

    def run(self):
        try:
            from duplicate_engine import hash_groups, find_suspects

            t0 = time.time()
            last_pct = [-1]
            files_done = [0]
            files_total = sum(len(ps) for _, ps in self.candidates)

            def _cb(done, total):
                # Dubliu tikrinimas - 0..85% juostos
                files_done[0] += 1
                pct = int(done * 85 / total) if total else 85
                pct_changed = pct != last_pct[0]
                if pct_changed:
                    last_pct[0] = pct
                    self.updateProgress.emit(pct)
                # Kampo skaitliukas: ir per procento suoli, IR kas 1000 failu
                # (smulkiu failu tukstanciai gali praeiti tarp procentu)
                if pct_changed or files_done[0] % 1000 == 0:
                    elapsed = time.time() - t0
                    if elapsed > 0.5:
                        speed = done / (1024 * 1024) / elapsed
                        eta = (total - done) / (1024 * 1024) / speed if speed else 0
                        self.updateStats.emit(
                            (_t("{f}/{ft} failu")
                             .format(f=f"{files_done[0]:,}",
                                     ft=f"{files_total:,}")
                             + f" • {_fmt_gb(done)}/{_fmt_gb(total)} • "
                             f"{speed:.0f} MB/s • {_t('liko')} {_fmt_eta(eta)}")
                            .replace(",", " "))

            results = hash_groups(self.candidates,
                                  total_files=self.total_files,
                                  progress_cb=_cb)
            self.updateProgress.emit(85)

            # ITARTINI: 85..95% juostos ruozas gyvas (nebe "pakibes" spinneris)
            last_sus = [-1]

            def _sus_cb(done, total):
                pct = 85 + (int(done * 10 / total) if total else 10)
                if pct != last_sus[0]:
                    last_sus[0] = pct
                    self.updateProgress.emit(pct)
                    self.updateStats.emit(
                        _t("ITARTINI paieska: {a}/{b} failu")
                        .format(a=f"{done:,}", b=f"{total:,}")
                        .replace(",", " "))

            suspects, suspects_truncated = find_suspects(
                self.suspect_files, progress_cb=_sus_cb)
            self.updateProgress.emit(95)

            # Vizualiai panasios nuotraukos (95..99%), jei pazymeta dialoge
            visual = []
            if self.visual_files:
                from duplicate_engine import find_similar_images
                last_vis = [-1]

                def _vis_cb(done, vtotal):
                    pct = 95 + (int(done * 4 / vtotal) if vtotal else 4)
                    if pct != last_vis[0]:
                        last_vis[0] = pct
                        self.updateProgress.emit(pct)
                    if done % 200 == 0 or done == vtotal:
                        self.updateStats.emit(
                            _t("Vizualus lyginimas: {a}/{b} nuotrauku")
                            .format(a=f"{done:,}", b=f"{vtotal:,}")
                            .replace(",", " "))

                visual = find_similar_images(self.visual_files,
                                             progress_cb=_vis_cb,
                                             exact_groups=results["groups"])

            elapsed = time.time() - t0
            bytes_read = sum(s * len(ps) for s, ps in self.candidates)
            speed_mbs = (bytes_read / (1024 * 1024) / elapsed) if elapsed > 1 else 0

            # Dydziu zodynas TIK kandidatu failams (RAM taupymas - ne visas
            # sarasas): eksportui/lentelei nebereikes getsize is disko
            sizes = {p: s for s, ps in self.candidates for p in ps}

            self.scanDone.emit({
                "stats": results["stats"],
                "groups": results["groups"],
                "suspects": suspects,
                "suspects_truncated": suspects_truncated,
                "visual": visual,
                "total_files": self.total_files,
                "speed_mbs": round(speed_mbs, 1),
                "sizes": sizes,
            })
            self.updateProgress.emit(100)
        except Exception as exc:
            self.scanError.emit(str(exc))


class ExportWorker(QObject):
    """Excel ataskaitos formavimas fone - kad GUI nesustingtu su dideliais
    rezultatais (openpyxl rasymas + spalvos + autofit uztrunka)."""

    exportDone = pyqtSignal(str)      # sukurtos ataskaitos kelias
    scanError = pyqtSignal(str)

    def __init__(self, scan_results, suspect_results, out_path, sizes=None,
                 visual=None):
        super().__init__()
        self.scan_results = scan_results
        self.suspect_results = suspect_results
        self.out_path = out_path
        self.sizes = sizes
        self.visual = visual

    def run(self):
        try:
            from exporter import export_excel
            p = export_excel(self.scan_results, self.suspect_results,
                             out_path=self.out_path, sizes=self.sizes,
                             visual=self.visual)
            self.exportDone.emit(p or "")
        except Exception as exc:
            self.scanError.emit(str(exc))


class JunkWorker(QObject):
    """Windows/Mac siuksliu salinimas fone (NAS'e tukstanciai smulkiu remove
    gali uztrukti). Trinama TIK su turinio paraso patvirtinimu."""

    updateStats = pyqtSignal(str)
    junkDone = pyqtSignal(dict)       # {deleted, skipped, freed}
    scanError = pyqtSignal(str)

    def __init__(self, junk_list):
        super().__init__()
        self.junk_list = list(junk_list)

    def run(self):
        try:
            from duplicate_engine import delete_junk

            def _cb(done, total):
                if done % 100 == 0 or done == total:
                    self.updateStats.emit(
                        _t("Salinamos siuksles: {a}/{b}")
                        .format(a=f"{done:,}", b=f"{total:,}")
                        .replace(",", " "))

            deleted, skipped, freed = delete_junk(self.junk_list, progress_cb=_cb)
            self.junkDone.emit({
                "deleted": deleted,
                "skipped": skipped,
                "freed": freed,
            })
        except Exception as exc:
            self.scanError.emit(str(exc))


def create_scan_thread(worker):
    """Sukurti fresh QThread (PYQT6_THREADING_GUARD).
    Grizina thread objektą. Thread sustoja _on_done/_on_error per QTimer.singleShot."""
    from PyQt6.QtCore import QThread

    thread = QThread()
    worker.moveToThread(thread)

    # Thread finished -> cleanup worker
    thread.finished.connect(worker.deleteLater)

    return thread
