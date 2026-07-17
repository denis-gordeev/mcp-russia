"""Планировщик запросов mcp-russia на базе LLM.

Использует API Anthropic для анализа пользовательских запросов и построения
структурированных планов выполнения с упорядоченными шагами, назначением
инструментов, параметрами и зависимостями.
"""

from __future__ import annotations

import json
import logging

from pydantic import BaseModel

from ..settings import KLYUCH_ANTHROPIC_API

logger = logging.getLogger("mcp-russia.planner")


class EtapPlana(BaseModel):
    """Один шаг плана выполнения."""

    etap: int
    """Номер шага (начиная с 1)."""

    opisanie: str
    """Описание действия шага."""

    imya_instrumenta: str
    """Имя инструмента (с префиксом модуля, напр. gosduma_poluchit_deputatov)."""

    parametry: dict[str, str]
    """Ключевые параметры (могут содержать плейсхолдеры вида '{etap_1.id}')."""

    zavisit_ot: list[int]
    """Шаги, которые должны завершиться до этого (пусто = независимый)."""

    obosnovanie: str
    """Обоснование необходимости шага."""


class PlanZaprosa(BaseModel):
    """Полный план выполнения запроса пользователя."""

    zapros: str
    """Оригинальный запрос пользователя."""

    slozhnost: str
    """Сложность запроса: 'prostoy', 'umerennyy' или 'slozhnyy'."""

    svodka: str
    """Краткое описание плана."""

    etapy: list[EtapPlana]
    """Упорядоченные шаги выполнения."""

    primechaniya: str = ""
    """Необязательные заметки (требования авторизации, оговорки)."""

    def v_markdown(self) -> str:
        """Рендеринг плана в удобочитаемый Markdown."""
        stroki: list[str] = [
            "## План запроса",
            f"**Запрос:** {self.zapros}",
            f"**Сложность:** {self.slozhnost}",
            f"**Сводка:** {self.svodka}",
            "",
        ]

        for etap in self.etapy:
            stroki.append(f"### Этап {etap.etap}: {etap.opisanie}")
            stroki.append(f"- **Инструмент:** `{etap.imya_instrumenta}`")

            if etap.parametry:
                parametry_str = ", ".join(
                    f'{klyuch}="{znachenie}"' for klyuch, znachenie in etap.parametry.items()
                )
                stroki.append(f"- **Параметры:** {parametry_str}")

            if etap.zavisit_ot:
                zavisimosti = ", ".join(f"Этап {nomer_etapa}" for nomer_etapa in etap.zavisit_ot)
                stroki.append(f"- **Зависит от:** {zavisimosti}")
            else:
                stroki.append("- **Зависит от:** (нет)")

            stroki.append(f"- **Обоснование:** {etap.obosnovanie}")
            stroki.append("")

        if self.primechaniya:
            stroki.append(f"**Примечания:** {self.primechaniya}")

        return "\n".join(stroki)


