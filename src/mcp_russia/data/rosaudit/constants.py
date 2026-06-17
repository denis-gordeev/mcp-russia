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
        "code": "ispolnenie_byudzheta",
        "name": "Контроль исполнения федерального бюджета",
    },
    {
        "code": "effektivnost",
        "name": "Аудит эффективности использования бюджетных средств",
    },
    {
        "code": "gosprogramma",
        "name": "Экспертиза государственных программ",
    },
    {
        "code": "zakonoproekty",
        "name": "Экспертиза законопроектов и нормативных актов",
    },
    {
        "code": "strategicheskie",
        "name": "Стратегический анализ и прогнозирование",
    },
    {
        "code": "antikorruptsiya",
        "name": "Антикоррупционная экспертиза",
    },
]

# Типы контрольных мероприятий
TIPY_MEROPRIYATIY = [
    {"code": "proverka", "name": "Проверка"},
    {"code": "auditorskaya_proverka", "name": "Аудиторская проверка"},
    {"code": "analiticheskaya_zapiska", "name": "Аналитическая записка"},
    {"code": "ekspertiza", "name": "Экспертиза"},
    {"code": "monitoring", "name": "Мониторинг"},
    {"code": "spravka", "name": "Справка"},
    {"code": "reviziya", "name": "Ревизия"},
    {"code": "obsledovanie", "name": "Обследование"},
]

# Субъекты внешнего государственного аудита
SUBIEKTY_AUDITA = [
    {"code": "fz", "name": "Федеральные органы исполнительной власти"},
    {"code": "gf", "name": "Государственные фонды (ПФР, ФСС, ФОМС)"},
    {"code": "gk", "name": "Государственные корпорации и компании"},
    {"code": "ak", "name": "Акционерные общества с госучастием"},
    {"code": "bk", "name": "Бюджеты бюджетной системы РФ"},
    {"code": "fn", "name": "Федеральные назначения"},
    {"code": "mb", "name": "Межбюджетные трансферты субъектам РФ"},
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
