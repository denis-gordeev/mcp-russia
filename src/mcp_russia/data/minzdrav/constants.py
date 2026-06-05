"""Constants for the Минздрав РФ feature."""

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
    {"code": "life_expectancy", "name": "Ожидаемая продолжительность жизни"},
    {"code": "mortality", "name": "Общая смертность"},
    {"code": "infant_mortality", "name": "Младенческая смертность"},
    {"code": "morbidity", "name": "Общая заболеваемость"},
    {"code": "hospital_beds", "name": "Обеспеченность больничными койками"},
    {"code": "doctors", "name": "Обеспеченность врачами"},
]

# Типы медицинских организаций
TIPLY_MO = [
    {"code": "hospital", "name": "Больница (стационар)"},
    {"code": "polyclinic", "name": "Поликлиника (амбулатория)"},
    {"code": "dispensary", "name": "Диспансер"},
    {"code": "emergency", "name": "Станция скорой помощи"},
    {"code": "maternity", "name": "Родильный дом"},
    {"code": "hospice", "name": "Хоспис"},
    {"code": "sanatorium", "name": "Санаторий"},
    {"code": "fap", "name": "Фельдшерско-акушерский пункт"},
    {"code": "dkb", "name": "Детская городская больница"},
    {"code": "dgp", "name": "Детская городская поликлиника"},
    {"code": "nc", "name": "Научный центр"},
    {"code": "kdl", "name": "Клинико-диагностическая лаборатория"},
]

# Классы специальностей врачей
SPETSIALNOSTI_VRACHEY = [
    {"code": "therapist", "name": "Терапевт"},
    {"code": "surgeon", "name": "Хирург"},
    {"code": "pediatrician", "name": "Педиатр"},
    {"code": "neurologist", "name": "Невролог"},
    {"code": "cardiologist", "name": "Кардиолог"},
    {"code": "ophthalmologist", "name": "Офтальмолог"},
    {"code": "dentist", "name": "Стоматолог"},
    {"code": "gynecologist", "name": "Акушер-гинеколог"},
    {"code": "traumatologist", "name": "Травматолог-ортопед"},
    {"code": "anesthesiologist", "name": "Анестезиолог-реаниматолог"},
    {"code": "psychiatrist", "name": "Психиатр"},
    {"code": "dermatologist", "name": "Дерматовенеролог"},
    {"code": "endocrinologist", "name": "Эндокринолог"},
    {"code": "urologist", "name": "Уролог"},
    {"code": "oncologist", "name": "Онколог"},
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
