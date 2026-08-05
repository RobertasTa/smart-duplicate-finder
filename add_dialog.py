"""
add_dialog.py - Multi-folder addition dialog (FAZE 2.2)
Sprendimas: QLineEdit + ctrl+V is Windows Explorer + browse mygtukas.
"""
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem, QFileDialog, QPlainTextEdit
)

from kalba import t


class AddFoldersDialog(QDialog):
    """Leidzia uzpildyti KELIUS vienu veiksmu: iklijuoti is Explorer arba browse."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("Prideti katalogus"))
        self.setMinimumSize(500, 320)

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel(t("Iklijuokite kelius is Explorer (Ctrl+V) arba pasirinkite paspausdami mygtuka:"))
        )
        self.line_edit = QPlainTextEdit()
        self.line_edit.setPlaceholderText(
            t("C:\\Ap1\nD:\\Ap2\nF:\\Ap3  (kiekvienas - naujoje eiluteje)")
        )
        self.line_edit.setObjectName("txt_paths")
        layout.addWidget(self.line_edit)

        browse_btn = QPushButton(t("Pasirinkti katalogus"))
        browse_btn.clicked.connect(self._browse)
        layout.addWidget(browse_btn)

        self.list_w = QListWidget()
        self.list_w.setVisible(False)
        layout.addWidget(self.list_w)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        ok = QPushButton(t("Prideti"))
        ok.clicked.connect(self.accept)
        cncl = QPushButton(t("Atstatyti"))
        cncl.clicked.connect(self.reject)
        btn_row.addWidget(ok)
        btn_row.addWidget(cncl)
        layout.addLayout(btn_row)

        self._collected = []

    def _browse(self):
        folder = QFileDialog.getExistingDirectory(self, t("Pasirinkti kataloga"))
        if folder:
            self._add_one(folder)

    def _add_one(self, path):
        if path and path not in self._collected:
            self._collected.append(path)
            self.list_w.addItem(QListWidgetItem(path))
            self.list_w.setVisible(True)

    def get_selected_paths(self):
        paths = list(self._collected)
        for line in self.line_edit.toPlainText().splitlines():
            p = line.strip()
            if p and os.path.isdir(p) and p not in paths:
                paths.append(p)
        return paths