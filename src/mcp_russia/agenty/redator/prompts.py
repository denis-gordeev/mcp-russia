"""Prompts: агенты по типам документов.

Каждый prompt — «виртуальный агент», который инструктирует LLM:
- Какой тип документа создать
- Какие нормы применять (ГОСТ Р 7.0.97-2016)
- Какую структуру использовать
"""

from __future__ import annotations

from fastmcp.prompts.prompt import Message


def redaktor_pismo(
    adresat: str,
    dolzhnost_adresata: str,
    tema: str,
    otpravitel: str = "",
) -> list[Message]:
    """Редактор официального письма.

    Args:
        adresat: Имя адресата.
        dolzhnost_adresata: Должность адресата.
        tema: Тема письма.
        otpravitel: Орган-отправитель.
    """
    return [
        Message(
            f"Мне нужно составить официальное ПИСЬМО.\n\n"
            f"Кому: {adresat} — {dolzhnost_adresata}\n"
            f"От: {otpravitel if otpravitel else '[указать орган отправителя]'}\n"
            f"Тема: {tema}\n\n"
            f"Инструкции (ГОСТ Р 7.0.97-2016, делопроизводство РФ):\n"
            f"1. Загрузи шаблон письма (resource template://pismo)\n"
            f"2. Загрузи нормы делопроизводства (resource normas://manual)\n"
            f"3. Используй konsulitirovat_obrashchenie() для правильной формы обращения\n"
            f"4. Формат даты: «г. Москва, 15 марта 2026 г.»\n"
            f"5. Структура: шапка → обращение → текст → подпись\n"
            f"6. Заключительная формула: «С уважением,»\n"
            f"7. Шрифт: Times New Roman, 12–14 пт, интервал 1,5\n"
            f"8. Стиль: официальный, без эмоций, кратко и по делу"
        ),
        Message(
            "Понял. Составлю письмо по ГОСТ Р 7.0.97-2016. "
            "Загружаю шаблон, нормы делопроизводства и формы обращения...",
            role="assistant",
        ),
    ]


def redaktor_prikaz(
    tema: str,
    rukovoditel: str = "",
    osnovanie: str = "",
) -> list[Message]:
    """Редактор приказа.

    Args:
        tema: Тема приказа.
        rukovoditel: Руководитель-инициатор.
        osnovanie: Основание для издания.
    """
    return [
        Message(
            f"Мне нужно составить ПРИКАЗ.\n\n"
            f"Тема: {tema}\n"
            f"Руководитель: {rukovoditel if rukovoditel else '[указать руководителя]'}\n"
            f"Основание: {osnovanie if osnovanie else '[указать основание]'}\n\n"
            f"Инструкции:\n"
            f"1. Загрузи шаблон приказа (resource template://prikaz)\n"
            f"2. Преамбула — основание/цель издания\n"
            f"3. Слово «ПРИКАЗЫВАЮ:» заглавными\n"
            f"4. Поручения с ответственными и сроками\n"
            f"5. Последний пункт — контроль за исполнением\n"
            f"6. Подпись руководителя"
        ),
        Message(
            "Составлю приказ с правильной структурой. Загружаю шаблон...",
            role="assistant",
        ),
    ]


def redaktor_rasporyazhenie(
    tema: str,
    osnovanie: str = "",
) -> list[Message]:
    """Редактор распоряжения.

    Args:
        tema: Тема распоряжения.
        osnovanie: Основание для издания.
    """
    return [
        Message(
            f"Мне нужно составить РАСПОРЯЖЕНИЕ.\n\n"
            f"Тема: {tema}\n"
            f"Основание: {osnovanie if osnovanie else '[указать основание]'}\n\n"
            f"Инструкции:\n"
            f"1. Загрузи шаблон (resource template://rasporyazhenie)\n"
            f"2. Преамбула — цель распоряжения\n"
            f"3. «РАСПОРЯЖАЮСЬ:» заглавными\n"
            f"4. Поручения с ответственными и сроками\n"
            f"5. Контроль за исполнением"
        ),
        Message(
            "Составлю распоряжение. Загружаю шаблон...",
            role="assistant",
        ),
    ]


def redaktor_akt(tema: str, komissiya: str = "") -> list[Message]:
    """Редактор акта.

    Args:
        tema: Тема акта.
        komissiya: Состав комиссии.
    """
    return [
        Message(
            f"Мне нужно составить АКТ.\n\n"
            f"Тема: {tema}\n"
            f"Комиссия: {komissiya if komissiya else '[указать состав]'}\n\n"
            f"Инструкции:\n"
            f"1. Загрузи шаблон акта (resource template://akt)\n"
            f"2. Комиссия не менее 3 человек\n"
            f"3. Факты излагаются последовательно\n"
            f"4. Подписи всех членов комиссии"
        ),
        Message(
            "Составлю акт. Загружаю шаблон...",
            role="assistant",
        ),
    ]


def redaktor_spravka(tema: str, dannye: str = "") -> list[Message]:
    """Редактор справки.

    Args:
        tema: Тема справки.
        dannye: Фактические данные.
    """
    return [
        Message(
            f"Мне нужно составить СПРАВКУ.\n\n"
            f"Тема: {tema}\n"
            f"Данные: {dannye if dannye else '[указать данные]'}\n\n"
            f"Инструкции:\n"
            f"1. Загрузи шаблон справки (resource template://spravka)\n"
            f"2. Только факты, без эмоций\n"
            f"3. Конкретные цифры и данные\n"
            f"4. Без поручений — это информационный документ"
        ),
        Message(
            "Составлю справку с фактическими данными. Загружаю шаблон...",
            role="assistant",
        ),
    ]


def redaktor_protokol(
    tema: str,
    uchastniki: str = "",
    voprosy: str = "",
) -> list[Message]:
    """Редактор протокола заседания.

    Args:
        tema: Тема заседания.
        uchastniki: Список участников.
        voprosy: Повестка дня.
    """
    return [
        Message(
            f"Мне нужно составить ПРОТОКОЛ заседания.\n\n"
            f"Тема: {tema}\n"
            f"Участники: {uchastniki if uchastniki else '[указать]'}\n"
            f"Вопросы: {voprosy if voprosy else '[указать повестку]'}\n\n"
            f"Инструкции:\n"
            f"1. Загрузи шаблон (resource template://protokol)\n"
            f"2. Председатель и секретарь\n"
            f"3. Повестка дня нумеруется\n"
            f"4. По каждому вопросу: слушали — выступили — постановили\n"
            f"5. Решения с ответственными и сроками"
        ),
        Message(
            "Составлю протокол заседания. Загружаю шаблон...",
            role="assistant",
        ),
    ]


def redaktor_dokladnaya_zapiska(
    tema: str,
    rukovoditel: str = "",
) -> list[Message]:
    """Редактор докладной записки.

    Args:
        tema: Тема записки.
        rukovoditel: Руководитель-адресат.
    """
    return [
        Message(
            f"Мне нужно составить ДОКЛАДНУЮ ЗАПИСКУ.\n\n"
            f"Тема: {tema}\n"
            f"Руководителю: {rukovoditel if rukovoditel else '[указать]'}\n\n"
            f"Инструкции:\n"
            f"1. Загрузи шаблон (resource template://dokladnaya_zapiska)\n"
            f"2. Шапка в правом верхнем углу\n"
            f"3. Изложение фактов → анализ → предложения\n"
            f"4. Без заключительной формулы"
        ),
        Message(
            "Составлю докладную записку. Загружаю шаблон...",
            role="assistant",
        ),
    ]