_SISTEMNYY_PROMPT = """\
Ты строишь планы запросов для mcp-russia. Каталог ниже может содержать
исторические названия модулей и инструментов, которые пока сохранены ради
совместимости. Твоя задача: по вопросу пользователя и каталогу инструментов
собрать структурированный план выполнения.

## Правила

1. Используй ТОЛЬКО инструменты из каталога. Никогда не придумывай новые имена.
2. Используй точные имена инструментов с префиксом модуля.
3. Заполняй параметры только теми именами и типами, которые есть в каталоге.
4. Для ссылок на результаты прошлых шагов используй placeholders вида
   {{etap_N.pole}}.
5. Отвечай только по-русски.
6. Максимум 8 этапов на один план.

## Сложность

- **prostoy**: один прямой вызов
- **umerennyy**: 2-3 вызова с линейной зависимостью
- **slozhnyy**: 4+ вызова, параллельные ветки или сравнение нескольких источников

## Комбинация источников

Полезные планы часто объединяют несколько модулей. Допустимые стратегии:

- **Обогащение**: обогатить данные вторым модулем
- **Сравнение**: сравнить одинаковую метрику из разных источников
- **Контекстуализация**: добавить справочные, демографические или макроэкономические данные
- **Параллелизм**: независимые этапы могут выполняться параллельно

Если вопрос это допускает, предпочитай планы, где объединяются 2+ модулей.
В поле "svodka" коротко скажи, какие источники комбинируются.

## Поле primechaniya

Используй его, чтобы указать:
- нужен ли ключ или другая авторизация
- известные ограничения данных
- какие именно межисточниковые связи делает план

## JSON-схема

Верни ТОЛЬКО валидный JSON, без markdown и без ``` блоков.

{{
  "zapros": "оригинальный вопрос пользователя",
  "slozhnost": "prostoy|umerennyy|slozhnyy",
  "svodka": "краткая сводка плана в 1 предложение",
  "etapy": [
    {{
      "etap": 1,
      "opisanie": "что делает этот этап",
      "imya_instrumenta": "modul_imya_instrumenta",
      "parametry": {{"parametr": "znachenie"}},
      "zavisit_ot": [],
      "obosnovanie": "почему этот этап необходим"
    }}
  ],
  "primechaniya": "заметки об авторизации, ограничениях и т.д."
}}

## Примеры

### Пример 1: умеренно сложный запрос

Вопрос: "Какие расходы были у депутата Иванова в 2024 году?"

{{
  "zapros": "Какие расходы были у депутата Иванова в 2024 году?",
  "slozhnost": "umerennyy",
  "svodka": "Найти депутата по фамилии в Госдуме и запросить его расходы за 2024 год.",
  "etapy": [
    {{
      "etap": 1,
      "opisanie": "Найти депутата по фамилии",
      "imya_instrumenta": "gosduma_poluchit_deputatov",
      "parametry": {{"familiya": "Иванов"}},
      "zavisit_ot": [],
      "obosnovanie": "Нужен ID депутата для запроса расходов"
    }},
    {{
      "etap": 2,
      "opisanie": "Запросить расходы депутата за 2024 год",
      "imya_instrumenta": "gosduma_raskhody_deputata",
      "parametry": {{"id": "{{etap_1.id}}", "god": "2024"}},
      "zavisit_ot": [1],
      "obosnovanie": "Получить расходы используя ID из предыдущего этапа"
    }}
  ],
  "primechaniya": ""
}}

### Пример 2: сложный запрос с параллельными этапами

Вопрос: "Какие расходы на здравоохранение на душу населения в Татарстане?"

{{
  "zapros": "Какие расходы на здравоохранение на душу населения в Татарстане?",
  "slozhnost": "slozhnyy",
  "svodka": "Сравнить данные Росстата (расходы на здравоохранение) с данными о населении.",
  "etapy": [
    {{
      "etap": 1,
      "opisanie": "Запросить расходы на здравоохранение в Татарстане",
      "imya_instrumenta": "rosstat_poluchit_indikator",
      "parametry": {{"indikator": "zdravookhranenie", "region": "16", "god": "2024"}},
      "zavisit_ot": [],
      "obosnovanie": "Получить общую сумму расходов на здравоохранение в регионе"
    }},
    {{
      "etap": 2,
      "opisanie": "Запросить численность населения Татарстана",
      "imya_instrumenta": "rosstat_poluchit_dannye_regiona",
      "parametry": {{"region": "16"}},
      "zavisit_ot": [],
      "obosnovanie": "Получить население для расчёта на душу населения"
    }}
  ],
  "primechaniya": "Этапы 1 и 2 выполняются параллельно. \
Расчёт на душу населения выполняется агентом после обоих этапов."
}}

## Каталог инструментов

{katalog}
"""


async def splanirovat_zapros_impl(zapros: str, katalog: str) -> str:
    """Вызов API Anthropic для построения структурированного плана выполнения.

    Аргументы:
        zapros: Вопрос пользователя на естественном языке.
        katalog: Предварительно собранный каталог всех инструментов.

    Возвращает:
        План выполнения в формате Markdown или сообщение об ошибке.
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
    sistemnyy_prompt = _SISTEMNYY_PROMPT.format(katalog=katalog)

    try:
        otvet = await klient.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=sistemnyy_prompt,
            messages=[{"role": "user", "content": zapros}],
        )
        blok = otvet.content[0]
        syrovoy_tekst = str(getattr(blok, "text", ""))

        try:
            plan_zaprosa = PlanZaprosa.model_validate(json.loads(syrovoy_tekst))
            return plan_zaprosa.v_markdown()
        except (json.JSONDecodeError, Exception):
            logger.warning("Не удалось разобрать JSON плана; возврат сырого текста")
            return syrovoy_tekst

    except Exception as e:
        logger.error("Ошибка вызова API Anthropic: %s", e)
        return (
            f"Ошибка при обращении к LLM: {e}\n\n"
            "В качестве альтернативы используйте 'search_tools'."
        )
