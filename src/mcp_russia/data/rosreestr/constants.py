"""Константы модуля Росреестра."""

# Росреестр (Федеральная служба государственной регистрации,
# кадастра и картографии)
# Основные источники данных:
# 1. Официальный сайт: https://rosreestr.gov.ru
# 2. Публичная кадастровая карта: https://pkk.rosreestr.ru
# 3. ФГИС ЕГРН: https://fgis.egrn.reestr.ru
# 4. Справочная информация: https://rosreestr.gov.ru/wps/portal/p/cc_ib_portal_services

ROSREESTR_BAZA_API = "https://rosreestr.gov.ru/api"
PKK_BAZA_API = "https://pkk.rosreestr.ru/api/features"

TipyNedvizhimosti = [
    {"kod": "zemelnyy_uchastok", "nazvanie": "Земельный участок"},
    {"kod": "zdanie", "nazvanie": "Здание"},
    {"kod": "pomeshchenie", "nazvanie": "Помещение"},
    {"kod": "sooruzhenie", "nazvanie": "Сооружение"},
    {"kod": "obekt_nedostroenny", "nazvanie": "Объект незавершённого строительства"},
    {"kod": "mnogokvartirnyy_dom", "nazvanie": "Многоквартирный дом"},
]

KategoriiZemel = [
    {
        "kod": "selskohozyaystvennogo_naznacheniya",
        "nazvanie": "Земли сельскохозяйственного назначения",
    },
    {"kod": "naselennyh_punktov", "nazvanie": "Земли населённых пунктов"},
    {"kod": "promyshlennosti", "nazvanie": "Земли промышленности"},
    {"kod": "osobo_ohranyaemyh_territoriy", "nazvanie": "Земли особо охраняемых территорий"},
    {"kod": "lesnogo_fonda", "nazvanie": "Земли лесного фонда"},
    {"kod": "vodnogo_fonda", "nazvanie": "Земли водного фонда"},
    {"kod": "zapasa", "nazvanie": "Земли запаса"},
]

VidyIspolzovaniya = [
    {"kod": "zhiloe", "nazvanie": "Жилое использование"},
    {"kod": "obschestvennoe", "nazvanie": "Общественное использование"},
    {"kod": "promyshlennoe", "nazvanie": "Промышленное использование"},
    {"kod": "selskohozyaystvennoe", "nazvanie": "Сельскохозяйственное использование"},
    {"kod": "rekreatsionnoe", "nazvanie": "Рекреационное использование"},
    {"kod": "transportnoe", "nazvanie": "Транспортное использование"},
    {"kod": "specialnoe", "nazvanie": "Специальное использование"},
]

StatusyObekta = [
    {"kod": "uchtenny", "nazvanie": "Учтённый"},
    {"kod": "ranee_uchtenny", "nazvanie": "Ранее учтённый"},
    {"kod": "vremennyy", "nazvanie": "Временный"},
    {"kod": "annulirovannyy", "nazvanie": "Аннулированный"},
    {"kod": "snyatyy_s_ucheta", "nazvanie": "Снятый с учёта"},
]

FormySobstvennosti = [
    {"kod": "chastnaya", "nazvanie": "Частная собственность"},
    {"kod": "gosudarstvennaya", "nazvanie": "Государственная собственность"},
    {"kod": "municipalnaya", "nazvanie": "Муниципальная собственность"},
    {"kod": "obschaya_dolevaya", "nazvanie": "Общая долевая собственность"},
    {"kod": "obschaya_sovmestnaya", "nazvanie": "Общая совместная собственность"},
]

KATEGORII_ZEMEL_SLOVAR = {
    kategoriya["kod"]: kategoriya["nazvanie"] for kategoriya in KategoriiZemel
}
STATUSY_UCHE_TA_SLOVAR = {
    sostoyanie["kod"]: sostoyanie["nazvanie"] for sostoyanie in StatusyObekta
}
