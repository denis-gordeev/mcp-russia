"""Константы модуля Минобрнауки."""

# Минобрнауки (Министерство науки и высшего образования РФ)
# Основные источники данных:
# 1. Рособрнадзор (аккредитация и лицензирование): https://obrnadzor.gov.ru
# 2. Реестр аккредитации: https://obrnadzor.gov.ru/ru/registry_accreditation
# 3. Реестр лицензий: https://obrnadzor.gov.ru/ru/registry_licensing
# 4. Рейтинг вузов: https://vuz.minobrnauki.gov.ru
# 5. Гранты РНФ: https://rscf.ru
# 6. ЕГИСУ науки: https://esu.minobrnauki.gov.ru

OBRNADZOR_API_BAZA = "https://obrnadzor.gov.ru"
OBRNADZOR_AKKREDITATSIYA_ADRES = (
    f"{OBRNADZOR_API_BAZA}/opendata/7710542907-FS_ACCRED/data-20240901.json"
)
OBRNADZOR_LITSENZIYA_ADRES = (
    f"{OBRNADZOR_API_BAZA}/opendata/7710542907-FS_LICENSE/data-20240901.json"
)
VUZ_REYTING_ADRES = "https://vuz.minobrnauki.gov.ru"

TIPY_VUZOV = [
    {"kod": "universitet", "nazvanie": "Университет"},
    {"kod": "akademiya", "nazvanie": "Академия"},
    {"kod": "institut", "nazvanie": "Институт"},
    {"kod": "filial", "nazvanie": "Филиал"},
    {"kod": "nii", "nazvanie": "Научно-исследовательский институт"},
]

FORMY_OBUCHENIYA = [
    {"kod": "ochnaya", "nazvanie": "Очная"},
    {"kod": "ochno_zaochnaya", "nazvanie": "Очно-заочная (вечерняя)"},
    {"kod": "zaochnaya", "nazvanie": "Заочная"},
    {"kod": "distancionnaya", "nazvanie": "Дистанционная"},
]

UROVNI_OBRAZOVANIYA = [
    {"kod": "bakalavriat", "nazvanie": "Бакалавриат"},
    {"kod": "specialitet", "nazvanie": "Специалитет"},
    {"kod": "magistratura", "nazvanie": "Магистратура"},
    {"kod": "aspirantura", "nazvanie": "Аспирантура"},
    {"kod": "doktorantura", "nazvanie": "Докторантура"},
    {"kod": "srednee_prof", "nazvanie": "Среднее профессиональное"},
]

OTRASLI_NAUKI = [
    {"kod": "estestvennye", "nazvanie": "Естественные науки"},
    {"kod": "tehnicheskie", "nazvanie": "Технические науки"},
    {"kod": "medicinskie", "nazvanie": "Медицинские науки"},
    {"kod": "selskohozyaystvennye", "nazvanie": "Сельскохозяйственные науки"},
    {"kod": "obschestvennye", "nazvanie": "Общественные науки"},
    {"kod": "gumanitarnye", "nazvanie": "Гуманитарные науки"},
    {"kod": "pedagogicheskie", "nazvanie": "Педагогические науки"},
]

TIPY_GRANTOV = [
    {"kod": "rnf", "nazvanie": "Гранты РНФ (Российский научный фонд)"},
    {"kod": "rffi", "nazvanie": "Гранты РФФИ (Российский фонд фундаментальных исследований)"},
    {"kod": "prezident", "nazvanie": "Гранты Президента РФ"},
    {"kod": "minobrnauki_goszadanie", "nazvanie": "Государственное задание Минобрнауки"},
    {"kod": "fund_potanina", "nazvanie": "Фонд Потанина"},
    {"kod": "fund_skolkovo", "nazvanie": "Фонд «Сколково»"},
]

STATUSY_AKKREDITATSII = [
    {"kod": "deystvuet", "nazvanie": "Действует"},
    {"kod": "priznak_ostanovki", "nazvanie": "Приостановлена"},
    {"kod": "otmenena", "nazvanie": "Отменена"},
    {"kod": "isklyuchena", "nazvanie": "Исключена из реестра"},
]

FEDERALNYE_OKRUGA = [
    {"kod": "cfo", "nazvanie": "Центральный федеральный округ"},
    {"kod": "szfo", "nazvanie": "Северо-Западный федеральный округ"},
    {"kod": "yuzfo", "nazvanie": "Южный федеральный округ"},
    {"kod": "skfo", "nazvanie": "Северо-Кавказский федеральный округ"},
    {"kod": "pfo", "nazvanie": "Приволжский федеральный округ"},
    {"kod": "urfo", "nazvanie": "Уральский федеральный округ"},
    {"kod": "sfo", "nazvanie": "Сибирский федеральный округ"},
    {"kod": "dvfo", "nazvanie": "Дальневосточный федеральный округ"},
]

VIDY_OBRAZOVATELNYH_ORGANIZATSYY = {
    "университет": "Университет",
    "академия": "Академия",
    "институт": "Институт",
    "филиал": "Филиал",
    "нии": "Научно-исследовательский институт",
}
