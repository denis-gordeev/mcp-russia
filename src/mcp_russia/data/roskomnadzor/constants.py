"""Constants for the Роскомнадзор feature."""

# Роскомнадзор (Федеральная служба по надзору в сфере связи,
# информационных технологий и массовых коммуникаций)
# Основные источники данных:
# 1. Официальный сайт: https://rkn.gov.ru
# 2. Реестр запрещённых сайтов: https://eais.rkn.gov.ru
# 3. Реестр операторов персональных данных: https://rkn.gov.ru/pdn
# 4. Реестр организаторов распространения информации: https://rkn.gov.ru/registry-ori
# 5. Открытые данные: https://rkn.gov.ru/it/opendata

RKN_API_BASE = "https://rkn.gov.ru"
RKN_OPENDATA_BASE = "https://rkn.gov.ru/it/opendata"
EAIS_API_BASE = "https://eais.rkn.gov.ru"
PDN_REGISTRY_URL = "https://rkn.gov.ru/pdn"
ORI_REGISTRY_URL = "https://rkn.gov.ru/registry-ori"

# Направления деятельности
NAPRAVLENIYA_DEYATELNOSTI = [
    {"code": "media_supervision", "name": "Надзор в сфере СМИ"},
    {"code": "telecom_supervision", "name": "Надзор в сфере связи (телекоммуникации)"},
    {"code": "it_supervision", "name": "Надзор в сфере информационных технологий"},
    {"code": "personal_data", "name": "Защита персональных данных"},
    {"code": "internet_control", "name": "Контроль информационного пространства в сети Интернет"},
    {"code": "copyright", "name": "Защита авторских прав в сети"},
]

# Типы лицензий связи
TIPY_LICENZIY_SVYAZI = [
    {"code": "telefonnaya", "name": "Телефонная связь"},
    {"code": "mobilnaya", "name": "Мобильная связь"},
    {"code": "internet", "name": "Интернет-доступ"},
    {"code": "tv_radio", "name": "Телевизионное и радиовещание"},
    {"code": "data_transmission", "name": "Передача данных"},
    {"code": "satellite", "name": "Спутниковая связь"},
]

# Категории нарушений
KATEGORII_NARUSHENIY = [
    {"code": "personal_data_leak", "name": "Утечка персональных данных"},
    {"code": "illegal_content", "name": "Распространение запрещённого контента"},
    {"code": "copyright_violation", "name": "Нарушение авторских прав"},
    {"code": "license_violation", "name": "Нарушение лицензионных требований"},
    {"code": "data_localization", "name": "Нарушение требований локализации данных"},
    {"code": "extremism", "name": "Экстремистские материалы"},
]

# Реестры Роскомнадзора
REGISTRY_RKN = [
    {
        "code": "blocked_sites",
        "name": "Единый реестр запрещённых сайтов",
        "url": "https://eais.rkn.gov.ru",
    },
    {
        "code": "pd_operators",
        "name": "Реестр операторов персональных данных",
        "url": "https://rkn.gov.ru/pdn",
    },
    {
        "code": "ori",
        "name": "Реестр организаторов распространения информации",
        "url": "https://rkn.gov.ru/registry-ori",
    },
    {
        "code": "it_companies",
        "name": "Реестр иностранных IT-компаний",
        "url": "https://rkn.gov.ru/it-companies",
    },
    {
        "code": "license_holders",
        "name": "Реестр лицензиатов связи",
        "url": "https://rkn.gov.ru/licenses",
    },
    {"code": "media_registry", "name": "Реестр СМИ", "url": "https://rkn.gov.ru/mass-media"},
]

# Типы СМИ
TIPY_SMI = [
    {"code": "print", "name": "Печатное издание (газета, журнал)"},
    {"code": "online", "name": "Сетевое издание"},
    {"code": "tv", "name": "Телеканал"},
    {"code": "radio", "name": "Радиоканал"},
    {"code": "news_agency", "name": "Информационное агентство"},
]

# Субъекты персональных данных (категории операторов)
KATEGORII_PD_OPERATOROV = [
    {"code": "government", "name": "Государственные органы"},
    {"code": "commercial", "name": "Коммерческие организации"},
    {"code": "nonprofit", "name": "Некоммерческие организации"},
    {"code": "individual_entrepreneur", "name": "Индивидуальные предприниматели"},
    {"code": "education", "name": "Образовательные учреждения"},
    {"code": "healthcare", "name": "Медицинские организации"},
]

# Основания включения в реестр запрещённых сайтов
OSNOVANIYA_BLOKIROVKI = {
    "drug": "Наркотические средства",
    "suicide": "Пропаганда самоубийств",
    "pornography": "Детская порнография",
    "extremism": "Экстремистские материалы",
    "gambling": "Нелегальные азартные игры",
    "copyright": "Нарушение авторских прав",
    "dangerous": "Опасная информация для детей",
    "fake": "Недостоверная информация",
    "personal_data": "Утечка персональных данных",
}
