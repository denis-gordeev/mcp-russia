"""LLM-powered query planner for mcp-russia.

Uses the Anthropic API to analyze user queries and build structured execution
plans with ordered steps, tool assignments, parameters, and dependencies.
The planner works against the current catalog, including legacy features that
remain available during the migration.
"""

from __future__ import annotations

import json
import logging

from pydantic import BaseModel

from ..settings import ANTHROPIC_API_KEY

logger = logging.getLogger("mcp-russia.planner")


class EtapaPlano(BaseModel):
    """One step of the execution plan."""

    etapa: int
    """Step number (1-based)."""

    descricao: str
    """What this step does."""

    tool: str
    """Tool name (with feature prefix, e.g. camara_buscar_deputados)."""

    parametros: dict[str, str]
    """Key parameters (may contain placeholders like '{etapa_1.id}')."""

    depende_de: list[int]
    """Steps that must complete before this one (empty = independent)."""

    justificativa: str
    """Why this step is needed."""


class PlanoConsulta(BaseModel):
    """Complete execution plan for a user query."""

    consulta: str
    """Original user query."""

    complexidade: str
    """Query complexity: 'simples', 'moderada', or 'complexa'."""

    resumo: str
    """Brief summary of the plan."""

    etapas: list[EtapaPlano]
    """Ordered execution steps."""

    observacoes: str = ""
    """Optional notes (auth requirements, caveats)."""

    def to_markdown(self) -> str:
        """Render the plan as human-friendly markdown."""
        lines: list[str] = [
            "## Plano de Consulta",
            f"**Consulta:** {self.consulta}",
            f"**Complexidade:** {self.complexidade}",
            f"**Resumo:** {self.resumo}",
            "",
        ]

        for etapa in self.etapas:
            lines.append(f"### Etapa {etapa.etapa}: {etapa.descricao}")
            lines.append(f"- **Tool:** `{etapa.tool}`")

            if etapa.parametros:
                params = ", ".join(f'{k}="{v}"' for k, v in etapa.parametros.items())
                lines.append(f"- **Parâmetros:** {params}")

            if etapa.depende_de:
                deps = ", ".join(f"Etapa {d}" for d in etapa.depende_de)
                lines.append(f"- **Depende de:** {deps}")
            else:
                lines.append("- **Depende de:** (nenhuma)")

            lines.append(f"- **Justificativa:** {etapa.justificativa}")
            lines.append("")

        if self.observacoes:
            lines.append(f"**Observações:** {self.observacoes}")

        return "\n".join(lines)


