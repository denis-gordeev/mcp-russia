"""Constants for the Zakupki (ЕИС — Единая информационная система закупок) feature."""

# API ЕИС (открытые данные)
ZAKUPKI_API_BASE = "https://zakupki.gov.ru"
ZAKUPKI_OPEN_DATA = "https://data.zakupki.gov.ru"
ZAKUPKI_API_DOCS = "https://zakupki.gov.ru/epz/order/quicksearch/search.html"

# Законы о закупках
ZAKON_44_FZ = "44-ФЗ (Федеральный закон о контрактной системе)"
ZAKON_223_FZ = "223-ФЗ (Федеральный закон о закупках отдельных видов юридических лиц)"

# Основные типы данных
TIPLY_DANNYKH = [
    {"code": "zakupki_44", "name": "Закупки по 44-ФЗ"},
    {"code": "zakupki_223", "name": "Закупки по 223-ФЗ"},
    {"code": "kontrakty", "name": "Реестр контрактов"},
    {"code": "plany", "name": "Планы-графики закупок"},
    {"code": "postavshchiki", "name": "Реестр недобросовестных поставщиков"},
]

# Способы определения поставщиков
SPOSOBY_ZAKUPOK = [
    {"code": "open", "name": "Открытый конкурс"},
    {"code": "auction", "name": "Электронный аукцион"},
    {"code": "query", "name": "Запрос котировок"},
    {"code": "single", "name": "Закупка у единственного поставщика"},
    {"code": "closed", "name": "Закрытый конкурс"},
    {"code": "limited", "name": "Закупка с ограниченным участием"},
]

# Основные отрасли (ОКВЭД верхнего уровня)
OTRASLI = [
    {"code": "construction", "name": "Строительство"},
    {"code": "it", "name": "Информационные технологии"},
    {"code": "medicine", "name": "Медицина и фармацевтика"},
    {"code": "education", "name": "Образование"},
    {"code": "transport", "name": "Транспорт и логистика"},
    {"code": "energy", "name": "Энергетика"},
    {"code": "food", "name": "Продовольствие"},
    {"code": "security", "name": "Безопасность и оборона"},
]

# Статусы закупок
STATUSY_ZAKUPOK = [
    {"code": "planning", "name": "Планирование"},
    {"code": "announced", "name": "Опубликована"},
    {"code": "bidding", "name": "Приём заявок"},
    {"code": "review", "name": "Рассмотрение заявок"},
    {"code": "completed", "name": "Завершена"},
    {"code": "cancelled", "name": "Отменена"},
]
