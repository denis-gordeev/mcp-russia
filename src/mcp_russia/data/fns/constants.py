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
    {"code": "osno", "name": "ОСНО — общая система налогообложения"},
    {"code": "usn_dohody", "name": "УСН «Доходы» — 6%"},
    {"code": "usn_dohody_minus_rashody", "name": "УСН «Доходы минус расходы» — 15%"},
    {"code": "envd", "name": "ЕНВД — единый налог на вменённый доход"},
    {"code": "psn", "name": "ПСН — патентная система налогообложения"},
    {"code": "esn", "name": "ЕСН — единый сельскохозяйственный налог"},
    {"code": "npd", "name": "НПД — налог на профессиональный доход (самозанятые)"},
]

VidyNalogov = [
    {"code": "nds", "name": "НДС — налог на добавленную стоимость"},
    {"code": "ndfl", "name": "НДФЛ — налог на доходы физических лиц"},
    {"code": "nalog_na_pribyl", "name": "Налог на прибыль организаций"},
    {"code": "nalog_na_imushchestvo", "name": "Налог на имущество организаций"},
    {"code": "transportnyy_nalog", "name": "Транспортный налог"},
    {"code": "zemelnyy_nalog", "name": "Земельный налог"},
    {"code": "strahovye_vznosy", "name": "Страховые взносы"},
    {"code": "akcizy", "name": "Акцизы"},
]

TipyProverok = [
    {"code": "vycznaya", "name": "Выездная налоговая проверка"},
    {"code": "kameralnaya", "name": "Камеральная налоговая проверка"},
    {"code": "dokumentalnaya", "name": "Документарная проверка"},
]

StatusyOrganizacii = [
    {"code": "deystvuyushchaya", "name": "Действующая"},
    {"code": "v_processe_likvidacii", "name": "В процессе ликвидации"},
    {"code": "likvidirovana", "name": "Ликвидирована"},
    {"code": "v_processe_reorganizacii", "name": "В процессе реорганизации"},
    {"code": "prekratila_deyatelnost", "name": "Прекратила деятельность"},
]

KategoriiNalogoplatelshchikov = [
    {"code": "yuridicheskoe_lico", "name": "Юридическое лицо"},
    {"code": "ip", "name": "Индивидуальный предприниматель"},
    {"code": "samozanyatyy", "name": "Самозанятый (НПД)"},
    {"code": "fizicheskoe_lico", "name": "Физическое лицо"},
]
