"""Constants for the Роспотребнадзор feature."""

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
    {"code": "sanitary", "name": "Санитарно-эпидемиологический надзор"},
    {"code": "consumer_protection", "name": "Защита прав потребителей"},
    {"code": "radiation_safety", "name": "Радиационная безопасность"},
    {"code": "water_safety", "name": "Безопасность водных объектов"},
    {"code": "air_quality", "name": "Контроль качества атмосферного воздуха"},
    {"code": "food_safety", "name": "Безопасность пищевых продуктов"},
    {"code": "product_safety", "name": "Безопасность непродовольственных товаров"},
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
    {"code": "food_enterprise", "name": "Предприятия пищевой промышленности"},
    {"code": "catering", "name": "Общественное питание"},
    {"code": "education", "name": "Образовательные учреждения"},
    {"code": "medical", "name": "Медицинские организации"},
    {"code": "water_supply", "name": "Водоснабжающие организации"},
    {"code": "retail", "name": "Объекты торговли"},
    {"code": "industrial", "name": "Промышленные предприятия"},
    {"code": "residential", "name": "Жилые здания"},
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
    "planned": "Запланирована",
    "in_progress": "Проводится",
    "completed": "Завершена",
    "canceled": "Отменена",
}

# Виды нарушений
VIDY_NARUSHENIY = {
    "sanitary": "Санитарно-эпидемиологическое",
    "consumer": "Защита прав потребителей",
    "radiation": "Радиационная безопасность",
    "food": "Безопасность пищевых продуктов",
}
