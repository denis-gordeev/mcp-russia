"""Рекомендация инструментов mcp-russia на базе LLM.

Использует API Anthropic для понимания намерений пользователя и подбора
наиболее релевантных инструментов из текущего каталога сервера.
"""

from __future__ import annotations

import logging

from ..settings import KLYUCH_ANTHROPIC_API

logger = logging.getLogger("mcp-russia.discovery")

_kesh_kataloga: str = ""


def _formatirovat_signaturu_instrumenta(
    imya_modulya: str, imya_instrumenta: str, instrument: object
) -> str:
    """Форматирование инструмента в читаемую сигнатуру с параметрами и описанием.

    Формирует вывод вида:
        - gosduma_poluchit_deputatov(familiya?: str) — Список депутатов Госдумы.

    Аргументы:
        imya_modulya: Имя модуля (префикс инструмента).
        imya_instrumenta: Имя инструмента.
        instrument: Объект инструмента.
    """
    parametry = getattr(instrument, "parameters", {})
    svoystva: dict[str, dict[str, object]] = parametry.get("properties", {})
    obyazatelnye: list[str] = parametry.get("required", [])

    chasti_parametra: list[str] = []
    for imya_param, skhema_param in svoystva.items():
        if imya_param == "ctx":
            continue
        tip_param = skhema_param.get("type", "any")
        neobyazatelen = "" if imya_param in obyazatelnye else "?"
        chasti_parametra.append(f"{imya_param}{neobyazatelen}: {tip_param}")

    signatura = ", ".join(chasti_parametra)
    polnoe_imya = f"{imya_modulya}_{imya_instrumenta}"

    opisanie_kratkoe = (getattr(instrument, "description", "") or "").split("\n")[0]

    return f"- `{polnoe_imya}({signatura})` — {opisanie_kratkoe}"


def postroit_katalog(reyestr: object) -> str:
    """Построение подробного каталога всех инструментов из реестра.

    Использует MetaFunktsii (имя, описание, авторизация) и схемы инструментов
    (параметры, типы, описания) для формирования детального каталога для LLM.

    Аргументы:
        reyestr: Экземпляр ReyestrFunktsiy с обнаруженными функциями.

    Возвращает:
        Каталог в формате Markdown с контекстом функций и сигнатурами инструментов.
    """
    global _kesh_kataloga
    if _kesh_kataloga:
        return _kesh_kataloga

    stroki: list[str] = []
    funktsii = getattr(reyestr, "funktsii", {})
    for funktsiya in funktsii.values():
        metadannye = funktsiya.metadannye
        svedeniya_ob_avtorizatsii = (
            f"Требуется аутентификация ({metadannye.peremennaya_avt_env})"
            if metadannye.trebuet_autentifikatsii
            else (
                f"Рекомендуется аутентификация ({metadannye.peremennaya_avt_env})"
                if metadannye.peremennaya_avt_env
                else "Без аутентификации"
            )
        )
        stroki.append(f"\n## {metadannye.imya}: {metadannye.opisanie}")
        stroki.append(f"Авторизация: {svedeniya_ob_avtorizatsii}")

        server_funktsiya = funktsiya.server_funktsiya
        if hasattr(server_funktsiya, "_tool_manager") and hasattr(
            server_funktsiya._tool_manager, "_tools"
        ):
            for imya_instrumenta, instrument in server_funktsiya._tool_manager._tools.items():
                stroki.append(
                    _formatirovat_signaturu_instrumenta(
                        metadannye.imya, imya_instrumenta, instrument
                    )
                )

    _kesh_kataloga = "\n".join(stroki)
    return _kesh_kataloga


async def rekomendovat_instrumenty_impl(zapros: str, katalog: str) -> str:
    """Вызов API Anthropic для рекомендации инструментов по запросу пользователя.

    Аргументы:
        zapros: Вопрос пользователя на естественном языке.
        katalog: Предварительно собранный каталог всех инструментов.

    Возвращает:
        Рекомендации LLM с пояснениями.
    """
    try:
        import anthropic
    except ImportError:
        return (
            "Ошибка: пакет 'anthropic' не установлен. "
            "Установите его командой: pip install 'mcp-russia[llm]'\n\n"
            "В качестве альтернативы используйте инструмент 'search_tools'."
        )

    klyuch_api = KLYUCH_ANTHROPIC_API
    if not klyuch_api:
        return (
            "Ошибка: переменная ANTHROPIC_API_KEY не настроена. "
            "Задайте ANTHROPIC_API_KEY, чтобы использовать этот мета-инструмент.\n\n"
            "В качестве альтернативы используйте инструмент 'search_tools'."
        )

    klient = anthropic.AsyncAnthropic(api_key=klyuch_api)

    sistemnyy_prompt = (
        "Ты помогаешь подобрать инструменты из каталога mcp-russia. "
        "В каталоге могут встречаться исторические названия функций, "
        "сохранённые для совместимости. На основе вопроса пользователя "
        "выбери 3-5 наиболее релевантных инструментов. Для каждого:\n"
        "1. Полное имя инструмента (с префиксом функции)\n"
        "2. Почему он релевантен запросу\n"
        "3. Пример использования с основными параметрами\n\n"
        "Отвечай по-русски, кратко и по делу.\n\n"
        f"## Каталог инструментов\n{katalog}"
    )

    try:
        otvet = await klient.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=sistemnyy_prompt,
            messages=[{"role": "user", "content": zapros}],
        )
        blok = otvet.content[0]
        return str(getattr(blok, "text", ""))
    except Exception as e:
        logger.error("Ошибка вызова API Anthropic: %s", e)
        return (
            f"Ошибка при обращении к LLM: {e}\n\n"
            "В качестве альтернативы используйте 'search_tools'."
        )
