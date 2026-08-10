"""Константы модуля МВД России."""

MVD_BAZA = "https://xn--b1aew.xn--p1ai"
MVD_OTKRYTYE_DANNYE = f"{MVD_BAZA}/открытые-данные"
DATA_GOV_RU_MVD = "https://data.gov.ru/opendata/7727739372"

NABORY_DANNYKH = {
    "dtp": {
        "identifikator": "7727739372-MVD_GIAC_3.1",
        "nazvanie": "Дорожно-транспортные происшествия",
    },
    "prestupnost": {
        "identifikator": "7727739372-MVD_GIAC_3.4",
        "nazvanie": "Статистика преступности и результаты расследования",
    },
    "organizovannaya": {
        "identifikator": "7727739372-MVD_GIAC_3.6",
        "nazvanie": "Результаты борьбы с организованной преступностью",
    },
    "litsa_prestupleniya": {
        "identifikator": "7727739372-MVDGIAC37",
        "nazvanie": "Лица, совершившие преступления",
    },
    "zaregistrirovannye": {
        "identifikator": "7727739372-MVDGIAC38",
        "nazvanie": "Зарегистрированные, раскрытые и нераскрытые преступления",
    },
    "s_poterpavshimi": {
        "identifikator": "7727739372-MVDGIAC310",
        "nazvanie": "Преступления с потерпевшими",
    },
    "rozysk": {
        "identifikator": "7727739372-MVD_GIAC_3.11",
        "nazvanie": "Розыскные дела, безвестно отсутствующие, неопознанные трупы",
    },
    "kontrol": {
        "identifikator": "7727739372-MVDGIAC314",
        "nazvanie": "Государственный контроль и надзор",
    },
    "litsenzirovanie": {
        "identifikator": "7727739372-MVDGIAC315",
        "nazvanie": "Лицензирование отдельных видов деятельности",
    },
    "narkotiki": {
        "identifikator": "7727739372-MVDGIAC325-326",
        "nazvanie": "Наркотические преступления и изъятия",
    },
    "bezopasnost_dorozhnogo": {
        "identifikator": "7727739372-MVDGIAC32",
        "nazvanie": "Обеспечение безопасности дорожного движения",
    },
    "obzor_prestupnosti": {
        "identifikator": "7727739372-MVDGIAC33",
        "nazvanie": "Обзор состояния преступности",
    },
}

VIDY_PRESTUPLENIY = [
    {"kod": "ubiystvo", "nazvanie": "Убийство"},
    {"kod": "umyshlennoe_prichinenie", "nazvanie": "Умышленное причинение тяжкого вреда здоровью"},
    {"kod": "iznasilovanie", "nazvanie": "Изнасилование"},
    {"kod": "grabezh", "nazvanie": "Грабёж"},
    {"kod": "razboy", "nazvanie": "Разбой"},
    {"kod": "krazha", "nazvanie": "Кража"},
    {"kod": "moshennichestvo", "nazvanie": "Мошенничество"},
    {"kod": "vymogatelstvo", "nazvanie": "Вымогательство"},
    {"kod": "ekologicheskoe", "nazvanie": "Экологическое преступление"},
    {"kod": "narkotiki", "nazvanie": "Преступление в сфере оборота наркотиков"},
    {"kod": "terrorizm", "nazvanie": "Террористический акт"},
    {"kod": "ekstremizm", "nazvanie": "Экстремизм"},
]

VIDY_DTP = [
    {"kod": "stolknovenie", "nazvanie": "Столкновение"},
    {"kod": "oprokidyvanie", "nazvanie": "Опрокидывание"},
    {"kod": "naezd_na_peshekhoda", "nazvanie": "Наезд на пешехода"},
    {"kod": "naezd_na_velosipedista", "nazvanie": "Наезд на велосипедиста"},
    {"kod": "naezd_na_stoyanku", "nazvanie": "Наезд на стоящее ТС"},
    {"kod": "padenie_paxazhira", "nazvanie": "Падение пассажира"},
    {"kod": "prochee", "nazvanie": "Иной вид ДТП"},
]

FEDERALNYE_OKRUGA = [
    {"kod": "ЦФО", "nazvanie": "Центральный"},
    {"kod": "СЗФО", "nazvanie": "Северо-Западный"},
    {"kod": "ЮФО", "nazvanie": "Южный"},
    {"kod": "ПФО", "nazvanie": "Приволжский"},
    {"kod": "УФО", "nazvanie": "Уральский"},
    {"kod": "СФО", "nazvanie": "Сибирский"},
    {"kod": "ДФО", "nazvanie": "Дальневосточный"},
    {"kod": "СКФО", "nazvanie": "Северо-Кавказский"},
]

STATISTIKA_PRESTUPNOSTI_2024 = {
    "zaregistrirovano_prestupleniy": 1470000,
    "raskryto_prestupleniy": 950000,
    "neraskryto_prestupleniy": 520000,
    "tyazhkie_osobo_tyazhkie": 420000,
    "s_poterpavshimi": 890000,
    "ekonomicheskie": 310000,
    "narkoticheskie": 195000,
    "po_fo": {
        "ЦФО": {"prestupleniy": 285000, "raskryto": 180000},
        "СЗФО": {"prestupleniy": 148000, "raskryto": 95000},
        "ЮФО": {"prestupleniy": 112000, "raskryto": 72000},
        "СКФО": {"prestupleniy": 68000, "raskryto": 43000},
        "ПФО": {"prestupleniy": 268000, "raskryto": 175000},
        "УФО": {"prestupleniy": 152000, "raskryto": 98000},
        "СФО": {"prestupleniy": 224000, "raskryto": 145000},
        "ДФО": {"prestupleniy": 113000, "raskryto": 72000},
    },
}

STATISTIKA_DTP_2024 = {
    "vsego_dtp": 134000,
    "pogibshikh": 13600,
    "postradavshikh": 171000,
    "dtp_s_detmi": 18500,
    "po_vinu_voditeley": 118000,
    "po_vinu_peshekhodov": 11000,
}
