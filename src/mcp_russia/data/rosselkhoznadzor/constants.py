"""Константы модуля Россельхознадзор."""

FSVPS_API_BASE = "https://fsvps.gov.ru/api"
FSVPS_BASE = "https://fsvps.gov.ru"
FSVPS_OPENDATA_BASE = "https://data.fsvps.gov.ru/opendata"
DATA_GOV_RU_FSVPS = "https://data.gov.ru/opendata/7710746433-fsvps"

VIDY_NADZORA = [
    {"kod": "veterinarnyy", "nazvanie": "Ветеринарный надзор"},
    {"kod": "fitosanitarnyy", "nazvanie": "Фитосанитарный контроль"},
    {"kod": "zemelnyy", "nazvanie": "Земельный надзор"},
    {"kod": "karantin_rasteniy", "nazvanie": "Карантин растений"},
    {"kod": "pestitsidy", "nazvanie": "Пестициды и агрохимикаты"},
    {"kod": "korma", "nazvanie": "Корма и кормовые добавки"},
]

KATEGORII_PROVEROK = [
    {"kod": "planoaya", "nazvanie": "Плановая проверка"},
    {"kod": "vneplanovaya", "nazvanie": "Внеплановая проверка"},
    {"kod": "reysovyy", "nazvanie": "Рейдовый осмотр"},
    {"kod": "monitoring", "nazvanie": "Мониторинг"},
]

STATUSY_PROVEROK = [
    {"kod": "zaplanirovana", "nazvanie": "Запланирована"},
    {"kod": "v_protsesse", "nazvanie": "В процессе"},
    {"kod": "zavershena", "nazvanie": "Завершена"},
    {"kod": "otmenena", "nazvanie": "Отменена"},
]

VIDY_NARUSHENIY_RSKHN = [
    {"kod": "veterinarnye", "nazvanie": "Нарушения ветеринарного законодательства"},
    {"kod": "fitosanitarnye", "nazvanie": "Нарушения фитосанитарных правил"},
    {"kod": "karantinnye", "nazvanie": "Нарушения карантинного режима"},
    {"kod": "zemelnye", "nazvanie": "Нарушения земельного законодательства"},
    {"kod": "pestitsidnye", "nazvanie": "Нарушения в области пестицидов"},
    {"kod": "kormovye", "nazvanie": "Нарушения в области кормов"},
]

TIPY_PRODUKTSII = [
    {"kod": "zhivotnovodcheskaya", "nazvanie": "Животноводческая продукция"},
    {"kod": "rastenievodcheskaya", "nazvanie": "Растениеводческая продукция"},
    {"kod": "kombinirovannaya", "nazvanie": "Комбинированная продукция"},
    {"kod": "korma_dobavki", "nazvanie": "Корма и кормовые добавки"},
    {"kod": "pestitsidy_ogakh", "nazvanie": "Пестициды и агрохимикаты"},
]

KARANTINNYE_OBYEKTY = [
    {"kod": "vreditel", "nazvanie": "Вредители растений"},
    {"kod": "bolezni", "nazvanie": "Болезни растений"},
    {"kod": "sornyaki", "nazvanie": "Сорняки (карантинные)"},
]

FEDERALNYE_OKRUGA_RSKHN = [
    {"kod": "tcentralnyy", "nazvanie": "Центральный", "tsentry": ["Москва"]},
    {"kod": "severo-zapadnyy", "nazvanie": "Северо-Западный", "tsentry": ["Санкт-Петербург"]},
    {"kod": "yuzhnyy", "nazvanie": "Южный", "tsentry": ["Ростов-на-Дону"]},
    {"kod": "privolzhskiy", "nazvanie": "Приволжский", "tsentry": ["Нижний Новгород"]},
    {"kod": "uralskiy", "nazvanie": "Уральский", "tsentry": ["Екатеринбург"]},
    {"kod": "sibirskiy", "nazvanie": "Сибирский", "tsentry": ["Красноярск"]},
    {"kod": "dalnevostochnyy", "nazvanie": "Дальневосточный", "tsentry": ["Хабаровск"]},
    {"kod": "krymskiy", "nazvanie": "Крымский", "tsentry": ["Симферополь"]},
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
