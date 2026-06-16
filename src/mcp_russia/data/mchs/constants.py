"""Константы модуля МЧС России."""

MCHS_API_BASE = "https://mchs.gov.ru/api"
MCHS_BASE = "https://mchs.gov.ru"
MCHS_OPENDATA_BASE = "https://data.mchs.gov.ru/opendata"
FIRES_STAT_BASE = "https://fires.ru/api"
DATA_GOV_RU_MCHS = "https://data.gov.ru/opendata/7719484243-mchs"

VIDY_CHS = [
    {"code": "tekhogennyy", "name": "Техногенная чрезвычайная ситуация"},
    {"code": "prirodnyy", "name": "Природная чрезвычайная ситуация"},
    {"code": "biologo-socialnyy", "name": "Биолого-социальная чрезвычайная ситуация"},
    {"code": "ekologicheskiy", "name": "Экологическая чрезвычайная ситуация"},
]

KLASSY_CHS = [
    {"code": "lokalnaya", "name": "Локальная"},
    {"code": "municipalnaya", "name": "Муниципальная"},
    {"code": "mezhmunicipalnaya", "name": "Межмуниципальная"},
    {"code": "regionalnaya", "name": "Региональная"},
    {"code": "mezhregionalnaya", "name": "Межрегиональная"},
    {"code": "federalnaya", "name": "Федеральная"},
]

VIDY_POZHAROV = [
    {"code": "zhiloy", "name": "Пожар в жилом секторе"},
    {"code": "proizvodstvennyy", "name": "Пожар на производственном объекте"},
    {"code": "transportnyy", "name": "Пожар на транспорте"},
    {"code": "lesnoy", "name": "Лесной пожар"},
    {"code": "torfyanoy", "name": "Торфяной пожар"},
    {"code": "stepnoy", "name": "Степной пожар"},
    {"code": "tekhnogennyy", "name": "Техногенный пожар"},
]

STATUSY_CHS = {
    "normalnaya": "Нормальная",
    "preduprezhdenie": "Предупреждение",
    "chrezvychaynaya": "Чрезвычайная",
    "likvidatsiya": "Ликвидация последствий",
}

TIPY_OPASNOSTI = [
    {"code": "radiacionnyy", "name": "Радиационная опасность"},
    {"code": "khimicheskiy", "name": "Химическая опасность"},
    {"code": "biologicheskiy", "name": "Биологическая опасность"},
    {"code": "gidrologicheskiy", "name": "Гидрологическая опасность"},
    {"code": "geologicheskiy", "name": "Геологическая опасность"},
    {"code": "meteorologicheskiy", "name": "Метеорологическая опасность"},
    {"code": "pozharnyy", "name": "Пожарная опасность"},
]

FEDERALNYE_OKRUGA_MCHS = [
    {"code": "tcentralnyy", "name": "Центральный", "centry": ["Москва"]},
    {"code": "severo-zapadnyy", "name": "Северо-Западный", "centry": ["Санкт-Петербург"]},
    {"code": "yuzhnyy", "name": "Южный", "centry": ["Ростов-на-Дону"]},
    {"code": "privolzhskiy", "name": "Приволжский", "centry": ["Нижний Новгород"]},
    {"code": "uralskiy", "name": "Уральский", "centry": ["Екатеринбург"]},
    {"code": "sibirskiy", "name": "Сибирский", "centry": ["Красноярск"]},
    {"code": "dalnevostochnyy", "name": "Дальневосточный", "centry": ["Хабаровск"]},
]

STATISTIKA_POZHAROV_2023 = {
    "vsego_pojarov": 356842,
    "pogibshikh": 7964,
    "postradavshikh": 8647,
    "usherb_mlrd_rub": 15.2,
    "po_fo": {
        "tcentralnyy": {"pojarov": 58432, "pogibshikh": 1254},
        "severo-zapadnyy": {"pojarov": 32145, "pogibshikh": 876},
        "yuzhnyy": {"pojarov": 28934, "pogibshikh": 643},
        "privolzhskiy": {"pojarov": 62178, "pogibshikh": 1543},
        "uralskiy": {"pojarov": 34521, "pogibshikh": 897},
        "sibirskiy": {"pojarov": 56876, "pogibshikh": 1298},
        "dalnevostochnyy": {"pojarov": 83756, "pogibshikh": 1453},
    },
}
