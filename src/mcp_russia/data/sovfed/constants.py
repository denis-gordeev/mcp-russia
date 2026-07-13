"""Константы модуля Совета Федерации РФ."""

# Совет Федерации Федерального Собрания Российской Федерации
# Основные источники данных:
# 1. Официальный сайт: https://sovfed.ru
# 2. Открытые данные: https://data.gov.ru/organizations/sovet_federatsii
# 3. Сенаторы: https://sovfed.ru/senators
# 4. Комитеты: https://sovfed.ru/committees
# 5. Законопроекты: https://sovfed.ru/bills
# 6. Заседания: https://sovfed.ru/sessions

SOVFED_BAZA_API = "https://sovfed.ru/api"
SOVFED_BAZA = "https://sovfed.ru"
DANNYE_GOV_RU_SOVFED = "https://data.gov.ru/api/dataset"
DANNYE_GOV_RU_BAZA = "https://data.gov.ru"

KOMITETY_SOVFEDA = [
    {
        "kod": "konst_zakon",
        "nazvanie": "Конституционное законодательство и государственное строительство",
    },
    {"kod": "oborona", "nazvanie": "Оборона и безопасность"},
    {"kod": "byudzhet", "nazvanie": "Бюджет и финансовые рынки"},
    {"kod": "ekonom_politika", "nazvanie": "Экономическая политика"},
    {"kod": "sotc_politika", "nazvanie": "Социальная политика"},
    {"kod": "agrarno_pish", "nazvanie": "Аграрно-продовольственная политика"},
    {"kod": "nauka", "nazvanie": "Наука, образование и культура"},
    {"kod": "mezhdunarodnye", "nazvanie": "Международные дела"},
    {
        "kod": "federalnoe",
        "nazvanie": "Федеративное устройство, региональная политика и местное самоуправление",
    },
    {"kod": "reglament", "nazvanie": "Регламент и организация парламентской деятельности"},
    {"kod": "pravovye", "nazvanie": "Правовые вопросы"},
    {"kod": "soprav_trud", "nazvanie": "Совместное ведение и социальная защита"},
    {"kod": "ekologiya", "nazvanie": "Природная среда и экология"},
    {"kod": "promyshlennost", "nazvanie": "Промышленная политика и предпринимательство"},
    {"kod": "transport", "nazvanie": "Транспорт и связь"},
    {"kod": "oborona_prav", "nazvanie": "Защита прав человека и гражданина"},
]

KOMISSII_SOVFEDA = [
    {
        "kod": "reglament",
        "nazvanie": "Комиссия по Регламенту и организации парламентской деятельности",
    },
    {"kod": "etika", "nazvanie": "Комиссия по этике"},
    {"kod": "schetnaya_palata", "nazvanie": "Комиссия по взаимодействию со Счётной палатой РФ"},
    {"kod": "prirodnye_resursy", "nazvanie": "Комиссия по использованию природных ресурсов"},
    {"kod": "nats_bezopasnost", "nazvanie": "Комиссия по национальной морской политике"},
    {"kod": "inform_politika", "nazvanie": "Комиссия по информационной политике"},
    {"kod": "molodezh", "nazvanie": "Комиссия Совета Федерации по делам молодёжи и туризму"},
]

STATUSY_ZAKONOPROEKTA = {
    "na_rassmotrenii": "На рассмотрении",
    "odobren": "Одобрен",
    "otklonen": "Отклонён",
    "dorabotka": "Доработка",
    "v_komitete": "В комитете",
    "na_zasedanii": "На заседании",
    "prinyat": "Принят",
}

DOLZHNOSTI_SENATORA = [
    {
        "kod": "predstavitel_exec",
        "nazvanie": "Представитель от исполнительного органа государственной власти субъекта РФ",
    },
    {
        "kod": "predstavitel_zakon",
        "nazvanie": "Представитель от законодательного органа государственной власти субъекта РФ",
    },
    {"kod": "predsedatel_sf", "nazvanie": "Председатель Совета Федерации"},
    {"kod": "zam_predsedatelya", "nazvanie": "Заместитель Председателя Совета Федерации"},
    {"kod": "predsedatel_komiteta", "nazvanie": "Председатель комитета"},
    {"kod": "zam_predsedatelya_komiteta", "nazvanie": "Заместитель председателя комитета"},
    {"kod": "senator_rf", "nazvanie": "Сенатор Российской Федерации"},
]

SENATORY_SPRAVOCHNIK = [
    {
        "familiya": "Матвиенко",
        "imya": "Валентина",
        "otchestvo": "Ивановна",
        "subiekt": "г. Санкт-Петербург",
        "dolzhnost": "Председатель Совета Федерации",
        "komitet": "",
    },
]
