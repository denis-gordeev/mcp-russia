# Каталог features

27 features · 205 tools · 58 resources · 47 prompts

Этот каталог описывает текущее содержимое сервера в переходном состоянии. Публичное позиционирование репозитория уже русскоязычное и ориентировано на `mcp-russia`, но многие интеграции и tool names пока сохраняют исторические бразильские идентификаторы как compatibility-слой.

> **Статус миграции:** сервер находится в процессе перехода от бразильского исходного проекта к российскому. Российские модули (CBRF, Rosstat, Gosduma, RosAPI) — это новые нативные интеграции. Остальные features помечены как **legacy/совместимость** и будут постепенно заменяться российскими аналогами.

---

## Российские модули (новые)

### `cbrf` — Центральный банк Российской Федерации (6 tools, 3 resources, 2 prompts)

Курсы валют, конвертация, сравнение валют и экономические индикаторы ЦБ РФ.

| Tool | Описание |
|------|----------|
| `cursos_atuais` | Официальные курсы основных валют ЦБ РФ на сегодня (USD, EUR, CNY, GBP, JPY, CHF) |
| `consultar_moeda` | Курс одной конкретной валюты с изменением за период |
| `listar_moedas` | Полный справочник доступных валют с кодами и номиналами |
| `converter_moeda` | Конвертация суммы из иностранной валюты в рубли по курсу ЦБ |
| `comparar_moedas` | Сравнительная таблица курсов нескольких валют (до 10) |
| `cursos_por_pais` | Курсы валют основных стран-партнёров России |

**Resources:** `data://moedas` (все валюты), `data://principais` (основные), `data://referencia` (справочник)

**Prompts:** `analise_valyut`, `obzor_ekonomiki`

**Авторизация:** не требуется

### `rosstat` — Федеральная служба государственной статистики (7 tools, 2 resources, 2 prompts)

Демография, экономика, региональная статистика, федеральные округа.

| Tool | Описание |
|------|----------|
| `spisok_regionov` | Список субъектов Российской Федерации с кодами OKATO |
| `spisok_okrugov` | Список федеральных округов РФ |
| `region_info` | Детальная информация о регионе: население, ВРП, средняя зарплата |
| `okrug_info` | Информация о федеральном округе |
| `pokazateli_rosstata` | Справочник основных показателей Росстата |
| `inflyaciya` | Данные об инфляции (ИПЦ) по России |
| `demografiya` | Демографические данные (рождаемость, смертность, численность) |

**Resources:** `data://istochniki` (источники данных), `data://metodologiya`

**Prompts:** `analiz_regiona`, `obzor_inflyacii`

**Авторизация:** не требуется (данные через ЕМИСС / fedstat.ru)

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

**Авторизация:** не требуется (данные через download.data.duma.gov.ru / sozd.duma.gov.ru)

### `rosapi` — Справочные данные РФ (8 tools, 2 resources, 2 prompts)

Адреса (ФИАС), организации (ИНН/ОГРН), банки (БИК), праздники, налоговые ставки.

| Tool | Описание |
|------|----------|
| `konsul_adres_po_indeksu` | Найти адрес по почтовому индексу РФ (6 цифр) |
| `poisk_adresa` | Поиск адреса по свободному запросу через ФИАС |
| `poisk_org_po_inn` | Найти организацию по ИНН (10 или 12 цифр) |
| `poisk_org_po_ogrn` | Найти организацию по ОГРН (13 или 15 цифр) |
| `spisok_bankov` | Справочник банков России с БИК |
| `konsul_bank_po_bik` | Информация о банке по БИК (9 цифр) |
| `prazdniki_rf` | Национальные праздники РФ с датами |
| `nalogovye_stavki` | Основные налоговые ставки РФ (НДС, НП, НДФЛ, УСН, ЕСН) |

**Resources:** `data://nalogovye-stavki`, `data://servisy`

**Prompts:** `analiz_organizacii`, `poisk_adresa_prompt`

**Авторизация:** опциональна (для расширенного поиска через Dadata нужен API-ключ)

---

## Legacy / совместимость (бразильский исходный проект)

Ниже перечислены features, унаследованные от исходного бразильского проекта. Они продолжают работать как compatibility-слой, но не являются приоритетными для `mcp-russia`. По мере разработки российские аналоги будут заменять соответствующие legacy-модули.

## Экономика и макростатистика

### `ibge` — legacy feature статистических данных (9 tools)

