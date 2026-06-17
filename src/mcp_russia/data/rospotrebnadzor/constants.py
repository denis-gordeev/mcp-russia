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
    {"code": "sanitarnyy_nadzor", "name": "Санитарно-эпидемиологический надзор"},
    {"code": "zashchita_prav_potrebiteley", "name": "Защита прав потребителей"},
    {"code": "radiatsionnaya_bezopasnost", "name": "Радиационная безопасность"},
    {"code": "bezopasnost_vodnykh", "name": "Безопасность водных объектов"},
    {"code": "kachestvo_atmosfernogo_vozdukha", "name": "Контроль качества атмосферного воздуха"},
    {"code": "bezopasnost_pishchevykh", "name": "Безопасность пищевых продуктов"},
    {
        "code": "bezopasnost_neprodovolstvennykh",
        "name": "Безопасность непродовольственных товаров",
    },
]

# Типы проверок
TIPY_PROVEROK = [
    {"code": "planovaya", "name": "Плановая проверка"},
    {"code": "vneplanovaya", "name": "Внеплановая проверка"},
    {"code": "dokumentalnaya", "name": "Документарная проверка"},
    {"code": "vyezdnaya", "name": "Выездная проверка"},
    {"code": "kontrolnaya", "name": "Контрольная проверка"},
]

# Категории объектов надзора
KATEGORII_OBIEKTOV = [
    {"code": "pishchevye_predpriyatiya", "name": "Предприятия пищевой промышленности"},
    {"code": "obshchestvennoe_pitanie", "name": "Общественное питание"},
    {"code": "obrazovatelnye_uchrezhdeniya", "name": "Образовательные учреждения"},
    {"code": "meditsinskie_organizatsii", "name": "Медицинские организации"},
    {"code": "vodosnabzhayushchie", "name": "Водоснабжающие организации"},
    {"code": "obekty_torgovli", "name": "Объекты торговли"},
    {"code": "promyshlennye_predpriyatiya", "name": "Промышленные предприятия"},
    {"code": "zhilye_zdaniya", "name": "Жилые здания"},
]

# Региональные управления (по федеральным округам)
REGIONALNYE_UPRAVLENIYA = [
    {"code": "CFD", "name": "Управление по Центральному федеральному округу"},
    {"code": "SZFD", "name": "Управление по Северо-Западному федеральному округу"},
    {"code": "YuFD", "name": "Управление по Южному федеральному округу"},
    {"code": "SKFD", "name": "Управление по Северо-Кавказскому федеральному округу"},
    {"code": "PFD", "name": "Управление по Приволжскому федеральному округу"},
    {"code": "UFD", "name": "Управление по Уральскому федеральному округу"},
    {"code": "SFD", "name": "Управление по Сибирскому федеральному округу"},
    {"code": "DFD", "name": "Управление по Дальневосточному федеральному округу"},
]

# Основные санитарные правила и нормативы (СанПиН)
SANPIN_OSNOVNYE = [
    {"code": "2.1.3684-21", "name": "СанПиН по содержанию территорий населённых мест"},
    {"code": "2.3/2.4.3590-20", "name": "СанПиН по организации общественного питания"},
    {"code": "1.2.3685-21", "name": "Гигиенические нормативы и требования к безопасности"},
    {"code": "2.4.3648-20", "name": "СанПиН к организациям воспитания и обучения"},
    {"code": "2.1.4.1074-01", "name": "СанПиН по питьевой воде"},
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
