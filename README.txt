=====================================================================
  SMART DUPLICATE FINDER v2 — dublikuotų failų paieškos programa
=====================================================================

KAS TAI
-------
Programa suranda dubliuotus (identiško turinio) failus pasirinktuose
kataloguose ar visame diske ir parodo, kiek vietos jie užima.
Failai lyginami pagal TURINĮ (MD5 kontrolinę sumą), ne pagal vardą —
todėl randami ir pervadinti dubliai, o vienodo vardo, bet skirtingo
turinio failai dubliais nelaikomi.

Papildomai programa moka surasti ir išvalyti NEMATOMAS sistemos
šiukšles (Thumbs.db ir pan.) — žr. skyrių žemiau.

SVARBU: dublių programa NETRINA — tik suranda ir parodo; ką daryti,
sprendžiate patys. Vienintelis trynimas — sistemos šiukšlių valymas,
ir tas vyksta tik jums patvirtinus.

Paklauskite bet ko, kas dublių ieškiklius naudoja ne pirmus metus,
ir išgirsite tą pačią istoriją: vieną dieną programa ištrynė ne
tuos failus. Tai ne vieno konkretaus įrankio klaida — tai kiekvieno
algoritmo riba. JOKS ALGORITMAS NEGALI NUSPRĘSTI, KAS SVARBU BŪTENT
JUMS: kas vienam šiukšlė, kitam — vienintelė išlikusi atsarginė
kopija.

Todėl tai SĄMONINGAS SAUGUMO PRINCIPAS, ne trūkumas: jokia automatika
nenuspręs už jus, kurią kopiją palikti — gal dublis kataloge guli
tyčia (atsarginė kopija, projekto komplektas). Programa niekada
neištrins to, ko nenorėjote — todėl ja galima drąsiai skenuoti
net svarbiausius archyvus.

O Excel ataskaita tam ir skirta: tvarkytis SAVO TEMPU. Nebūtina
viską daryti iš karto — ataskaita lieka failu, ją galima atsidaryti
kad ir po savaitės, rūšiuoti, žymėtis spalvomis kas sutvarkyta,
ir eiti per dublius po kelis kasdien, kol diskas švarus. O jei
peržiūrėję nuspręsite pasilikti visas kopijas iki vienos — tai
irgi visiškai geras rezultatas. Tikslas čia ne ištrinti gigabaitai,
o žinojimas, ką tiksliai turite, ir JŪSŲ paties priimtas sprendimas.

KAIP PALEISTI
-------------
1. Reikia tik vieno failo: SmartDuplicateFinder.exe
   Jokio diegimo, jokio Python — veikia tiesiai iš fleškės ar bet
   kurio katalogo.
2. Pirmas paleidimas užtrunka kelias sekundes ilgiau — tai normalu.
3. Jei Windows parodo mėlyną langą „Windows protected your PC" —
   spauskite „More info" → „Run anyway". Taip nutinka, nes programa
   nepasirašyta sertifikatu (ji saugi, tiesiog namudinė).

KAIP NAUDOTIS (žingsnis po žingsnio)
------------------------------------
1. „+ Pridėti katalogus" — pasirinkite, kur ieškoti (galima visą
   diską, pvz. D:\). Kelius galima ir įklijuoti iš Explorer.
2. „>>> Skenuoti" — pirmiausia įvyks greita ŽVALGYBA (skaitomi tik
   failų dydžiai, tai užtrunka sekundes).
3. Iššoks langas „Rasti kandidatai į dublius" — kandidatai suskirstyti
   pagal tipą (Paveiksliukai, Video, Dokumentai, CAD, Kodas ir t.t.)
   su apimtimi ir LAIKO PROGNOZE kiekvienai eilutei.
   PATARIMAS: „Kodas" ir „Kita" dažniausiai verta atžymėti — ten
   tūkstančiai smulkių programų failiukų, kurių valyti nereikia,
   o tikrinimas ilgiausias. Palikite Paveiksliukus, Video, Audio,
   Dokumentus, Archyvus, Programas.
4. „Tikrinti pažymėtus" — vyks gilus tikrinimas pagal turinį.
   Apatiniame dešiniame kampe matysite gyvą eigą: kiek failų
   patikrinta, greitį (MB/s) ir kiek liko laukti.
5. Rezultatų lentelėje dubliai sugrupuoti spalvomis pagal tipą;
   DIDŽIAUSI dubliai — viršuje. Užvedus pelę matysite failo tipo
   aprašymą.
6. DVIGUBAS KLIKAS ant eilutės atidaro Explorer su pažymėtu failu —
   patogu iškart nueiti ir sutvarkyti. DEŠINYS KLAVIŠAS (nuo v1.3)
   siūlo: atidaryti failą / atidaryti katalogą / kopijuoti kelią
   (vykdomųjų failų atidarymas saugumo sumetimais išjungtas).
7. „Eksportuoti ataskaitą" — pilnas sąrašas išsaugomas į spalvotą
   Excel failą (paklaus, kur padėti; siūlys Dokumentus).

