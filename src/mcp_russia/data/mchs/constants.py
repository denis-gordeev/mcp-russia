"""Константы модуля МЧС России."""

MCHS_BAZA_API = "https://mchs.gov.ru/api"
MCHS_BAZA = "https://mchs.gov.ru"
MCHS_BAZA_OTKRYTYKH_DANNYKH = "https://data.mchs.gov.ru/opendata"
POZHARY_BAZA_STATISTIKI = "https://fires.ru/api"
DANNYE_GOV_RU_MCHS = "https://data.gov.ru/opendata/7719484243-mchs"

VIDY_CHS = [
    {"kod": "tekhogennyy", "nazvanie": "Техногенная чрезвычайная ситуация"},
    {"kod": "prirodnyy", "nazvanie": "Природная чрезвычайная ситуация"},
    {"kod": "biologo-socialnyy", "nazvanie": "Биолого-социальная чрезвычайная ситуация"},
    {"kod": "ekologicheskiy", "nazvanie": "Экологическая чрезвычайная ситуация"},
]

KLASSY_CHS = [
    {"kod": "lokalnaya", "nazvanie": "Локальная"},
    {"kod": "municipalnaya", "nazvanie": "Муниципальная"},
    {"kod": "mezhmunicipalnaya", "nazvanie": "Межмуниципальная"},
    {"kod": "regionalnaya", "nazvanie": "Региональная"},
    {"kod": "mezhregionalnaya", "nazvanie": "Межрегиональная"},
    {"kod": "federalnaya", "nazvanie": "Федеральная"},
]

VIDY_POZHAROV = [
    {"kod": "zhiloy", "nazvanie": "Пожар в жилом секторе"},
    {"kod": "proizvodstvennyy", "nazvanie": "Пожар на производственном объекте"},
    {"kod": "transportnyy", "nazvanie": "Пожар на транспорте"},
    {"kod": "lesnoy", "nazvanie": "Лесной пожар"},
    {"kod": "torfyanoy", "nazvanie": "Торфяной пожар"},
    {"kod": "stepnoy", "nazvanie": "Степной пожар"},
    {"kod": "tekhnogennyy", "nazvanie": "Техногенный пожар"},
]

STATUSY_CHS = {
    "normalnaya": "Нормальная",
    "preduprezhdenie": "Предупреждение",
    "chrezvychaynaya": "Чрезвычайная",
    "likvidatsiya": "Ликвидация последствий",
}

TIPY_OPASNOSTI = [
    {"kod": "radiatsionnyy", "nazvanie": "Радиационная опасность"},
    {"kod": "khimicheskiy", "nazvanie": "Химическая опасность"},
    {"kod": "biologicheskiy", "nazvanie": "Биологическая опасность"},
    {"kod": "gidrologicheskiy", "nazvanie": "Гидрологическая опасность"},
    {"kod": "geologicheskiy", "nazvanie": "Геологическая опасность"},
    {"kod": "meteorologicheskiy", "nazvanie": "Метеорологическая опасность"},
    {"kod": "pozharnyy", "nazvanie": "Пожарная опасность"},
]

FEDERALNYE_OKRUGA_MCHS = [
    {"kod": "ЦФО", "nazvanie": "Центральный", "centry": ["Москва"]},
    {"kod": "СЗФО", "nazvanie": "Северо-Западный", "centry": ["Санкт-Петербург"]},
    {"kod": "ЮФО", "nazvanie": "Южный", "centry": ["Ростов-на-Дону"]},
    {"kod": "ПФО", "nazvanie": "Приволжский", "centry": ["Нижний Новгород"]},
    {"kod": "УФО", "nazvanie": "Уральский", "centry": ["Екатеринбург"]},
    {"kod": "СФО", "nazvanie": "Сибирский", "centry": ["Красноярск"]},
    {"kod": "ДФО", "nazvanie": "Дальневосточный", "centry": ["Хабаровск"]},
]

STATISTIKA_POZHAROV_2023 = {
    "vsego_pojarov": 356842,
    "pogibshikh": 7964,
    "postradavshikh": 8647,
    "usherb_mlrd_rub": 15.2,
    "po_fo": {
        "ЦФО": {"pojarov": 58432, "pogibshikh": 1254},
        "СЗФО": {"pojarov": 32145, "pogibshikh": 876},
        "ЮФО": {"pojarov": 28934, "pogibshikh": 643},
        "ПФО": {"pojarov": 62178, "pogibshikh": 1543},
        "УФО": {"pojarov": 34521, "pogibshikh": 897},
        "СФО": {"pojarov": 56876, "pogibshikh": 1298},
        "ДФО": {"pojarov": 83756, "pogibshikh": 1453},
    },
}
