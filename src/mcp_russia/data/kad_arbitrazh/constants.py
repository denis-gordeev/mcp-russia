"""Constants for the Kad Arbitrazh (Картотека арбитражных дел) feature."""

# API Картотеки арбитражных дел
KAD_ARBITR_API_BASE = "https://kad.arbitr.ru"
KAD_ARBITR_SEARCH = "https://kad.arbitr.ru/Search"
KAD_ARBITR_CASE_URL = "https://kad.arbitr.ru/Case/"

# Инстанции арбитражных судов
INSTANTSII_SUDOV = [
    {"code": "first", "name": "Арбитражный суд субъекта РФ (первая инстанция)"},
    {"code": "appeal", "name": "Арбитражный апелляционный суд"},
    {"code": "cassation", "name": "Арбитражный суд округа (кассация)"},
    {"code": "supreme", "name": "Судебная коллегия ВС РФ"},
]

# Категории дел
KATEGORII_DEL = [
    {"code": "bankruptcy", "name": "Банкротство"},
    {"code": "contract", "name": "Споры из договоров"},
    {"code": "tax", "name": "Налоговые споры"},
    {"code": "property", "name": "Имущественные споры"},
    {"code": "corporate", "name": "Корпоративные споры"},
    {"code": "ip", "name": "Интеллектуальная собственность"},
    {"code": "administrative", "name": "Административные дела"},
    {"code": "enforcement", "name": "Дела о принудительном исполнении"},
]

# Статусы дел
STATUSY_DEL = [
    {"code": "new", "name": "Новое"},
    {"code": "accepted", "name": "Принято к производству"},
    {"code": "pending", "name": "На рассмотрении"},
    {"code": "postponed", "name": "Отложено"},
    {"code": "decided", "name": "Решение вынесено"},
    {"code": "appealed", "name": "Обжаловано"},
    {"code": "closed", "name": "Дело завершено"},
]

# Типы судебных актов
TIPLY_AKTOV = [
    {"code": "decision", "name": "Решение"},
    {"code": "definition", "name": "Определение"},
    {"code": "resolution", "name": "Постановление"},
    {"code": "order", "name": "Приказ"},
    {"code": "ruling", "name": "Распоряжение"},
]

# Арбитражные суды по округам (основные)
ARBITRAZHNYE_SUDY = [
    {"code": "VAS", "name": "Судебная коллегия по экономическим спорам ВС РФ"},
    {"code": "ASMO", "name": "Арбитражный суд Московского округа"},
    {"code": "ASZPO", "name": "Арбитражный суд Западно-Сибирского округа"},
    {"code": "ASVSO", "name": "Арбитражный суд Восточно-Сибирского округа"},
    {"code": "ASDO", "name": "Арбитражный суд Дальневосточного округа"},
    {"code": "ASZSO", "name": "Арбитражный суд Западно-Сибирского округа"},
    {"code": "ASPO", "name": "Арбитражный суд Поволжского округа"},
    {"code": "ASZSO", "name": "Арбитражный суд Уральского округа"},
    {"code": "ASCZO", "name": "Арбитражный суд Северо-Кавказского округа"},
    {"code": "ASSZO", "name": "Арбитражный суд Северо-Западного округа"},
    {"code": "ASMSO", "name": "Арбитражный суд Московского округа"},
    {"code": "ASCZO", "name": "Арбитражный суд Центрального округа"},
]
