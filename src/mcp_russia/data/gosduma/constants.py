"""Константы модуля Госдумы."""

# API Государственной Думы (открытые данные)
DUMA_API_BASE = "https://api.duma.gov.ru/api/v1"
DUMA_DEPUTATS = "https://api.duma.gov.ru/api/v1/deputies"
DUMA_LAWS = "https://sozd.duma.gov.ru/api/open-api"
DUMA_VOTES = "https://api.duma.gov.ru/api/v1/votes"
DUMA_TRANSCRIPTS = "https://api.duma.gov.ru/api/v1/transcripts"

# Ключевые показатели
KLYUCHEVYE_INDIKATORY = [
    {"code": "deputats", "name": "Список депутатов"},
    {"code": "laws", "name": "Законопроекты"},
    {"code": "sessions", "name": "Пленарные заседания"},
    {"code": "votes", "name": "Результаты голосований"},
]

# Созывы Государственной Думы
SOZYVY = [
    {"code": "1", "name": "I созыв (1993–1995)"},
    {"code": "2", "name": "II созыв (1995–1999)"},
    {"code": "3", "name": "III созыв (1999–2003)"},
    {"code": "4", "name": "IV созыв (2003–2007)"},
    {"code": "5", "name": "V созыв (2007–2011)"},
    {"code": "6", "name": "VI созыв (2011–2016)"},
    {"code": "7", "name": "VII созыв (2016–2021)"},
    {"code": "8", "name": "VIII созыв (2021–2026)"},
]

# Фракции (текущий созыв)
FRAKCII = [
    {"code": "ER", "name": "Единая Россия"},
    {"code": "KPRF", "name": "КПРФ"},
    {"code": "SRZP", "name": "Справедливая Россия — За правду"},
    {"code": "LDPR", "name": "ЛДПР"},
    {"code": "NL", "name": "Новые люди"},
]

# Комитеты (основные)
KOMITETY = [
    {"code": "budget", "name": "Комитет по бюджету и налогам"},
    {
        "code": "legislation",
        "name": "Комитет по госстроительству и законодательству",
    },
    {"code": "defense", "name": "Комитет по обороне"},
    {"code": "foreign", "name": "Комитет по международным делам"},
    {"code": "economy", "name": "Комитет по экономической политике"},
    {"code": "health", "name": "Комитет по охране здоровья"},
    {"code": "education", "name": "Комитет по просвещению"},
    {"code": "energy", "name": "Комитет по энергетике"},
]

# Статусы законопроектов
STATUSY_ZAKONOPROEKTOV = [
    {"code": "introduced", "name": "Внесён в ГД"},
    {"code": "committee", "name": "На рассмотрении комитета"},
    {"code": "first_reading", "name": "Прошёл первое чтение"},
    {"code": "second_reading", "name": "Прошёл второе чтение"},
    {"code": "third_reading", "name": "Прошёл третье чтение"},
    {"code": "approved", "name": "Одобрен Советом Федерации"},
    {"code": "signed", "name": "Подписан Президентом"},
    {"code": "rejected", "name": "Отклонён"},
    {"code": "withdrawn", "name": "Отозван инициатором"},
]

# Фракции — маппинг кодов API → русские названия
FRAKCIYA_API_MAP = {
    "ЕР": "Единая Россия",
    "НЛ": "Новые люди",
    "Единая Россия": "Единая Россия",
    "КПРФ": "КПРФ",
    "Справедливая Россия - За правду": "Справедливая Россия — За правду",
    "ЛДПР": "ЛДПР",
    "Новые люди": "Новые люди",
}
