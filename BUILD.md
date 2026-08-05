# Smart Duplicate Finder v2 — kompiliavimas / Building

## Paleidimas is kodo / Run from source

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main_window.py
```

GUI kalba / UI language: lietuviu (numatytoji). English:
`set SDF_LANG=en` pries paleidziant / before launching.

## EXE kompiliavimas / Building the EXE

```bash
.venv\Scripts\pip install pyinstaller
```

Lietuviska versija / Lithuanian build:

```bash
pyinstaller --noconfirm --onefile --windowed --name "SmartDuplicateFinder" ^
  --icon app.ico --add-data "pletiniai.json;." --add-data "app.ico;." main_window.py
```

Angliska versija / English build (sukurkite tuscia `lang_en.flag` faila /
create an empty `lang_en.flag` file first):

```bash
echo en > lang_en.flag
pyinstaller --noconfirm --onefile --windowed --name "SmartDuplicateFinder-en" ^
  --icon app.ico --add-data "pletiniai.json;." --add-data "app.ico;." ^
  --add-data "lang_en.flag;." main_window.py
```

Rezultatas / result: `dist\SmartDuplicateFinder[-en].exe` (~54 MB, portable,
jokio diegimo / no installation required).

## Architektura / Architecture

| Failas / File | Paskirtis / Purpose |
|---|---|
| `main_window.py` | GUI langas, faziu orkestravimas / main window, phase flow |
| `duplicate_engine.py` | Variklis be Qt: skenas, MD5, ITARTINI, siuksles / zero-Qt engine |
| `scan_worker.py` | Foniniai QThread darbininkai / background workers |
| `select_dialog.py` | Kandidatu pasirinkimo dialogas / candidate picker dialog |
| `add_dialog.py` | Katalogu pridejimo dialogas / folder picker dialog |
| `table_populator.py` | Rezultatu lentele, seimu spalvos / results table, family colours |
| `exporter.py` | Excel ataskaita (openpyxl write-only) / Excel report |
| `kalba.py` | LT/EN vertimu sluoksnis / i18n layer |
| `pletiniai.json` | Pletiniu zinynas (redaguojamas) / extension catalog (editable) |
