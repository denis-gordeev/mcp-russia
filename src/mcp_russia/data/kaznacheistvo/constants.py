"""Константы модуля Федерального казначейства."""

KAZNACHEISTVO_BAZA_API = "https://roskazna.gov.ru/api"
KAZNACHEISTVO_BAZA = "https://roskazna.gov.ru"
ROSKAZNA_BAZA_OTKRYTYKH_DANNYKH = "https://roskazna.gov.ru/opendata"
BYUDZHET_GOV_RU_BAZA = "https://budget.gov.ru/api"

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
    {"kod": "obshchegosudarstvennye", "nazvanie": "Общегосударственные вопросы"},
    {"kod": "natsionalnaya_oborona", "nazvanie": "Национальная оборона"},
    {
        "kod": "natsionalnaya_bezopasnost",
        "nazvanie": "Национальная безопасность и правоохранительная деятельность",
    },
    {"kod": "natsionalnaya_ekonomika", "nazvanie": "Национальная экономика"},
    {"kod": "zhkkh", "nazvanie": "Жилищно-коммунальное хозяйство"},
    {"kod": "okhrana_okruzhayushchey_sredy", "nazvanie": "Охрана окружающей среды"},
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
    {"kod": "uslugi_obshchego_kharaktera", "nazvanie": "Услуги общего характера"},
]

STATUSY_ISPOLNENIYA = {
    "utverzhdyon": "Утверждён",
    "ispolnyaetsya": "Исполняется",
    "ispolnen": "Исполнен",
    "skorrektirovan": "Скорректирован",
    "predvaritelnyy": "Предварительный",
}
