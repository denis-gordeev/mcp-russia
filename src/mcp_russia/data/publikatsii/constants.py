"""Constants for the Официальные публикации РФ feature."""

# Официальные публикации Российской Федерации
# Основные источники данных:
# 1. Официальный интернет-портал правовой информации: https://pravo.gov.ru
# 2. КонсультантПлюс: https://consultant.ru
# 3. Российская газета: https://rg.ru
# 4. Собрание законодательства РФ

PRAVO_API_BASE = "https://api.pravo.gov.ru/v1"
CONSULTANT_API_BASE = "https://api.consultant.ru/v1"

# Типы нормативных актов
TIPY_NORMATIVNYKH_AKTOV = [
    {"code": "fz", "name": "Федеральный закон"},
    {"code": "ukaz", "name": "Указ Президента РФ"},
    {"code": "postanovlenie_pr", "name": "Постановление Правительства РФ"},
    {"code": "prikaz", "name": "Приказ федерального органа"},
    {"code": "fkz", "name": "Федеральный конституционный закон"},
    {"code": "ukaz_gd", "name": "Постановление Государственной Думы"},
    {"code": "ukaz_sf", "name": "Постановление Совета Федерации"},
    {"code": "pismo", "name": "Письмо федерального органа"},
    {"code": "raspor", "name": "Распоряжение Правительства РФ"},
]

# Отрасли законодательства
OTRASLI_ZAKONODATELSTVA = [
    {"code": "konstitucionnoe", "name": "Конституционное право"},
    {"code": "grazhdanskoe", "name": "Гражданское право"},
    {"code": "ugolovnoe", "name": "Уголовное право"},
    {"code": "administrativnoe", "name": "Административное право"},
    {"code": "trudovoe", "name": "Трудовое право"},
    {"code": "nalogovoe", "name": "Налоговое право"},
    {"code": "byudzhetnoe", "name": "Бюджетное право"},
    {"code": "zemelnoe", "name": "Земельное право"},
    {"code": "ekologicheskoe", "name": "Экологическое право"},
    {"code": "predprinimatelskoe", "name": "Предпринимательское право"},
]

# Источники официальных публикаций
ISTOCHNIKI_PUBLIKATSIY = [
    {
        "code": "pravo_gov_ru",
        "name": "pravo.gov.ru — Официальный интернет-портал правовой информации",
    },
    {"code": "rg_ru", "name": "rg.ru — Российская газета"},
    {"code": "consultant_ru", "name": "consultant.ru — КонсультантПлюс"},
    {"code": "garant_ru", "name": "garant.ru — ГАРАНТ"},
    {"code": "sobranie_zak", "name": "Собрание законодательства РФ"},
]

# Статусы документов
STATUSY_DOKUMENTOV = [
    {"code": "deystvuyushchiy", "name": "Действующий"},
    {"code": "utratil_silu", "name": "Утратил силу"},
    {"code": "izmeneniya", "name": "С изменениями"},
    {"code": "proekt", "name": "Проект"},
    {"code": "priostanovlen", "name": "Приостановлен"},
]
