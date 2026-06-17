"""Константы модуля Минздрава РФ."""

# Министерство здравоохранения Российской Федерации
# Основные источники данных:
# 1. Открытые данные Минздрава: https://data.minzdrav.gov.ru
# 2. Росздравнадзор: https://roszdravnadzor.gov.ru
# 3. ФРМО (Федеральный реестр медицинских организаций)
# 4. Официальный сайт: https://minzdrav.gov.ru

MINZDRAV_OPEN_DATA = "https://data.minzdrav.gov.ru/api/v1"
ROSZDRAVNADZOR_API = "https://roszdravnadzor.gov.ru/api"
FRMO_API_BASE = "https://frrr.rosminzdrav.ru/api"

# Основные показатели здоровья
POKAZATELI_ZDOROVYA = [
    {"code": "prodolzhitelnost_zhizni", "name": "Ожидаемая продолжительность жизни"},
    {"code": "smertnost", "name": "Общая смертность"},
    {"code": "mladencheskaya_smertnost", "name": "Младенческая смертность"},
    {"code": "zabolevaemost", "name": "Общая заболеваемость"},
    {"code": "bolnichnye_koyki", "name": "Обеспеченность больничными койками"},
    {"code": "vrachi", "name": "Обеспеченность врачами"},
]

# Типы медицинских организаций
TIPLY_MO = [
    {"code": "bolnitsa", "name": "Больница (стационар)"},
    {"code": "poliklinika", "name": "Поликлиника (амбулатория)"},
    {"code": "dispanser", "name": "Диспансер"},
    {"code": "skoraya_pomoshch", "name": "Станция скорой помощи"},
    {"code": "roddom", "name": "Родильный дом"},
    {"code": "khospis", "name": "Хоспис"},
    {"code": "sanatoriy", "name": "Санаторий"},
    {"code": "fap", "name": "Фельдшерско-акушерский пункт"},
    {"code": "dkb", "name": "Детская городская больница"},
    {"code": "dgp", "name": "Детская городская поликлиника"},
    {"code": "nt", "name": "Научный центр"},
    {"code": "kdl", "name": "Клинико-диагностическая лаборатория"},
]

# Классы специальностей врачей
SPETSIALNOSTI_VRACHEY = [
    {"code": "terapevt", "name": "Терапевт"},
    {"code": "khirurg", "name": "Хирург"},
    {"code": "pediatr", "name": "Педиатр"},
    {"code": "nevropatolog", "name": "Невролог"},
    {"code": "kardiolog", "name": "Кардиолог"},
    {"code": "oftalmolog", "name": "Офтальмолог"},
    {"code": "stomatolog", "name": "Стоматолог"},
    {"code": "akusher_ginekolog", "name": "Акушер-гинеколог"},
    {"code": "travmatolog", "name": "Травматолог-ортопед"},
    {"code": "anesteziolog", "name": "Анестезиолог-реаниматолог"},
    {"code": "psikhiatr", "name": "Психиатр"},
    {"code": "dermatovenerolog", "name": "Дерматовенеролог"},
    {"code": "endokrinolog", "name": "Эндокринолог"},
    {"code": "urolog", "name": "Уролог"},
    {"code": "onkolog", "name": "Онколог"},
]

# Классы МКБ-10 (основные)
MKB10_CLASSES = [
    {"code": "A00-B99", "name": "Инфекционные и паразитарные болезни"},
    {"code": "C00-D48", "name": "Новообразования"},
    {"code": "E00-E90", "name": "Болезни эндокринной системы"},
    {"code": "F00-F99", "name": "Психические расстройства"},
    {"code": "I00-I99", "name": "Болезни системы кровообращения"},
    {"code": "J00-J99", "name": "Болезни органов дыхания"},
    {"code": "K00-K93", "name": "Болезни органов пищеварения"},
    {"code": "S00-T98", "name": "Травмы и отравления"},
    {"code": "M00-M99", "name": "Болезни костно-мышечной системы"},
    {"code": "N00-N99", "name": "Болезни мочеполовой системы"},
]

# Федеральные округа
FEDERALNYE_OKRUGA = [
    {"code": "CFD", "name": "Центральный федеральный округ"},
    {"code": "SZFD", "name": "Северо-Западный федеральный округ"},
    {"code": "YuFD", "name": "Южный федеральный округ"},
    {"code": "SKFD", "name": "Северо-Кавказский федеральный округ"},
    {"code": "PFD", "name": "Приволжский федеральный округ"},
    {"code": "UFD", "name": "Уральский федеральный округ"},
    {"code": "SFD", "name": "Сибирский федеральный округ"},
    {"code": "DFD", "name": "Дальневосточный федеральный округ"},
]

# Виды лицензируемой деятельности
VIDY_LITSENZIRUEMOY_DEYATELNOSTI = [
    {"code": "med", "name": "Медицинская деятельность"},
    {"code": "pharma", "name": "Фармацевтическая деятельность"},
    {"code": "radio", "name": "Деятельность, связанная с источниками ионизирующего излучения"},
]