Историческая интеграция исходного проекта: регионы, муниципалитеты, частотность имен, статистические агрегаты, классификаторы и геоданные.

| Tool | Описание |
|------|----------|
| `ibge_listar_estados` | Список регионов с кодом, названием, сокращением и макрорегионом |
| `ibge_buscar_municipios` | Список муниципалитетов по коду региона |
| `ibge_listar_regioes` | Список макрорегионов |
| `ibge_consultar_nome` | Частотность имен по данным переписи |
| `ibge_ranking_nomes` | Рейтинг имен по региону или муниципалитету |
| `ibge_consultar_agregado` | Статистические агрегаты: население, ВВП, площадь, временные ряды |
| `ibge_listar_pesquisas` | Список исследовательских программ источника |
| `ibge_obter_malha` | Географические контуры в формате GeoJSON |
| `ibge_buscar_cnae` | Поиск кодов экономической деятельности |

**Авторизация:** не требуется

### `bacen` — legacy feature центрального банка (9 tools)

Историческая интеграция исходного проекта: процентные ставки, инфляция, курс валют, ВВП и другие временные ряды.

**Аналог в mcp-russia:** модуль `cbrf` (курсы валют ЦБ РФ)

| Tool | Описание |
|------|----------|
| `bacen_consultar_serie` | Получить временной ряд по коду |
| `bacen_ultimos_valores` | Последние N значений ряда |
| `bacen_metadados_serie` | Метаданные ряда: название, единица измерения, периодичность |
| `bacen_series_populares` | Подборка популярных рядов |
| `bacen_buscar_serie` | Поиск рядов по ключевому слову |
| `bacen_indicadores_atuais` | Сводка ключевых макроиндикаторов |
| `bacen_calcular_variacao` | Процентное изменение между датами |
| `bacen_comparar_series` | Сравнение 2-5 рядов |
| `bacen_expectativas_focus` | Рыночные ожидания по макропоказателям |

**Авторизация:** не требуется

## Законодательство

### `camara` — legacy feature нижней палаты парламента (10 tools)

Депутаты, законопроекты, голосования, расходы, комиссии и парламентские объединения.

**Аналог в mcp-russia:** модуль `gosduma` (Государственная Дума)

| Tool | Описание |
|------|----------|
| `camara_listar_deputados` | Список депутатов с фильтрами по имени, партии и региону |
| `camara_buscar_deputado` | Карточка депутата по ID |
| `camara_buscar_proposicao` | Поиск законопроектов и инициатив |
| `camara_consultar_tramitacao` | История прохождения инициативы |
| `camara_buscar_votacao` | Сессии голосования |
| `camara_votos_nominais` | Поименное голосование |
| `camara_despesas_deputado` | Отчет по расходам депутата |
| `camara_agenda_legislativa` | Законодательный календарь |
| `camara_buscar_comissoes` | Список комиссий |
| `camara_frentes_parlamentares` | Парламентские фронты и группы |

**Авторизация:** не требуется

### `senado` — legacy feature верхней палаты парламента (26 tools)

Сенаторы, законопроекты, голосования, комиссии, календарь заседаний и вспомогательные справочники.

**Сенаторы (4):** `senado_listar_senadores`, `senado_buscar_senador`, `senado_buscar_senador_por_nome`, `senado_votacoes_senador`

**Материи и инициативы (5):** `senado_buscar_materia`, `senado_detalhe_materia`, `senado_consultar_tramitacao_materia`, `senado_textos_materia`, `senado_votos_materia`

**Голосования (3):** `senado_listar_votacoes`, `senado_detalhe_votacao`, `senado_votacoes_recentes`

**Комиссии (4):** `senado_listar_comissoes`, `senado_detalhe_comissao`, `senado_membros_comissao`, `senado_reunioes_comissao`

**Повестка (2):** `senado_agenda_plenario`, `senado_agenda_comissoes`

**Справочники (6):** `senado_legislatura_atual`, `senado_partidos_senado`, `senado_ufs_senado`, `senado_tipos_materia`, `senado_emendas_materia`, `senado_listar_blocos`

**Дополнительно (2):** `senado_listar_liderancas`, `senado_relatorias_senador`

**Авторизация:** не требуется

## Прозрачность и аудит

### `transparencia` — legacy feature портала прозрачности (18 tools)

Федеральные контракты, расходы, госслужащие, санкции, социальные выплаты, командировки и платежные карты.

