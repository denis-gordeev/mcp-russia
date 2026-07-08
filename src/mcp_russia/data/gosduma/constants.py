"""Константы модуля Госдумы."""

# API Государственной Думы (открытые данные)
DUMA_BAZA_API = "https://api.duma.gov.ru/api/v1"
DUMA_DEPUTATY = "https://api.duma.gov.ru/api/v1/deputies"
DUMA_ZAKONOPROEKTY = "https://sozd.duma.gov.ru/api/open-api"
DUMA_GOLOSOVANIYA = "https://api.duma.gov.ru/api/v1/votes"
DUMA_STENOGRAMMY = "https://api.duma.gov.ru/api/v1/transcripts"

# Ключевые показатели
KLYUCHEVYE_INDIKATORY = [
    {"kod": "deputaty", "nazvanie": "Список депутатов"},
    {"kod": "zakonoproekty", "nazvanie": "Законопроекты"},
    {"kod": "zasedaniya", "nazvanie": "Пленарные заседания"},
    {"kod": "golosovaniya", "nazvanie": "Результаты голосований"},
]

# Созывы Государственной Думы
SOZYVY = [
    {"kod": "1", "nazvanie": "I созыв (1993–1995)"},
    {"kod": "2", "nazvanie": "II созыв (1995–1999)"},
    {"kod": "3", "nazvanie": "III созыв (1999–2003)"},
    {"kod": "4", "nazvanie": "IV созыв (2003–2007)"},
    {"kod": "5", "nazvanie": "V созыв (2007–2011)"},
    {"kod": "6", "nazvanie": "VI созыв (2011–2016)"},
    {"kod": "7", "nazvanie": "VII созыв (2016–2021)"},
    {"kod": "8", "nazvanie": "VIII созыв (2021–2026)"},
]

# Фракции (текущий созыв)
FRAKCII = [
    {"kod": "ER", "nazvanie": "Единая Россия"},
    {"kod": "KPRF", "nazvanie": "КПРФ"},
    {"kod": "SRZP", "nazvanie": "Справедливая Россия — За правду"},
    {"kod": "LDPR", "nazvanie": "ЛДПР"},
    {"kod": "NL", "nazvanie": "Новые люди"},
]

# Комитеты (основные)
KOMITETY = [
    {"kod": "byudzhet_i_nalogi", "nazvanie": "Комитет по бюджету и налогам"},
    {
        "kod": "gosstroitelstvo_i_zakonodatelstvo",
        "nazvanie": "Комитет по госстроительству и законодательству",
    },
    {"kod": "oborona", "nazvanie": "Комитет по обороне"},
    {"kod": "mezhdunarodnye_dela", "nazvanie": "Комитет по международным делам"},
    {"kod": "ekonomicheskaya_politika", "nazvanie": "Комитет по экономической политике"},
    {"kod": "okhrana_zdorovya", "nazvanie": "Комитет по охране здоровья"},
    {"kod": "prosvishchenie", "nazvanie": "Комитет по просвещению"},
    {"kod": "energetika", "nazvanie": "Комитет по энергетике"},
]

# Статусы законопроектов
STATUSY_ZAKONOPROEKTOV = [
    {"kod": "vnesen_v_gd", "nazvanie": "Внесён в ГД"},
    {"kod": "v_komitete", "nazvanie": "На рассмотрении комитета"},
    {"kod": "pervoe_chtenie", "nazvanie": "Прошёл первое чтение"},
    {"kod": "vtoroe_chtenie", "nazvanie": "Прошёл второе чтение"},
    {"kod": "tretie_chtenie", "nazvanie": "Прошёл третье чтение"},
    {"kod": "odobren_sf", "nazvanie": "Одобрен Советом Федерации"},
    {"kod": "podpisan_prezidentom", "nazvanie": "Подписан Президентом"},
    {"kod": "otklonen", "nazvanie": "Отклонён"},
    {"kod": "otozvan_initsiatorom", "nazvanie": "Отозван инициатором"},
]

# Фракции — маппинг кодов API → русские названия
FRAKCIYA_SLOVAR_API = {
    "ЕР": "Единая Россия",
    "НЛ": "Новые люди",
    "Единая Россия": "Единая Россия",
    "КПРФ": "КПРФ",
    "Справедливая Россия - За правду": "Справедливая Россия — За правду",
    "ЛДПР": "ЛДПР",
    "Новые люди": "Новые люди",
}
