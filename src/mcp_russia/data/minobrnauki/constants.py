"""Constants for the Минобрнауки feature."""

# Минобрнауки (Министерство науки и высшего образования РФ)
# Основные источники данных:
# 1. Рособрнадзор (аккредитация и лицензирование): https://obrnadzor.gov.ru
# 2. Реестр аккредитации: https://obrnadzor.gov.ru/ru/registry_accreditation
# 3. Реестр лицензий: https://obrnadzor.gov.ru/ru/registry_licensing
# 4. Рейтинг вузов: https://vuz.minobrnauki.gov.ru
# 5. Гранты РНФ: https://rscf.ru
# 6. ЕГИСУ науки: https://esu.minobrnauki.gov.ru

OBRNADZOR_API_BASE = "https://obrnadzor.gov.ru"
OBRNADZOR_ACCRED_URL = f"{OBRNADZOR_API_BASE}/opendata/7710542907-FS_ACCRED/data-20240901.json"
OBRNADZOR_LICENSE_URL = f"{OBRNADZOR_API_BASE}/opendata/7710542907-FS_LICENSE/data-20240901.json"
VUZ_RATING_URL = "https://vuz.minobrnauki.gov.ru"

TIPY_VUZOV = [
    {"code": "universitet", "name": "Университет"},
    {"code": "akademiya", "name": "Академия"},
    {"code": "institut", "name": "Институт"},
    {"code": "filial", "name": "Филиал"},
    {"code": "nii", "name": "Научно-исследовательский институт"},
]

FORMY_OBUCHENIYA = [
    {"code": "ochnaya", "name": "Очная"},
    {"code": "ochno_zaochnaya", "name": "Очно-заочная (вечерняя)"},
    {"code": "zaochnaya", "name": "Заочная"},
    {"code": "distancionnaya", "name": "Дистанционная"},
]

UROVNI_OBRAZOVANIYA = [
    {"code": "bakalavriat", "name": "Бакалавриат"},
    {"code": "specialitet", "name": "Специалитет"},
    {"code": "magistratura", "name": "Магистратура"},
    {"code": "aspirantura", "name": "Аспирантура"},
    {"code": "doktorantura", "name": "Докторантура"},
    {"code": "srednee_prof", "name": "Среднее профессиональное"},
]

OTRASLI_NAUKI = [
    {"code": "estestvennye", "name": "Естественные науки"},
    {"code": "tehnicheskie", "name": "Технические науки"},
    {"code": "medicinskie", "name": "Медицинские науки"},
    {"code": "selskohozyaystvennye", "name": "Сельскохозяйственные науки"},
    {"code": "obschestvennye", "name": "Общественные науки"},
    {"code": "gumanitarnye", "name": "Гуманитарные науки"},
    {"code": "pedagogicheskie", "name": "Педагогические науки"},
]

TIPY_GRANTOV = [
    {"code": "rnf", "name": "Гранты РНФ (Российский научный фонд)"},
    {"code": "rffi", "name": "Гранты РФФИ (Российский фонд фундаментальных исследований)"},
    {"code": "prezident", "name": "Гранты Президента РФ"},
    {"code": "minobrnauki_goszadanie", "name": "Государственное задание Минобрнауки"},
    {"code": "fund_potanina", "name": "Фонд Потанина"},
    {"code": "fund_skolkovo", "name": "Фонд «Сколково»"},
]

STATUSY_AKKREDITATSII = [
    {"code": "deystvuet", "name": "Действует"},
    {"code": "priznak_ostanovki", "name": "Приостановлена"},
    {"code": "otmenena", "name": "Отменена"},
    {"code": "isklyuchena", "name": "Исключена из реестра"},
]

FEDERALNYE_OKRUGA = [
    {"code": "cfo", "name": "Центральный федеральный округ"},
    {"code": "szfo", "name": "Северо-Западный федеральный округ"},
    {"code": "yuzfo", "name": "Южный федеральный округ"},
    {"code": "skfo", "name": "Северо-Кавказский федеральный округ"},
    {"code": "pfo", "name": "Приволжский федеральный округ"},
    {"code": "urfo", "name": "Уральский федеральный округ"},
    {"code": "sfo", "name": "Сибирский федеральный округ"},
    {"code": "dvfo", "name": "Дальневосточный федеральный округ"},
]

STATUSY_AKKREDITATSII_MAP = {
    "Действует": "Действует",
    "Приостановлена": "Приостановлена",
    "Отменена": "Отменена",
    "Исключена из реестра": "Исключена из реестра",
}

VIDY_OBRAZOVATELNYH_ORGANIZATSYY = {
    "университет": "Университет",
    "академия": "Академия",
    "институт": "Институт",
    "филиал": "Филиал",
    "нии": "Научно-исследовательский институт",
}
