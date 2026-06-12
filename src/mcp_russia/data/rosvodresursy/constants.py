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
    {"code": "01", "name": "Донской бассейновый округ"},
    {"code": "02", "name": "Волжский бассейновый округ"},
    {"code": "03", "name": "Кубанский бассейновый округ"},
    {"code": "04", "name": "Обский бассейновый округ"},
    {"code": "05", "name": "Уральский бассейновый округ"},
    {"code": "06", "name": "Енисейский бассейновый округ"},
    {"code": "07", "name": "Ленский бассейновый округ"},
    {"code": "08", "name": "Амурский бассейновый округ"},
    {"code": "09", "name": "Невский бассейновый округ"},
    {"code": "10", "name": "Балтийский бассейновый округ"},
    {"code": "11", "name": "Терско-Кумский бассейновый округ"},
    {"code": "12", "name": "Азовский бассейновый округ"},
    {"code": "13", "name": "Байкальский бассейновый округ"},
    {"code": "14", "name": "Каспийский бассейновый округ"},
    {"code": "15", "name": "Охотский бассейновый округ"},
    {"code": "16", "name": "Беломоро-Баренцевый бассейновый округ"},
    {"code": "17", "name": "Анадыро-Корякский бассейновый округ"},
    {"code": "18", "name": "Камчатский бассейновый округ"},
    {"code": "19", "name": "Сахалинский бассейновый округ"},
    {"code": "20", "name": "Охотский бассейновый округ"},
    {"code": "21", "name": "Бассейн реки Невы"},
]

# Типы водных объектов
TIPY_VODNYKH_OBIEKTOV = [
    {"code": "reka", "name": "Река"},
    {"code": "ozero", "name": "Озеро"},
    {"code": "vodokhranilishche", "name": "Водохранилище"},
    {"code": "kanal", "name": "Канал"},
    {"code": "more", "name": "Море"},
    {"code": "zaliz", "name": "Залив"},
    {"code": "prud", "name": "Пруд"},
    {"code": "podzemny_vod", "name": "Подземные воды"},
]

# Типы гидрологических данных
TIPY_GIDRO_DANNYKH = [
    {"code": "uroven", "name": "Уровень воды"},
    {"code": "raskhod", "name": "Расход воды"},
    {"code": "temperatura", "name": "Температура воды"},
    {"code": "led", "name": "Ледовая обстановка"},
    {"code": "navodnenie", "name": "Паводковая обстановка"},
]

# Крупные водохранилища с характеристиками
KRUPNYE_VODOKHRANILISHCHA = [
    {
        "code": "bratsk",
        "name": "Братское водохранилище",
        "region": "Иркутская область",
        "obiem_km3": 169.0,
        "ploshchad_km2": 5470,
    },
    {
        "code": "kuybyshev",
        "name": "Куйбышевское водохранилище",
        "region": "Самарская область",
        "obiem_km3": 58.0,
        "ploshchad_km2": 6450,
    },
    {
        "code": "volgograd",
        "name": "Волгоградское водохранилище",
        "region": "Волгоградская область",
        "obiem_km3": 31.5,
        "ploshchad_km2": 3117,
    },
    {
        "code": "tsimlyansk",
        "name": "Цимлянское водохранилище",
        "region": "Ростовская область",
        "obiem_km3": 23.9,
        "ploshchad_km2": 2702,
    },
    {
        "code": "kama",
        "name": "Камское водохранилище",
        "region": "Пермский край",
        "obiem_km3": 12.2,
        "ploshchad_km2": 1915,
    },
    {
        "code": "rybinsk",
        "name": "Рыбинское водохранилище",
        "region": "Ярославская область",
        "obiem_km3": 25.4,
        "ploshchad_km2": 4550,
    },
    {
        "code": "sayano_shushensk",
        "name": "Саяно-Шушенское водохранилище",
        "region": "Республика Хакасия",
        "obiem_km3": 31.3,
        "ploshchad_km2": 621,
    },
    {
        "code": "krasnoyarsk",
        "name": "Красноярское водохранилище",
        "region": "Красноярский край",
        "obiem_km3": 73.3,
        "ploshchad_km2": 2000,
    },
    {
        "code": "zeya",
        "name": "Зейское водохранилище",
        "region": "Амурская область",
        "obiem_km3": 68.4,
        "ploshchad_km2": 2419,
    },
    {
        "code": "bureya",
        "name": "Бурейское водохранилище",
        "region": "Амурская область",
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
