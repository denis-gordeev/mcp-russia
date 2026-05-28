"""Constants for the Минобрнауки feature."""

# Минобрнауки (Министерство науки и высшего образования РФ)
# Основные источники данных:
# 1. Официальный сайт: https://minobrnauki.gov.ru
# 2. Рейтинг вузов: https://vuz.minobrnauki.gov.ru
# 3. Гранты РНФ: https://rscf.ru
# 4. Гранты РФФИ: https://www.rfbr.ru
# 5. ЕГИСУ науки: https://esu.minobrnauki.gov.ru

MINOBRNAUKI_API_BASE = "https://minobrnauki.gov.ru"

TipyVUZov = [
    {"code": "universitet", "name": "Университет"},
    {"code": "akademiya", "name": "Академия"},
    {"code": "institut", "name": "Институт"},
    {"code": "filial", "name": "Филиал"},
    {"code": "nii", "name": "Научно-исследовательский институт"},
]

FormyObucheniya = [
    {"code": "ochnaya", "name": "Очная"},
    {"code": "ochno_zaochnaya", "name": "Очно-заочная (вечерняя)"},
    {"code": "zaochnaya", "name": "Заочная"},
    {"code": "distancionnaya", "name": "Дистанционная"},
]

UrovniObrazovaniya = [
    {"code": "bakalavriat", "name": "Бакалавриат"},
    {"code": "specialitet", "name": "Специалитет"},
    {"code": "magistratura", "name": "Магистратура"},
    {"code": "aspirantura", "name": "Аспирантура"},
    {"code": "doktorantura", "name": "Докторантура"},
    {"code": "srednee_prof", "name": "Среднее профессиональное"},
]

OtrasliNauki = [
    {"code": "estestvennye", "name": "Естественные науки"},
    {"code": "tehnicheskie", "name": "Технические науки"},
    {"code": "medicinskie", "name": "Медицинские науки"},
    {"code": "selskohozyaystvennye", "name": "Сельскохозяйственные науки"},
    {"code": "obschestvennye", "name": "Общественные науки"},
    {"code": "gumanitarnye", "name": "Гуманитарные науки"},
    {"code": "pedagogicheskie", "name": "Педагогические науки"},
]

TipyGrantov = [
    {"code": "rnf", "name": "Гранты РНФ (Российский научный фонд)"},
    {"code": "rffi", "name": "Гранты РФФИ (Российский фонд фундаментальных исследований)"},
    {"code": "prezident", "name": "Гранты Президента РФ"},
    {"code": "minobrnauki_goszadanie", "name": "Государственное задание Минобрнауки"},
    {"code": "fund_potanina", "name": "Фонд Потанина"},
    {"code": "fund_skolkovo", "name": "Фонд «Сколково»"},
]

StatusyAkkreditatsii = [
    {"code": "deystvuet", "name": "Действует"},
    {"code": "priznak_ostanovki", "name": "Приостановлена"},
    {"code": "otmenena", "name": "Отменена"},
    {"code": "isklyuchena", "name": "Исключена из реестра"},
]

FederalnyeOkruga = [
    {"code": "cfo", "name": "Центральный федеральный округ"},
    {"code": "szfo", "name": "Северо-Западный федеральный округ"},
    {"code": "yuzfo", "name": "Южный федеральный округ"},
    {"code": "pfo", "name": "Приволжский федеральный округ"},
    {"code": "urfo", "name": "Уральский федеральный округ"},
    {"code": "sfo", "name": "Сибирский федеральный округ"},
    {"code": "dvfo", "name": "Дальневосточный федеральный округ"},
]
