# Smart Duplicate Finder — kompiliavimas / Building

## Paleidimas is kodo / Run from source

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main_window.py
```

GUI kalba / UI language: perjungiama programos viduje; pirmas paleidimas seka
Windows kalba / switched inside the app; first run follows your Windows language.

## EXE kompiliavimas / Building the EXE

Nuo v1.1 vienas exe aptarnauja abi kalbas — atskiro `-en` build'o nebera. /
Since v1.1 a single exe serves both languages — there is no separate `-en` build.

```bash
.venv\Scripts\pip install pyinstaller
.venv\Scripts\python -m PyInstaller --noconfirm --onefile --windowed ^
  --name "SmartDuplicateFinder" --icon app.ico ^
  --add-data "pletiniai.json;." --add-data "app.ico;." ^
  --add-data "README.txt;." --add-data "README-en.txt;." ^
  --add-data "README-ru.txt;." --add-data "README-de.txt;." main_window.py
```

Pastabos / Notes:

- Kvieskite `python -m PyInstaller` (ne `pyinstaller.exe`) — veikia ir tada,
  kai venv shim'ai luze. / Call `python -m PyInstaller` (not `pyinstaller.exe`) —
  robust even when venv shims break.
- `pletiniai.json` PRIVALO buti supakuotas (`--add-data`): be jo frozen exe
  pletiniu zinynas tyliai degraduotu. / `pletiniai.json` MUST be bundled:
  without it the frozen exe silently degrades the extension catalog.
- **pillow-heif (nuo v1.3, HEIC/AVIF vizualiniame skene):** PyInstaller
  DLL'us susirenka pats (hooks-contrib). libx265 (~21,5 MB isskleisto)
  ismesti NEGALIMA - patikrinta gyvai 2026-08-22: nors tai enkoderis,
  libheif DLL su juo susietas krovimo metu (be jo `import _pillow_heif`
  luzta ImportError, dingsta VISAS HEIC palaikymas). Nesvarstyti is
  naujo. / Excluding libx265 was tested 2026-08-22 and does NOT work:
  libheif is hard-linked against it at load time - without it the whole
  plugin fails to import. Ship the full DLL set.

Rezultatas / result: `dist\SmartDuplicateFinder.exe` (~43 MB, portable,
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
| `kalba.py` | LT/EN/RU/DE vertimu sluoksnis / i18n layer |
| `kalba_ru.py`, `kalba_de.py` | RU/DE zodynai (v1.3) / RU-DE dictionaries |
| `pletiniai.json` | Pletiniu zinynas (redaguojamas) / extension catalog (editable) |
