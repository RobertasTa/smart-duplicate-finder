# -*- coding: utf-8 -*-
"""SDF GUI lietuviškas žodynas (v1.3, 2026-08-22, Roberto pastaba iš gyvo
testo: „meškinė be Š varnelių — kliūva, kas lietuvių rimtai žiūri kalbą").

Raktai kode istoriškai ASCII be diakritikų; ŠIS žodynas grąžina taisyklingą
lietuvių kalbą rodymui. Įtraukti TIK raktai, kuriems reikia pakeitimų —
kitiems t() grąžina patį raktą. Placeholder'iai {n}/{mb:.2f}... privalo
sutapti su raktu.
"""

_LT = {
    "+   Prideti katalogus": "+   Pridėti katalogus",
    "-   Pasalinti pasirinktus": "-   Pašalinti pasirinktus",
    "Eksportuoti ataskaita": "Eksportuoti ataskaitą",
    "Salinti OS siuksles": "Šalinti OS šiukšles",
    "Windows ir Mac miniatiuru kesai: Thumbs.db, ehthumbs.db,\n"
    ".DS_Store. Jusu failu neliecia. Pries trynima tikrinamas\n"
    "kiekvieno failo turinio parasas - neatitinkantys lieka.":
        "Windows ir Mac miniatiūrų kešai: Thumbs.db, ehthumbs.db,\n"
        ".DS_Store. Jūsų failų neliečia. Prieš trynimą tikrinamas\n"
        "kiekvieno failo turinio parašas — neatitinkantys lieka.",
    "Itraukti katalogai:": "Įtraukti katalogai:",
    "Sukurimo data": "Sukūrimo data",
    "Grupe": "Grupė",
    # v1.4 „Kuris čia pirminis?"
    "Greiciausiai pirminis": "Greičiausiai pirminis",
    "Pastaba": "Pastaba",
    "mazesnes raiskos nei kiti grupeje": "mažesnės raiškos nei kiti grupėje",
    "kita orientacija nei kiti grupeje - patikrinkite, ar taip ir turi buti":
        "kita orientacija nei kiti grupėje – patikrinkite, ar taip ir turi būti",
    "Kodel": "Kodėl",
    "kiti grupeje vardu pazymeti kaip kopijos":
        "kiti grupėje vardu pažymėti kaip kopijos",
    "kiti guli kopiju aplankuose": "kiti guli kopijų aplankuose",
    "kiti guli laikinuose aplankuose": "kiti guli laikinuose aplankuose",
    "kiti guli giliau aplankuose": "kiti guli giliau aplankuose",
    "kiti sukurti veliau": "kiti sukurti vėliau",
    "neaisku - pozymiu nera": "neaišku — požymių nėra",
    "visos kopijos laikinuose aplankuose":
        "visos šios grupės kopijos guli laikinuose aplankuose",
    # v1.4 „Ar yra naujesnė versija?"
    "Ar yra naujesne versija?": "Ar yra naujesnė versija?",
    "Jusu versija: {v}": "Jūsų versija: {v}",
    "Ar yra naujesne? Trys keliai:": "Ar yra naujesnė? Trys keliai:",
    "1. Naujienu puslapyje matysite naujausia versija:":
        "1. Naujienų puslapyje matysite naujausią versiją:",
    "Atidaryti naujienu puslapi": "Atidaryti naujienų puslapį",
    "2. Jei diegete per winget - spauskite Win+R, irasykite cmd,\n"
    "   spauskite Enter ir iklijuokite:":
        "2. Jei diegėte per winget — spauskite Win+R, įrašykite cmd,\n"
        "   spauskite Enter ir įklijuokite:",
    "Kopijuoti komanda": "Kopijuoti komandą",
    "Komanda nukopijuota": "Komanda nukopijuota",
    "3. Arba paprasykite DI konsultanto - jis pats\n"
    "   pasitikrins ir pasakys, ko jums truksta:":
        "3. Arba paprašykite DI konsultanto — jis pats\n"
        "   pasitikrins ir pasakys, ko jums trūksta:",
    "Programa pati interneto neliecia. Sprendziate jus.":
        "Programa pati interneto neliečia. Sprendžiate jūs.",
    "Pasirenges": "Pasirengęs",
    "Prideti katalogus ir spauskite 'Skenuoti'.":
        "Pridėkite katalogus ir spauskite „Skenuoti“.",
    "Pirma prideti bent viena kataloga.":
        "Pirma pridėkite bent vieną katalogą.",
    "Zvalgyba: renkami failu dydziai...":
        "Žvalgyba: renkami failų dydžiai...",
    "Gilus tikrinimas (MD5 pagal turini)...":
        "Gilus tikrinimas (MD5 pagal turinį)...",
    "Skenavimas atsauktas.": "Skenavimas atšauktas.",
    "Nepazymeta ne viena seima - skenavimas atsauktas.":
        "Nepažymėta nė viena šeima — skenavimas atšauktas.",
    "Salinamos siuksles": "Šalinamos šiukšlės",
    "Pirma atlikti skana.": "Pirma atlikite skeną.",
    "Exportuojama...": "Eksportuojama...",
    "Eksportas atsauktas.": "Eksportas atšauktas.",
    "Kur issaugoti ataskaita?": "Kur išsaugoti ataskaitą?",
    "Eksportas sekmingas": "Eksportas sėkmingas",
    "Portable rezimas": "Portable režimas",
    "Kalba pritaikoma paleidus programa is naujo.":
        "Kalba pritaikoma paleidus programą iš naujo.",
    "Kalba pasikeis paleidus programa is naujo.":
        "Kalba pasikeis paleidus programą iš naujo.",
    "Kalba issaugota. Perleisti programa dabar?":
        "Kalba išsaugota. Perleisti programą dabar?",
    "Nepavyko issaugoti: {}": "Nepavyko išsaugoti: {}",
    "Ijungta: kesas ir zurnalas saugomi salia programos (pvz., flesiuke) - kompiuteryje pedsaku nelieka.\nIsjungta (numatyta): saugoma vartotojo kataloge %LOCALAPPDATA%\\SmartDuplicateFinder.":
        "Įjungta: kešas ir žurnalas saugomi šalia programos (pvz., flešiuke) — kompiuteryje pėdsakų nelieka.\nIšjungta (numatyta): saugoma vartotojo kataloge %LOCALAPPDATA%\\SmartDuplicateFinder.",
    "Nepavyko perjungti rezimo: {}": "Nepavyko perjungti režimo: {}",
    "Portable rezimas IJUNGTAS - duomenys salia programos":
        "Portable režimas ĮJUNGTAS — duomenys šalia programos",
    "Portable rezimas isjungtas - duomenys vartotojo kataloge":
        "Portable režimas išjungtas — duomenys vartotojo kataloge",
    "Perziureta failu: {n}, katalogu: {k} - dublikatu grupiu: {g}, {mb:.2f} MB":
        "Peržiūrėta failų: {n}, katalogų: {k} — dublikatų grupių: {g}, {mb:.2f} MB",
    "Perziureta failu: {n}, katalogu: {k} - dublikatu grupiu: {g}; dubliai uzima {mb:.2f} MB, atlaisvinti galima {fmb:.2f} MB":
        "Peržiūrėta failų: {n}, katalogų: {k} — dublikatų grupių: {g}; dubliai užima {mb:.2f} MB, atlaisvinti galima {fmb:.2f} MB",
    "; ITARTINI sarasas nukirptas ties {n} poru riba (susiaurink katalogus, jei nori visu)":
        "; ĮTARTINŲ sąrašas nukirptas ties {n} porų riba (susiaurinkite katalogus, jei norite visų)",
    "; {n} nuotrauku nepavyko atverti (sugadintos, nezinomo formato arba per didzuliu)":
        "; {n} nuotraukų nepavyko atverti (sugadintos, nežinomo formato arba per didžiulės)",
    "; {n} nuotrauku liko nepalygintos - per daug panasiu vienoje vietoje (susiaurink katalogus)":
        "; {n} nuotraukų liko nepalygintos – per daug panašių vienoje vietoje (susiaurinkite katalogus)",
    "; nepasiekiamu failu praleista: {n}":
        "; nepasiekiamų failų praleista: {n}",
    "Dubliu kandidatu nerasta (perziureta failu: {n}{skip}).":
        "Dublių kandidatų nerasta (peržiūrėta failų: {n}{skip}).",
    "Rasti ankstesnio skeno rezultatai ({kada}; dubliu grupiu: {n}).\nIkelti be pakartotinio skenavimo?":
        "Rasti ankstesnio skeno rezultatai ({kada}, {n} dublių grupių).\nĮkelti be pakartotinio skenavimo?",
    "Ikelti {kada} skeno rezultatai - dublikatu grupiu: {g}, {mb:.2f} MB (galima eksportuoti be skenavimo)":
        "Įkelti {kada} skeno rezultatai — dublikatų grupių: {g}, {mb:.2f} MB (galima eksportuoti be skenavimo)",
    "Keso ikelti nepavyko - skenuok is naujo.":
        "Kešo įkelti nepavyko — skenuokite iš naujo.",
    "Siuksliu nerasta - pirma atlik zvalgyba.":
        "Šiukšlių nerasta — pirma atlikite žvalgybą.",
    "Salinti Windows/Mac siuksles?": "Šalinti Windows/Mac šiukšles?",
    "Sistemos siuksliu rasta: {n} ({mb:.1f} MB):":
        "Sistemos šiukšlių rasta: {n} ({mb:.1f} MB):",
    "Tai miniaturu/narsymo kesai - OS juos atsikuria pati.\nPries trynima kiekvienam failui tikrinamas turinio parasas;\nneatitinkantys NEBUS trinami.\n\nDEMESIO: tinklo diskuose (NAS) trynimas negriztamas\n(siuksliadeze ten neveikia). Trinti?":
        "Tai miniatiūrų/naršymo kešai — OS juos atsikuria pati.\nPrieš trynimą kiekvienam failui tikrinamas turinio parašas;\nneatitinkantys NEBUS trinami.\n\nDĖMESIO: tinklo diskuose (NAS) trynimas negrįžtamas\n(šiukšliadėžė ten neveikia). Trinti?",
    "Siuksliu salinimas atsauktas.": "Šiukšlių šalinimas atšauktas.",
    "Siuksliu istrinta: {n}, atlaisvinta {mb:.1f} MB":
        "Šiukšlių ištrinta: {n}, atlaisvinta {mb:.1f} MB",
    "; praleista {n} (parasas nesutapo arba failas uzrakintas)":
        "; praleista {n} (parašas nesutapo arba failas užrakintas)",
    "Rasti kandidatai i dublius": "Rasti kandidatai į dublius",
    "Vienodo dydzio failu grupes (kandidatai). Pazymekite,\nkurias seimas tikrinti giliai (MD5 pagal turini):":
        "Vienodo dydžio failų grupės (kandidatai). Pažymėkite,\nkurias šeimas tikrinti giliai (MD5 pagal turinį):",
    "Seima": "Šeima",
    "Grupiu": "Grupių",
    "Failu": "Failų",
    "Tikrinti pazymetus": "Tikrinti pažymėtus",
    "Atsaukti": "Atšaukti",
    "Is viso pazymejus viska: {mb} skaitymo, {t} (disko greitis ~{v} MB/s)":
        "Iš viso pažymėjus viską: {mb} skaitymo, {t} (disko greitis ~{v} MB/s)",
    "Prideti katalogus": "Pridėti katalogus",
    "Iklijuokite kelius is Explorer (Ctrl+V) arba pasirinkite paspausdami mygtuka:":
        "Įklijuokite kelius iš Explorer (Ctrl+V) arba pasirinkite paspausdami mygtuką:",
    "C:\\Ap1\nD:\\Ap2\nF:\\Ap3  (kiekvienas - naujoje eiluteje)":
        "C:\\Ap1\nD:\\Ap2\nF:\\Ap3  (kiekvienas — naujoje eilutėje)",
    "Pasirinkti kataloga": "Pasirinkti katalogą",
    "Prideti": "Pridėti",
    "Grupe {idx}": "Grupė {idx}",
    "Panasios nuotraukos": "Panašios nuotraukos",
    "Itartini": "Įtartini",
    "Itartinas {n}": "Įtartinas {n}",
    "RODOMA {a} IS {b} EILUCIU - virsyta Excel lapo riba (1 048 576)":
        "RODOMA {a} IŠ {b} EILUČIŲ — viršyta Excel lapo riba (1 048 576)",
    "ITARINI": "ĮTARTINAS",
    "ITARTINI (panasus, bet ne identiski)":
        "ĮTARTINI (panašūs, bet ne identiški)",
    "Rodoma eiluciu: {n} (didziausios grupes virsuje) - PILNAS sarasas Excel ataskaitoje":
        "Rodoma eilučių: {n} (didžiausios grupės viršuje) — PILNAS sąrašas Excel ataskaitoje",
    "Zvalgyba - failu: {n}...": "Žvalgyba — failų: {n}...",
    "Panasios nuotraukos (vizualiai)": "Panašios nuotraukos (vizualiai)",
    "VIZUALIAI PANASUS (skirtinga rezoliucija/kokybe)":
        "VIZUALIAI PANAŠŪS (skirtinga rezoliucija/kokybė)",
    "Vizualus lyginimas: {a}/{b} nuotrauku":
        "Vizualus lyginimas: {a}/{b} nuotraukų",
    "; vizualiai panasiu grupiu: {n}": "; vizualiai panašių grupių: {n}",
    "ITARTINI paieska: {a}/{b} failu": "ĮTARTINŲ paieška: {a}/{b} failų",
    "Salinamos siuksles: {a}/{b}": "Šalinamos šiukšlės: {a}/{b}",
    "{f}/{ft} failu": "{f}/{ft} failų",
    "Atidaryti faila": "Atidaryti failą",
    "Atidaryti kataloga": "Atidaryti katalogą",
    "Kopijuoti kelia": "Kopijuoti kelią",
    "Apie programa": "Apie programą",
    "Dubliuotu failu paieska pagal turini - nieko netrina.":
        "Dubliuotų failų paieška pagal turinį — nieko netrina.",
    "Kurejo puslapis:": "Kūrėjo puslapis:",
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
    "paskyra). Niekas neissiunciama be jusu rankos.":
        "Kas įvyks paspaudus OK:\n\n"
        "1. Atsidarys interneto naršyklė su DI padėjėjo\n"
        "   claude.ai puslapiu. Žinutės laukelyje jau bus\n"
        "   įrašyta angliška pradžia — prisistatymas, kas per\n"
        "   programa ir kur jos kodas.\n"
        "2. NEIŠSIGĄSKITE raudono pranešimo virš žinutės —\n"
        "   claude.ai jį rodo visada, kai tekstas ateina per\n"
        "   nuorodą. Tai tik priminimas perskaityti, kas\n"
        "   siunčiama.\n"
        "3. Žinutės gale, po žodžių \"My question:\", įrašykite\n"
        "   SAVO klausimą — galima lietuviškai! — ir spauskite\n"
        "   siuntimo mygtuką (rodyklė). Klausti galima visko,\n"
        "   pvz.: „kaip atsinaujinti programą į naujesnę\n"
        "   versiją? paaiškink žingsnis po žingsnio“.\n"
        "4. Jei DI atsakys angliškai — tiesiog paprašykite kita\n"
        "   žinute: „atsakyk lietuviškai“, ir toliau bendraus\n"
        "   lietuviškai.\n\n"
        "Pastaba: claude.ai gali paprašyti prisijungti (nemokama\n"
        "paskyra). Niekas neišsiunčiama be jūsų rankos.",
}
