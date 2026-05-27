"""Constants for the ФССП feature."""

# ФССП (Федеральная служба судебных приставов)
# Основные источники данных:
# 1. Официальный сайт: https://fssp.gov.ru
# 2. Банк данных исполнительных производств: https://fssp.gov.ru/iss/ip
# 3. Портал государственных услуг: https://gosuslugi.ru

FSSP_API_BASE = "https://fssp.gov.ru/api"

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
    {"code": "upravlenie_transportom", "name": "Ограничение специального права управления транспортом"},
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
