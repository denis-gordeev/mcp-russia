"""Константы модуля Счётной палаты РФ."""

# Счётная палата Российской Федерации
# Основные источники данных:
# 1. Официальный сайт: https://ach.gov.ru
# 2. Открытые данные: https://ach.gov.ru/open-data
# 3. Портал бюджетных данных: https://budget.gov.ru
# 4. Контрольные мероприятия: https://ach.gov.ru/controls

ACH_API_BASE = "https://ach.gov.ru/api"
BUDGET_GOV_RU_BASE = "https://budget.gov.ru/api"

# Направления контрольной деятельности
NAPRAVLENIYA_KONTROLYA = [
    {
        "kod": "ispolnenie_byudzheta",
        "nazvanie": "Контроль исполнения федерального бюджета",
    },
    {
        "kod": "effektivnost",
        "nazvanie": "Аудит эффективности использования бюджетных средств",
    },
    {
        "kod": "gosprogramma",
        "nazvanie": "Экспертиза государственных программ",
    },
    {
        "kod": "zakonoproekty",
        "nazvanie": "Экспертиза законопроектов и нормативных актов",
    },
    {
        "kod": "strategicheskie",
        "nazvanie": "Стратегический анализ и прогнозирование",
    },
    {
        "kod": "antikorruptsiya",
        "nazvanie": "Антикоррупционная экспертиза",
    },
]

# Типы контрольных мероприятий
TIPY_MEROPRIYATIY = [
    {"kod": "proverka", "nazvanie": "Проверка"},
    {"kod": "auditorskaya_proverka", "nazvanie": "Аудиторская проверка"},
    {"kod": "analiticheskaya_zapiska", "nazvanie": "Аналитическая записка"},
    {"kod": "ekspertiza", "nazvanie": "Экспертиза"},
    {"kod": "monitoring", "nazvanie": "Мониторинг"},
    {"kod": "spravka", "nazvanie": "Справка"},
    {"kod": "reviziya", "nazvanie": "Ревизия"},
    {"kod": "obsledovanie", "nazvanie": "Обследование"},
]

# Субъекты внешнего государственного аудита
SUBIEKTY_AUDITA = [
    {"kod": "fz", "nazvanie": "Федеральные органы исполнительной власти"},
    {"kod": "gf", "nazvanie": "Государственные фонды (ПФР, ФСС, ФОМС)"},
    {"kod": "gk", "nazvanie": "Государственные корпорации и компании"},
    {"kod": "ak", "nazvanie": "Акционерные общества с госучастием"},
    {"kod": "bk", "nazvanie": "Бюджеты бюджетной системы РФ"},
    {"kod": "fn", "nazvanie": "Федеральные назначения"},
    {"kod": "mb", "nazvanie": "Межбюджетные трансферты субъектам РФ"},
]

# Статусы контрольных мероприятий
STATUSY_KONTROLYA = {
    "zaplanirovano": "Запланировано",
    "provoditsya": "Проводится",
    "zaversheno": "Завершено",
    "otmeneno": "Отменено",
    "utverzhdeno": "Утверждено",
}

# Виды нарушений
VIDY_NARUSHENIY = {
    "finansovoe": "Финансовое нарушение",
    "byudzhetnoe": "Бюджетное нарушение",
    "v_sfere_zakupok": "Нарушение в сфере закупок",
    "pri_ispolzovanii_gossobstvennosti": "Нарушение при использовании госсобственности",
    "pri_realizatsii_gosprogramm": "Нарушение при реализации госпрограмм",
}