| Tool | Описание |
|------|----------|
| `transparencia_buscar_contratos` | Поиск федеральных контрактов |
| `transparencia_consultar_despesas` | Расходы по функции, региону и году |
| `transparencia_buscar_servidores` | Поиск госслужащих |
| `transparencia_buscar_licitacoes` | Закупочные процедуры |
| `transparencia_consultar_bolsa_familia` | Получатели социальной выплаты |
| `transparencia_buscar_sancoes` | Санкционные и ограничительные реестры |
| `transparencia_buscar_emendas` | Парламентские поправки и ассигнования |
| `transparencia_consultar_viagens` | Служебные поездки |
| `transparencia_buscar_convenios` | Соглашения и субсидии |
| `transparencia_buscar_cartoes_pagamento` | Операции по государственным картам |
| `transparencia_buscar_pep` | Политически значимые лица |
| `transparencia_buscar_acordos_leniencia` | Соглашения о leniency |
| `transparencia_buscar_notas_fiscais` | Счета и чеки |
| `transparencia_consultar_beneficio_social` | Социальные пособия |
| `transparencia_consultar_cpf` | Проверка данных физлица |
| `transparencia_consultar_cnpj` | Проверка данных юрлица |
| `transparencia_detalhar_contrato` | Карточка контракта |
| `transparencia_detalhar_servidor` | Карточка госслужащего |

**Авторизация:** опциональна, нужен ключ API

### `tcu` — legacy feature высшего контрольного органа (8 tools)

Решения, дисквалификации, справки APF, задолженности и контракты.

| Tool | Описание |
|------|----------|
| `tcu_buscar_acordaos` | Поиск решений |
| `tcu_consultar_inabilitados` | Реестр дисквалифицированных лиц |
| `tcu_consultar_inidoneos` | Реестр недобросовестных компаний |
| `tcu_consultar_certidoes_apf` | Сводные справки APF |
| `tcu_calcular_debito_tcu` | Расчет корректировки долга |
| `tcu_buscar_pedidos_congresso` | Запросы парламента к контрольному органу |
| `tcu_buscar_contratos_tcu` | Контракты ведомства |
| `tcu_consultar_cadirreg` | Реестр нарушений |

**Авторизация:** не требуется

### Государственные региональные аудиторские органы (9 features, legacy)

| Feature | Регион | Tools | Покрытие |
|---------|--------|-------|----------|
| `tce_sp` | Сан-Паулу | 3 | Расходы, доходы, муниципалитеты |
| `tce_rj` | Рио-де-Жанейро | 7 | Закупки, контракты, стройки, штрафы |
| `tce_rs` | Риу-Гранди-ду-Сул | 5 | Образование, здравоохранение, бюджетная дисциплина |
| `tce_sc` | Санта-Катарина | 2 | Муниципалитеты и администраторы |
| `tce_pe` | Пернамбуку | 5 | Закупки, контракты, расходы, поставщики |
| `tce_ce` | Сеара | 4 | Закупки, контракты, обязательства |
| `tce_rn` | Риу-Гранди-ду-Норти | 5 | Поднадзорные организации, закупки, контракты |
| `tce_pi` | Пиауи | 5 | Муниципалитеты, расходы, доходы |
| `tce_to` | Токантинс | 3 | Дела, повестки заседаний |

**Авторизация:** не требуется

## Судебный контур

### `datajud` — legacy feature судебного поиска (7 tools)

Поиск дел, движений по делу и расширенных выборок по судебной системе.

| Tool | Описание |
|------|----------|
| `datajud_buscar_processos` | Поиск дел по набору фильтров |
| `datajud_buscar_processo_por_numero` | Поиск дела по номеру |
| `datajud_buscar_processos_por_classe` | Поиск по классу дела |
| `datajud_buscar_processos_por_assunto` | Поиск по тематике |
| `datajud_buscar_processos_por_orgao` | Поиск по суду или органу |
| `datajud_buscar_processos_avancado` | Расширенный поиск с пагинацией |
| `datajud_consultar_movimentacoes` | Движения по делу |

**Авторизация:** опциональна, нужен ключ API

### `jurisprudencia` — legacy feature по прецедентам и обзорам (6 tools)

Решения высших судов, обзоры, тематические подборки и краткие судебные сводки.

