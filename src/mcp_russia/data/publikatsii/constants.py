"""Константы модуля Официальные публикации РФ."""

# Официальные публикации Российской Федерации
# Основные источники данных:
# 1. Официальный интернет-портал правовой информации: https://pravo.gov.ru
# 2. КонсультантПлюс: https://consultant.ru
# 3. Российская газета: https://rg.ru
# 4. Собрание законодательства РФ

PRAVO_BAZA_API = "https://pravo.gov.ru/opendata/7700748144-prfgi"
PRAVO_ADRES_POISKA = "https://pravo.gov.ru/opendata/7700748144-prfgi/search"
PRAVO_ADRES_DOKUMENTA = "https://pravo.gov.ru/opendata/7700748144-prfgi/document"
KONSULTANT_BAZA_API = "https://api.consultant.ru/v1"  # платный сервис

# Типы документов pravo.gov.ru (коды портала)
TIPY_DOKUMENTOV_PRAVO = {
    "1": "Конституция РФ",
    "2": "Федеральный конституционный закон",
    "3": "Федеральный закон",
    "4": "Указ Президента РФ",
    "5": "Постановление Правительства РФ",
    "6": "Распоряжение Правительства РФ",
    "7": "Постановление Совета Федерации",
    "8": "Постановление Государственной Думы",
    "9": "Приказ федерального органа",
    "10": "Письмо федерального органа",
    "11": "Решение Конституционного Суда",
    "12": "Определение Конституционного Суда",
    "13": "Постановление Пленума ВС РФ",
    "14": "Закон субъекта РФ",
    "15": "Международный договор",
    "16": "Нормативный акт СССР",
    "17": "Прочий нормативный акт",
}

# Типы нормативных актов
TIPY_NORMATIVNYKH_AKTOV = [
    {"kod": "fz", "nazvanie": "Федеральный закон"},
    {"kod": "ukaz", "nazvanie": "Указ Президента РФ"},
    {"kod": "postanovlenie_pr", "nazvanie": "Постановление Правительства РФ"},
    {"kod": "prikaz", "nazvanie": "Приказ федерального органа"},
    {"kod": "fkz", "nazvanie": "Федеральный конституционный закон"},
    {"kod": "ukaz_gd", "nazvanie": "Постановление Государственной Думы"},
    {"kod": "ukaz_sf", "nazvanie": "Постановление Совета Федерации"},
    {"kod": "pismo", "nazvanie": "Письмо федерального органа"},
    {"kod": "raspor", "nazvanie": "Распоряжение Правительства РФ"},
]

# Отрасли законодательства
OTRASLI_ZAKONODATELSTVA = [
    {"kod": "konstitutsionnoe", "nazvanie": "Конституционное право"},
    {"kod": "grazhdanskoe", "nazvanie": "Гражданское право"},
    {"kod": "ugolovnoe", "nazvanie": "Уголовное право"},
    {"kod": "administrativnoe", "nazvanie": "Административное право"},
    {"kod": "trudovoe", "nazvanie": "Трудовое право"},
    {"kod": "nalogovoe", "nazvanie": "Налоговое право"},
    {"kod": "byudzhetnoe", "nazvanie": "Бюджетное право"},
    {"kod": "zemelnoe", "nazvanie": "Земельное право"},
    {"kod": "ekologicheskoe", "nazvanie": "Экологическое право"},
    {"kod": "predprinimatelskoe", "nazvanie": "Предпринимательское право"},
]

# Источники официальных публикаций
ISTOCHNIKI_PUBLIKATSIY = [
    {
        "kod": "pravo_gov_ru",
        "nazvanie": "pravo.gov.ru — Официальный интернет-портал правовой информации",
    },
    {"kod": "rg_ru", "nazvanie": "rg.ru — Российская газета"},
    {"kod": "consultant_ru", "nazvanie": "consultant.ru — КонсультантПлюс"},
    {"kod": "garant_ru", "nazvanie": "garant.ru — ГАРАНТ"},
    {"kod": "sobranie_zak", "nazvanie": "Собрание законодательства РФ"},
]

# Статусы документов
STATUSY_DOKUMENTOV = [
    {"kod": "deystvuyushchiy", "nazvanie": "Действующий"},
    {"kod": "utratil_silu", "nazvanie": "Утратил силу"},
    {"kod": "izmeneniya", "nazvanie": "С изменениями"},
    {"kod": "proekt", "nazvanie": "Проект"},
    {"kod": "priostanovlen", "nazvanie": "Приостановлен"},
]
