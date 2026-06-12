"""Константы модуля Совета Федерации РФ."""

# Совет Федерации Федерального Собрания Российской Федерации
# Основные источники данных:
# 1. Официальный сайт: https://sovfed.ru
# 2. Открытые данные: https://data.gov.ru/organizations/sovet_federatsii
# 3. Сенаторы: https://sovfed.ru/senators
# 4. Комитеты: https://sovfed.ru/committees
# 5. Законопроекты: https://sovfed.ru/bills
# 6. Заседания: https://sovfed.ru/sessions

SOVFED_API_BASE = "https://sovfed.ru/api"
SOVFED_BASE = "https://sovfed.ru"
DATA_GOV_RU_SOVFED = "https://data.gov.ru/api/dataset"
DATA_GOV_RU_BASE = "https://data.gov.ru"

KOMITETY_SOVFEDA = [
    {
        "code": "konst_zakon",
        "name": "Конституционное законодательство и государственное строительство",
    },
    {"code": "oborona", "name": "Оборона и безопасность"},
    {"code": "byudzhet", "name": "Бюджет и финансовые рынки"},
    {"code": "ekonom_politika", "name": "Экономическая политика"},
    {"code": "sotc_politika", "name": "Социальная политика"},
    {"code": "agrarno_pish", "name": "Аграрно-продовольственная политика"},
    {"code": "nauka", "name": "Наука, образование и культура"},
    {"code": "mezhdunarodnye", "name": "Международные дела"},
    {
        "code": "federalnoe",
        "name": "Федеративное устройство, региональная политика и местное самоуправление",
    },
    {"code": "reglament", "name": "Регламент и организация парламентской деятельности"},
    {"code": "pravovye", "name": "Правовые вопросы"},
    {"code": "soprav_trud", "name": "Совместное ведение и социальная защита"},
    {"code": "ekologiya", "name": "Природная среда и экология"},
    {"code": "promyshlennost", "name": "Промышленная политика и предпринимательство"},
    {"code": "transport", "name": "Транспорт и связь"},
    {"code": "oborona_prav", "name": "Защита прав человека и гражданина"},
]

KOMISSII_SOVFEDA = [
    {
        "code": "reglament",
        "name": "Комиссия по Регламенту и организации парламентской деятельности",
    },
    {"code": "etika", "name": "Комиссия по этике"},
    {"code": "schetnaya_palata", "name": "Комиссия по взаимодействию со Счётной палатой РФ"},
    {"code": "prirodnye_resursy", "name": "Комиссия по использованию природных ресурсов"},
    {"code": "nats_bezopasnost", "name": "Комиссия по национальной морской политике"},
    {"code": "inform_politika", "name": "Комиссия по информационной политике"},
    {"code": "molodezh", "name": "Комиссия Совета Федерации по делам молодёжи и туризму"},
]

STATUSY_ZAKONOPROEKTA = {
    "pending": "На рассмотрении",
    "approved": "Одобрен",
    "rejected": "Отклонён",
    "revision": "Доработка",
    "committee": "В комитете",
    "session": "На заседании",
    "enacted": "Принят",
}

DOLZHNOSTI_SENATORA = [
    {
        "code": "predstavitel_exec",
        "name": "Представитель от исполнительного органа государственной власти субъекта РФ",
    },
    {
        "code": "predstavitel_zakon",
        "name": "Представитель от законодательного органа государственной власти субъекта РФ",
    },
    {"code": "predsedatel_sf", "name": "Председатель Совета Федерации"},
    {"code": "zam_predsedatelya", "name": "Заместитель Председателя Совета Федерации"},
    {"code": "predsedatel_komiteta", "name": "Председатель комитета"},
    {"code": "zam_predsedatelya_komiteta", "name": "Заместитель председателя комитета"},
    {"code": "senator_rf", "name": "Сенатор Российской Федерации"},
]

SENATORY_SPRAVOCHNIK = [
    {
        "familiya": "Матвиенко",
        "imya": "Валентина",
        "otchestvo": "Ивановна",
        "region": "г. Санкт-Петербург",
        "dolzhnost": "Председатель Совета Федерации",
        "komitet": "",
    },
]
