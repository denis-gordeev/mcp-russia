"""Константы модуля Роспотребнадзора."""

# Роспотребнадзор (Федеральная служба по надзору в сфере защиты прав
# потребителей и благополучия человека)
# Основные источники данных:
# 1. Официальный сайт: https://rospotrebnadzor.ru
# 2. Открытые данные: https://rospotrebnadzor.ru/opendata
# 3. Реестр проверок: https://proverki.rospotrebnadzor.ru
# 4. Защита прав потребителей: https://zpp.rospotrebnadzor.ru

ROSPOTREBNADZOR_API_BASE = "https://rospotrebnadzor.ru/api"
PROVERKI_API_BASE = "https://proverki.rospotrebnadzor.ru"
ZPP_API_BASE = "https://zpp.rospotrebnadzor.ru"

# Направления деятельности
NAPRAVLENIYA_DEYATELNOSTI = [
    {"kod": "sanitarnyy_nadzor", "nazvanie": "Санитарно-эпидемиологический надзор"},
    {"kod": "zashchita_prav_potrebiteley", "nazvanie": "Защита прав потребителей"},
    {"kod": "radiatsionnaya_bezopasnost", "nazvanie": "Радиационная безопасность"},
    {"kod": "bezopasnost_vodnykh", "nazvanie": "Безопасность водных объектов"},
    {
        "kod": "kachestvo_atmosfernogo_vozdukha",
        "nazvanie": "Контроль качества атмосферного воздуха",
    },
    {"kod": "bezopasnost_pishchevykh", "nazvanie": "Безопасность пищевых продуктов"},
    {
        "kod": "bezopasnost_neprodovolstvennykh",
        "nazvanie": "Безопасность непродовольственных товаров",
    },
]

# Типы проверок
TIPY_PROVEROK = [
    {"kod": "planovaya", "nazvanie": "Плановая проверка"},
    {"kod": "vneplanovaya", "nazvanie": "Внеплановая проверка"},
    {"kod": "dokumentalnaya", "nazvanie": "Документарная проверка"},
    {"kod": "vyezdnaya", "nazvanie": "Выездная проверка"},
    {"kod": "kontrolnaya", "nazvanie": "Контрольная проверка"},
]

# Категории объектов надзора
KATEGORII_OBIEKTOV = [
    {"kod": "pishchevye_predpriyatiya", "nazvanie": "Предприятия пищевой промышленности"},
    {"kod": "obshchestvennoe_pitanie", "nazvanie": "Общественное питание"},
    {"kod": "obrazovatelnye_uchrezhdeniya", "nazvanie": "Образовательные учреждения"},
    {"kod": "meditsinskie_organizatsii", "nazvanie": "Медицинские организации"},
    {"kod": "vodosnabzhayushchie", "nazvanie": "Водоснабжающие организации"},
    {"kod": "obekty_torgovli", "nazvanie": "Объекты торговли"},
    {"kod": "promyshlennye_predpriyatiya", "nazvanie": "Промышленные предприятия"},
    {"kod": "zhilye_zdaniya", "nazvanie": "Жилые здания"},
]

# Региональные управления (по федеральным округам)
REGIONALNYE_UPRAVLENIYA = [
    {"kod": "CFD", "nazvanie": "Управление по Центральному федеральному округу"},
    {"kod": "SZFD", "nazvanie": "Управление по Северо-Западному федеральному округу"},
    {"kod": "YuFD", "nazvanie": "Управление по Южному федеральному округу"},
    {"kod": "SKFD", "nazvanie": "Управление по Северо-Кавказскому федеральному округу"},
    {"kod": "PFD", "nazvanie": "Управление по Приволжскому федеральному округу"},
    {"kod": "UFD", "nazvanie": "Управление по Уральскому федеральному округу"},
    {"kod": "SFD", "nazvanie": "Управление по Сибирскому федеральному округу"},
    {"kod": "DFD", "nazvanie": "Управление по Дальневосточному федеральному округу"},
]

# Основные санитарные правила и нормативы (СанПиН)
SANPIN_OSNOVNYE = [
    {"kod": "2.1.3684-21", "nazvanie": "СанПиН по содержанию территорий населённых мест"},
    {"kod": "2.3/2.4.3590-20", "nazvanie": "СанПиН по организации общественного питания"},
    {"kod": "1.2.3685-21", "nazvanie": "Гигиенические нормативы и требования к безопасности"},
    {"kod": "2.4.3648-20", "nazvanie": "СанПиН к организациям воспитания и обучения"},
    {"kod": "2.1.4.1074-01", "nazvanie": "СанПиН по питьевой воде"},
]

# Статусы проверок
STATUSY_PROVEROK = {
    "zaplanirovana": "Запланирована",
    "provoditsya": "Проводится",
    "zavershena": "Завершена",
    "otmenena": "Отменена",
}

# Виды нарушений
VIDY_NARUSHENIY = {
    "sanitarnoe": "Санитарно-эпидемиологическое",
    "prava_potrebiteley": "Защита прав потребителей",
    "radiatsionnaya": "Радиационная безопасность",
    "pishchevaya_bezopasnost": "Безопасность пищевых продуктов",
}
