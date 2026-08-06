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

RAZDELY_BYUDZHETNOY_KLASSIFIKATSII = [
    {"kod": "0100", "nazvanie": "Общегосударственные вопросы"},
    {"kod": "0200", "nazvanie": "Национальная оборона"},
    {"kod": "0300", "nazvanie": "Национальная безопасность и правоохранительная деятельность"},
    {"kod": "0400", "nazvanie": "Национальная экономика"},
    {"kod": "0500", "nazvanie": "Жилищно-коммунальное хозяйство"},
    {"kod": "0600", "nazvanie": "Охрана окружающей среды"},
    {"kod": "0700", "nazvanie": "Образование"},
    {"kod": "0800", "nazvanie": "Культура и кинематография"},
    {"kod": "0900", "nazvanie": "Здравоохранение"},
    {"kod": "1000", "nazvanie": "Социальная политика"},
    {"kod": "1100", "nazvanie": "Физическая культура и спорт"},
    {"kod": "1200", "nazvanie": "Средства массовой информации"},
    {"kod": "1300", "nazvanie": "Обслуживание государственного и муниципального долга"},
    {"kod": "1400", "nazvanie": "Межбюджетные трансферты общего характера"},
]

PODRAZDELY_BYUDZHETNOY_KLASSIFIKATSII = [
    {"kod": "0101", "razdel": "0100", "nazvanie": "Функционирование Президента РФ"},
    {"kod": "0102", "razdel": "0100", "nazvanie": "Функционирование Федерального собрания"},
    {"kod": "0103", "razdel": "0100", "nazvanie": "Функционирование Правительства РФ"},
    {"kod": "0104", "razdel": "0100", "nazvanie": "Судебная система"},
    {
        "kod": "0105",
        "razdel": "0100",
        "nazvanie": "Обеспечение деятельности финансовых и налоговых органов",
    },
    {"kod": "0106", "razdel": "0100", "nazvanie": "Обеспечение деятельности органов прокуратуры"},
    {"kod": "0201", "razdel": "0200", "nazvanie": "Вооружённые силы РФ"},
    {"kod": "0202", "razdel": "0200", "nazvanie": "Модернизация Вооружённых сил РФ"},
    {"kod": "0203", "razdel": "0200", "nazvanie": "Мобилизационная подготовка экономики"},
    {"kod": "0301", "razdel": "0300", "nazvanie": "Органы внутренних дел"},
    {"kod": "0302", "razdel": "0300", "nazvanie": "Внутренние войска"},
    {"kod": "0303", "razdel": "0300", "nazvanie": "Органы уголовно-исполнительной системы"},
    {"kod": "0401", "razdel": "0400", "nazvanie": "Общеэкономические вопросы"},
    {"kod": "0402", "razdel": "0400", "nazvanie": "Топливно-энергетический комплекс"},
    {"kod": "0403", "razdel": "0400", "nazvanie": "Сельское хозяйство и рыболовство"},
    {"kod": "0404", "razdel": "0400", "nazvanie": "Водное хозяйство"},
    {"kod": "0405", "razdel": "0400", "nazvanie": "Связь и информатика"},
    {"kod": "0406", "razdel": "0400", "nazvanie": "Транспорт"},
    {"kod": "0407", "razdel": "0400", "nazvanie": "Дорожное хозяйство"},
    {"kod": "0701", "razdel": "0700", "nazvanie": "Дошкольное образование"},
    {"kod": "0702", "razdel": "0700", "nazvanie": "Общее образование"},
    {"kod": "0703", "razdel": "0700", "nazvanie": "Среднее профессиональное образование"},
    {"kod": "0704", "razdel": "0700", "nazvanie": "Высшее образование"},
    {"kod": "0705", "razdel": "0700", "nazvanie": "Молодёжная политика"},
    {"kod": "0901", "razdel": "0900", "nazvanie": "Медицинская помощь"},
    {"kod": "0902", "razdel": "0900", "nazvanie": "Санаторно-курортное дело"},
    {"kod": "0903", "razdel": "0900", "nazvanie": "Заготовка и переработка донорской крови"},
    {"kod": "0904", "razdel": "0900", "nazvanie": "Санитарно-эпидемиологическое благополучие"},
    {"kod": "1001", "razdel": "1000", "nazvanie": "Пенсионное обеспечение"},
    {"kod": "1002", "razdel": "1000", "nazvanie": "Социальное обслуживание населения"},
    {"kod": "1003", "razdel": "1000", "nazvanie": "Социальное обеспечение населения"},
    {"kod": "1004", "razdel": "1000", "nazvanie": "Охрана семьи и детства"},
]
