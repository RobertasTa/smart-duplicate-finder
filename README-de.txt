=====================================================================
  SMART DUPLICATE FINDER v2 — Duplikat-Finder für Windows
=====================================================================

WAS IST DAS
-----------
Das Programm findet Duplikate (Dateien mit identischem Inhalt) in
ausgewählten Ordnern oder auf ganzen Laufwerken und zeigt, wie viel
Platz sie belegen. Dateien werden nach INHALT verglichen
(MD5-Prüfsumme), nicht nach Namen — umbenannte Duplikate werden
gefunden, während gleichnamige Dateien mit unterschiedlichem Inhalt
nie als Duplikate gemeldet werden.

Zusätzlich kann das Programm UNSICHTBAREN Systemmüll (Thumbs.db
u. Ä.) finden und aufräumen — siehe Abschnitt unten.

WICHTIG: Ihre Duplikate LÖSCHT das Programm NICHT — es findet und
zeigt sie nur; was damit geschieht, entscheiden Sie. Die einzige
Löschfunktion ist die Systemmüll-Bereinigung, und die läuft nur
nach Ihrer Bestätigung.

Fragen Sie jemanden, der seit Jahren Duplikat-Finder benutzt, und
Sie hören dieselbe Geschichte: Eines Tages hat das Programm die
falschen Dateien gelöscht. Das ist kein Fehler eines bestimmten
Werkzeugs — es ist die Grenze jedes Algorithmus. KEIN ALGORITHMUS
KANN ENTSCHEIDEN, WAS IHNEN WICHTIG IST: Was für den einen Müll
ist, ist für den anderen die einzige erhaltene Sicherungskopie.

Deshalb ist das ein BEWUSSTES SICHERHEITSPRINZIP, kein Mangel:
Keine Automatik sollte entscheiden, welche Kopie bleibt — ein
Duplikat kann absichtlich in einem Ordner liegen (ein Backup, ein
Projektpaket). Das Programm löscht nie, was Sie behalten wollten —
darum können Sie damit bedenkenlos selbst Ihre wertvollsten
Archive scannen.

Dafür ist auch der Excel-Bericht da: Aufräumen IN IHREM EIGENEN
TEMPO. Nichts zwingt Sie, sofort zu handeln — der Bericht ist eine
Datei, die Sie auch eine Woche später öffnen, sortieren, farbig
abhaken und ein paar Duplikate pro Tag abarbeiten können, bis das
Laufwerk sauber ist. Und wenn Sie nach der Durchsicht entscheiden,
jede einzelne Kopie zu behalten — auch das ist ein völlig gutes
Ergebnis. Das Ziel sind nicht gelöschte Gigabytes, sondern dass
SIE genau wissen, was Sie haben, und selbst entscheiden.

STARTEN
-------
1. Sie brauchen nur eine Datei: SmartDuplicateFinder.exe
   Keine Installation, kein Python — läuft direkt vom USB-Stick.
2. Der erste Start dauert ein paar Sekunden länger — das ist normal.
3. Zeigt Windows den blauen Bildschirm "Windows protected your PC" —
   klicken Sie "More info" -> "Run anyway". Das Programm ist nicht
   signiert (selbstgebaut), aber sicher.
4. SPRACHE: Deutsch wählen Sie in der Auswahlliste unten in der
   linken Leiste; die Wahl wird gespeichert und nach dem Neustart
   der App angewendet.

BEDIENUNG (Schritt für Schritt)
-------------------------------
1. "+ Ordner hinzufügen" — wählen Sie, wo gesucht wird (ein ganzes
   Laufwerk wie D:\ geht auch). Pfade können Sie auch aus dem
   Explorer einfügen (Ctrl+V).
2. ">>> Scannen" — zuerst läuft eine schnelle VORERKUNDUNG (nur
   Dateigrößen werden gelesen, dauert Sekunden).
3. Ein Fenster "Duplikat-Kandidaten gefunden" erscheint — die
   Kandidaten sind nach Typ gruppiert (Bilder, Videos, Dokumente,
   CAD, Code usw.) mit Volumen und ZEITSCHÄTZUNG pro Zeile.
   TIPP: "Code" und "Sonstiges" meist abwählen — Tausende kleiner
   Programmdateien, die niemand aufräumen muss, aber am längsten
   zu prüfen sind.
4. "Ausgewählte prüfen" — die tiefe Inhaltsprüfung läuft. Unten
   rechts sehen Sie den Live-Fortschritt: geprüfte Dateien,
   Geschwindigkeit (MB/s), Restzeit.
5. Die Ergebnisse sind farbig nach Typ gruppiert; die GRÖSSTEN
   Duplikate stehen oben. Beim Überfahren einer Zeile mit der Maus
   erscheint die Beschreibung des Dateityps.
6. DOPPELKLICK auf eine Zeile öffnet den Explorer mit markierter
   Datei. RECHTSKLICK (ab v1.3) bietet: Datei öffnen / Ordner
   öffnen / Pfad kopieren.
7. "Bericht exportieren" — die vollständige Liste wird in eine
   farbige Excel-Datei gespeichert (Sie wählen den Ort; Dokumente
   wird vorgeschlagen).

SYSTEMMÜLL-BEREINIGUNG (Button "Systemmüll entfernen")
------------------------------------------------------
Windows und macOS hinterlassen in Ordnern UNSICHTBARE Cache-Dateien,
die der Explorer normalerweise versteckt:
  * Thumbs.db, ehthumbs.db — Windows-Miniaturansichten-Cache
  * .DS_Store — macOS-Finder-Reste (häufig auf NAS-Freigaben)
