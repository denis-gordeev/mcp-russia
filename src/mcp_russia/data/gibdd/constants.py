"""Константы модуля ГИБДД/МВД."""

# ГИБДД (Государственная автомобильная инспекция)
# Основные источники данных:
# 1. Официальный сайт: https://гибдд.рф
# 2. Госуслуги (штрафы): https://www.gosuslugi.ru/10001/1
# 3. Проверка ТС: https://гибдд.рф/check/auto
# 4. Проверка ВУ: https://гибдд.рф/check/driver

GIBDD_API_BASE = "https://гибдд.рф"
GIBDD_CHECK_BASE = "https://гибдд.рф/proxy/check"
GIBDD_STAT_BASE = "https://stat.gibdd.ru"

TipyTransportnykhSredstv = [
    {"code": "legkovoy", "name": "Легковой автомобиль"},
    {"code": "gruzovoy", "name": "Грузовой автомобиль"},
    {"code": "avtobus", "name": "Автобус"},
    {"code": "mototsikl", "name": "Мотоцикл"},
    {"code": "pritsep", "name": "Прицеп"},
    {"code": "spectehnika", "name": "Спецтехника"},
    {"code": "motokolyaska", "name": "Мотоколяска"},
]

KategoriiVoditelskihUdostovereniy = [
    {"code": "a", "name": "A — мотоциклы"},
    {"code": "a1", "name": "A1 — мотоциклы малой мощности"},
    {"code": "b", "name": "B — автомобили до 3500 кг"},
    {"code": "b1", "name": "B1 — трициклы/квадрициклы"},
    {"code": "c", "name": "C — автомобили свыше 3500 кг"},
    {"code": "c1", "name": "C1 — автомобили 3500–7500 кг"},
    {"code": "d", "name": "D — автобусы"},
    {"code": "d1", "name": "D1 — автобусы малой вместимости"},
    {"code": "be", "name": "BE — автомобили с прицепом"},
    {"code": "ce", "name": "CE — грузовики с прицепом"},
    {"code": "de", "name": "DE — автобусы с прицепом"},
    {"code": "m", "name": "M — мопеды и скутеры"},
    {"code": "tm", "name": "Tm — трамваи"},
    {"code": "tb", "name": "Tb — троллейбусы"},
]

VidyNarusheniy = [
    {"code": "skorost", "name": "Превышение скорости"},
    {"code": "proezd_krasnyy", "name": "Проезд на запрещающий сигнал"},
    {"code": "neustupka_peshehod", "name": "Непредоставление преимущества пешеходу"},
    {"code": "vyezd_vstrechnaya", "name": "Выезд на полосу встречного движения"},
    {"code": "ostanovka_zapret", "name": "Нарушение правил остановки/стоянки"},
    {"code": "remni_bezopasnosti", "name": "Непристёгнутый ремень безопасности"},
    {"code": "telefon", "name": "Использование телефона за рулём"},
    {"code": "tonirovka", "name": "Нарушение правил тонировки"},
    {"code": "net_osago", "name": "Отсутствие полиса ОСАГО"},
    {"code": "net_prav", "name": "Управление без водительского удостоверения"},
    {"code": "pyanyy", "name": "Управление в состоянии опьянения"},
    {"code": "dbezopasnosti_detey", "name": "Нарушение правил перевозки детей"},
]

StatusyShtrafov = [
    {"code": "ne_oplachen", "name": "Не оплачен"},
    {"code": "oplachen", "name": "Оплачен"},
    {"code": "v_sude", "name": "Обжалуется в суде"},
    {"code": "peredan_fssp", "name": "Передан приставам (ФССП)"},
    {"code": "dvoynoy", "name": "Двойной штраф (просрочка оплаты)"},
]

TipyDTP = [
    {"code": "stolknovenie", "name": "Столкновение"},
    {"code": "oprokidyvanie", "name": "Опрокидывание"},
    {"code": "naezd_peshehod", "name": "Налёт на пешехода"},
    {"code": "naezd_velosiped", "name": "Налёт на велосипедиста"},
    {"code": "naezd_stoyanka", "name": "Налёт на стоящее ТС"},
    {"code": "naezd_prepyatstvie", "name": "Налёт на препятствие"},
    {"code": "padenie_passazhir", "name": "Падение пассажира"},
]

RegionyRegistratsii = [
    {"code": "77", "name": "Москва"},
    {"code": "78", "name": "Санкт-Петербург"},
    {"code": "50", "name": "Московская область"},
    {"code": "47", "name": "Ленинградская область"},
    {"code": "16", "name": "Республика Татарстан"},
    {"code": "24", "name": "Красноярский край"},
    {"code": "25", "name": "Приморский край"},
    {"code": "23", "name": "Краснодарский край"},
    {"code": "02", "name": "Республика Башкортостан"},
    {"code": "61", "name": "Ростовская область"},
    {"code": "63", "name": "Самарская область"},
    {"code": "74", "name": "Челябинская область"},
    {"code": "66", "name": "Свердловская область"},
    {"code": "52", "name": "Нижегородская область"},
    {"code": "54", "name": "Новосибирская область"},
]
