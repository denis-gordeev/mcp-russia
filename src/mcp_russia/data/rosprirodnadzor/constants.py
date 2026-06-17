"""Константы модуля Росприроднадзора."""

ROSPRIRODNADZOR_API_BASE = "https://rpn.gov.ru/api"
ROSPRIRODNADZOR_BASE = "https://rpn.gov.ru"
ROSPRIRODNADZOR_OPENDATA_BASE = "https://rpn.gov.ru/opendata"
ONV_REGISTER_BASE = "https://onv.register.rpn.gov.ru/api"
GOSUSLUGI_EKO_BASE = "https://gosuslugi.ru/api/eco"

VIDY_NADZORA = [
    {
        "code": "ekologicheskiy",
        "name": "Государственный экологический надзор",
    },
    {
        "code": "zemelnyy",
        "name": "Государственный земельный надзор",
    },
    {
        "code": "geologicheskiy",
        "name": "Государственный надзор за геологическим изучением",
    },
    {
        "code": "rybolovstvo",
        "name": "Государственный контроль и надзор в сфере рыболовства",
    },
    {
        "code": "radiacionnyy",
        "name": "Радиационный контроль",
    },
]

KATEGORII_OBNV = [
    {"code": "I", "name": "I — значительное негативное воздействие"},
    {"code": "II", "name": "II — умеренное негативное воздействие"},
    {"code": "III", "name": "III — незначительное негативное воздействие"},
    {"code": "IV", "name": "IV — минимальное негативное воздействие"},
]

VIDY_LITSENZIY_NEDRA = [
    {"code": "dobycha", "name": "Добыча полезных ископаемых"},
    {"code": "geologicheskoe", "name": "Геологическое изучение"},
    {"code": "razvedka_dobycha", "name": "Разведка и добыча"},
    {
        "code": "podzemnye_soouruzheniya",
        "name": "Строительство и эксплуатация подземных сооружений",
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
