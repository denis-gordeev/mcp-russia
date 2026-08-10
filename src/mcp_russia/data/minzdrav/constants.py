"""Константы модуля Минздрава РФ."""

# Министерство здравоохранения Российской Федерации
# Основные источники данных:
# 1. Открытые данные Минздрава: https://data.minzdrav.gov.ru
# 2. Росздравнадзор: https://roszdravnadzor.gov.ru
# 3. ФРМО (Федеральный реестр медицинских организаций)
# 4. Официальный сайт: https://minzdrav.gov.ru

MINZDRAV_OTKRYTYE_DANNYE = "https://data.minzdrav.gov.ru/api/v1"
ROSZDRAVNADZOR_API = "https://roszdravnadzor.gov.ru/api"
FRMO_API_BAZA = "https://frrr.rosminzdrav.ru/api"

# Основные показатели здоровья
POKAZATELI_ZDOROVYA = [
    {"kod": "prodolzhitelnost_zhizni", "nazvanie": "Ожидаемая продолжительность жизни"},
    {"kod": "smertnost", "nazvanie": "Общая смертность"},
    {"kod": "mladencheskaya_smertnost", "nazvanie": "Младенческая смертность"},
    {"kod": "zabolevaemost", "nazvanie": "Общая заболеваемость"},
    {"kod": "bolnichnye_koyki", "nazvanie": "Обеспеченность больничными койками"},
    {"kod": "vrachi", "nazvanie": "Обеспеченность врачами"},
]

# Типы медицинских организаций
TIPLY_MO = [
    {"kod": "bolnitsa", "nazvanie": "Больница (стационар)"},
    {"kod": "poliklinika", "nazvanie": "Поликлиника (амбулатория)"},
    {"kod": "dispanser", "nazvanie": "Диспансер"},
    {"kod": "skoraya_pomoshch", "nazvanie": "Станция скорой помощи"},
    {"kod": "roddom", "nazvanie": "Родильный дом"},
    {"kod": "khospis", "nazvanie": "Хоспис"},
    {"kod": "sanatoriy", "nazvanie": "Санаторий"},
    {"kod": "fap", "nazvanie": "Фельдшерско-акушерский пункт"},
    {"kod": "dkb", "nazvanie": "Детская городская больница"},
    {"kod": "dgp", "nazvanie": "Детская городская поликлиника"},
    {"kod": "nt", "nazvanie": "Научный центр"},
    {"kod": "kdl", "nazvanie": "Клинико-диагностическая лаборатория"},
]

# Классы специальностей врачей
SPETSIALNOSTI_VRACHEY = [
    {"kod": "terapevt", "nazvanie": "Терапевт"},
    {"kod": "khirurg", "nazvanie": "Хирург"},
    {"kod": "pediatr", "nazvanie": "Педиатр"},
    {"kod": "nevropatolog", "nazvanie": "Невролог"},
    {"kod": "kardiolog", "nazvanie": "Кардиолог"},
    {"kod": "oftalmolog", "nazvanie": "Офтальмолог"},
    {"kod": "stomatolog", "nazvanie": "Стоматолог"},
    {"kod": "akusher_ginekolog", "nazvanie": "Акушер-гинеколог"},
    {"kod": "travmatolog", "nazvanie": "Травматолог-ортопед"},
    {"kod": "anesteziolog", "nazvanie": "Анестезиолог-реаниматолог"},
    {"kod": "psikhiatr", "nazvanie": "Психиатр"},
    {"kod": "dermatovenerolog", "nazvanie": "Дерматовенеролог"},
    {"kod": "endokrinolog", "nazvanie": "Эндокринолог"},
    {"kod": "urolog", "nazvanie": "Уролог"},
    {"kod": "onkolog", "nazvanie": "Онколог"},
]

# Классы МКБ-10 (основные)
MKB10_KLASSY = [
    {"kod": "A00-B99", "nazvanie": "Инфекционные и паразитарные болезни"},
    {"kod": "C00-D48", "nazvanie": "Новообразования"},
    {"kod": "E00-E90", "nazvanie": "Болезни эндокринной системы"},
    {"kod": "F00-F99", "nazvanie": "Психические расстройства"},
    {"kod": "I00-I99", "nazvanie": "Болезни системы кровообращения"},
    {"kod": "J00-J99", "nazvanie": "Болезни органов дыхания"},
    {"kod": "K00-K93", "nazvanie": "Болезни органов пищеварения"},
    {"kod": "S00-T98", "nazvanie": "Травмы и отравления"},
    {"kod": "M00-M99", "nazvanie": "Болезни костно-мышечной системы"},
    {"kod": "N00-N99", "nazvanie": "Болезни мочеполовой системы"},
]

# Федеральные округа
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

# Виды лицензируемой деятельности
VIDY_LITSENZIRUEMOY_DEYATELNOSTI = [
    {"kod": "med", "nazvanie": "Медицинская деятельность"},
    {"kod": "farmatsevticheskaya", "nazvanie": "Фармацевтическая деятельность"},
    {
        "kod": "radiatsionnaya",
        "nazvanie": "Деятельность, связанная с источниками ионизирующего излучения",
    },
]