Harmlos, aber unordentlich — und von Hand schwer zu löschen, weil
man sie nicht sieht.

So funktioniert es:
1. Wenn die Vorerkundung Müll gefunden hat, wird der Button
   "Systemmüll entfernen (N)" aktiv — in Klammern die Anzahl.
2. Ein Klick zeigt eine Übersicht nach Typ und fragt nach
   Bestätigung.
3. SICHERUNG: Vor dem Löschen wird bei JEDER Datei die
   Inhalts-Signatur (magic bytes) geprüft. Eine Datei, die nur
   Thumbs.db HEISST, deren Inhalt aber abweicht, bleibt unberührt.
   Im Zweifel = nie löschen.
4. Danach sehen Sie, wie viele Dateien entfernt und wie viel Platz
   freigegeben wurde. Das Betriebssystem legt diese Caches bei
   Bedarf neu an.
ACHTUNG: Auf Netzlaufwerken (NAS) ist das Löschen endgültig — dort
gibt es keinen Papierkorb. Genau darum werden Signaturen geprüft.

Hinweis: desktop.ini-Dateien werden bewusst NIE angerührt — sie
speichern Ordnereinstellungen.

ÄHNLICHE FOTOS (visueller Vergleich)
------------------------------------
Im Kandidaten-Fenster gibt es die Zusatzzeile "Ähnliche Fotos
(visuell)" (standardmäßig angehakt wie die anderen). Damit werden
Fotos VISUELL verglichen — dasselbe Bild wird auch gefunden, wenn
es verkleinert, in anderer Qualität gespeichert oder in ein anderes
Format umgewandelt wurde (MD5 sieht das nicht, weil die Bytes
abweichen). Funktioniert mit den üblichen Bildformaten (JPG, PNG,
GIF, BMP, TIFF, WebP) und seit v1.3 auch mit den iPhone-Formaten
HEIC/AVIF; "gedreht" gespeicherte Handyfotos (EXIF-Orientierung)
werden ebenfalls korrekt zugeordnet. Solche Gruppen erscheinen in
Violett ("VISUELL ÄHNLICH") und im Excel-Bericht auf einem eigenen
Blatt.
Zum Zeitbedarf: Für diesen Vergleich muss JEDES Foto geöffnet
werden (~40 Fotos/s); bei großen Archiven (Zehntausende Fotos)
dauert das — in Eile den Haken abwählen. Gruppen, deren Dateien
ohnehin byte-identisch sind (bereits als Duplikate gemeldet),
werden hier nicht wiederholt — nur echte "versteckte" Kopien.

GUT ZU WISSEN
-------------
* SCAN-GEDÄCHTNIS, DAS ALLES ÜBERLEBT: Die Ergebnisse werden sofort
  nach dem Scan auf die Festplatte geschrieben — noch BEVOR die
  Tabelle gezeichnet wird. Selbst wenn das Programm direkt nach
  einem langen Scan abstürzt oder beendet wird, sind die Ergebnisse
  da: Beim nächsten Start bietet es an, den letzten Scan zu laden —
  sofort durchsehen und exportieren, ohne neu zu scannen. Ein Scan,
  der Stunden gedauert hat, geht nie verloren.
* Die Tabelle zeigt bis zu 2 000 Zeilen (die größten Gruppen); die
  VOLLE Liste steht immer im Excel-Bericht.
* Abschnitt VERDÄCHTIG (gelb) — Dateien mit gleichem Namen und
  ähnlicher Größe, aber ANDEREM Inhalt. Keine Duplikate, aber einen
  Blick wert (z. B. zwei Versionen desselben Dokuments).
* Unterschiedliche Dateigröße = garantiert kein Duplikat, solche
  Dateien werden gar nicht erst gelesen — darum sind Scans auch auf
  großen Laufwerken schnell.
* Leere Dateien (0 Byte) werden bewusst übersprungen.

WO WAS GESPEICHERT WIRD
-----------------------
* Excel-Berichte — wo Sie wollen (Dokumente wird vorgeschlagen).
* Dienstdateien — in %LOCALAPPDATA%\SmartDuplicateFinder\:
    paskutinis_skenas.json  - Scan-Gedächtnis
    scan_speed.json         - Laufwerksgeschwindigkeit für
                              Zeitschätzungen
    veiklos.log             - Aktivitätsprotokoll (hilfreich, falls
                              je etwas hängt)
* PORTABLE-MODUS (Häkchen unten in der linken Leiste): Wenn AN,
  liegen die Dienstdateien im Ordner _darbal NEBEN der App (z. B.
  auf dem USB-Stick), und am Computer bleiben keine Spuren — die
  App entfernt sogar ihren zuvor angelegten
  %LOCALAPPDATA%-Ordner. Die Wahl merkt sich die Datei portable.txt
  neben der exe (die Notepad++/VS-Code-Konvention) — sie reist mit
  dem Stick.
* Alle Dienstdateien können Sie jederzeit löschen — das Programm
  beginnt einfach mit einem sauberen Blatt.
* SPRACHE (Lietuvių / English / Русский / Deutsch) wird in der
  Auswahlliste unten in der linken Leiste umgeschaltet; die Wahl
  wird gespeichert und nach dem Neustart angewendet.

---------------------------------------------------------------------
Erstellt von: Robertas + Claude (Anthropic AI) + lokaler KI-Helfer
2026-08-22        Version: v2 (deutsche Oberfläche ab v1.3)
=====================================================================
