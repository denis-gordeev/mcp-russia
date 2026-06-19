"""Константы модуля ФССП."""

FSSP_API_BASE = "https://fssp.gov.ru/api"
FSSP_SEARCH_API = "https://fssp.gov.ru/iss/search"
FSSP_IP_BASE = "https://fssp.gov.ru/iss/ip"

KODY_REGIONOV_FSSP: dict[str, int] = {
    "Все регионы": 0,
    "Республика Адыгея": 1,
    "Республика Башкортостан": 2,
    "Республика Татарстан": 16,
    "Республика Саха (Якутия)": 14,
    "Краснодарский край": 23,
    "Красноярский край": 24,
    "Пермский край": 59,
    "Ставропольский край": 26,
    "Волгоградская область": 34,
    "Воронежская область": 36,
    "Иркутская область": 38,
    "Кемеровская область": 42,
    "Ленинградская область": 47,
    "Нижегородская область": 52,
    "Новосибирская область": 54,
    "Омская область": 55,
    "Ростовская область": 61,
    "Самарская область": 63,
    "Свердловская область": 66,
    "Тюменская область": 72,
    "Челябинская область": 74,
    "Московская область": 50,
    "Москва": 77,
    "Санкт-Петербург": 78,
}

VidyIspolnitelnyhProizvodstv = [
    {"kod": "imushchestvennoe", "nazvanie": "Имущественного характера"},
    {"kod": "neimushchestvennoe", "nazvanie": "Неимущественного характера"},
    {"kod": "shtrafy_gibdd", "nazvanie": "Штрафы ГИБДД"},
    {"kod": "nalogovye_vzyskaniya", "nazvanie": "Налоговые взыскания"},
    {"kod": "kreditnye_dolgi", "nazvanie": "Кредитные задолженности"},
    {"kod": "alimenty", "nazvanie": "Алименты"},
    {"kod": "zhkx", "nazvanie": "Задолженности по ЖКХ"},
]

StatusyProizvodstva = [
    {"kod": "vozbuzhdeno", "nazvanie": "Возбуждено"},
    {"kod": "v_proizvodstve", "nazvanie": "В производстве"},
    {"kod": "priostanovleno", "nazvanie": "Приостановлено"},
    {"kod": "okoncheno", "nazvanie": "Окончено"},
    {"kod": "prekrashcheno", "nazvanie": "Прекращено"},
    {"kod": "peredano", "nazvanie": "Передано в другое подразделение"},
]

Ogranicheniya = [
    {"kod": "vyezd", "nazvanie": "Временное ограничение на выезд из РФ"},
    {
        "kod": "upravlenie_transportom",
        "nazvanie": "Ограничение специального права управления транспортом",
    },
    {"kod": "arest_schetov", "nazvanie": "Арест банковских счетов"},
    {"kod": "arest_imushchestva", "nazvanie": "Арест имущества"},
    {"kod": "zapret_registracii", "nazvanie": "Запрет на регистрационные действия с имуществом"},
]

KategoriiDolzhnikov = [
    {"kod": "fizicheskoe_lico", "nazvanie": "Физическое лицо"},
    {"kod": "yuridicheskoe_lico", "nazvanie": "Юридическое лицо"},
    {"kod": "ip", "nazvanie": "Индивидуальный предприниматель"},
]

OsnovaniyaVozbuzhdeniya = [
    {"kod": "sudebnyy_akt", "nazvanie": "Судебный акт"},
    {"kod": "akt_upolnomochennogo_organom", "nazvanie": "Акт уполномоченного органа"},
    {"kod": "postanovlenie_nalogovogo_organom", "nazvanie": "Постановление налогового органа"},
    {"kod": "postanovlenie_gibdd", "nazvanie": "Постановление ГИБДД"},
    {"kod": "ispolnitelnaya_nadpis_notariusa", "nazvanie": "Исполнительная надпись нотариуса"},
]
