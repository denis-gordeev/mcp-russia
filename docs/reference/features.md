# Каталог features

22 российских модуля · 184 инструмента · 65 ресурсов · 44 промпта

Этот каталог описывает текущее содержимое сервера. Все модули используют русские имена переменных и функций и подключены к реальным российским API.

> **Статус миграции:** сервер полностью перешёл на российские реалии. 22 российских модуля данных подключены к реальным API. Legacy-модули с бразильскими данными удалены из кодовой базы.

---

## Российские модули

### `cbrf` — Центральный банк Российской Федерации (6 tools, 3 resources, 2 prompts)

Курсы валют, конвертация, сравнение валют и экономические индикаторы ЦБ РФ.

| Tool | Описание |
|------|----------|
| `tekushchie_kursy` | Официальные курсы основных валют ЦБ РФ на сегодня (USD, EUR, CNY, GBP, JPY, CHF) |
| `uznat_kurs_valyuty` | Курс одной конкретной валюты с изменением за период |
| `spisok_valyut` | Полный справочник доступных валют с кодами и номиналами |
| `konvertirovat_valyutu` | Конвертация суммы из иностранной валюты в рубли по курсу ЦБ |
| `sravnit_valyuty` | Сравнительная таблица курсов нескольких валют (до 10) |
| `kursy_po_stranam` | Курсы валют основных стран-партнёров России |

**Resources:** `data://valyuty` (все валюты), `data://osnovnye` (основные), `data://spravochnik` (справочник)

**Prompts:** `analise_valyut`, `obzor_ekonomiki`

**Авторизация:** не требуется

### `rosstat` — Федеральная служба государственной статистики (13 tools, 2 resources, 2 prompts)

Демография, экономика, региональная статистика, федеральные округа, ВРП, заработная плата, отраслевая структура ВРП по ОКВЭД, инвестиции по видам деятельности, региональное сравнение, универсальный запрос по коду ЕМИСС. Реальные API: fedstat.ru (ЕМИСС). 92 субъекта РФ. 27 кодов показателей ЕМИСС.

| Tool | Описание |
|------|----------|
| `spisok_regionov` | Список субъектов Российской Федерации (92 субъекта) с кодами OKATO |
| `spisok_okrugov` | Список федеральных округов РФ |
| `region_info` | Детальная информация о регионе: население, ВРП, средняя зарплата (ЕМИСС) |
| `okrug_info` | Информация о федеральном округе с перечнем субъектов |
| `pokazateli_rosstata` | Справочник основных показателей Росстата (21 показатель) |
| `inflyaciya` | Данные об инфляции (ИПЦ) из ЕМИСС |
| `demografiya` | Демографические данные из ЕМИСС (рождаемость, смертность, численность) |
| `vrp_dannye` | Данные о валовом региональном продукте (ВРП) с разбивкой по регионам |
| `zarplata_dannye` | Данные о средней заработной плате с региональной разбивкой |
| `sravnenie_regionov` | Рейтинг и сравнение регионов по выбранному показателю |
| `indikator_dannye` | Универсальный запрос данных показателя по коду ЕМИСС или мнемоническому коду |
| `otraslevaya_struktura_vrp` | Отраслевая структура ВРП по видам экономической деятельности (ОКВЭД) |
| `investitsii_po_vidam` | Инвестиции в основной капитал по видам экономической деятельности |

**Resources:** `data://istochniki` (источники данных), `data://metodologiya`

**Prompts:** `analiz_regiona`, `obzor_inflyacii`

**Авторизация:** не требуется

### `gosduma` — Государственная Дума (6 tools, 2 resources, 2 prompts)

Депутаты, фракции, комитеты, законопроекты, созывы.

| Tool | Описание |
|------|----------|
| `spisok_deputatov` | Список депутатов Госдумы с фильтрацией по созыву |
| `info_deputata` | Карточка депутата: фракция, комитет, регион, созыв |
| `spisok_frakcii` | Справочник фракций Государственной Думы |
| `spisok_komitetov` | Справочник комитетов Госдумы |
| `spisok_sozyvov` | Список созывов Государственной Думы |
| `zakonoproekty` | Законопроекты с фильтрацией по статусу |

**Resources:** `data://istochniki` (источники), `data://struktura` (структура Думы)

