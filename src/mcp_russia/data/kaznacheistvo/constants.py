"""Константы модуля Федерального казначейства."""

KAZNACHEISTVO_API_BASE = "https://roskazna.gov.ru/api"
KAZNACHEISTVO_BASE = "https://roskazna.gov.ru"
ROSKAZNA_OPENDATA_BASE = "https://roskazna.gov.ru/opendata"
BUDGET_GOV_RU_BASE = "https://budget.gov.ru/api"

VIDY_BUDZHETOV = [
    {"kod": "federalnyy", "nazvanie": "Федеральный бюджет"},
    {"kod": "subiekta_rf", "nazvanie": "Бюджет субъекта РФ"},
    {"kod": "mestnyy", "nazvanie": "Местный бюджет"},
    {"kod": "byudzhet_gf", "nazvanie": "Бюджет государственного внебюджетного фонда"},
    {"kod": "byudzhet_tf", "nazvanie": "Бюджет территориального внебюджетного фонда"},
    {"kod": "svodnyy", "nazvanie": "Сводный бюджет"},
]

UROVNI_BUDZHETOV = [
    {"kod": "federalnyy", "nazvanie": "Федеральный уровень"},
    {"kod": "regionalnyy", "nazvanie": "Региональный уровень"},
    {"kod": "municipalnyy", "nazvanie": "Муниципальный уровень"},
]

KATEGORII_RASKHODOV = [
    {"kod": "obshhegosudarstvennye", "nazvanie": "Общегосударственные вопросы"},
    {"kod": "nacionalnaya_oborona", "nazvanie": "Национальная оборона"},
    {
        "kod": "nacionalnaya_bezopasnost",
        "nazvanie": "Национальная безопасность и правоохранительная деятельность",
    },
    {"kod": "nacionalnaya_ekonomika", "nazvanie": "Национальная экономика"},
    {"kod": "zhkkh", "nazvanie": "Жилищно-коммунальное хозяйство"},
    {"kod": "ohrana_okruzhayushhej_sredy", "nazvanie": "Охрана окружающей среды"},
    {"kod": "obrazovanie", "nazvanie": "Образование"},
    {"kod": "kulutura", "nazvanie": "Культура и кинематография"},
    {"kod": "zdravoohranenie", "nazvanie": "Здравоохранение"},
    {"kod": "socialnaya_politika", "nazvanie": "Социальная политика"},
    {"kod": "fizicheskaya_kultura", "nazvanie": "Физическая культура и спорт"},
    {"kod": "smi", "nazvanie": "Средства массовой информации"},
    {
        "kod": "obsluzhivanie_dolga",
        "nazvanie": "Обслуживание государственного и муниципального долга",
    },
    {"kod": "mezhdunarodnaya_deyatelnost", "nazvanie": "Международная деятельность"},
    {"kod": "uslugi_obshhego_haraktera", "nazvanie": "Услуги общего характера"},
]

STATUSY_ISPOLNENIYA = {
    "utverzhdyon": "Утверждён",
    "ispolnyaetsya": "Исполняется",
    "ispolnen": "Исполнен",
    "skorrektirovan": "Скорректирован",
    "predvaritelnyy": "Предварительный",
}
