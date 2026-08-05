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

Tai SĄMONINGAS SAUGUMO PRINCIPAS, ne trūkumas: jokia automatika
nenuspręs už jus, kurią kopiją palikti — gal dublis kataloge guli
tyčia (atsarginė kopija, projekto komplektas). Programa niekada
neištrins to, ko nenorėjote — todėl ja galima drąsiai skenuoti
net svarbiausius archyvus.

O Excel ataskaita tam ir skirta: tvarkytis SAVO TEMPU. Nebūtina
viską daryti iš karto — ataskaita lieka failu, ją galima atsidaryti
kad ir po savaitės, rūšiuoti, žymėtis spalvomis kas sutvarkyta,
ir eiti per dublius po kelis kasdien, kol diskas švarus.

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
   patogu iškart nueiti ir sutvarkyti.
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
baitais). Rezultatuose tokios grupės rodomos violetine spalva
(„VIZUALIAI PANAŠŪS"), o Excel ataskaitoje — atskirame lape
„Similar Images".
Pastaba dėl laiko: šiam lyginimui reikia atverti KIEKVIENĄ nuotrauką
(~40 nuotr./s), tad dideliems archyvams (dešimtys tūkstančių nuotraukų)
tai užtrunka — skubant varnelę galima nuimti. Grupės, kur visi failai ir taip
identiški (jau rasti kaip dubliai), čia nekartojamos — rodomos tik
tikros „paslėptos" kopijos.

GUDRYBĖS, KURIAS VERTA ŽINOTI
-----------------------------
* SKENO ATMINTIS: baigus skenavimą rezultatai įsimenami. Kitą kartą
  paleidus programą ji pasiūlys įkelti praėjusio skeno rezultatus
  be pakartotinio skenavimo — galima iškart eksportuoti.
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
* Tarnybiniai failai — kompiuterio %TEMP%\SmartDuplicateFinder\:
    paskutinis_skenas.json  – skeno atmintis
    scan_speed.json         – disko greitis laiko prognozėms
    veiklos.log             – veiklos žurnalas (jei kas stringa,
                              šis failas padeda išsiaiškinti kur)
  Į fleškę ar programos katalogą nerašoma nieko — galima drąsiai
  leisti iš fleškės svetimame kompiuteryje.
* Visus tarnybinius failus galima bet kada ištrinti — programa
  tiesiog pradės nuo švaraus lapo.

---------------------------------------------------------------------
Sukūrė: Robertas + Claude (Anthropic AI) + vietinė AI „mergytė"
2026-08-05        Versija: v2
=====================================================================
