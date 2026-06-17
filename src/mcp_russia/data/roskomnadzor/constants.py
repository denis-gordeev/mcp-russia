"""Константы модуля Роскомнадзора."""

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
    {"code": "nadzor_smi", "name": "Надзор в сфере СМИ"},
    {"code": "nadzor_svyazi", "name": "Надзор в сфере связи (телекоммуникации)"},
    {"code": "nadzor_it", "name": "Надзор в сфере информационных технологий"},
    {"code": "zashchita_pd", "name": "Защита персональных данных"},
    {"code": "kontrol_interneta", "name": "Контроль информационного пространства в сети Интернет"},
    {"code": "zashchita_avtorskikh_prav", "name": "Защита авторских прав в сети"},
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
        "code": "zapreshchennye_sayty",
        "name": "Единый реестр запрещённых сайтов",
        "url": "https://eais.rkn.gov.ru",
    },
    {
        "code": "operatory_pd",
        "name": "Реестр операторов персональных данных",
        "url": "https://rkn.gov.ru/pdn",
    },
    {
        "code": "ori",
        "name": "Реестр организаторов распространения информации",
        "url": "https://rkn.gov.ru/registry-ori",
    },
    {
        "code": "inostrannye_it_kompanii",
        "name": "Реестр иностранных IT-компаний",
        "url": "https://rkn.gov.ru/it-companies",
    },
    {
        "code": "litsenziaty_svyazi",
        "name": "Реестр лицензиатов связи",
        "url": "https://rkn.gov.ru/licenses",
    },
    {"code": "reestr_smi", "name": "Реестр СМИ", "url": "https://rkn.gov.ru/mass-media"},
]

# Типы СМИ
TIPY_SMI = [
    {"code": "pechatnoe_izdanie", "name": "Печатное издание (газета, журнал)"},
    {"code": "setevoe_izdanie", "name": "Сетевое издание"},
    {"code": "telekanal", "name": "Телеканал"},
    {"code": "radiokanal", "name": "Радиоканал"},
    {"code": "informatsionnoe_agentstvo", "name": "Информационное агентство"},
]

# Субъекты персональных данных (категории операторов)
KATEGORII_PD_OPERATOROV = [
    {"code": "gosudarstvennye_organy", "name": "Государственные органы"},
    {"code": "kommercheskie_organizatsii", "name": "Коммерческие организации"},
    {"code": "nekommercheskie_organizatsii", "name": "Некоммерческие организации"},
    {"code": "individualnye_predprinimateli", "name": "Индивидуальные предприниматели"},
    {"code": "obrazovatelnye_uchrezhdeniya", "name": "Образовательные учреждения"},
    {"code": "meditsinskie_organizatsii", "name": "Медицинские организации"},
]

# Основания включения в реестр запрещённых сайтов
OSNOVANIYA_BLOKIROVKI = {
    "narkotiki": "Наркотические средства",
    "samoubiystva": "Пропаганда самоубийств",
    "detskaya_porografiya": "Детская порнография",
    "ekstremizm": "Экстремистские материалы",
    "azarntnye_igry": "Нелегальные азартные игры",
    "avtorskoe_pravo": "Нарушение авторских прав",
    "opasnaya_informatsiya": "Опасная информация для детей",
    "nedostovernaya_informatsiya": "Недостоверная информация",
    "utechka_pd": "Утечка персональных данных",
}