**Prompts:** `analiz_deputata`, `obzor_zakonodatelstva`

**Авторизация:** опциональная (MCP_RUSSIA_DUMA_API_TOKEN для полного доступа)

### `cekrf` — Центральная избирательная комиссия РФ (10 tools, 5 resources, 2 prompts)

Выборы, кандидаты, партии, результаты, явка. Подключено к ГАС «Выборы» (vybory.izbirkom.ru).

| Tool | Описание |
|------|----------|
| `tipy_vyborov` | Типы выборов в РФ |
| `subyekty_rf` | Список субъектов РФ |
| `dolzhnosti_federal` | Избираемые федеральные должности |
| `partii_rf` | Зарегистрированные политические партии |
| `gody_vyborov` | Годы проведения выборов |
| `poisk_kandidata` | Поиск кандидата по имени |
| `kandidat_podrobno` | Подробная карточка кандидата |
| `rezultaty_vyborov` | Результаты выборов |
| `yavka_i_itogi` | Явка и итоги голосования |
| `spisok_vyborov` | Список известных выборов (федеральные) |

**Resources:** `data://tipy-vyborov`, `data://subyekty-rf`, `data://partii-rf`, `data://info-api`, `data://izvestnye-vybory`

**Prompts:** `analiz_kandidata`, `sravnenie_partiy`

**Авторизация:** не требуется

### `rosapi` — Справочные данные РФ (8 tools, 2 resources, 2 prompts)

Адреса (ФИАС), организации (ИНН/ОГРН), банки (БИК), праздники, налоговые ставки.

| Tool | Описание |
|------|----------|
| `konsul_adres_po_indeksu` | Найти адрес по почтовому индексу РФ |
| `poisk_adresa` | Поиск адреса по свободному запросу через ФИАС |
| `poisk_org_po_inn` | Найти организацию по ИНН |
| `poisk_org_po_ogrn` | Найти организацию по ОГРН |
| `spisok_bankov` | Справочник банков России с БИК |
| `konsul_bank_po_bik` | Информация о банке по БИК |
| `prazdniki_rf` | Национальные праздники РФ |
| `nalogovye_stavki` | Основные налоговые ставки РФ |

**Resources:** `data://nalogovye-stavki`, `data://servisy`

**Prompts:** `analiz_organizacii`, `poisk_adresa_prompt`

**Авторизация:** требуется (MCP_RUSSIA_DADATA_API_KEY)

### `zakupki` — Единая информационная система закупок (7 tools, 3 resources, 2 prompts)

Государственные закупки, контракты, заказчики, поставщики (44-ФЗ, 223-ФЗ).

| Tool | Описание |
|------|----------|
| `poisk_zakupok` | Поиск закупок по параметрам |
| `info_zakupki` | Информация о закупке |
| `info_zakazchika` | Информация о заказчике |
| `info_postavshchika` | Информация о поставщике |
| `statusy_zakupok` | Справочник статусов закупок |
| `sposoby_zakupok` | Справочник способов закупок |
| `plany_zakupok` | Планы закупок |

**Resources:** `data://istochniki`, `data://zakonodatelstvo`, `data://struktura`

**Prompts:** `analiz_zakupki`, `obzor_zakupok`

**Авторизация:** опциональная (MCP_RUSSIA_ZAKUPKI_API_TOKEN для полного доступа)

### `minzdrav` — Министерство здравоохранения РФ (7 tools, 3 resources, 2 prompts)

Медицинские организации, кадры, показатели здоровья, заболеваемость.

| Tool | Описание |
|------|----------|
| `poisk_med_organizatsiy` | Поиск медицинских организаций |
| `info_med_organizatsii` | Информация о медицинской организации |
| `pokazateli_zdorovya` | Показатели здоровья населения |
| `statistika_zabolevaniy` | Статистика заболеваемости |
| `spravochnik_mo` | Справочник типов медицинских организаций |
| `spravochnik_spetsialnostey` | Справочник медицинских специальностей |
| `spravochnik_mkb10` | Справочник МКБ-10 |

**Resources:** `data://istochniki`, `data://klassifikatsii`, `data://okruga`

**Prompts:** `analiz_zdorovya_regiona`, `obzor_med_organizatsiy`

**Авторизация:** не требуется

