"""Константы модуля Росводресурсов."""

# Федеральное агентство водных ресурсов (Росводресурсы)
# Основные источники данных:
# 1. Государственный водный реестр: https://text.water.ru
# 2. ГМВО (гидромониторинг): https://gmvo.skniigkh.ru
# 3. Открытые данные: https://data.gov.ru
# 4. Официальный сайт: https://rosvodresursy.ru

VODNYY_REESTR_BASE = "https://text.water.ru"
GMVO_API_BASE = "https://gmvo.skniigkh.ru"
DATA_GOV_RU_BASE = "https://data.gov.ru/api/v1"

# Бассейновые округа РФ
BASSEYNOVYE_OKRUGA = [
    {"kod": "01", "nazvanie": "Донской бассейновый округ"},
    {"kod": "02", "nazvanie": "Волжский бассейновый округ"},
    {"kod": "03", "nazvanie": "Кубанский бассейновый округ"},
    {"kod": "04", "nazvanie": "Обский бассейновый округ"},
    {"kod": "05", "nazvanie": "Уральский бассейновый округ"},
    {"kod": "06", "nazvanie": "Енисейский бассейновый округ"},
    {"kod": "07", "nazvanie": "Ленский бассейновый округ"},
    {"kod": "08", "nazvanie": "Амурский бассейновый округ"},
    {"kod": "09", "nazvanie": "Невский бассейновый округ"},
    {"kod": "10", "nazvanie": "Балтийский бассейновый округ"},
    {"kod": "11", "nazvanie": "Терско-Кумский бассейновый округ"},
    {"kod": "12", "nazvanie": "Азовский бассейновый округ"},
    {"kod": "13", "nazvanie": "Байкальский бассейновый округ"},
    {"kod": "14", "nazvanie": "Каспийский бассейновый округ"},
    {"kod": "15", "nazvanie": "Охотский бассейновый округ"},
    {"kod": "16", "nazvanie": "Беломоро-Баренцевый бассейновый округ"},
    {"kod": "17", "nazvanie": "Анадыро-Корякский бассейновый округ"},
    {"kod": "18", "nazvanie": "Камчатский бассейновый округ"},
    {"kod": "19", "nazvanie": "Сахалинский бассейновый округ"},
    {"kod": "20", "nazvanie": "Охотский бассейновый округ"},
    {"kod": "21", "nazvanie": "Бассейн реки Невы"},
]

# Типы водных объектов
TIPY_VODNYKH_OBIEKTOV = [
    {"kod": "reka", "nazvanie": "Река"},
    {"kod": "ozero", "nazvanie": "Озеро"},
    {"kod": "vodokhranilishche", "nazvanie": "Водохранилище"},
    {"kod": "kanal", "nazvanie": "Канал"},
    {"kod": "more", "nazvanie": "Море"},
    {"kod": "zaliz", "nazvanie": "Залив"},
    {"kod": "prud", "nazvanie": "Пруд"},
    {"kod": "podzemny_vod", "nazvanie": "Подземные воды"},
]

# Типы гидрологических данных
TIPY_GIDRO_DANNYKH = [
    {"kod": "uroven", "nazvanie": "Уровень воды"},
    {"kod": "raskhod", "nazvanie": "Расход воды"},
    {"kod": "temperatura", "nazvanie": "Температура воды"},
    {"kod": "led", "nazvanie": "Ледовая обстановка"},
    {"kod": "navodnenie", "nazvanie": "Паводковая обстановка"},
]

# Крупные водохранилища с характеристиками
KRUPNYE_VODOKHRANILISHCHA = [
    {
        "kod": "bratsk",
        "nazvanie": "Братское водохранилище",
        "subiekt": "Иркутская область",
        "obiem_km3": 169.0,
        "ploshchad_km2": 5470,
    },
    {
        "kod": "kuybyshev",
        "nazvanie": "Куйбышевское водохранилище",
        "subiekt": "Самарская область",
        "obiem_km3": 58.0,
        "ploshchad_km2": 6450,
    },
    {
        "kod": "volgograd",
        "nazvanie": "Волгоградское водохранилище",
        "subiekt": "Волгоградская область",
        "obiem_km3": 31.5,
        "ploshchad_km2": 3117,
    },
    {
        "kod": "tsimlyansk",
        "nazvanie": "Цимлянское водохранилище",
        "subiekt": "Ростовская область",
        "obiem_km3": 23.9,
        "ploshchad_km2": 2702,
    },
    {
        "kod": "kama",
        "nazvanie": "Камское водохранилище",
        "subiekt": "Пермский край",
        "obiem_km3": 12.2,
        "ploshchad_km2": 1915,
    },
    {
        "kod": "rybinsk",
        "nazvanie": "Рыбинское водохранилище",
        "subiekt": "Ярославская область",
        "obiem_km3": 25.4,
        "ploshchad_km2": 4550,
    },
    {
        "kod": "sayano_shushensk",
        "nazvanie": "Саяно-Шушенское водохранилище",
        "subiekt": "Республика Хакасия",
        "obiem_km3": 31.3,
        "ploshchad_km2": 621,
    },
    {
        "kod": "krasnoyarsk",
        "nazvanie": "Красноярское водохранилище",
        "subiekt": "Красноярский край",
        "obiem_km3": 73.3,
        "ploshchad_km2": 2000,
    },
    {
        "kod": "zeya",
        "nazvanie": "Зейское водохранилище",
        "subiekt": "Амурская область",
        "obiem_km3": 68.4,
        "ploshchad_km2": 2419,
    },
    {
        "kod": "bureya",
        "nazvanie": "Бурейское водохранилище",
        "subiekt": "Амурская область",
        "obiem_km3": 20.9,
        "ploshchad_km2": 743,
    },
]

# Признаки наполнения водохранилищ
PRIZNAKI_NAPOLNENIYA = {
    "normalnoe": "Нормальное",
    "nizkoe": "Ниже нормы",
    "vysokoe": "Выше нормы",
    "kriticheskoe": "Критическое",
}

# Опасные гидрологические явления
OPASNYYE_GIDRO_YAVLENIYA = {
    "navodnenie": "Наводнение",
    "pavodok": "Паводок",
    "polovode": "Половодье",
    "zator": "Затор льда",
    "zazhor": "Зажор льда",
    "selevoy_potok": "Селевой поток",
}