SISTEMOS ŠIUKŠLIŲ VALYMAS (mygtukas „Šalinti šiukšles")
-------------------------------------------------------
Kas tai: Windows ir Mac naršant katalogus palieka NEMATOMUS kešo
failiukus, kurių Explorer paprastai nerodo (jie paslėpti sisteminiai):
  * Thumbs.db, ehthumbs.db — Windows miniatiūrų (peržiūros ikonėlių)
    kešas; atsiranda kataloguose su paveiksliukais
  * .DS_Store — Mac Finder naršymo šiukšlė (dažna NAS diskuose)
Jie nepavojingi, bet šiukšlina, ypač tinklo diskus — o kadangi
nematomi, ranka jų ištrinti sunku.

Kaip veikia:
1. Po žvalgybos (jei šiukšlių rasta) suaktyvėja mygtukas
   „Šalinti šiukšles (N)" — skliaustuose kiekis.
2. Paspaudus rodoma santrauka pagal tipą ir prašoma patvirtinti.
3. SAUGIKLIS: prieš trinant KIEKVIENAM failui patikrinamas turinio
   parašas (magic bytes). Jei failas tik vadinasi Thumbs.db, bet jo
   turinys kitoks — jis NELIEČIAMAS. Abejonė = netrinama.
4. Po valymo parodoma, kiek ištrinta ir kiek vietos atlaisvinta.
   Windows šiuos kešus prireikus susikuria iš naujo — tai normalu.
DĖMESIO: tinklo diskuose (NAS) trynimas negrįžtamas — šiukšliadėžės
ten nėra. Dėl to ir tikrinami parašai.

Pastaba: desktop.ini failų programa SĄMONINGAI neliečia — jie saugo
katalogų nustatymus (ikonas, rodinius).

PANAŠIOS NUOTRAUKOS (vizualus lyginimas)
----------------------------------------
Kandidatų lange yra papildoma eilutė „Panašios nuotraukos (vizualiai)"
(varnelė uždėta kaip ir kitoms). Su ja programa palygina nuotraukas
VIZUALIAI — randa tą pačią nuotrauką net jei ji sumažinta, išsaugota
kita kokybe ar kitu formatu (MD5 tokių nemato, nes failai skiriasi
baitais). Veikia su įprastais formatais (JPG, PNG, GIF, BMP, TIFF,
WebP), o nuo v1.3 — ir su iPhone formatais HEIC/AVIF; telefono
nuotraukos, saugomos „pasuktos" (EXIF orientacija), sulyginamos
teisingai. Rezultatuose tokios grupės rodomos violetine spalva
(„VIZUALIAI PANAŠŪS"), o Excel ataskaitoje — atskirame lape
„Similar Images".
Pastaba dėl laiko: šiam lyginimui reikia atverti KIEKVIENĄ nuotrauką
(~40 nuotr./s), tad dideliems archyvams (dešimtys tūkstančių nuotraukų)
tai užtrunka — skubant varnelę galima nuimti. Grupės, kur visi failai ir taip
identiški (jau rasti kaip dubliai), čia nekartojamos — rodomos tik
tikros „paslėptos" kopijos.

KURIS IŠ JŲ PIRMINIS? (nuo v1.4)
--------------------------------
Excel ataskaitos lape „Dublikatai" yra du stulpeliai: „Greičiausiai
pirminis" (varnelė) ir „Kodėl". Programa pažiūri, ką apie failus sako
jų pačių vardai ir vietos, ir pasako, kuris grupės failas atrodo esąs
senelis — IR KODĖL būtent jis. Pavyzdžiui:
  * kiti grupėje vardu pažymėti kaip kopijos („svente (1).jpg");
  * kiti guli kopijų aplankuose („Atsarginė kopija", „Backup");
  * kiti guli laikinuose aplankuose (Atsisiuntimai, Temp);
  * kiti guli giliau aplankuose arba sukurti vėliau.

Trys dalykai, kuriuos svarbu pasakyti garsiai:
1. Tai INFORMACIJA, o ne nurodymas. Programa nieko nežymi trynimui ir
   nieko netrina — sprendžiate jūs. Varnelė reiškia „štai kas krito į
   akis", ne „šitą palik, kitus naikink".
2. Kai požymių nėra, stulpelyje rašoma „neaišku — požymių nėra".
   Sąžiningas „nežinau" čia geriau už gražiai atrodantį spėjimą.
3. Programa nežino jūsų istorijos. Ji mato tik vardus, aplankus ir
   datas. Jei failą kadaise persikėlėte ar pervadinote, tie požymiai
   gali rodyti ne ten — todėl paskutinis žodis visada jūsų.

AR YRA NAUJESNĖ VERSIJA?
------------------------
Programa PATI naujinimų netikrina ir niekada apie juos nepraneš —
ji visiškai neturi prieigos prie interneto, ir tai sąmoningas
sprendimas: nieko neišsiunčia, nieko neatsiunčia, nieko apie jus
nežino. Kaina už tą tylą — pasitikrinti turite patys. Verta tai
padaryti kartą per kelis mėnesius.

Greičiausias kelias: „?" -> „Ar yra naujesnė versija?". Tas langelis
parodo jūsų versiją ir visus tris būdus pasitikrinti (mygtukai jame
patys atidaro naujienų puslapį arba nukopijuoja winget komandą).

Kaip pasitikrinti rankomis (pusė minutės):
  github.com/RobertasTa/smart-duplicate-finder/releases/latest
Tame puslapyje visada nurodyta naujausia versija ir kas joje
pasikeitė. Savo versiją rasite programoje: „?" -> „Apie programą".

Kaip atsinaujinti:
* Jei diegėtės per winget (Windows paketų tvarkyklė) — komandinėje
  eilutėje: winget upgrade RobertasTa.SmartDuplicateFinder
  (winget katalogas gali kelias dienas atsilikti nuo GitHub; jei
  jis dar rodo senąją versiją, naudokite kelią žemiau).
* Jei tiesiog parsisiuntėte exe — parsisiųskite naują iš nuorodos
  aukščiau ir pakeiskite senąjį failą. Nieko daugiau daryti
  nereikia: diegimo programos nėra, registre nieko nesaugoma,
  senąjį exe galima tiesiog ištrinti.

Jūsų duomenys nepražūva: skenų atmintis ir nustatymai gyvena
atskirai nuo exe (žr. skyrių „KUR PROGRAMA KĄ SAUGO"), o jūsų
paties failų programa neliečia niekada.

Tinginio būdas: „?" -> „Neradote atsakymo? Klauskite DI" ir
paprašykite: „patikrink, ar yra naujesnė versija už mano".
Naršyklėje atsidariusiam DI padėjėjui internetas prieinamas — jis
pats pasitikrins, palygins su jūsų versija ir paaiškins, ką
naujoji duoda.

GUDRYBĖS, KURIAS VERTA ŽINOTI
-----------------------------
* SKENO ATMINTIS, ATSPARI LŪŽIMAMS: rezultatai įrašomi į diską vos
  skenui pasibaigus — dar PRIEŠ piešiant lentelę. Net jei programa
  būtų nudobta ar nulūžtų iškart po ilgo skeno, rezultatai
  neprapuola: kitą kartą paleidus ji pasiūlys įkelti praėjusio skeno
  rezultatus be pakartotinio skenavimo — galima iškart eksportuoti.
  Valandų trukmės skenas niekada neprarandamas.
* Lentelėje rodoma iki 2 000 eilučių (didžiausios grupės), kad langas
  neliūžtų — PILNAS sąrašas visada yra Excel ataskaitoje.
* ITARTINI sekcija (geltona) — failai vienodais vardais ir panašiu
  dydžiu, bet SKIRTINGU turiniu. Tai ne dubliai, bet verta žvilgtelti
  (pvz. dvi skirtingos to paties dokumento versijos).
* Skirtingas failo dydis = garantuotai ne dublis, todėl tokie failai
  net neskaitomi — dėl to programa tokia greita net dideliems diskams.
* Tušti (0 baitų) failai praleidžiami sąmoningai.

KUR PROGRAMA KĄ SAUGO
---------------------
* Excel ataskaitos — kur pasirinksite (siūlomi Dokumentai).
* Tarnybiniai failai — %LOCALAPPDATA%\SmartDuplicateFinder\:
    last_scan.json   – skeno atmintis
    scan_speed.json  – disko greitis laiko prognozėms
    activity.log     – veiklos žurnalas (jei kas stringa, šis
                       failas padeda išsiaiškinti kur)
    language.txt     – pasirinkta kalba
  (iki v1.4 šie failai vadinosi lietuviškai; programa senuosius
  persivadina pati, nieko daryti nereikia.)
* PORTABLE REŽIMAS (varnelė kairės juostos apačioje): įjungus,
  tarnybiniai failai saugomi kataloge SmartDuplicateFinder_data
  ŠALIA programos (pvz., fleškėje), o kompiuteryje pėdsakų nelieka —
  programa net ištrina savo anksčiau sukurtą %LOCALAPPDATA% katalogą.
  Pasirinkimą atsimena failas SDF_portable.txt šalia exe (Notepad++ /
  VS Code konvencija) — jis keliauja kartu su fleške.
  (Iki v1.4 duomenys gulėjo bendrame _darbal kataloge — tame pačiame,
  kurį naudojo ir Temp Cleaner, tad viena programa išsiveždavo kitos
  duomenis. Nuo v1.4 kiekviena turi savo katalogą; senieji duomenys
  perkeliami automatiškai pirmo paleidimo metu.)
* Visus tarnybinius failus galima bet kada ištrinti — programa
  tiesiog pradės nuo švaraus lapo.
* KALBA (Lietuvių / English / Русский / Deutsch) perjungiama
  išsiskleidžiančiame sąraše kairės juostos apačioje; pasirinkimas
  įsimenamas ir pritaikomas paleidus programą iš naujo.

---------------------------------------------------------------------
Sukūrė: Robertas + Claude (Anthropic AI) + vietinis AI pagalbininkas
2026-08-05        Versija: v2
=====================================================================
