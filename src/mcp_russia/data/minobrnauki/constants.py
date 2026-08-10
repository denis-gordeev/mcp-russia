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
    {"kod": "distantsionnaya", "nazvanie": "Дистанционная"},
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
    {"kod": "ЦФО", "nazvanie": "Центральный федеральный округ"},
    {"kod": "СЗФО", "nazvanie": "Северо-Западный федеральный округ"},
    {"kod": "ЮФО", "nazvanie": "Южный федеральный округ"},
    {"kod": "СКФО", "nazvanie": "Северо-Кавказский федеральный округ"},
    {"kod": "ПФО", "nazvanie": "Приволжский федеральный округ"},
    {"kod": "УФО", "nazvanie": "Уральский федеральный округ"},
    {"kod": "СФО", "nazvanie": "Сибирский федеральный округ"},
    {"kod": "ДФО", "nazvanie": "Дальневосточный федеральный округ"},
]

VIDY_OBRAZOVATELNYH_ORGANIZATSYY = {
    "университет": "Университет",
    "академия": "Академия",
    "институт": "Институт",
    "филиал": "Филиал",
    "нии": "Научно-исследовательский институт",
}

OBRNADZOR_KONTROL_ADRES = f"{OBRNADZOR_API_BAZA}/opendata/7701537808-statctrl/data-20240901.json"
OBRNADZOR_PROVERKI_ADRES = f"{OBRNADZOR_API_BAZA}/opendata/7701537808-ronchecks/data-20240901.json"
OBRNADZOR_EKSPERTY_ADRES = f"{OBRNADZOR_API_BAZA}/opendata/7701537808-akexperts/data-20240901.json"

VUZY_ZAPRET_PRIEMA = [
    {
        "nazvanie": "Московский университет имени С.Ю. Витте",
        "inn": "7717563274",
        "prichina": "Приказ Рособрнадзора от 28.02.2024",
    },
    {
        "nazvanie": "Московский финансово-промышленный университет «Синергия»",
        "inn": "7710142601",
        "prichina": "Приказ Рособрнадзора от 24.01.2024",
    },
    {
        "nazvanie": "Институт мировых цивилизаций",
        "inn": "7710356967",
        "prichina": "Приказ Рособрнадзора от 15.03.2024",
    },
]