| Tool | Описание |
|------|----------|
| `jurisprudencia_buscar_jurisprudencia_stf` | Решения STF |
| `jurisprudencia_buscar_jurisprudencia_stj` | Решения STJ |
| `jurisprudencia_buscar_jurisprudencia_tst` | Решения трудового суда |
| `jurisprudencia_buscar_sumulas` | Судебные тезисы и sumulas |
| `jurisprudencia_buscar_repercussao_geral` | Темы repercussao geral |
| `jurisprudencia_buscar_informativos` | Информационные бюллетени судов |

**Авторизация:** не требуется

## Выборы

### `tse` — legacy feature электоральных данных (15 tools)

Выборы, кандидаты, результаты, финансовая отчетность и ход подсчета голосов.

| Tool | Описание |
|------|----------|
| `tse_anos_eleitorais` | Годы с доступными выборами |
| `tse_listar_eleicoes` | Выборы по году |
| `tse_listar_eleicoes_suplementares` | Дополнительные выборы |
| `tse_listar_estados_suplementares` | Регионы с дополнительными выборами |
| `tse_listar_cargos` | Список избираемых должностей |
| `tse_listar_candidatos` | Кандидаты с фильтрами |
| `tse_buscar_candidato` | Карточка кандидата |
| `tse_resultado_eleicao` | Итоги конкретных выборов |
| `tse_consultar_prestacao_contas` | Финансовая отчетность кандидатов |
| `tse_resultado_nacional` | Национальные результаты |
| `tse_resultado_por_estado` | Итоги по региону |
| `tse_mapa_resultado_estados` | Сравнение результатов по всем регионам |
| `tse_listar_municipios_eleitorais` | Муниципалитеты в электоральном контуре |
| `tse_resultado_por_municipio` | Итоги по муниципалитету |
| `tse_apuracao_status` | Статус подсчета |

**Авторизация:** не требуется

## Природа и экология

### `inpe` — legacy feature спутникового мониторинга (4 tools)

Очаги пожаров, обезлесение и спутниковые наблюдения.

| Tool | Описание |
|------|----------|
| `inpe_buscar_focos_queimadas` | Активные очаги возгорания |
| `inpe_consultar_desmatamento` | Данные по обезлесению |
| `inpe_alertas_deter` | Оперативные экологические алерты |
| `inpe_dados_satelite` | Данные по сенсорам спутников |

**Авторизация:** не требуется

### `ana` — legacy feature водного мониторинга (3 tools)

Станции наблюдений, телеметрия и состояние водохранилищ.

| Tool | Описание |
|------|----------|
| `ana_buscar_estacoes` | Поиск гидрологических станций |
| `ana_consultar_telemetria` | Телеметрические измерения |
| `ana_monitorar_reservatorios` | Состояние водохранилищ |

**Авторизация:** не требуется

## Здравоохранение

### `saude` — legacy feature медицинских справочников (4 tools)

Медицинские учреждения, специалисты, койки и типы организаций.

| Tool | Описание |
|------|----------|
| `saude_buscar_estabelecimentos` | Медицинские организации |
| `saude_buscar_profissionais` | Медицинские специалисты |
| `saude_listar_tipos_estabelecimento` | Типы организаций |
| `saude_consultar_leitos` | Наличие коек |

**Авторизация:** не требуется

## Публичные закупки

### `compras/pncp` — legacy feature национального каталога закупок (6 tools)

Публичные закупки, контракты, рамочные соглашения, поставщики и заказчики.

| Tool | Описание |
|------|----------|
| `compras_pncp_buscar_contratacoes` | Поиск закупок по тексту, CNPJ и дате |
| `compras_pncp_buscar_contratos` | Поиск контрактов |
| `compras_pncp_buscar_atas` | Реестр рамочных соглашений |
| `compras_pncp_consultar_fornecedor` | Карточка поставщика |
| `compras_pncp_buscar_itens` | Позиции закупки |
| `compras_pncp_consultar_orgao` | Информация о заказчике |

**Авторизация:** не требуется

### `compras/dadosabertos` — legacy feature по архивным закупочным данным (8 tools)

Архивные закупки, тендеры, исключения, договоры и классификаторы.

| Tool | Описание |
|------|----------|
| `compras_dadosabertos_buscar_licitacoes` | Поиск тендеров по дате |
| `compras_dadosabertos_buscar_pregoes` | Электронные аукционы |
| `compras_dadosabertos_buscar_dispensas` | Закупки у единственного поставщика |
| `compras_dadosabertos_buscar_contratos` | Поиск контрактов по периоду |
| `compras_dadosabertos_consultar_fornecedor` | Поиск поставщиков |
| `compras_dadosabertos_buscar_material_catmat` | Каталог материалов CATMAT |
| `compras_dadosabertos_buscar_servico_catser` | Каталог услуг CATSER |
| `compras_dadosabertos_buscar_uasg` | Коды заказчиков UASG |

