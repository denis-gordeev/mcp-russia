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
    {"code": "imushchestvennoe", "name": "Имущественного характера"},
    {"code": "neimushchestvennoe", "name": "Неимущественного характера"},
    {"code": "shtrafy_gibdd", "name": "Штрафы ГИБДД"},
    {"code": "nalogovye_vzyskaniya", "name": "Налоговые взыскания"},
    {"code": "kreditnye_dolgi", "name": "Кредитные задолженности"},
    {"code": "alimenty", "name": "Алименты"},
    {"code": "zhkx", "name": "Задолженности по ЖКХ"},
]

StatusyProizvodstva = [
    {"code": "vozbuzhdeno", "name": "Возбуждено"},
    {"code": "v_proizvodstve", "name": "В производстве"},
    {"code": "priostanovleno", "name": "Приостановлено"},
    {"code": "okoncheno", "name": "Окончено"},
    {"code": "prekrashcheno", "name": "Прекращено"},
    {"code": "peredano", "name": "Передано в другое подразделение"},
]

Ogranicheniya = [
    {"code": "vyezd", "name": "Временное ограничение на выезд из РФ"},
    {
        "code": "upravlenie_transportom",
        "name": "Ограничение специального права управления транспортом",
    },
    {"code": "arest_schetov", "name": "Арест банковских счетов"},
    {"code": "arest_imushchestva", "name": "Арест имущества"},
    {"code": "zapret_registracii", "name": "Запрет на регистрационные действия с имуществом"},
]

KategoriiDolzhnikov = [
    {"code": "fizicheskoe_lico", "name": "Физическое лицо"},
    {"code": "yuridicheskoe_lico", "name": "Юридическое лицо"},
    {"code": "ip", "name": "Индивидуальный предприниматель"},
]

OsnovaniyaVozbuzhdeniya = [
    {"code": "sudebnyy_akt", "name": "Судебный акт"},
    {"code": "akt_upolnomochennogo_organom", "name": "Акт уполномоченного органа"},
    {"code": "postanovlenie_nalogovogo_organom", "name": "Постановление налогового органа"},
    {"code": "postanovlenie_gibdd", "name": "Постановление ГИБДД"},
    {"code": "ispolnitelnaya_nadpis_notariusa", "name": "Исполнительная надпись нотариуса"},
]