### `kad_arbitrazh` — Картотека арбитражных дел (8 tools, 3 resources, 2 prompts)

Судебные дела, акты, стороны, справочники категорий и инстанций.

| Tool | Описание |
|------|----------|
| `poisk_del` | Поиск судебных дел |
| `info_dela` | Информация о деле |
| `akty_po_delu` | Судебные акты по делу |
| `storony_dela` | Стороны дела |
| `spravochnik_kategoriy` | Справочник категорий дел |
| `spravochnik_instantsiy` | Справочник судебных инстанций |
| `spravochnik_statusov` | Справочник статусов дел |
| `spravochnik_aktov` | Справочник типов актов |

**Resources:** `data://istochniki`, `data://sistema`, `data://kodifikatsiya`

**Prompts:** `analiz_dela`, `analiz_uchastnika`

**Авторизация:** не требуется

### `rosaudit` — Счётная палата РФ (7 tools, 3 resources, 2 prompts)

Контрольные мероприятия, аудиторские заключения, нарушения, исполнение бюджета.

| Tool | Описание |
|------|----------|
| `spisok_napravleniy` | Справочник направлений контроля |
| `spisok_tipov_meropriyatiy` | Справочник типов мероприятий |
| `spisok_subiektov_audita` | Справочник субъектов аудита |
| `info_kontrolnogo_meropriyatiya` | Информация о контрольном мероприятии |
| `info_auditorskogo_zaklyucheniya` | Информация об аудиторском заключении |
| `ispolnenie_byudzheta` | Данные об исполнении бюджета |
| `poisk_narusheniy` | Поиск нарушений |

**Resources:** `data://istochniki`, `data://zakonodatelstvo`, `data://struktura`

**Prompts:** `analiz_auditorskogo_zaklyucheniya`, `obzor_ispolneniya_byudzheta`

**Авторизация:** не требуется

### `rosgidromet` — Росгидромет (7 tools, 3 resources, 2 prompts)

Погода, прогнозы, экология, предупреждения, спутниковый мониторинг.

| Tool | Описание |
|------|----------|
| `spisok_stanciy` | Справочник станций мониторинга |
| `spisok_tipov_dannykh` | Справочник типов данных |
| `pogoda_seychas` | Текущая погода |
| `prognoz_pogody` | Прогноз погоды |
| `ekologiya_regiona` | Экологические данные по региону |
| `preduprezhdeniya` | Предупреждения об опасных явлениях |
| `sputnik_monitoring` | Данные спутникового мониторинга |

**Resources:** `data://istochniki`, `data://metodologiya`, `data://opasnye-yavleniya`

**Prompts:** `analiz_pogody_regiona`, `obzor_ekologii`

**Авторизация:** не требуется

### `rosvodresursy` — Росводресурсы (7 tools, 3 resources, 2 prompts)

Бассейновые округа, водные объекты, водохранилища, мониторинг, водопользование.

| Tool | Описание |
|------|----------|
| `spisok_basseynovykh_okrugov` | Справочник бассейновых округов |
| `spisok_tipov_vodnykh_obektov` | Справочник типов водных объектов |
| `spisok_vodokhranilishch` | Справочник водохранилищ |
| `info_vodnogo_obekta` | Информация о водном объекте |
| `gidro_monitoring` | Данные гидрологического мониторинга |
| `info_vodokhranilishcha` | Информация о водохранилище |
| `vodopolzovanie_regionov` | Данные о водопользовании по регионам |

**Resources:** `data://istochniki`, `data://basseynovye-okruga`, `data://vodokhozyaystvo`

**Prompts:** `analiz_vodnogo_obekta`, `obzor_vodokhranilishch`

**Авторизация:** не требуется

### `publikatsii` — Официальные публикации (9 tools, 3 resources, 2 prompts)

Нормативные акты, законопроекты, поиск, официальные публикации pravo.gov.ru. Подключено к порталу открытых данных pravo.gov.ru.

| Tool | Описание |
|------|----------|
| `spisok_tipov_aktov` | Справочник типов нормативных актов |
| `spisok_otrasley` | Справочник отраслей законодательства |
| `spisok_istochnikov` | Справочник источников публикаций |
| `spisok_statusov` | Справочник статусов актов |
| `info_normativnogo_akta` | Информация о нормативном акте |
| `info_zakonproekta` | Информация о законопроекте |
| `poisk_aktov` | Поиск нормативных актов |
| `publikatsii_po_datam` | Публикации по датам |
| `izmeneniya_akta` | Изменения нормативного акта |

