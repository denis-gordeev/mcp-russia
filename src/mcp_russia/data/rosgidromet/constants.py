"""Константы модуля Росгидромета."""

# Федеральная служба по гидрометеорологии и мониторингу окружающей среды (Росгидромет)
# Основные источники данных:
# 1. Официальный сайт: https://meteorf.ru
# 2. Гидрометцентр России: https://meteoinfo.ru
# 3. Спутниковый мониторинг: https://smis-evm2.niikp-atm.ru
# 4. Мониторинг загрязнения: https://mosecom.ru
#
# Рабочий API: Open-Meteo (бесплатный, без авторизации)
# - Погода: https://api.open-meteo.com/v1/forecast
# - Качество воздуха: https://air-quality-api.open-meteo.com/v1/air-quality

ROSGIDROMET_API_BASE = "https://api.meteorf.ru/v1"
OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_AIR_QUALITY_BASE = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Код направления ветра → русское название
VETER_NAPRAVLENIYA = {
    "N": "С",
    "NNE": "ССВ",
    "NE": "СВ",
    "ENE": "ВСВ",
    "E": "В",
    "ESE": "ВЮВ",
    "SE": "ЮВ",
    "SSE": "ЮЮВ",
    "S": "Ю",
    "SSW": "ЮЮЗ",
    "SW": "ЮЗ",
    "WSW": "ЗЮЗ",
    "W": "З",
    "WNW": "ЗСЗ",
    "NW": "СЗ",
    "NNW": "ССЗ",
}

# Код погодного условия → русское описание (коды ВМО)
WMO_KODY_POGODY = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Изморозь",
    51: "Лёгкая морось",
    53: "Умеренная морось",
    55: "Сильная морось",
    56: "Лёгкая замерзающая морось",
    57: "Сильная замерзающая морось",
    61: "Небольшой дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    66: "Лёгкий ледяной дождь",
    67: "Сильный ледяной дождь",
    71: "Небольшой снегопад",
    73: "Умеренный снегопад",
    75: "Сильный снегопад",
    77: "Снежные зёрна",
    80: "Небольшой ливень",
    81: "Умеренный ливень",
    82: "Сильный ливень",
    85: "Небольшой снегопад (ливень)",
    86: "Сильный снегопад (ливень)",
    95: "Гроза",
    96: "Гроза с градом",
    99: "Гроза с сильным градом",
}

# Типы метеорологических данных
TIPY_METEODANNYKH = [
    {"kod": "pogoda", "nazvanie": "Текущая погода"},
    {"kod": "prognoz", "nazvanie": "Прогноз погоды"},
    {"kod": "klimat", "nazvanie": "Климатические данные"},
    {"kod": "osadki", "nazvanie": "Осадки"},
    {"kod": "temperatura", "nazvanie": "Температура"},
    {"kod": "veter", "nazvanie": "Ветер"},
    {"kod": "davlenie", "nazvanie": "Атмосферное давление"},
    {"kod": "vlazhnost", "nazvanie": "Влажность"},
]

# Типы экологических данных
TIPY_EKODANNYKH = [
    {"kod": "vozdukh", "nazvanie": "Качество атмосферного воздуха"},
    {"kod": "voda", "nazvanie": "Качество водных ресурсов"},
    {"kod": "pochva", "nazvanie": "Загрязнение почв"},
    {"kod": "radiaciya", "nazvanie": "Радиационный фон"},
    {"kod": "shum", "nazvanie": "Шумовое загрязнение"},
]

# Станции мониторинга (основные города с координатами для Open-Meteo)
STANCII_MONITORINGA = [
    {"kod": "77", "nazvanie": "Москва", "subiekt": "ЦФО", "shirota": 55.75, "dolgota": 37.62},
    {
        "kod": "78",
        "nazvanie": "Санкт-Петербург",
        "subiekt": "СЗФО",
        "shirota": 59.93,
        "dolgota": 30.32,
    },
    {"kod": "23", "nazvanie": "Краснодар", "subiekt": "ЮФО", "shirota": 45.04, "dolgota": 38.98},
    {
        "kod": "66",
        "nazvanie": "Екатеринбург",
        "subiekt": "УФО",
        "shirota": 56.83,
        "dolgota": 60.60,
    },
    {"kod": "54", "nazvanie": "Новосибирск", "subiekt": "СФО", "shirota": 55.03, "dolgota": 82.92},
    {
        "kod": "25",
        "nazvanie": "Владивосток",
        "subiekt": "ДФО",
        "shirota": 43.12,
        "dolgota": 131.91,
    },
    {"kod": "16", "nazvanie": "Казань", "subiekt": "ПФО", "shirota": 55.79, "dolgota": 49.11},
    {
        "kod": "61",
        "nazvanie": "Ростов-на-Дону",
        "subiekt": "ЮФО",
        "shirota": 47.23,
        "dolgota": 39.71,
    },
    {"kod": "38", "nazvanie": "Иркутск", "subiekt": "СФО", "shirota": 52.30, "dolgota": 104.30},
    {"kod": "24", "nazvanie": "Красноярск", "subiekt": "СФО", "shirota": 56.01, "dolgota": 92.85},
    {
        "kod": "52",
        "nazvanie": "Нижний Новгород",
        "subiekt": "ПФО",
        "shirota": 56.33,
        "dolgota": 44.00,
    },
    {"kod": "02", "nazvanie": "Уфа", "subiekt": "ПФО", "shirota": 54.74, "dolgota": 55.97},
    {"kod": "74", "nazvanie": "Челябинск", "subiekt": "УФО", "shirota": 55.16, "dolgota": 61.40},
    {"kod": "63", "nazvanie": "Самара", "subiekt": "ПФО", "shirota": 53.20, "dolgota": 50.14},
    {"kod": "70", "nazvanie": "Томск", "subiekt": "СФО", "shirota": 56.50, "dolgota": 84.97},
]

# Предупреждения об опасных явлениях
TIPY_PREDUPREZHDENIY = [
    {"kod": "shtorm", "nazvanie": "Штормовое предупреждение"},
    {"kod": "navodnenie", "nazvanie": "Паводковое/наводнительное предупреждение"},
    {"kod": "moroz", "nazvanie": "Предупреждение о сильных морозах"},
    {"kod": "zhara", "nazvanie": "Предупреждение о сильной жаре"},
    {"kod": "grad", "nazvanie": "Предупреждение о граде"},
    {"kod": "tuman", "nazvanie": "Предупреждение о сильном тумане"},
    {"kod": "urogan", "nazvanie": "Предупреждение об урагане"},
]
