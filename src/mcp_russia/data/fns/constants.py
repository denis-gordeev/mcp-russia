"""Константы модуля ФНС."""

# ФНС (Федеральная налоговая служба)
# Основные источники данных:
# 1. Официальный сайт: https://www.nalog.gov.ru
# 2. Открытый API: https://api.nalog.ru
# 3. ЕГРЮЛ/ЕГРИП: https://egrul.nalog.ru
# 4. Прозрачный бизнес: https://pb.nalog.ru

FNS_API_BASE = "https://api.nalog.ru"
EGRUL_API_BASE = "https://egrul.nalog.ru"

NalogovyeRezhimy = [
    {"kod": "osno", "nazvanie": "ОСНО — общая система налогообложения"},
    {"kod": "usn_dohody", "nazvanie": "УСН «Доходы» — 6%"},
    {"kod": "usn_dohody_minus_rashody", "nazvanie": "УСН «Доходы минус расходы» — 15%"},
    {"kod": "envd", "nazvanie": "ЕНВД — единый налог на вменённый доход"},
    {"kod": "psn", "nazvanie": "ПСН — патентная система налогообложения"},
    {"kod": "esn", "nazvanie": "ЕСН — единый сельскохозяйственный налог"},
    {"kod": "npd", "nazvanie": "НПД — налог на профессиональный доход (самозанятые)"},
]

VidyNalogov = [
    {"kod": "nds", "nazvanie": "НДС — налог на добавленную стоимость"},
    {"kod": "ndfl", "nazvanie": "НДФЛ — налог на доходы физических лиц"},
    {"kod": "nalog_na_pribyl", "nazvanie": "Налог на прибыль организаций"},
    {"kod": "nalog_na_imushchestvo", "nazvanie": "Налог на имущество организаций"},
    {"kod": "transportnyy_nalog", "nazvanie": "Транспортный налог"},
    {"kod": "zemelnyy_nalog", "nazvanie": "Земельный налог"},
    {"kod": "strahovye_vznosy", "nazvanie": "Страховые взносы"},
    {"kod": "akcizy", "nazvanie": "Акцизы"},
]

TipyProverok = [
    {"kod": "vycznaya", "nazvanie": "Выездная налоговая проверка"},
    {"kod": "kameralnaya", "nazvanie": "Камеральная налоговая проверка"},
    {"kod": "dokumentalnaya", "nazvanie": "Документарная проверка"},
]

StatusyOrganizacii = [
    {"kod": "deystvuyushchaya", "nazvanie": "Действующая"},
    {"kod": "v_processe_likvidacii", "nazvanie": "В процессе ликвидации"},
    {"kod": "likvidirovana", "nazvanie": "Ликвидирована"},
    {"kod": "v_processe_reorganizacii", "nazvanie": "В процессе реорганизации"},
    {"kod": "prekratila_deyatelnost", "nazvanie": "Прекратила деятельность"},
]

KategoriiNalogoplatelshchikov = [
    {"kod": "yuridicheskoe_lico", "nazvanie": "Юридическое лицо"},
    {"kod": "ip", "nazvanie": "Индивидуальный предприниматель"},
    {"kod": "samozanyatyy", "nazvanie": "Самозанятый (НПД)"},
    {"kod": "fizicheskoe_lico", "nazvanie": "Физическое лицо"},
]