_SYSTEM_PROMPT = """\
Ты строишь планы запросов для mcp-russia. Каталог ниже может содержать
исторические названия features и tools, которые пока сохранены ради
совместимости. Твоя задача: по вопросу пользователя и каталогу tools
собрать структурированный план выполнения.

## Правила

1. Используй ТОЛЬКО tools из каталога. Никогда не придумывай новые names.
2. Используй точные имена tools с префиксом feature.
3. Заполняй параметры только теми именами и типами, которые есть в каталоге.
4. Для ссылок на результаты прошлых шагов используй placeholders вида
   {{etapa_N.campo}}.
5. Отвечай только по-русски.
6. Максимум 8 этапов на один план.

## Сложность

- **simples**: один прямой вызов
- **moderada**: 2-3 вызова с линейной зависимостью
- **complexa**: 4+ вызова, параллельные ветки или сравнение нескольких источников

## Комбинация источников

Полезные планы часто объединяют несколько features. Допустимые стратегии:

- **Enriquecimento**: обогатить данные второй feature
- **Comparação**: сравнить одинаковую метрику из разных источников
- **Contextualização**: добавить справочные, демографические или макроэкономические данные
- **Paralelismo**: независимые этапы могут выполняться параллельно

Если вопрос это допускает, предпочитай планы, где объединяются 2+ features.
В поле "resumo" коротко скажи, какие источники комбинируются.

## Поле observacoes

Используй его, чтобы указать:
- нужен ли ключ или другая авторизация
- известные ограничения данных
- какие именно cross-source связи делает план

## JSON schema

Верни ТОЛЬКО валидный JSON, без markdown и без ``` блоков.

{{
  "consulta": "pergunta original do usuário",
  "complexidade": "simples|moderada|complexa",
  "resumo": "resumo breve do plano em 1 frase",
  "etapas": [
    {{
      "etapa": 1,
      "descricao": "o que esta etapa faz",
      "tool": "feature_nome_da_tool",
      "parametros": {{"param": "valor"}},
      "depende_de": [],
      "justificativa": "por que esta etapa é necessária"
    }}
  ],
  "observacoes": "notas sobre autenticação, limitações, etc."
}}

## Примеры

### Пример 1: умеренно сложный запрос

Вопрос: "Quais foram os gastos do deputado Nikolas Ferreira em 2024?"

{{
  "consulta": "Quais foram os gastos do deputado Nikolas Ferreira em 2024?",
  "complexidade": "moderada",
  "resumo": "Buscar o deputado pelo nome na Câmara e consultar suas despesas em 2024.",
  "etapas": [
    {{
      "etapa": 1,
      "descricao": "Buscar deputado pelo nome",
      "tool": "camara_listar_deputados",
      "parametros": {{"nome": "Nikolas Ferreira"}},
      "depende_de": [],
      "justificativa": "Precisamos do ID do deputado para consultar despesas"
    }},
    {{
      "etapa": 2,
      "descricao": "Consultar despesas do deputado em 2024",
      "tool": "camara_despesas_deputado",
      "parametros": {{"id": "{{etapa_1.id}}", "ano": "2024"}},
      "depende_de": [1],
      "justificativa": "Obter os gastos usando o ID encontrado na etapa anterior"
    }}
  ],
  "observacoes": ""
}}

### Пример 2: сложный запрос с параллельными этапами

Вопрос: "Qual o gasto per capita com saúde em Minas Gerais?"

{{
  "consulta": "Qual o gasto per capita com saúde em Minas Gerais?",
  "complexidade": "complexa",
  "resumo": "Cruzar Transparência (gastos saúde) com IBGE (população MG).",
  "etapas": [
    {{
      "etapa": 1,
      "descricao": "Buscar gastos federais com saúde em MG",
      "tool": "transparencia_consultar_despesas",
      "parametros": {{"funcao": "saude", "uf": "MG", "ano": "2024"}},
      "depende_de": [],
      "justificativa": "Obter o valor total gasto com saúde no estado"
    }},
    {{
      "etapa": 2,
      "descricao": "Consultar população de Minas Gerais",
      "tool": "ibge_buscar_populacao",
      "parametros": {{"localidade": "31"}},
      "depende_de": [],
      "justificativa": "Obter a população para calcular o valor per capita"
    }}
  ],
  "observacoes": "Etapas 1 e 2 rodam em paralelo. \
Cálculo per capita feito pelo agente após ambas. \
Transparencia requer TRANSPARENCIA_API_KEY."
}}

## Каталог tools

{catalog}
"""


async def planejar_consulta_impl(query: str, catalog: str) -> str:
    """Call Anthropic API to build a structured execution plan.

    Args:
        query: Natural language question from the user.
        catalog: Pre-built catalog string of all tools.

    Returns:
        Markdown-rendered execution plan or error message.
    """
    try:
        import anthropic
    except ImportError:
        return (
            "Erro / Ошибка: пакет 'anthropic' не установлен. "
            "Установите его командой: pip install 'mcp-russia[llm]'\n\n"
            "В качестве альтернативы используйте tool 'search_tools'."
        )

    api_key = ANTHROPIC_API_KEY
    if not api_key:
        return (
            "Erro / Ошибка: переменная ANTHROPIC_API_KEY не настроена. "
            "Задайте ANTHROPIC_API_KEY, чтобы использовать этот meta-tool.\n\n"
            "В качестве альтернативы используйте tool 'search_tools'."
        )

    client = anthropic.AsyncAnthropic(api_key=api_key)
    system_prompt = _SYSTEM_PROMPT.format(catalog=catalog)

    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": query}],
        )
        block = response.content[0]
        raw_text = str(getattr(block, "text", ""))

        # Try to parse as structured plan
        try:
            plano = PlanoConsulta.model_validate(json.loads(raw_text))
            return plano.to_markdown()
        except (json.JSONDecodeError, Exception):
            logger.warning("Failed to parse plan JSON; returning raw text")
            return raw_text

    except Exception as e:
        logger.error("Anthropic API call failed: %s", e)
        return (
            f"Erro / Ошибка при обращении к LLM: {e}\n\n"
            "В качестве альтернативы используйте 'search_tools'."
        )
