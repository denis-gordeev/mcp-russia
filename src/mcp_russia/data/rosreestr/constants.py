"""Constants for the Росреестр feature."""

# Росреестр (Федеральная служба государственной регистрации,
# кадастра и картографии)
# Основные источники данных:
# 1. Официальный сайт: https://rosreestr.gov.ru
# 2. Публичная кадастровая карта: https://pkk.rosreestr.ru
# 3. ФГИС ЕГРН: https://fgis.egrn.reestr.ru
# 4. Справочная информация: https://rosreestr.gov.ru/wps/portal/p/cc_ib_portal_services

ROSREESTR_API_BASE = "https://rosreestr.gov.ru/api"
PKK_API_BASE = "https://pkk.rosreestr.ru/api/features"

TipyNedvizhimosti = [
    {"code": "zemelnyy_uchastok", "name": "Земельный участок"},
    {"code": "zdanie", "name": "Здание"},
    {"code": "pomeshchenie", "name": "Помещение"},
    {"code": "sooruzhenie", "name": "Сооружение"},
    {"code": "obekt_nedostroenny", "name": "Объект незавершённого строительства"},
    {"code": "mnogokvartirnyy_dom", "name": "Многоквартирный дом"},
]

KategoriiZemel = [
    {
        "code": "selskohozyaystvennogo_naznacheniya",
        "name": "Земли сельскохозяйственного назначения",
    },
    {"code": "naselennyh_punktov", "name": "Земли населённых пунктов"},
    {"code": "promyshlennosti", "name": "Земли промышленности"},
    {"code": "osobo_ohranyaemyh_territoriy", "name": "Земли особо охраняемых территорий"},
    {"code": "lesnogo_fonda", "name": "Земли лесного фонда"},
    {"code": "vodnogo_fonda", "name": "Земли водного фонда"},
    {"code": "zapasa", "name": "Земли запаса"},
]

VidyIspolzovaniya = [
    {"code": "zhiloe", "name": "Жилое использование"},
    {"code": "obschestvennoe", "name": "Общественное использование"},
    {"code": "promyshlennoe", "name": "Промышленное использование"},
    {"code": "selskohozyaystvennoe", "name": "Сельскохозяйственное использование"},
    {"code": "rekreacionnoe", "name": "Рекреационное использование"},
    {"code": "transportnoe", "name": "Транспортное использование"},
    {"code": "specialnoe", "name": "Специальное использование"},
]

StatusyObiekta = [
    {"code": "uchtenny", "name": "Учтённый"},
    {"code": "ranee_uchtenny", "name": "Ранее учтённый"},
    {"code": "vremennyy", "name": "Временный"},
    {"code": "annulirovannyy", "name": "Аннулированный"},
    {"code": "snyatyy_s_ucheta", "name": "Снятый с учёта"},
]

FormySobstvennosti = [
    {"code": "chastnaya", "name": "Частная собственность"},
    {"code": "gosudarstvennaya", "name": "Государственная собственность"},
    {"code": "municipalnaya", "name": "Муниципальная собственность"},
    {"code": "obschaya_dolevaya", "name": "Общая долевая собственность"},
    {"code": "obschaya_sovmestnaya", "name": "Общая совместная собственность"},
]

TIPY_NEDVIZIMOSTI_MAP = {t["code"]: t["name"] for t in TipyNedvizhimosti}
KATEGORII_ZEMEL_MAP = {k["code"]: k["name"] for k in KategoriiZemel}
VIDY_ISPOLZOVANIYA_MAP = {v["code"]: v["name"] for v in VidyIspolzovaniya}
STATUSY_UCHE_TA_MAP = {s["code"]: s["name"] for s in StatusyObiekta}
FORMY_SOBSTVENNOSTI_MAP = {f["code"]: f["name"] for f in FormySobstvennosti}
