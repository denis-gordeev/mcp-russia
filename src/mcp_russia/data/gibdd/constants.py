"""Константы модуля ГИБДД/МВД."""

# ГИБДД (Государственная автомобильная инспекция)
# Основные источники данных:
# 1. Официальный сайт: https://гибдд.рф
# 2. Госуслуги (штрафы): https://www.gosuslugi.ru/10001/1
# 3. Проверка ТС: https://гибдд.рф/check/auto
# 4. Проверка ВУ: https://гибдд.рф/check/driver

GIBDD_BAZA_API = "https://гибдд.рф"
GIBDD_BAZA_PROVEROK = "https://гибдд.рф/proxy/check"
GIBDD_BAZA_STATISTIKI = "https://stat.gibdd.ru"

TipyTransportnykhSredstv = [
    {"kod": "legkovoy", "nazvanie": "Легковой автомобиль"},
    {"kod": "gruzovoy", "nazvanie": "Грузовой автомобиль"},
    {"kod": "avtobus", "nazvanie": "Автобус"},
    {"kod": "mototsikl", "nazvanie": "Мотоцикл"},
    {"kod": "pritsep", "nazvanie": "Прицеп"},
    {"kod": "spectehnika", "nazvanie": "Спецтехника"},
    {"kod": "motokolyaska", "nazvanie": "Мотоколяска"},
]

KategoriiVoditelskihUdostovereniy = [
    {"kod": "a", "nazvanie": "A — мотоциклы"},
    {"kod": "a1", "nazvanie": "A1 — мотоциклы малой мощности"},
    {"kod": "b", "nazvanie": "B — автомобили до 3500 кг"},
    {"kod": "b1", "nazvanie": "B1 — трициклы/квадрициклы"},
    {"kod": "c", "nazvanie": "C — автомобили свыше 3500 кг"},
    {"kod": "c1", "nazvanie": "C1 — автомобили 3500–7500 кг"},
    {"kod": "d", "nazvanie": "D — автобусы"},
    {"kod": "d1", "nazvanie": "D1 — автобусы малой вместимости"},
    {"kod": "be", "nazvanie": "BE — автомобили с прицепом"},
    {"kod": "ce", "nazvanie": "CE — грузовики с прицепом"},
    {"kod": "de", "nazvanie": "DE — автобусы с прицепом"},
    {"kod": "m", "nazvanie": "M — мопеды и скутеры"},
    {"kod": "tm", "nazvanie": "Tm — трамваи"},
    {"kod": "tb", "nazvanie": "Tb — троллейбусы"},
]

VidyNarusheniy = [
    {"kod": "skorost", "nazvanie": "Превышение скорости"},
    {"kod": "proezd_krasnyy", "nazvanie": "Проезд на запрещающий сигнал"},
    {"kod": "neustupka_peshehod", "nazvanie": "Непредоставление преимущества пешеходу"},
    {"kod": "vyezd_vstrechnaya", "nazvanie": "Выезд на полосу встречного движения"},
    {"kod": "ostanovka_zapret", "nazvanie": "Нарушение правил остановки/стоянки"},
    {"kod": "remni_bezopasnosti", "nazvanie": "Непристёгнутый ремень безопасности"},
    {"kod": "telefon", "nazvanie": "Использование телефона за рулём"},
    {"kod": "tonirovka", "nazvanie": "Нарушение правил тонировки"},
    {"kod": "net_osago", "nazvanie": "Отсутствие полиса ОСАГО"},
    {"kod": "net_prav", "nazvanie": "Управление без водительского удостоверения"},
    {"kod": "pyanyy", "nazvanie": "Управление в состоянии опьянения"},
    {"kod": "dbezopasnosti_detey", "nazvanie": "Нарушение правил перевозки детей"},
]

StatusyShtrafov = [
    {"kod": "ne_oplachen", "nazvanie": "Не оплачен"},
    {"kod": "oplachen", "nazvanie": "Оплачен"},
    {"kod": "v_sude", "nazvanie": "Обжалуется в суде"},
    {"kod": "peredan_fssp", "nazvanie": "Передан приставам (ФССП)"},
    {"kod": "dvoynoy", "nazvanie": "Двойной штраф (просрочка оплаты)"},
]

TipyDTP = [
    {"kod": "stolknovenie", "nazvanie": "Столкновение"},
    {"kod": "oprokidyvanie", "nazvanie": "Опрокидывание"},
    {"kod": "naezd_peshehod", "nazvanie": "Налёт на пешехода"},
    {"kod": "naezd_velosiped", "nazvanie": "Налёт на велосипедиста"},
    {"kod": "naezd_stoyanka", "nazvanie": "Налёт на стоящее ТС"},
    {"kod": "naezd_prepyatstvie", "nazvanie": "Налёт на препятствие"},
    {"kod": "padenie_passazhir", "nazvanie": "Падение пассажира"},
]

RegionyRegistratsii = [
    {"kod": "77", "nazvanie": "Москва"},
    {"kod": "78", "nazvanie": "Санкт-Петербург"},
    {"kod": "50", "nazvanie": "Московская область"},
    {"kod": "47", "nazvanie": "Ленинградская область"},
    {"kod": "16", "nazvanie": "Республика Татарстан"},
    {"kod": "24", "nazvanie": "Красноярский край"},
    {"kod": "25", "nazvanie": "Приморский край"},
    {"kod": "23", "nazvanie": "Краснодарский край"},
    {"kod": "02", "nazvanie": "Республика Башкортостан"},
    {"kod": "61", "nazvanie": "Ростовская область"},
    {"kod": "63", "nazvanie": "Самарская область"},
    {"kod": "74", "nazvanie": "Челябинская область"},
    {"kod": "66", "nazvanie": "Свердловская область"},
    {"kod": "52", "nazvanie": "Нижегородская область"},
    {"kod": "54", "nazvanie": "Новосибирская область"},
]
