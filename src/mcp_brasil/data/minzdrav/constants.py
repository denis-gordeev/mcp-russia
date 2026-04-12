"""Constants for the MinZdrav (Минздрав РФ) feature."""

# API Минздрава и медицинских источников
MINZDRAV_API_BASE = "https://minzdrav.gov.ru"
MINZDRAV_OPEN_DATA = "https://data.minzdrav.gov.ru"
ROSZDRAVNADZOR_API = "https://roszdravnadzor.gov.ru"

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
