"""Константы модуля ЕИС Закупок."""

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
    {"code": "otkrytyy_konkurs", "name": "Открытый конкурс"},
    {"code": "elektronnyy_auktsion", "name": "Электронный аукцион"},
    {"code": "zapros_kotirovok", "name": "Запрос котировок"},
    {"code": "edinyy_postavshchik", "name": "Закупка у единственного поставщика"},
    {"code": "zakrytyy_konkurs", "name": "Закрытый конкурс"},
    {"code": "ogranichennoe_uchastie", "name": "Закупка с ограниченным участием"},
]

# Основные отрасли (ОКВЭД верхнего уровня)
OTRASLI = [
    {"code": "stroitelstvo", "name": "Строительство"},
    {"code": "informatsionnye_tekhnologii", "name": "Информационные технологии"},
    {"code": "meditsina_i_farmvtsevtika", "name": "Медицина и фармацевтика"},
    {"code": "obrazovanie", "name": "Образование"},
    {"code": "transport_i_logistika", "name": "Транспорт и логистика"},
    {"code": "energetika", "name": "Энергетика"},
    {"code": "prodovolstvie", "name": "Продовольствие"},
    {"code": "bezopasnost_i_oborona", "name": "Безопасность и оборона"},
]

# Статусы закупок
STATUSY_ZAKUPOK = [
    {"code": "planirovanie", "name": "Планирование"},
    {"code": "opublikovana", "name": "Опубликована"},
    {"code": "priem_zayavok", "name": "Приём заявок"},
    {"code": "rassmotrenie_zayavok", "name": "Рассмотрение заявок"},
    {"code": "zavershena", "name": "Завершена"},
    {"code": "otmenena", "name": "Отменена"},
]
