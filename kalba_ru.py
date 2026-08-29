# -*- coding: utf-8 -*-
"""SDF GUI RU zodynas (v1.3, 2026-08-22). Raktas - lietuviskas
tekstas is kalba.py _EN. Vertimu juodrastis - dukryte (lokalus
Hermes agentas), perziura ir taisymai - Claude. Neredaguoti ranka
be perziuros: placeholder'iai {n}/{mb:.2f}... privalo sutapti su raktu."""

_RU = {
    'Duplicate Finder':
        'Duplicate Finder',
    # v1.4 "Kuris cia pirminis?" - ataskaitos skiltys (informacija, ne
    # nurodymas: programa nieko netrina ir trinti nesiulo)
    'Greiciausiai pirminis':
        'Скорее всего оригинал',
    'Pastaba': 'Примечание',
    'mazesnes raiskos nei kiti grupeje': 'меньшее разрешение, чем у остальных',
    'kita orientacija nei kiti grupeje - patikrinkite, ar taip ir turi buti':
        'другая ориентация, чем у остальных — проверьте, так ли задумано',
    'Kodel':
        'Почему',
    'kiti grupeje vardu pazymeti kaip kopijos':
        'остальные по имени похожи на копии',
    'kiti guli kopiju aplankuose':
        'остальные лежат в папках с копиями',
    'kiti guli laikinuose aplankuose':
        'остальные лежат во временных папках',
    'kiti guli giliau aplankuose':
        'остальные лежат глубже в папках',
    'kiti sukurti veliau':
        'остальные созданы позже',
    'neaisku - pozymiu nera':
        'неясно — отличий нет',
    'visos kopijos laikinuose aplankuose':
        'все копии этой группы лежат во временных папках',
    # v1.4 "Ar yra naujesne versija?" langelis
    'Ar yra naujesne versija?':
        'Есть ли более новая версия?',
    'Jusu versija: {v}':
        'Ваша версия: {v}',
    'Ar yra naujesne? Trys keliai:':
        'Есть ли новее? Три пути:',
    '1. Naujienu puslapyje matysite naujausia versija:':
        '1. На странице релизов видна самая новая версия:',
    'Atidaryti naujienu puslapi':
        'Открыть страницу релизов',
    '2. Jei diegete per winget - spauskite Win+R, irasykite cmd,\n'
    '   spauskite Enter ir iklijuokite:':
        '2. Если устанавливали через winget — нажмите Win+R, введите cmd,\n'
        '   нажмите Enter и вставьте:',
    'Kopijuoti komanda':
        'Копировать команду',
    'Komanda nukopijuota':
        'Команда скопирована',
    '3. Arba paprasykite DI konsultanto - jis pats\n'
    '   pasitikrins ir pasakys, ko jums truksta:':
        '3. Или попросите ИИ-помощника — он сам проверит\n'
        '   и скажет, чего вам не хватает:',
    'Programa pati interneto neliecia. Sprendziate jus.':
        'Сама программа в интернет не выходит. Решаете вы.',
    '+   Prideti katalogus':
        '+   Добавить папки',
    '-   Pasalinti pasirinktus':
        '-   Удалить выбранные',
    '>>> Skenuoti':
        '>>> Сканировать',
    'Eksportuoti ataskaita':
        'Экспортировать отчёт',
    'Salinti OS siuksles':
        'Очистить мусор ОС',
    'Windows ir Mac miniatiuru kesai: Thumbs.db, ehthumbs.db,\n'
    '.DS_Store. Jusu failu neliecia. Pries trynima tikrinamas\n'
    'kiekvieno failo turinio parasas - neatitinkantys lieka.':
        'Кеши миниатюр Windows и Mac: Thumbs.db, ehthumbs.db,\n'
        '.DS_Store. Ваших файлов не касается. Перед удалением\n'
        'проверяется сигнатура содержимого — не совпавшие остаются.',
    'Itraukti katalogai:':
        'Папки для сканирования:',
    'Rezultatai:':
        'Результаты:',
    'Failo vardas':
        'Имя файла',
    'Pilnas kelias':
        'Полный путь',
    'Dydis (MB)':
        'Размер (МБ)',
    'Sukurimo data':
        'Дата создания',
    'Grupe':
        'Группа',
    'Pasirenges':
        'Готово',
    "Prideti katalogus ir spauskite 'Skenuoti'.":
        'Добавьте папки и нажмите «Сканировать».',
    'Pirma prideti bent viena kataloga.':
        'Сначала добавьте хотя бы одну папку.',
    'Zvalgyba: renkami failu dydziai...':
        'Разведка: собираем размеры файлов...',
    'Gilus tikrinimas (MD5 pagal turini)...':
        'Глубокая проверка (MD5 по содержимому)...',
    'Skenavimas atsauktas.':
        'Сканирование отменено.',
    'Nepazymeta ne viena seima - skenavimas atsauktas.':
        'Не выбрано ни одно семейство — сканирование отменено.',
    'Vyksta skenavimas':
        'Идёт сканирование',
    'Formuojama ataskaita':
        'Формируется отчёт',
    'Salinamos siuksles':
        'Удаляется мусор',
    'Pirma atlikti skana.':
        'Сначала выполните сканирование.',
    'Exportuojama...':
        'Идёт экспорт...',
    'Eksportas atsauktas.':
        'Экспорт отменён.',
    'Kur issaugoti ataskaita?':
        'Куда сохранить отчёт?',
    'Excel failai (*.xlsx)':
        'Файлы Excel (*.xlsx)',
    'Eksportas sekmingas':
        'Экспорт завершён',
    'Ataskaita sukurta:':
        'Отчёт создан:',
    'Failas neberastas:':
        'Файл больше не существует:',
    'Klaida:':
        'Ошибка:',
    'Exporto klaida:':
        'Ошибка экспорта:',
    'veikia':
        'работает',
    'Portable rezimas':
        'Портативный режим',
    'Kalba':
        'Язык',
    'Kalba pritaikoma paleidus programa is naujo.':
        'Язык будет применён после перезапуска программы.',
    'Kalba pasikeis paleidus programa is naujo.':
        'Язык изменится после перезапуска программы.',
    'Kalba issaugota. Perleisti programa dabar?':
        'Язык сохранён. Перезапустить программу сейчас?',
    'Nepavyko issaugoti: {}':
        'Не удалось сохранить: {}',
    'Ijungta: kesas ir zurnalas saugomi salia programos (pvz., flesiuke) - kompiuteryje pedsaku nelieka.\nIsjungta (numatyta): saugoma vartotojo kataloge %LOCALAPPDATA%\\SmartDuplicateFinder.':
        'Вкл.: кэш и журнал хранятся рядом с программой (напр. на флешке) — следов на компьютере не остаётся.\nВыкл. (по умолчанию): хранится в профиле пользователя %LOCALAPPDATA%\\SmartDuplicateFinder.',
    'Nepavyko perjungti rezimo: {}':
        'Не удалось переключить режим: {}',
    'Portable rezimas IJUNGTAS - duomenys salia programos':
        'Портативный режим ВКЛЮЧЁН — данные рядом с программой',
    'Portable rezimas isjungtas - duomenys vartotojo kataloge':
        'Портативный режим выключен — данные в профиле пользователя',
    'Perziureta failu: {n}, katalogu: {k} - dublikatu grupiu: {g}, {mb:.2f} MB':
        'Просмотрено файлов: {n}, папок: {k} — групп дубликатов: {g}, {mb:.2f} МБ',
    'Perziureta failu: {n}, katalogu: {k} - dublikatu grupiu: {g}; dubliai uzima {mb:.2f} MB, atlaisvinti galima {fmb:.2f} MB':
        'Просмотрено файлов: {n}, папок: {k} — групп дубликатов: {g}; дубликаты занимают {mb:.2f} МБ, можно высвободить {fmb:.2f} МБ',
    '; ITARTINI sarasas nukirptas ties {n} poru riba (susiaurink katalogus, jei nori visu)':
        '; Список ПОДОЗРИТЕЛЬНЫХ обрезан на пределе {n} пар (сузьте папки, чтобы видеть всё)',
    '; {n} failu ITARTINI patikroje praleista - per daug vienodo vardo failu vienoje vietoje (susiaurink katalogus)':
        '; {n} файлов пропущено в проверке ПОДОЗРИТЕЛЬНЫХ — слишком много одноимённых файлов в одном месте (сузьте папки)',
    '; {n} nuotrauku nepavyko atverti (sugadintos, nezinomo formato arba per didzuliu)':
        '; {n} снимков не удалось открыть (повреждены, неизвестный формат или слишком велики)',
    '; {n} nuotrauku liko nepalygintos - per daug panasiu vienoje vietoje (susiaurink katalogus)':
        '; {n} снимков остались несравнёнными — слишком много похожих в одном месте (сузьте папки)',
    '; nepasiekiamu failu praleista: {n}':
        '; недоступных файлов пропущено: {n}',
    'Dubliu kandidatu nerasta (perziureta failu: {n}{skip}).':
        'Кандидаты на дубликаты не найдены (проверено файлов: {n}{skip}).',
    ', {n} praleista':
        ', пропущено {n}',
    'Ankstesnio skeno rezultatai':
        'Результаты предыдущего сканирования',
    'Rasti ankstesnio skeno rezultatai ({kada}; dubliu grupiu: {n}).\nIkelti be pakartotinio skenavimo?':
        'Найдены результаты предыдущего сканирования ({kada}; групп дубликатов: {n}).\nЗагрузить без повторного сканирования?',
    'Ikelti {kada} skeno rezultatai - dublikatu grupiu: {g}, {mb:.2f} MB (galima eksportuoti be skenavimo)':
        'Загружены результаты сканирования от {kada} — групп дубликатов: {g}, {mb:.2f} МБ (можно экспортировать без сканирования)',
    'Keso ikelti nepavyko - skenuok is naujo.':
        'Не удалось загрузить кэш — просканируйте заново.',
    'Siuksliu nerasta - pirma atlik zvalgyba.':
        'Мусор не найден — сначала выполните разведку.',
    'Salinti Windows/Mac siuksles?':
        'Удалить системный мусор Windows/Mac?',
    'Sistemos siuksliu rasta: {n} ({mb:.1f} MB):':
        'Системного мусора найдено: {n} ({mb:.1f} МБ):',
    'Tai miniaturu/narsymo kesai - OS juos atsikuria pati.\nPries trynima kiekvienam failui tikrinamas turinio parasas;\nneatitinkantys NEBUS trinami.\n\nDEMESIO: tinklo diskuose (NAS) trynimas negriztamas\n(siuksliadeze ten neveikia). Trinti?':
        'Это кэши миниатюр и просмотра папок — ОС создаёт их заново.\nПеред удалением у каждого файла проверяется сигнатура\nсодержимого; несовпадающие НЕ будут удалены.\n\nВНИМАНИЕ: на сетевых дисках (NAS) удаление необратимо\n(корзина там не работает). Удалить?',
    'Siuksliu salinimas atsauktas.':
        'Удаление мусора отменено.',
    'Siuksliu istrinta: {n}, atlaisvinta {mb:.1f} MB':
        'Мусорных файлов удалено: {n}, освобождено {mb:.1f} МБ',
    '; praleista {n} (parasas nesutapo arba failas uzrakintas)':
        '; пропущено {n} (сигнатура не совпала или файл заблокирован)',
    'Rasti kandidatai i dublius':
        'Найдены кандидаты на дубликаты',
    'Vienodo dydzio failu grupes (kandidatai). Pazymekite,\nkurias seimas tikrinti giliai (MD5 pagal turini):':
        'Группы файлов одинакового размера (кандидаты).\nОтметьте, какие семейства проверить глубоко (MD5 по содержимому):',
    'Seima':
        'Семейство',
    'Grupiu':
        'Групп',
    'Failu':
        'Файлов',
    'Apimtis':
        'Объём',
    '~Laikas':
        '~Время',
    'Tikrinti pazymetus':
        'Проверить выбранные',
    'Atsaukti':
        'Отмена',
    'Is viso pazymejus viska: {mb} skaitymo, {t} (disko greitis ~{v} MB/s)':
        'Если отметить всё: чтение {mb}, {t} (скорость диска ~{v} МБ/с)',
    'akimirka':
        'мгновенно',
    'Prideti katalogus':
        'Добавить папки',
    'Iklijuokite kelius is Explorer (Ctrl+V) arba pasirinkite paspausdami mygtuka:':
        'Вставьте пути из Explorer (Ctrl+V) или выберите кнопкой:',
    'C:\\Ap1\nD:\\Ap2\nF:\\Ap3  (kiekvienas - naujoje eiluteje)':
        'C:\\Папка1\nD:\\Папка2\nF:\\Папка3  (каждая — с новой строки)',
    'Pasirinkti katalogus':
        'Выбрать папки',
    'Pasirinkti kataloga':
        'Выбрать папку',
    'Prideti':
        'Добавить',
    'Atstatyti':
        'Отмена',
    'Grupe {idx}':
        'Группа {idx}',
    'Dublikatai':
        'Дубликаты',
    'Panasios nuotraukos':
        'Похожие изображения',
    'Itartini':
        'Подозрительные',
    'Itartinas {n}':
        'Подозрительный {n}',
    'RODOMA {a} IS {b} EILUCIU - virsyta Excel lapo riba (1 048 576)':
        'ПОКАЗАНО {a} ИЗ {b} СТРОК — превышен лимит листа Excel (1 048 576)',
    # "на {n} файлов" luzta ties dazniausiu atveju n=2 (turi buti "файла") -
    # frazuojama be linksniavimo po skaiciaus, kaip v1.4 gramatikos pamokoje
    'DALIS {k} IS {n} - eiluciu daugiau nei telpa viename Excel faile, ataskaita padalinta i {n} failus':
        'ЧАСТЬ {k} ИЗ {n} — строк больше, чем вмещает один файл Excel; отчёт разделён на несколько файлов (всего: {n})',
    'Ataskaita padalinta i {n} failus (-1, -2, ...) - eiluciu daugiau nei telpa viename Excel faile':
        'Отчёт разделён на несколько файлов (всего: {n}; -1, -2, ...) — строк больше, чем вмещает один файл Excel',
    'ITARINI':
        'ПОДОЗРИТЕЛЬНЫЙ',
    'ITARTINI (panasus, bet ne identiski)':
        'ПОДОЗРИТЕЛЬНЫЕ (похожи, но не идентичны)',
    'Rodoma eiluciu: {n} (didziausios grupes virsuje) - PILNAS sarasas Excel ataskaitoje':
        'Показано строк: {n} (крупнейшие группы сверху) — ПОЛНЫЙ список в отчёте Excel',
    'Zvalgyba - failu: {n}...':
        'Разведка — файлов: {n}...',
    'Panasios nuotraukos (vizualiai)':
        'Похожие фото (визуально)',
    'VIZUALIAI PANASUS (skirtinga rezoliucija/kokybe)':
        'ВИЗУАЛЬНО ПОХОЖИЕ (другое разрешение/качество)',
    'Vaizdas {idx}':
        'Изображение {idx}',
    'Vizualus lyginimas: {a}/{b} nuotrauku':
        'Визуальное сравнение: {a}/{b} фото',
    '; vizualiai panasiu grupiu: {n}':
        '; групп визуально похожих: {n}',
    'ITARTINI paieska: {a}/{b} failu':
        'Поиск ПОДОЗРИТЕЛЬНЫХ: {a}/{b} файлов',
    'Salinamos siuksles: {a}/{b}':
        'Удаляется мусор: {a}/{b}',
    '{f}/{ft} failu':
        '{f}/{ft} файлов',
    'liko':
        'осталось',
    'Pagalba':
        'Справка',
    'Apie...':
        'О программе...',
    'Instrukcija':
        'Руководство пользователя',
    'Neradote atsakymo? Klauskite DI':
        'Не нашли ответа? Спросите ИИ',
    'Nepavyko atidaryti: {}':
        'Не удалось открыть: {}',
    'Apie programa':
        'О программе',
    'Dubliuotu failu paieska pagal turini - nieko netrina.':
        'Поиск дубликатов файлов по содержимому — ничего не удаляет.',
    'Versija {v}':
        'Версия {v}',
    'Kurejo puslapis:':
        'Страница проекта:',
    'Kas ivyks paspaudus OK:\n\n1. Atsidarys interneto narsykle su DI padejejo\n   claude.ai puslapiu. Zinutes laukelyje jau bus\n   irasyta angliska pradzia - prisistatymas, kas per\n   programa ir kur jos kodas.\n2. NEISSIGASKITE raudono pranesimo virs zinutes -\n   claude.ai ji rodo visada, kai tekstas ateina per\n   nuoroda. Tai tik priminimas perskaityti, kas\n   siunciama.\n3. Zinutes gale, po zodziu "My question:", irasykite\n   SAVO klausima - galima lietuviskai! - ir spauskite\n   siuntimo mygtuka (rodykle). Klausti galima visko,\n   pvz.: "kaip atsinaujinti programa i naujesne\n   versija? paaiskink zingsnis po zingsnio".\n4. Jei DI atsakys angliskai - tiesiog paprasykite kita\n   zinute: "atsakyk lietuviskai", ir toliau bendraus\n   lietuviskai.\n\nPastaba: claude.ai gali paprasyti prisijungti (nemokama\npaskyra). Niekas neissiunciama be jusu rankos.':
        'Что произойдёт после нажатия OK:\n\n1. Откроется веб-браузер с ИИ-помощником\n   на странице claude.ai. В поле сообщения уже будет\n   вписано английское начало — представление, какая это\n   программа и где находится её код.\n2. НЕ пугайтесь красного уведомления над сообщением —\n   claude.ai показывает его всегда, когда текст приходит\n   по ссылке. Это лишь напоминание прочитать, что\n   Вы отправляете.\n3. В конце сообщения, после слов "My question:",\n   впишите СВОЙ вопрос — на любом языке! — и нажмите\n   кнопку отправки (стрелка). Спрашивать можно о чём\n   угодно, напр.: "как обновить программу до последней\n   версии? объясни шаг за шагом".\n4. Если ИИ ответит не на том языке — просто попросите\n   в следующем сообщении: "ответь по-русски", и тогда\n   беседа пойдёт на русском.\n\nПримечание: claude.ai может попросить войти (бесплатная\nучётная запись). Ничего не будет отправлено без\nВашего действия.',
    'Atidaryti faila':
        'Открыть файл',
    'Atidaryti kataloga':
        'Открыть папку',
    'Kopijuoti kelia':
        'Копировать путь',
    'Kelias nukopijuotas':
        'Путь скопирован',
}

_FAM_RU = {
    'Paveiksliukai': 'Изображения',
    'Video': 'Видео',
    'Audio': 'Аудио',
    'Dokumentai': 'Документы',
    'Archyvai': 'Архивы',
    'CAD': 'CAD',
    'Kodas': 'Код',
    'Programos': 'Программы',
    'Kita': 'Прочее',
}
