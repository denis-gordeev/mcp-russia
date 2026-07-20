"""Константы модуля Роскомнадзора."""

# Роскомнадзор (Федеральная служба по надзору в сфере связи,
# информационных технологий и массовых коммуникаций)
# Основные источники данных:
# 1. Официальный сайт: https://rkn.gov.ru
# 2. Реестр запрещённых сайтов: https://eais.rkn.gov.ru
# 3. Реестр операторов персональных данных: https://rkn.gov.ru/pdn
# 4. Реестр организаторов распространения информации: https://rkn.gov.ru/registry-ori
# 5. Открытые данные: https://rkn.gov.ru/it/opendata

RKN_BAZA_API = "https://rkn.gov.ru"
RKN_BAZA_OTKRYTYKH_DANNYKH = "https://rkn.gov.ru/it/opendata"
EAIS_BAZA_API = "https://eais.rkn.gov.ru"
PDN_REESTR_ADRES = "https://rkn.gov.ru/pdn"
ORI_REESTR_ADRES = "https://rkn.gov.ru/registry-ori"

# Направления деятельности
NAPRAVLENIYA_DEYATELNOSTI = [
    {"kod": "nadzor_smi", "nazvanie": "Надзор в сфере СМИ"},
    {"kod": "nadzor_svyazi", "nazvanie": "Надзор в сфере связи (телекоммуникации)"},
    {"kod": "nadzor_it", "nazvanie": "Надзор в сфере информационных технологий"},
    {"kod": "zashchita_pd", "nazvanie": "Защита персональных данных"},
    {
        "kod": "kontrol_interneta",
        "nazvanie": "Контроль информационного пространства в сети Интернет",
    },
    {"kod": "zashchita_avtorskikh_prav", "nazvanie": "Защита авторских прав в сети"},
]

# Типы лицензий связи
TIPY_LITSENZIY_SVYAZI = [
    {"kod": "telefonnaya", "nazvanie": "Телефонная связь"},
    {"kod": "mobilnaya", "nazvanie": "Мобильная связь"},
    {"kod": "internet", "nazvanie": "Интернет-доступ"},
    {"kod": "tv_radio", "nazvanie": "Телевизионное и радиовещание"},
    {"kod": "peredacha_dannykh", "nazvanie": "Передача данных"},
    {"kod": "sputnikovaya", "nazvanie": "Спутниковая связь"},
]

# Категории нарушений
KATEGORII_NARUSHENIY = [
    {"kod": "utechka_personalnykh_dannykh", "nazvanie": "Утечка персональных данных"},
    {"kod": "zapreshchennyy_kontent", "nazvanie": "Распространение запрещённого контента"},
    {"kod": "narushenie_avtorskikh_prav", "nazvanie": "Нарушение авторских прав"},
    {
        "kod": "narushenie_litsenzionnykh_trebovaniy",
        "nazvanie": "Нарушение лицензионных требований",
    },
    {
        "kod": "narushenie_lokalizatsii_dannykh",
        "nazvanie": "Нарушение требований локализации данных",
    },
    {"kod": "ekstremistskie_materialy", "nazvanie": "Экстремистские материалы"},
]

# Реестры Роскомнадзора
REESTR_RKN = [
    {
        "kod": "zapreshchennye_sayty",
        "nazvanie": "Единый реестр запрещённых сайтов",
        "ssylka": "https://eais.rkn.gov.ru",
    },
    {
        "kod": "operatory_pd",
        "nazvanie": "Реестр операторов персональных данных",
        "ssylka": "https://rkn.gov.ru/pdn",
    },
    {
        "kod": "ori",
        "nazvanie": "Реестр организаторов распространения информации",
        "ssylka": "https://rkn.gov.ru/registry-ori",
    },
    {
        "kod": "inostrannye_it_kompanii",
        "nazvanie": "Реестр иностранных IT-компаний",
        "ssylka": "https://rkn.gov.ru/it-companies",
    },
    {
        "kod": "litsenziaty_svyazi",
        "nazvanie": "Реестр лицензиатов связи",
        "ssylka": "https://rkn.gov.ru/licenses",
    },
    {"kod": "reestr_smi", "nazvanie": "Реестр СМИ", "ssylka": "https://rkn.gov.ru/mass-media"},
]

# Типы СМИ
TIPY_SMI = [
    {"kod": "pechatnoe_izdanie", "nazvanie": "Печатное издание (газета, журнал)"},
    {"kod": "setevoe_izdanie", "nazvanie": "Сетевое издание"},
    {"kod": "telekanal", "nazvanie": "Телеканал"},
    {"kod": "radiokanal", "nazvanie": "Радиоканал"},
    {"kod": "informatsionnoe_agentstvo", "nazvanie": "Информационное агентство"},
]

# Субъекты персональных данных (категории операторов)
KATEGORII_PD_OPERATOROV = [
    {"kod": "gosudarstvennye_organy", "nazvanie": "Государственные органы"},
    {"kod": "kommercheskie_organizatsii", "nazvanie": "Коммерческие организации"},
    {"kod": "nekommercheskie_organizatsii", "nazvanie": "Некоммерческие организации"},
    {"kod": "individualnye_predprinimateli", "nazvanie": "Индивидуальные предприниматели"},
    {"kod": "obrazovatelnye_uchrezhdeniya", "nazvanie": "Образовательные учреждения"},
    {"kod": "meditsinskie_organizatsii", "nazvanie": "Медицинские организации"},
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
