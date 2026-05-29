"""Constants for the Росгидромет feature."""

# Федеральная служба по гидрометеорологии и мониторингу окружающей среды (Росгидромет)
# Основные источники данных:
# 1. Официальный сайт: https://meteorf.ru
# 2. Гидрометцентр России: https://meteoinfo.ru
# 3. Спутниковый мониторинг: https://smis-evm2.niikp-atm.ru
# 4. Мониторинг загрязнения: https://mosecom.ru

ROSGIDROMET_API_BASE = "https://api.meteorf.ru/v1"

# Типы метеорологических данных
TIPY_METEODANNYKH = [
    {"code": "pogoda", "name": "Текущая погода"},
    {"code": "prognoz", "name": "Прогноз погоды"},
    {"code": "klimat", "name": "Климатические данные"},
    {"code": "osadki", "name": "Осадки"},
    {"code": "temperatura", "name": "Температура"},
    {"code": "veter", "name": "Ветер"},
    {"code": "davlenie", "name": "Атмосферное давление"},
    {"code": "vlazhnost", "name": "Влажность"},
]

# Типы экологических данных
TIPY_EKODANNYKH = [
    {"code": "vozdukh", "name": "Качество атмосферного воздуха"},
    {"code": "voda", "name": "Качество водных ресурсов"},
    {"code": "pochva", "name": "Загрязнение почв"},
    {"code": "radiaciya", "name": "Радиационный фон"},
    {"code": "shum", "name": "Шумовое загрязнение"},
]

# Станции мониторинга (основные города)
STANCII_MONITORINGA = [
    {"code": "77", "name": "Москва", "region": "ЦФО"},
    {"code": "78", "name": "Санкт-Петербург", "region": "СЗФО"},
    {"code": "23", "name": "Краснодар", "region": "ЮФО"},
    {"code": "66", "name": "Екатеринбург", "region": "УФО"},
    {"code": "54", "name": "Новосибирск", "region": "СФО"},
    {"code": "25", "name": "Владивосток", "region": "ДФО"},
    {"code": "16", "name": "Казань", "region": "ПФО"},
    {"code": "61", "name": "Ростов-на-Дону", "region": "ЮФО"},
]

# Предупреждения об опасных явлениях
TIPY_PREDUPREZHDENIY = [
    {"code": "shtorm", "name": "Штормовое предупреждение"},
    {"code": "navodnenie", "name": "Паводковое/наводнительное предупреждение"},
    {"code": "moroz", "name": "Предупреждение о сильных морозах"},
    {"code": "zhara", "name": "Предупреждение о сильной жаре"},
    {"code": "grad", "name": "Предупреждение о граде"},
    {"code": "tuman", "name": "Предупреждение о сильном тумане"},
    {"code": "urogan", "name": "Предупреждение об урагане"},
]
