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
    "planned": "Запланирована",
    "in_progress": "Проводится",
    "completed": "Завершена",
    "cancelled": "Отменена",
    "violations_found": "Выявлены нарушения",
    "no_violations": "Нарушений не выявлено",
}

TIPY_NARUSHENIY_EKO = {
    "air": "Нарушение требований охраны атмосферного воздуха",
    "water": "Нарушение водного законодательства",
    "soil": "Нарушение требований охраны почв",
    "waste": "Нарушение требований в области обращения с отходами",
    "subsoil": "Нарушение требований недропользования",
    "radiation": "Нарушение требований радиационной безопасности",
    "land": "Нарушение земельного законодательства",
    "bio": "Нарушение в области охраны объектов животного мира",
}