**Resources:** `data://istochniki`, `data://poryadok-opublikovaniya`, `data://struktura-zakonodatelstva`

**Prompts:** `analiz_normativnogo_akta`, `obzor_zakonodatelstva`

**Авторизация:** не требуется

### `rospotrebnadzor` — Роспотребнадзор (11 tools, 3 resources, 2 prompts)

Проверки, нарушения, санитарные нормы, потребительские жалобы. Реальные API: proverki.rospotrebnadzor.ru, zpp.rospotrebnadzor.ru.

| Tool | Описание |
|------|----------|
| `spisok_napravleniy` | Справочник направлений надзора |
| `spisok_tipov_proverok` | Справочник типов проверок |
| `spisok_kategoriy_obiektov` | Справочник категорий объектов |
| `spisok_regionalnyh_upravleniy` | Справочник региональных управлений |
| `info_proverki` | Информация о проверке из реестра proverki.rospotrebnadzor.ru |
| `poisk_proverok` | Поиск проверок по ИНН/названию/региону |
| `plan_proverok` | План проверок Роспотребнадзора |
| `poisk_narusheniy` | Поиск нарушений в реестре проверок |
| `spisok_sanpinov` | Справочник СанПиН |
| `zhaloby_potrebiteley` | Потребительские жалобы (zpp.rospotrebnadzor.ru) |
| `pokazateli_bezopasnosti` | Показатели безопасности |

**Resources:** `data://istochniki`, `data://zakonodatelstvo`, `data://struktura`

**Prompts:** `analiz_proverki`, `obzor_sanitarnoy_situacii`

**Авторизация:** не требуется

### `roskomnadzor` — Роскомнадзор (13 tools, 3 resources, 2 prompts)

Лицензии, СМИ, персональные данные, реестры, нарушения. Реальные API: rkn.gov.ru, eais.rkn.gov.ru.

| Tool | Описание |
|------|----------|
| `spisok_napravleniy` | Справочник направлений надзора |
| `spisok_tipov_licenziy` | Справочник типов лицензий |
| `spisok_kategoriy_narusheniy` | Справочник категорий нарушений |
| `spisok_reestrov` | Справочник реестров |
| `spisok_tipov_smi` | Справочник типов СМИ |
| `spisok_kategoriy_pd_operatorov` | Справочник категорий операторов ПД |
| `info_licenzii` | Информация о лицензии из реестра rkn.gov.ru |
| `poisk_smi` | Поиск СМИ в реестре Роскомнадзора |
| `info_operatora_pd` | Информация об операторе ПД (rkn.gov.ru/pdn) |
| `poisk_narusheniy` | Поиск нарушений |
| `proverka_blokirovki` | Проверка домена в реестре запрещённых сайтов (eais.rkn.gov.ru) |
| `poisk_ori` | Поиск организаторов распространения информации (rkn.gov.ru/registry-ori) |
| `zapisi_reestra` | Информация о реестре |

**Resources:** `data://istochniki`, `data://zakonodatelstvo`, `data://struktura`

**Prompts:** `analiz_narusheniya`, `obzor_reestrov`

**Авторизация:** не требуется

### `fns` — Федеральная налоговая служба (9 tools, 3 resources, 2 prompts)

Налоговые режимы, проверки, ЕГРЮЛ/ЕГРИП, начисления.

| Tool | Описание |
|------|----------|
| `spisok_nalogovyh_rezhimov` | Справочник режимов налогообложения |
| `spisok_vidov_nalogov` | Справочник видов налогов |
| `spisok_tipov_proverok` | Справочник типов проверок |
| `spisok_statusov_organizaciy` | Справочник статусов организаций |
| `spisok_kategoriy_nalogoplatelshchikov` | Справочник категорий налогоплательщиков |
| `info_organizacii` | Информация об организации (ЕГРЮЛ) |
| `info_ip` | Информация об ИП (ЕГРИП) |
| `proverki_organizacii` | Налоговые проверки организации |
| `nalogovye_nachisleniya` | Налоговые начисления |

