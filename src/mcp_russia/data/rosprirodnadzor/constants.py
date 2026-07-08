"""Константы модуля Росприроднадзора."""

ROSPRIRODNADZOR_BAZA_API = "https://rpn.gov.ru/api"
ROSPRIRODNADZOR_BAZA = "https://rpn.gov.ru"
ROSPRIRODNADZOR_BAZA_OTKRYTYKH_DANNYKH = "https://rpn.gov.ru/opendata"
ONV_REESTR_BAZA = "https://onv.register.rpn.gov.ru/api"
GOSUSLUGI_EKO_BAZA = "https://gosuslugi.ru/api/eco"

VIDY_NADZORA = [
    {
        "kod": "ekologicheskiy",
        "nazvanie": "Государственный экологический надзор",
    },
    {
        "kod": "zemelnyy",
        "nazvanie": "Государственный земельный надзор",
    },
    {
        "kod": "geologicheskiy",
        "nazvanie": "Государственный надзор за геологическим изучением",
    },
    {
        "kod": "rybolovstvo",
        "nazvanie": "Государственный контроль и надзор в сфере рыболовства",
    },
    {
        "kod": "radiacionnyy",
        "nazvanie": "Радиационный контроль",
    },
]

KATEGORII_OBNV = [
    {"kod": "I", "nazvanie": "I — значительное негативное воздействие"},
    {"kod": "II", "nazvanie": "II — умеренное негативное воздействие"},
    {"kod": "III", "nazvanie": "III — незначительное негативное воздействие"},
    {"kod": "IV", "nazvanie": "IV — минимальное негативное воздействие"},
]

VIDY_LITSENZIY_NEDRA = [
    {"kod": "dobycha", "nazvanie": "Добыча полезных ископаемых"},
    {"kod": "geologicheskoe", "nazvanie": "Геологическое изучение"},
    {"kod": "razvedka_dobycha", "nazvanie": "Разведка и добыча"},
    {
        "kod": "podzemnye_soouruzheniya",
        "nazvanie": "Строительство и эксплуатация подземных сооружений",
    },
]

STATUSY_PROVEROK = {
    "zaplanirovana": "Запланирована",
    "provoditsya": "Проводится",
    "zavershena": "Завершена",
    "otmenena": "Отменена",
    "narusheniya_vyyavleny": "Выявлены нарушения",
    "narusheniy_net": "Нарушений не выявлено",
}

TIPY_NARUSHENIY_EKO = {
    "atmosfernyy_vozdukh": "Нарушение требований охраны атмосферного воздуха",
    "vodnoe": "Нарушение водного законодательства",
    "pochvy": "Нарушение требований охраны почв",
    "otkhody": "Нарушение требований в области обращения с отходами",
    "nedropolzovanie": "Нарушение требований недропользования",
    "radiatsionnaya_bezopasnost": "Нарушение требований радиационной безопасности",
    "zemelnoe": "Нарушение земельного законодательства",
    "zhivotnyy_mir": "Нарушение в области охраны объектов животного мира",
}
