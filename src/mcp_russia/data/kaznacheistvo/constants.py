"""Constants for the Федеральное казначейство feature."""

KAZNACHEISTVO_API_BASE = "https://roskazna.gov.ru/api"
KAZNACHEISTVO_BASE = "https://roskazna.gov.ru"
ROSKAZNA_OPENDATA_BASE = "https://roskazna.gov.ru/opendata"
BUDGET_GOV_RU_BASE = "https://budget.gov.ru/api"

VIDY_BUDZHETOV = [
    {"code": "federalnyy", "name": "Федеральный бюджет"},
    {"code": "subiekta_rf", "name": "Бюджет субъекта РФ"},
    {"code": "mestnyy", "name": "Местный бюджет"},
    {"code": "byudzhet_gf", "name": "Бюджет государственного внебюджетного фонда"},
    {"code": "byudzhet_tf", "name": "Бюджет территориального внебюджетного фонда"},
    {"code": "svodnyy", "name": "Сводный бюджет"},
]

UROVNI_BUDZHETOV = [
    {"code": "federalnyy", "name": "Федеральный уровень"},
    {"code": "regionalnyy", "name": "Региональный уровень"},
    {"code": "municipalnyy", "name": "Муниципальный уровень"},
]

KATEGORII_RASKHODOV = [
    {"code": "obshhegosudarstvennye", "name": "Общегосударственные вопросы"},
    {"code": "nacionalnaya_oborona", "name": "Национальная оборона"},
    {
        "code": "nacionalnaya_bezopasnost",
        "name": "Национальная безопасность и правоохранительная деятельность",
    },
    {"code": "nacionalnaya_ekonomika", "name": "Национальная экономика"},
    {"code": "zhkkh", "name": "Жилищно-коммунальное хозяйство"},
    {"code": "ohrana_okruzhayushhej_sredy", "name": "Охрана окружающей среды"},
    {"code": "obrazovanie", "name": "Образование"},
    {"code": "kulutura", "name": "Культура и кинематография"},
    {"code": "zdravoohranenie", "name": "Здравоохранение"},
    {"code": "socialnaya_politika", "name": "Социальная политика"},
    {"code": "fizicheskaya_kultura", "name": "Физическая культура и спорт"},
    {"code": "smi", "name": "Средства массовой информации"},
    {
        "code": "obsluzhivanie_dolga",
        "name": "Обслуживание государственного и муниципального долга",
    },
    {"code": "mezhdunarodnaya_deyatelnost", "name": "Международная деятельность"},
    {"code": "uslugi_obshhego_haraktera", "name": "Услуги общего характера"},
]

STATUSY_ISPOLNENIYA = {
    "approved": "Утверждён",
    "in_execution": "Исполняется",
    "completed": "Исполнен",
    "revised": "Скорректирован",
    "preliminary": "Предварительный",
}