**Resources:** `data://istochniki`, `data://zakonodatelstvo`, `data://struktura`

**Prompts:** `analiz_nalogoplatelshchika`, `obzor_rezhimov_nalogooblozheniya`

**Авторизация:** не требуется

### `rosreestr` — Росреестр (8 tools, 3 resources, 2 prompts)

Кадастровая стоимость, объекты недвижимости, ЕГРН, формы собственности.

| Tool | Описание |
|------|----------|
| `spisok_tipov_nedvizhimosti` | Справочник типов недвижимости |
| `spisok_kategoriy_zemel` | Справочник категорий земель |
| `spisok_vidov_ispolzovaniya` | Справочник видов разрешённого использования |
| `spisok_statusov_obiekta` | Справочник статусов учёта |
| `spisok_form_sobstvennosti` | Справочник форм собственности |
| `info_obekta` | Информация об объекте недвижимости |
| `kadastrovaya_stoimost` | Кадастровая стоимость объекта |
| `prava_na_obekt` | Права на объект |

**Resources:** `data://istochniki`, `data://zakonodatelstvo`, `data://struktura`

**Prompts:** `analiz_nedvizhimosti`, `obzor_zemelnogo_uchastka`

**Авторизация:** не требуется

### `fssp` — Федеральная служба судебных приставов (10 tools, 3 resources, 2 prompts)

Исполнительные производства, ограничения, розыск должников. Подключено к Банку данных ИП ФССП (fssp.gov.ru).

| Tool | Описание |
|------|----------|
| `spisok_vidov_proizvodstv` | Справочник видов производств |
| `spisok_statusov_proizvodstva` | Справочник статусов производств |
| `spisok_ogranicheniy` | Справочник ограничений |
| `spisok_kategoriy_dolzhnikov` | Справочник категорий должников |
| `spisok_osnovaniy_vozbuzhdeniya` | Справочник оснований возбуждения |
| `spisok_regionov` | Справочник регионов ФССП |
| `info_proizvodstva` | Информация об исполнительном производстве |
| `poisk_dolzhnika` | Поиск должника |
| `ogranicheniya_dolzhnika` | Ограничения должника |
| `rozysk_dolzhnika` | Розыск должника |

**Resources:** `data://istochniki`, `data://zakonodatelstvo`, `data://struktura`

**Prompts:** `analiz_dolzhnika`, `obzor_ispolnitelnogo_proizvodstva`

**Авторизация:** не требуется

### `gibdd` — ГИБДД / МВД (12 tools, 3 resources, 2 prompts)

Транспортные средства, водительские удостоверения, проверки ТС, ДТП. Подключено к API ГИБДД (гибдд.рф).

| Tool | Описание |
|------|----------|
| `spisok_tipov_ts` | Справочник типов транспортных средств |
| `spisok_kategoriyy_vu` | Справочник категорий водительских удостоверений |
| `spisok_vidov_narusheniy` | Справочник видов нарушений |
| `spisok_statusov_shtrafov` | Справочник статусов штрафов |
| `spisok_tipov_dtp` | Справочник типов ДТП |
| `spisok_regionov_registratsii` | Справочник регионов регистрации |
| `info_ts` | Информация о транспортном средстве |
| `info_vu` | Информация о водительском удостоверении |
| `shtrafy_po_ts` | Штрафы по транспортному средству |
| `shtrafy_po_vu` | Штрафы по водительскому удостоверению |
| `statistika_dtp` | Статистика ДТП |
| `istoriya_registraciy` | История регистраций транспортного средства |

**Resources:** `data://istochniki`, `data://zakonodatelstvo`, `data://struktura`

**Prompts:** `analiz_transportnogo_sredstva`, `analiz_voditelya`

**Авторизация:** не требуется

### `minobrnauki` — Минобрнауки (13 tools, 3 resources, 2 prompts)

Вузы, образовательные программы, научные гранты, аспирантура. Реальные API: obrnadzor.gov.ru (аккредитация и лицензии), vuz.minobrnauki.gov.ru (рейтинги).