**Авторизация:** не требуется

## Справочные и сервисные данные

### `brasilapi` — legacy utility feature (16 tools)

CEP, CNPJ, DDD, банки, валюты, FIPE, праздники, PIX, ISBN, NCM и домены `.br`.

**Аналоги в mcp-russia:** модуль `rosapi` (адреса по индексу, организации по ИНН/ОГРН, банки по БИК, праздники РФ, налоговые ставки)

| Tool | Описание |
|------|----------|
| `brasilapi_consultar_cep` | Проверка почтового индекса |
| `brasilapi_consultar_cnpj` | Проверка юридического лица |
| `brasilapi_consultar_ddd` | Проверка телефонного кода |
| `brasilapi_listar_bancos` | Список банков |
| `brasilapi_consultar_banco` | Детали банка |
| `brasilapi_listar_moedas` | Доступные валюты |
| `brasilapi_consultar_cotacao` | Курс валюты |
| `brasilapi_consultar_feriados` | Национальные праздники по году |
| `brasilapi_consultar_taxa` | Ставки и индексы |
| `brasilapi_listar_tabelas_fipe` | Таблицы FIPE |
| `brasilapi_listar_marcas_fipe` | Марки в справочнике FIPE |
| `brasilapi_buscar_veiculos_fipe` | Поиск транспорта в FIPE |
| `brasilapi_consultar_isbn` | Данные книги по ISBN |
| `brasilapi_buscar_ncm` | Коды товарной номенклатуры |
| `brasilapi_consultar_pix_participantes` | Участники PIX |
| `brasilapi_consultar_registro_br` | Домены `.br` |

**Авторизация:** не требуется

### `dados_abertos` — legacy feature каталога datasets (4 tools)

Наборы данных, их ресурсы и организации-публикаторы.

| Tool | Описание |
|------|----------|
| `dados_abertos_buscar_conjuntos` | Поиск наборов данных |
| `dados_abertos_detalhar_conjunto` | Детали набора |
| `dados_abertos_listar_organizacoes` | Список организаций |
| `dados_abertos_buscar_recursos` | Ресурсы внутри набора |

**Авторизация:** не требуется

### `diario_oficial` — legacy feature по официальным публикациям (4 tools)

Поиск по выпускам официальных бюллетеней и по муниципалитетам.

| Tool | Описание |
|------|----------|
| `diario_oficial_buscar_diarios` | Полнотекстовый поиск по выпускам |
| `diario_oficial_buscar_trechos` | Поиск фрагментов по муниципалитету |
| `diario_oficial_buscar_cidades` | Поиск муниципалитетов по названию |
| `diario_oficial_listar_territorios` | Территории с доступными выпусками |

**Авторизация:** не требуется

### `transferegov` — legacy feature по трансфертам и поправкам (5 tools)

Парламентские трансферты, детали по ID, выборки по муниципалитету и ежегодные сводки.

| Tool | Описание |
|------|----------|
| `transferegov_buscar_emendas_pix` | Поиск специальных трансфертов |
| `transferegov_buscar_emenda_por_autor` | Поиск по автору |
| `transferegov_detalhe_emenda` | Детали трансферта |
| `transferegov_emendas_por_municipio` | Трансферты конкретному муниципалитету |
| `transferegov_resumo_emendas_ano` | Годовая сводка |

**Авторизация:** не требуется

## AI-агенты

### `redator` — legacy агент официального письма (5 tools + 6 prompts + 10 resources)

Исторический агент исходного проекта для генерации официальных документов: письма, memo, despacho, portaria, parecer и note tecnica.

| Tool | Описание |
|------|----------|
| `redator_formatar_data_extenso` | Форматирование даты прописью |
| `redator_gerar_numeracao` | Генерация регистрационного номера документа |
| `redator_consultar_pronome_tratamento` | Подсказка по официальной форме обращения |
| `redator_validar_documento` | Проверка CPF/CNPJ |
| `redator_listar_tipos_documento` | Список поддерживаемых типов документов |

**Prompts:** `redator_despacho`, `redator_memorando`, `redator_oficio`, `redator_portaria`, `redator_parecer`, `redator_nota_tecnica`

**Resources:** 7 шаблонов документов и 3 нормативных справочника

**Авторизация:** не требуется
