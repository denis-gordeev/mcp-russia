"""Константы модуля Ростехнадзора."""

ROSTEKHNADZOR_BAZA = "https://rostechnadzor.gov.ru"
ROSTEKHNADZOR_OTKRYTYE_DANNYE = f"{ROSTEKHNADZOR_BAZA}/opendata"
DATA_GOV_RU_RT = "https://data.gov.ru/opendata/7710543274"

VIDY_NADZORA = [
    {"kod": "promyshlennyy", "nazvanie": "Промышленная безопасность"},
    {"kod": "atomnyy", "nazvanie": "Атомный надзор"},
    {"kod": "ekologicheskiy", "nazvanie": "Экологический надзор"},
    {"kod": "gornyy", "nazvanie": "Горный надзор"},
    {"kod": "stroitelnaya", "nazvanie": "Строительный надзор"},
    {"kod": "pozharnaya", "nazvanie": "Пожарный надзор"},
]

KLASSY_OPASNOSTI = [
    {"kod": "i_klass", "nazvanie": "I класс — особо опасные"},
    {"kod": "ii_klass", "nazvanie": "II класс — высокоопасные"},
    {"kod": "iii_klass", "nazvanie": "III класс — умеренно опасные"},
    {"kod": "iv_klass", "nazvanie": "IV класс — малоопасные"},
]

VIDY_LITSENZIY = [
    {"kod": "ekspluatatsiya", "nazvanie": "Эксплуатация опасных производственных объектов"},
    {"kod": "proektirovanie", "nazvanie": "Проектирование ОПО"},
    {"kod": "stroitelstvo", "nazvanie": "Строительство ОПО"},
    {"kod": "rasshirenie", "nazvanie": "Расширение ОПО"},
    {"kod": "tekhnicheskoe_perevooruzhenie", "nazvanie": "Техническое перевооружение ОПО"},
    {"kod": "konservatsiya", "nazvanie": "Консервация ОПО"},
    {"kod": "likvidatsiya", "nazvanie": "Ликвидация ОПО"},
    {"kod": "yadernye_materialy", "nazvanie": "Обращение с ядерными материалами"},
    {"kod": "radioaktivnye_otkhody", "nazvanie": "Обращение с радиоактивными отходами"},
]

VIDY_INTSIDENTOV = [
    {"kod": "avariya", "nazvanie": "Авария"},
    {"kod": "intsident", "nazvanie": "Инцидент"},
    {"kod": "pozhar", "nazvanie": "Пожар"},
    {"kod": "vzryv", "nazvanie": "Взрыв"},
    {"kod": "vybroz", "nazvanie": "Выброс опасных веществ"},
    {"kod": "oblava", "nazvanie": "Облако опасных веществ"},
]

FEDERALNYE_OKRUGA = [
    {"kod": "ЦФО", "nazvanie": "Центральный"},
    {"kod": "СЗФО", "nazvanie": "Северо-Западный"},
    {"kod": "ЮФО", "nazvanie": "Южный"},
    {"kod": "ПФО", "nazvanie": "Приволжский"},
    {"kod": "УФО", "nazvanie": "Уральский"},
    {"kod": "СФО", "nazvanie": "Сибирский"},
    {"kod": "ДФО", "nazvanie": "Дальневосточный"},
    {"kod": "СКФО", "nazvanie": "Северо-Кавказский"},
]

STATISTIKA_PROMBEZ_2024 = {
    "vsego_avariy": 28,
    "vsego_intsidentov": 840,
    "pogibshikh_pri_avariyakh": 15,
    "postradavshikh_pri_avariyakh": 42,
    "zaregistrirovano_opo": 218000,
    "vydano_litsenziy": 12400,
    "provedeno_proverok": 38000,
    "po_vidu_nadzora": {
        "promyshlennyy": {"avariy": 18, "intsidentov": 520, "proverok": 22000},
        "atomnyy": {"avariy": 0, "intsidentov": 12, "proverok": 4500},
        "gornyy": {"avariy": 7, "intsidentov": 180, "proverok": 8200},
        "ekologicheskiy": {"avariy": 3, "intsidentov": 128, "proverok": 3300},
    },
}
