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
    {"kod": "zakupki_44", "nazvanie": "Закупки по 44-ФЗ"},
    {"kod": "zakupki_223", "nazvanie": "Закупки по 223-ФЗ"},
    {"kod": "kontrakty", "nazvanie": "Реестр контрактов"},
    {"kod": "plany", "nazvanie": "Планы-графики закупок"},
    {"kod": "postavshchiki", "nazvanie": "Реестр недобросовестных поставщиков"},
]

# Способы определения поставщиков
SPOSOBY_ZAKUPOK = [
    {"kod": "otkrytyy_konkurs", "nazvanie": "Открытый конкурс"},
    {"kod": "elektronnyy_auktsion", "nazvanie": "Электронный аукцион"},
    {"kod": "zapros_kotirovok", "nazvanie": "Запрос котировок"},
    {"kod": "edinyy_postavshchik", "nazvanie": "Закупка у единственного поставщика"},
    {"kod": "zakrytyy_konkurs", "nazvanie": "Закрытый конкурс"},
    {"kod": "ogranichennoe_uchastie", "nazvanie": "Закупка с ограниченным участием"},
]

# Основные отрасли (ОКВЭД верхнего уровня)
OTRASLI = [
    {"kod": "stroitelstvo", "nazvanie": "Строительство"},
    {"kod": "informatsionnye_tekhnologii", "nazvanie": "Информационные технологии"},
    {"kod": "meditsina_i_farmvtsevtika", "nazvanie": "Медицина и фармацевтика"},
    {"kod": "obrazovanie", "nazvanie": "Образование"},
    {"kod": "transport_i_logistika", "nazvanie": "Транспорт и логистика"},
    {"kod": "energetika", "nazvanie": "Энергетика"},
    {"kod": "prodovolstvie", "nazvanie": "Продовольствие"},
    {"kod": "bezopasnost_i_oborona", "nazvanie": "Безопасность и оборона"},
]

# Статусы закупок
STATUSY_ZAKUPOK = [
    {"kod": "planirovanie", "nazvanie": "Планирование"},
    {"kod": "opublikovana", "nazvanie": "Опубликована"},
    {"kod": "priem_zayavok", "nazvanie": "Приём заявок"},
    {"kod": "rassmotrenie_zayavok", "nazvanie": "Рассмотрение заявок"},
    {"kod": "zavershena", "nazvanie": "Завершена"},
    {"kod": "otmenena", "nazvanie": "Отменена"},
]