| Tool | Описание |
|------|----------|
| `spisok_tipov_vuzov` | Справочник типов вузов |
| `spisok_form_obucheniya` | Справочник форм обучения |
| `spisok_urovney_obrazovaniya` | Справочник уровней образования |
| `spisok_otrasley_nauki` | Справочник отраслей науки |
| `spisok_tipov_grantov` | Справочник типов грантов |
| `spisok_statusov_akkreditatsii` | Справочник статусов аккредитации |
| `spisok_federalnyh_okrugov` | Справочник федеральных округов |
| `info_vuza` | Информация о вузе из реестра аккредитации Рособрнадзора |
| `programmy_vuza` | Образовательные программы вуза |
| `granty_i_isledovaniya` | Гранты и исследования |
| `reyting_vuzov` | Рейтинг вузов (vuz.minobrnauki.gov.ru) |
| `aspirantura` | Данные об аспирантуре |
| `poisk_licenziy` | Поиск лицензий в реестре Рособрнадзора |

**Resources:** `data://istochniki`, `data://zakonodatelstvo`, `data://struktura`

**Prompts:** `analiz_vuza`, `obzor_nauchnyh_grantov`

**Авторизация:** не требуется

### `sovfed` — Совет Федерации РФ (6 tools, 3 resources, 2 prompts)

Сенаторы, комитеты и комиссии, законопроекты, заседания. Реальные API: sovfed.ru, data.gov.ru.

| Tool | Описание |
|------|----------|
| `spisok_senatorov` | Список сенаторов Совета Федерации |
| `info_senatora` | Информация о сенаторе |
| `spisok_komitetov` | Список комитетов Совета Федерации |
| `spisok_komissiy` | Список комиссий Совета Федерации |
| `poisk_zakonoproektov` | Поиск законопроектов, рассмотренных Советом Федерации |
| `spisok_zasedaniy` | Список заседаний Совета Федерации |

**Resources:** `data://istochniki-sovfeda`, `data://struktura-sovfeda`, `data://reglament-sovfeda`

**Prompts:** `analiz_senatora`, `obzor_zakonodatelstva`

**Авторизация:** не требуется

### `kaznacheistvo` — Федеральное казначейство (6 tools, 3 resources, 2 prompts)

Исполнение бюджета, участники бюджетного процесса, учреждения, межбюджетные трансферты. Реальные API: roskazna.gov.ru, budget.gov.ru.

| Tool | Описание |
|------|----------|
| `spisok_vidov_byudzhetov` | Справочник видов бюджетов бюджетной системы РФ |
| `spisok_kategoriy_raskhodov` | Справочник категорий расходов бюджета |
| `ispolnenie_byudzheta` | Данные об исполнении бюджета |
| `poisk_uchastnikov_bp` | Поиск участников бюджетного процесса |
| `poisk_uchrezhdeniy` | Поиск учреждений в сводном реестре |
| `mezhbyudzhetnye_transferty` | Данные о межбюджетных трансфертах |

**Resources:** `data://kaznacheistvo/istochniki`, `data://kaznacheistvo/struktura`, `data://kaznacheistvo/byudzhetnaya-sistema`

**Prompts:** `analiz_ispolneniya_byudzheta`, `obzor_byudzhetnoy_sistemy`

**Авторизация:** не требуется

### `rosprirodnadzor` — Росприроднадзор (8 tools, 3 resources, 2 prompts)

Экологические проверки, объекты негативного воздействия, лицензии на недропользование, экологические платежи. Реальные API: rpn.gov.ru.

| Tool | Описание |
|------|----------|
| `spisok_vidov_nadzora` | Справочник видов государственного надзора |
| `spisok_kategoriy_obnv` | Справочник категорий объектов негативного воздействия |
| `spisok_vidov_litsenziy_nedra` | Справочник видов лицензий на пользование недрами |
| `poisk_proverok` | Поиск экологических проверок |
| `info_proverki` | Информация о проверке по номеру |
| `poisk_obektov_negativnogo` | Поиск объектов негативного воздействия на окружающую среду |
| `poisk_litsenziy_nedra` | Поиск лицензий на пользование недрами |
| `ekologicheskie_platezhi` | Данные об экологических платежах |

**Resources:** `data://istochniki`, `data://struktura`, `data://zakonodatelstvo`

**Prompts:** `analiz_ekologicheskoy_proverki`, `obzor_nedropolzovaniya`

**Авторизация:** не требуется
