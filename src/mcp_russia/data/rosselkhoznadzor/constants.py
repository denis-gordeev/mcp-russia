"""Константы модуля Россельхознадзор."""

FSVPS_API_BASE = "https://fsvps.gov.ru/api"
FSVPS_BASE = "https://fsvps.gov.ru"
FSVPS_OPENDATA_BASE = "https://data.fsvps.gov.ru/opendata"
DATA_GOV_RU_FSVPS = "https://data.gov.ru/opendata/7710746433-fsvps"

VIDY_NADZORA = [
    {"code": "veterinarnyy", "name": "Ветеринарный надзор"},
    {"code": "fitosanitarnyy", "name": "Фитосанитарный контроль"},
    {"code": "zemelnyy", "name": "Земельный надзор"},
    {"code": "karantin_rasteniy", "name": "Карантин растений"},
    {"code": "pestitsidy", "name": "Пестициды и агрохимикаты"},
    {"code": "korma", "name": "Корма и кормовые добавки"},
]

KATEGORII_PROVEROK = [
    {"code": "planoaya", "name": "Плановая проверка"},
    {"code": "vneplanovaya", "name": "Внеплановая проверка"},
    {"code": "reysovyy", "name": "Рейдовый осмотр"},
    {"code": "monitoring", "name": "Мониторинг"},
]

STATUSY_PROVEROK = [
    {"code": "zaplanirovana", "name": "Запланирована"},
    {"code": "v_protsesse", "name": "В процессе"},
    {"code": "zavershena", "name": "Завершена"},
    {"code": "otmenena", "name": "Отменена"},
]

VIDY_NARUSHENIY_RSKHN = [
    {"code": "veterinarnye", "name": "Нарушения ветеринарного законодательства"},
    {"code": "fitosanitarnye", "name": "Нарушения фитосанитарных правил"},
    {"code": "karantinnye", "name": "Нарушения карантинного режима"},
    {"code": "zemelnye", "name": "Нарушения земельного законодательства"},
    {"code": "pestitsidnye", "name": "Нарушения в области пестицидов"},
    {"code": "kormovye", "name": "Нарушения в области кормов"},
]

TIPY_PRODUKTSII = [
    {"code": "zhivotnovodcheskaya", "name": "Животноводческая продукция"},
    {"code": "rastenievodcheskaya", "name": "Растениеводческая продукция"},
    {"code": "kombinirovannaya", "name": "Комбинированная продукция"},
    {"code": "korma_dobavki", "name": "Корма и кормовые добавки"},
    {"code": "pestitsidy_ogakh", "name": "Пестициды и агрохимикаты"},
]

KARANTINNYE_OBYEKTY = [
    {"code": "vreditel", "name": "Вредители растений"},
    {"code": "bolezni", "name": "Болезни растений"},
    {"code": "sornyaki", "name": "Сорняки (карантинные)"},
]

FEDERALNYE_OKRUGA_RSKHN = [
    {"code": "tcentralnyy", "name": "Центральный", "tsentry": ["Москва"]},
    {"code": "severo-zapadnyy", "name": "Северо-Западный", "tsentry": ["Санкт-Петербург"]},
    {"code": "yuzhnyy", "name": "Южный", "tsentry": ["Ростов-на-Дону"]},
    {"code": "privolzhskiy", "name": "Приволжский", "tsentry": ["Нижний Новгород"]},
    {"code": "uralskiy", "name": "Уральский", "tsentry": ["Екатеринбург"]},
    {"code": "sibirskiy", "name": "Сибирский", "tsentry": ["Красноярск"]},
    {"code": "dalnevostochnyy", "name": "Дальневосточный", "tsentry": ["Хабаровск"]},
    {"code": "krymskiy", "name": "Крымский", "tsentry": ["Симферополь"]},
]

STATISTIKA_RSKHN_2023 = {
    "vsego_proverok": 32450,
    "narusheniy_vyyavleno": 18230,
    "shtrafov_nalozheno": 8940,
    "summa_shtrafov_mlrd_rub": 1.8,
    "iz_yato_produktsii_tonn": 45600,
    "po_vidam": {
        "veterinarnyy": {"proverok": 12800, "narusheniy": 7450},
        "fitosanitarnyy": {"proverok": 8900, "narusheniy": 4320},
        "zemelnyy": {"proverok": 5600, "narusheniy": 3410},
        "karantin_rasteniy": {"proverok": 3100, "narusheniy": 1850},
        "pestitsidy": {"proverok": 2050, "narusheniy": 1200},
    },
}
