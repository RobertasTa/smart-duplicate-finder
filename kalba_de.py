# -*- coding: utf-8 -*-
"""SDF GUI DE zodynas (v1.3, 2026-08-22). Raktas - lietuviskas
tekstas is kalba.py _EN. Vertimu juodrastis - dukryte (lokalus
Hermes agentas), perziura ir taisymai - Claude. Neredaguoti ranka
be perziuros: placeholder'iai {n}/{mb:.2f}... privalo sutapti su raktu."""

_DE = {
    'Duplicate Finder':
        'Duplicate Finder',
    # v1.4 "Kuris cia pirminis?" - ataskaitos skiltys (informacija, ne
    # nurodymas: programa nieko netrina ir trinti nesiulo)
    'Greiciausiai pirminis':
        'Wahrscheinlich das Original',
    'Pastaba': 'Hinweis',
    'pasukta arba veidrodine - patikrinkite, ar taip ir turi buti':
        'gedreht oder gespiegelt – prüfen Sie, ob das so gewollt ist',
    'Kodel':
        'Warum',
    'kiti grupeje vardu pazymeti kaip kopijos':
        'die anderen heißen wie Kopien',
    'kiti guli kopiju aplankuose':
        'die anderen liegen in Kopie-Ordnern',
    'kiti guli laikinuose aplankuose':
        'die anderen liegen in temporären Ordnern',
    'kiti guli giliau aplankuose':
        'die anderen liegen tiefer in Ordnern',
    'kiti sukurti veliau':
        'die anderen wurden später erstellt',
    'neaisku - pozymiu nera':
        'unklar – keine Unterschiede',
    'visos kopijos laikinuose aplankuose':
        'alle Kopien dieser Gruppe liegen in temporären Ordnern',
    # v1.4 "Ar yra naujesne versija?" langelis
    'Ar yra naujesne versija?':
        'Gibt es eine neuere Version?',
    'Jusu versija: {v}':
        'Ihre Version: {v}',
    'Ar yra naujesne? Trys keliai:':
        'Gibt es eine neuere? Drei Wege:',
    '1. Naujienu puslapyje matysite naujausia versija:':
        '1. Auf der Releases-Seite sehen Sie die neueste Version:',
    'Atidaryti naujienu puslapi':
        'Releases-Seite öffnen',
    '2. Jei diegete per winget - spauskite Win+R, irasykite cmd,\n'
    '   spauskite Enter ir iklijuokite:':
        '2. Falls über winget installiert – Win+R drücken, cmd eingeben,\n'
        '   Enter drücken und einfügen:',
    'Kopijuoti komanda':
        'Befehl kopieren',
    'Komanda nukopijuota':
        'Befehl kopiert',
    '3. Arba paprasykite DI konsultanto - jis pats\n'
    '   pasitikrins ir pasakys, ko jums truksta:':
        '3. Oder fragen Sie einen KI-Assistenten – er prüft es\n'
        '   selbst und sagt Ihnen, was Ihnen fehlt:',
    'Programa pati interneto neliecia. Sprendziate jus.':
        'Das Programm selbst geht nie ins Internet. Sie entscheiden.',
    '+   Prideti katalogus':
        '+   Ordner hinzufügen',
    '-   Pasalinti pasirinktus':
        '-   Ausgewählte entfernen',
    '>>> Skenuoti':
        '>>> Scannen',
    'Eksportuoti ataskaita':
        'Bericht exportieren',
    # DE jau buvo konkretus ("Systemmüll" = sistemos siuksles), tad
    # teksto nekeiciam - tik rakta, kad sutaptu su kitomis kalbomis
    'Salinti OS siuksles':
        'Systemmüll entfernen',
    'Windows ir Mac miniatiuru kesai: Thumbs.db, ehthumbs.db,\n'
    '.DS_Store. Jusu failu neliecia. Pries trynima tikrinamas\n'
    'kiekvieno failo turinio parasas - neatitinkantys lieka.':
        'Miniaturansicht-Caches von Windows und Mac: Thumbs.db,\n'
        'ehthumbs.db, .DS_Store. Ihre eigenen Dateien bleiben unberührt.\n'
        'Vor dem Löschen wird die Inhaltssignatur jeder Datei geprüft.',
    'Itraukti katalogai:':
        'Zu scannende Ordner:',
    'Rezultatai:':
        'Ergebnisse:',
    'Failo vardas':
        'Dateiname',
    'Pilnas kelias':
        'Vollständiger Pfad',
    'Dydis (MB)':
        'Größe (MB)',
    'Sukurimo data':
        'Erstellt',
    'Grupe':
        'Gruppe',
    'Pasirenges':
        'Bereit',
    "Prideti katalogus ir spauskite 'Skenuoti'.":
        'Ordner hinzufügen und „Scannen“ klicken.',
    'Pirma prideti bent viena kataloga.':
        'Fügen Sie zuerst mindestens einen Ordner hinzu.',
    'Zvalgyba: renkami failu dydziai...':
        'Vorerkundung: Dateigrößen werden ermittelt...',
    'Gilus tikrinimas (MD5 pagal turini)...':
        'Tiefe Prüfung (MD5 nach Inhalt)...',
    'Skenavimas atsauktas.':
        'Scan abgebrochen.',
    'Nepazymeta ne viena seima - skenavimas atsauktas.':
        'Keine Familie ausgewählt – Scan abgebrochen.',
    'Vyksta skenavimas':
        'Wird gescannt',
    'Formuojama ataskaita':
        'Bericht wird erstellt',
    'Salinamos siuksles':
        'Systemmüll wird entfernt',
    'Pirma atlikti skana.':
        'Führen Sie zuerst einen Scan durch.',
    'Exportuojama...':
        'Export läuft...',
    'Eksportas atsauktas.':
        'Export abgebrochen.',
    'Kur issaugoti ataskaita?':
        'Wo soll der Bericht gespeichert werden?',
    'Excel failai (*.xlsx)':
        'Excel-Dateien (*.xlsx)',
    'Eksportas sekmingas':
        'Export abgeschlossen',
    'Ataskaita sukurta:':
        'Bericht erstellt:',
    'Failas neberastas:':
        'Datei nicht mehr vorhanden:',
    'Klaida:':
        'Fehler:',
    'Exporto klaida:':
        'Exportfehler:',
    'veikia':
        'läuft',
    'Portable rezimas':
        'Portable-Modus',
    'Kalba':
        'Sprache',
    'Kalba pritaikoma paleidus programa is naujo.':
        'Die Sprache wird nach dem Neustart der App angewendet.',
    'Kalba pasikeis paleidus programa is naujo.':
        'Die Sprache ändert sich nach dem Neustart der App.',
    'Kalba issaugota. Perleisti programa dabar?':
        'Sprache gespeichert. App jetzt neu starten?',
    'Nepavyko issaugoti: {}':
        'Konnte nicht gespeichert werden: {}',
    'Ijungta: kesas ir zurnalas saugomi salia programos (pvz., flesiuke) - kompiuteryje pedsaku nelieka.\nIsjungta (numatyta): saugoma vartotojo kataloge %LOCALAPPDATA%\\SmartDuplicateFinder.':
        'An: Cache und Log werden neben der App gespeichert (z. B. auf einem USB-Stick) – am Computer bleiben keine Spuren.\nAus (Standard): im Benutzerprofil unter %LOCALAPPDATA%\\SmartDuplicateFinder.',
    'Nepavyko perjungti rezimo: {}':
        'Modus konnte nicht umgestellt werden: {}',
    'Portable rezimas IJUNGTAS - duomenys salia programos':
        'Portable-Modus AN – Daten liegen neben der App',
    'Portable rezimas isjungtas - duomenys vartotojo kataloge':
        'Portable-Modus aus – Daten liegen im Benutzerprofil',
    'Perziureta failu: {n}, katalogu: {k} - dublikatu grupiu: {g}, {mb:.2f} MB':
        'Geprüfte Dateien: {n}, Ordner: {k} – Duplikatgruppen: {g}, {mb:.2f} MB',
    'Perziureta failu: {n}, katalogu: {k} - dublikatu grupiu: {g}; dubliai uzima {mb:.2f} MB, atlaisvinti galima {fmb:.2f} MB':
        'Geprüfte Dateien: {n}, Ordner: {k} – Duplikatgruppen: {g}; Duplikate belegen {mb:.2f} MB, {fmb:.2f} MB können freigegeben werden',
    '; ITARTINI sarasas nukirptas ties {n} poru riba (susiaurink katalogus, jei nori visu)':
        '; Liste der VERDÄCHTIGEN bei {n} Paaren abgeschnitten (Ordner eingrenzen, um alle zu sehen)',
    '; {n} nuotrauku liko nepalygintos - per daug panasiu vienoje vietoje (susiaurink katalogus)':
        '; {n} Bilder blieben unverglichen – zu viele Ähnliche an einer Stelle (Ordner eingrenzen)',
    '; nepasiekiamu failu praleista: {n}':
        '; unlesbare Dateien übersprungen: {n}',
    'Dubliu kandidatu nerasta (perziureta failu: {n}{skip}).':
        'Keine Duplikat-Kandidaten gefunden (geprüfte Dateien: {n}{skip}).',
    ', {n} praleista':
        ', {n} übersprungen',
    'Ankstesnio skeno rezultatai':
        'Ergebnisse des letzten Scans',
    'Rasti ankstesnio skeno rezultatai ({kada}; dubliu grupiu: {n}).\nIkelti be pakartotinio skenavimo?':
        'Ergebnisse des letzten Scans gefunden ({kada}; Duplikatgruppen: {n}).\nOhne erneuten Scan laden?',
    'Ikelti {kada} skeno rezultatai - dublikatu grupiu: {g}, {mb:.2f} MB (galima eksportuoti be skenavimo)':
        'Scan-Ergebnisse von {kada} geladen – Duplikatgruppen: {g}, {mb:.2f} MB (Export ohne Scan möglich)',
    'Keso ikelti nepavyko - skenuok is naujo.':
        'Cache konnte nicht geladen werden – bitte neu scannen.',
    'Siuksliu nerasta - pirma atlik zvalgyba.':
        'Kein Systemmüll gefunden – bitte zuerst die Vorerkundung ausführen.',
    'Salinti Windows/Mac siuksles?':
        'Windows/Mac-Systemmüll löschen?',
    'Sistemos siuksliu rasta: {n} ({mb:.1f} MB):':
        'Systemmüll gefunden: {n} ({mb:.1f} MB):',
    'Tai miniaturu/narsymo kesai - OS juos atsikuria pati.\nPries trynima kiekvienam failui tikrinamas turinio parasas;\nneatitinkantys NEBUS trinami.\n\nDEMESIO: tinklo diskuose (NAS) trynimas negriztamas\n(siuksliadeze ten neveikia). Trinti?':
        'Das sind Miniaturansichten- und Ordner-Caches – das\nBetriebssystem legt sie bei Bedarf neu an.\nVor dem Löschen wird die Inhalts-Signatur jeder Datei geprüft;\nabweichende werden NICHT gelöscht.\n\nACHTUNG: Auf Netzlaufwerken (NAS) ist das Löschen endgültig\n(dort gibt es keinen Papierkorb). Löschen?',
    'Siuksliu salinimas atsauktas.':
        'Aufräumen abgebrochen.',
    'Siuksliu istrinta: {n}, atlaisvinta {mb:.1f} MB':
        'Müll-Dateien gelöscht: {n}, {mb:.1f} MB freigegeben',
    '; praleista {n} (parasas nesutapo arba failas uzrakintas)':
        '; {n} übersprungen (Signatur weicht ab oder Datei gesperrt)',
    'Rasti kandidatai i dublius':
        'Duplikat-Kandidaten gefunden',
    'Vienodo dydzio failu grupes (kandidatai). Pazymekite,\nkurias seimas tikrinti giliai (MD5 pagal turini):':
        'Gruppen gleichgroßer Dateien (Kandidaten).\nAnkreuzen, welche Familien tief geprüft werden (MD5 nach Inhalt):',
    'Seima':
        'Familie',
    'Grupiu':
        'Gruppen',
    'Failu':
        'Dateien',
    'Apimtis':
        'Volumen',
    '~Laikas':
        '~Zeit',
    'Tikrinti pazymetus':
        'Ausgewählte prüfen',
    'Atsaukti':
        'Abbrechen',
    'Is viso pazymejus viska: {mb} skaitymo, {t} (disko greitis ~{v} MB/s)':
        'Bei Auswahl von allem: {mb} lesen, {t} (Disk-Geschwindigkeit ~{v} MB/s)',
    'akimirka':
        'sofort',
    'Prideti katalogus':
        'Ordner hinzufügen',
    'Iklijuokite kelius is Explorer (Ctrl+V) arba pasirinkite paspausdami mygtuka:':
        'Pfade aus dem Explorer (Ctrl+V) einfügen oder per Button auswählen:',
    'C:\\Ap1\nD:\\Ap2\nF:\\Ap3  (kiekvienas - naujoje eiluteje)':
        'C:\\Ordner1\nD:\\Ordner2\nF:\\Ordner3  (jeweils in einer neuen Zeile)',
    'Pasirinkti katalogus':
        'Ordner auswählen',
    'Pasirinkti kataloga':
        'Ordner wählen',
    'Prideti':
        'Hinzufügen',
    'Atstatyti':
        'Abbrechen',
    'Grupe {idx}':
        'Gruppe {idx}',
    'Dublikatai':
        'Duplikate',
    'Panasios nuotraukos':
        'Ähnliche Bilder',
    'Itartini':
        'Verdächtige',
    'Itartinas {n}':
        'Verdächtiger {n}',
    'RODOMA {a} IS {b} EILUCIU - virsyta Excel lapo riba (1 048 576)':
        'ANGEZEIGT: {a} VON {b} ZEILEN – Excel-Blatt-Limit (1 048 576) überschritten',
    'ITARINI':
        'VERDÄCHTIG',
    'ITARTINI (panasus, bet ne identiski)':
        'VERDÄCHTIG (ähnlich, aber nicht identisch)',
    'Rodoma eiluciu: {n} (didziausios grupes virsuje) - PILNAS sarasas Excel ataskaitoje':
        'Zeilen angezeigt: {n} (größte Gruppen oben) – VOLLE Liste im Excel-Bericht',
    'Zvalgyba - failu: {n}...':
        'Vorerkundung – Dateien: {n}...',
    'Panasios nuotraukos (vizualiai)':
        'Ähnliche Fotos (visuell)',
    'VIZUALIAI PANASUS (skirtinga rezoliucija/kokybe)':
        'VISUELL ÄHNLICH (andere Auflösung/Qualität)',
    'Vaizdas {idx}':
        'Bild {idx}',
    'Vizualus lyginimas: {a}/{b} nuotrauku':
        'Visueller Vergleich: {a}/{b} Fotos',
    '; vizualiai panasiu grupiu: {n}':
        '; visuell ähnliche Gruppen: {n}',
    'ITARTINI paieska: {a}/{b} failu':
        'Suche nach VERDÄCHTIGEN: {a}/{b} Dateien',
    'Salinamos siuksles: {a}/{b}':
        'Systemmüll wird entfernt: {a}/{b}',
    '{f}/{ft} failu':
        '{f}/{ft} Dateien',
    'liko':
        'übrig',
    'Pagalba':
        'Hilfe',
    'Apie...':
        'Über...',
    'Instrukcija':
        'Anleitung',
    'Neradote atsakymo? Klauskite DI':
        'Keine Antwort gefunden? Fragen Sie die KI',
    'Nepavyko atidaryti: {}':
        'Konnte nicht geöffnet werden: {}',
    'Apie programa':
        'Über die App',
    'Dubliuotu failu paieska pagal turini - nieko netrina.':
        'Findet Duplikate nach Inhalt – löscht nichts.',
    'Versija {v}':
        'Version {v}',
    'Kurejo puslapis:':
        'Projektseite:',
    'Kas ivyks paspaudus OK:\n\n1. Atsidarys interneto narsykle su DI padejejo\n   claude.ai puslapiu. Zinutes laukelyje jau bus\n   irasyta angliska pradzia - prisistatymas, kas per\n   programa ir kur jos kodas.\n2. NEISSIGASKITE raudono pranesimo virs zinutes -\n   claude.ai ji rodo visada, kai tekstas ateina per\n   nuoroda. Tai tik priminimas perskaityti, kas\n   siunciama.\n3. Zinutes gale, po zodziu "My question:", irasykite\n   SAVO klausima - galima lietuviskai! - ir spauskite\n   siuntimo mygtuka (rodykle). Klausti galima visko,\n   pvz.: "kaip atsinaujinti programa i naujesne\n   versija? paaiskink zingsnis po zingsnio".\n4. Jei DI atsakys angliskai - tiesiog paprasykite kita\n   zinute: "atsakyk lietuviskai", ir toliau bendraus\n   lietuviskai.\n\nPastaba: claude.ai gali paprasyti prisijungti (nemokama\npaskyra). Niekas neissiunciama be jusu rankos.':
        'Was passiert, wenn Sie OK drücken:\n\n1. Ihr Webbrowser öffnet den KI-Assistenten auf der\n   Seite claude.ai. Im Nachrichtenfeld steht bereits\n   eine vorbereitete englische Einleitung – was das\n   Programm ist und wo sein Code liegt.\n2. ERSCHRECKEN SIE NICHT über den roten Hinweis über\n   der Nachricht – claude.ai zeigt ihn immer, wenn\n   Text über einen Link ankommt. Es ist nur eine\n   Erinnerung, zu lesen, was gesendet wird.\n3. Am Ende der Nachricht, nach den Worten "My question:",\n   TIPPEN SIE IHRE Frage – in jeder Sprache! – und\n   drücken Sie die Senden-Taste (den Pfeil). Fragen Sie\n   alles, z. B.: "wie aktualisiere ich die App auf die\n   neueste Version? erkläre es Schritt für Schritt".\n4. Wenn die KI in der falschen Sprache antwortet –\n   bitten Sie einfach in der nächsten Nachricht:\n   "antworte auf Deutsch", und die Unterhaltung geht\n   auf Deutsch weiter.\n\nHinweis: claude.ai bittet Sie eventuell, sich anzumelden\n(kostenloses Konto). Ohne Ihr Zutun wird nichts versendet.',
    'Atidaryti faila':
        'Datei öffnen',
    'Atidaryti kataloga':
        'Ordner öffnen',
    'Kopijuoti kelia':
        'Pfad kopieren',
    'Kelias nukopijuotas':
        'Pfad kopiert',
}

_FAM_DE = {
    'Paveiksliukai': 'Bilder',
    'Video': 'Videos',
    'Audio': 'Audio',
    'Dokumentai': 'Dokumente',
    'Archyvai': 'Archive',
    'CAD': 'CAD',
    'Kodas': 'Code',
    'Programos': 'Programme',
    'Kita': 'Sonstiges',
}
