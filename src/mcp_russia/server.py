"""Корневой сервер mcp-russia — автоматическое обнаружение и монтирование функций.

Использует ReyestrFunktsiy для подключения функций без ручного редактирования.
Для добавления новой функции достаточно создать директорию по конвенции ADR-001/002.

Запуск:
    fastmcp run mcp_russia.server:mcp
    fastmcp run mcp_russia.server:mcp --transport http --port 8000
"""

import logging
import time

import mcp.types as mt
from fastmcp import Context, FastMCP
from fastmcp.prompts import PromptResult
from fastmcp.resources import ResourceResult
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools import ToolResult

from ._shared.batch import postroit_dispetcherizatsiyu, vypolnit_paket_vnutrenniy
from ._shared.feature import ReyestrFunktsiy
from ._shared.lifespan import http_zhiznennyy_tsikl
from .settings import TOOL_SEARCH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("mcp-russia")


# ---------------------------------------------------------------------------
# Промежуточный слой — логирование запросов
# ---------------------------------------------------------------------------
class PosrednikLogirovaniyaZaprosov(Middleware):
    """Логирует все вызовы инструментов, чтения ресурсов и запросы промптов."""

    async def pri_vyzove_instrumenta(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        """Логирование вызова инструмента с замером времени."""
        name = context.message.name
        logger.info("Вызов инструмента: %s", name)
        start = time.monotonic()
        result = await call_next(context)
        elapsed = time.monotonic() - start
        logger.info("Инструмент %s завершён за %.2fс", name, elapsed)
        return result

    async def pri_chtenii_resursa(
        self,
        context: MiddlewareContext[mt.ReadResourceRequestParams],
        call_next: CallNext[mt.ReadResourceRequestParams, ResourceResult],
    ) -> ResourceResult:
        """Логирование чтения ресурса."""
        uri = context.message.uri
        logger.info("Чтение ресурса: %s", uri)
        return await call_next(context)

    async def pri_zaprose_prompta(
        self,
        context: MiddlewareContext[mt.GetPromptRequestParams],
        call_next: CallNext[mt.GetPromptRequestParams, PromptResult],
    ) -> PromptResult:
        """Логирование запроса промпта."""
        name = context.message.name
        logger.info("Запрос промпта: %s", name)
        return await call_next(context)


# ---------------------------------------------------------------------------
# Настройка сервера
# ---------------------------------------------------------------------------

# Создание корневого сервера
mcp = FastMCP("mcp-russia", lifespan=http_zhiznennyy_tsikl)

# Добавление промежуточного слоя
mcp.add_middleware(PosrednikLogirovaniyaZaprosov())

# Автоматическое обнаружение и монтирование всех функций
registry = ReyestrFunktsiy()
registry.obnaruzhit("mcp_russia.data")
registry.obnaruzhit("mcp_russia.agenty")
registry.smontirovat_vse(mcp)

logger.info("\n%s", registry.svodka())

# Формирование таблицы диспетчеризации для vypolnit_paket
postroit_dispetcherizatsiyu(registry)


# Мета-инструмент для интроспекции
@mcp.tool(tags={"meta", "discovery"})
def spisok_funktsiy() -> str:
    """Список всех доступных функций (API) в mcp-russia.

    Используйте этот инструмент, чтобы узнать, какие государственные API
    подключены и какие инструменты предоставляет каждая функция.

    Возвращает:
        Сводка активных функций с описанием и статусом аутентификации.
    """
    return registry.svodka()


@mcp.tool(tags={"meta", "discovery"})
async def rekomendovat_instrumenty(query: str, ctx: Context) -> str:
    """Рекомендует релевантные инструменты по запросу на естественном языке.

    Использует ИИ для понимания намерения и подбора наиболее подходящих
    инструментов mcp-russia с объяснением, когда и как их применять.

    Аргументы:
        query: Вопрос или описание потребности
               (напр.: «нужны данные о расходах федерального бюджета»).
    """
    from ._shared.discovery import postroit_katalog, rekomendovat_instrumenty_impl

    await ctx.info(f"Поиск рекомендаций для: {query}")
    catalog = postroit_katalog(registry)
    return await rekomendovat_instrumenty_impl(query, catalog)


@mcp.tool(tags={"meta", "discovery", "планирование"})
async def splanirovat_zapros(query: str, ctx: Context) -> str:
    """Создаёт план выполнения для сложных запросов.

    Анализирует вопрос, определяет, какие инструменты использовать,
    в каком порядке, и какие этапы зависят от других. Полезно для запросов,
    требующих нескольких комбинированных вызовов.

    Аргументы:
        query: Вопрос на естественном языке
               (напр.: «сравните расходы депутата X со средним значением»).
    """
    from ._shared.discovery import postroit_katalog
    from ._shared.planner import splanirovat_zapros_impl

    await ctx.info(f"Планирование запроса: {query}")
    catalog = postroit_katalog(registry)
    return await splanirovat_zapros_impl(query, catalog)


@mcp.tool(tags={"meta", "batch"})
async def vypolnit_paket(zaprosy: list[dict[str, object]], ctx: Context) -> str:
    """Выполняет несколько инструментов за один вызов, параллельно.

    Используйте для ускорения, когда нужны данные из нескольких источников
    или с разными параметрами одновременно.

    Каждый запрос должен содержать полное имя инструмента (с пространством
    имён, напр.: «gosduma_poisk_deputata») и его аргументы.

    Аргументы:
        zaprosy: Список запросов. Каждый элемент — объект с:
                 - "tool": полное имя инструмента
                   (напр.: «gosduma_info_deputata»)
                 - "args": объект с аргументами инструмента
                 Пример: [
                   {"tool": "gosduma_info_deputata",
                    "args": {"deputat_id": 99100142}},
                   {"tool": "cbrf_kursy_valyut",
                    "args": {}}
                 ]
    """
    await ctx.info(f"Выполнение пакета из {len(zaprosy)} запрос(ов)...")
    return await vypolnit_paket_vnutrenniy(zaprosy, ctx)


# ---------------------------------------------------------------------------
# Трансформация поиска инструментов — настраивается через MCP_RUSSIA_TOOL_SEARCH
# ---------------------------------------------------------------------------
_vsegda_vidimye = [
    "spisok_funktsiy",
    "rekomendovat_instrumenty",
    "splanirovat_zapros",
    "vypolnit_paket",
]

if TOOL_SEARCH == "bm25":
    from fastmcp.server.transforms.search import BM25SearchTransform

    mcp.add_transform(
        BM25SearchTransform(
            max_results=10,
            always_visible=_vsegda_vidimye,
        )
    )
    logger.info("Поиск инструментов: BM25 (search_tools + call_tool)")

elif TOOL_SEARCH == "code_mode":
    try:
        from fastmcp.experimental.transforms.code_mode import (
            CodeMode,
            GetSchemas,
            GetTags,
            Search,
        )

        mcp.add_transform(
            CodeMode(
                discovery_tools=[GetTags(name="get_tags"), Search(name="search"), GetSchemas()],
            )
        )
        logger.info("Поиск инструментов: CodeMode (экспериментальный)")
    except ImportError:
        logger.warning(
            "CodeMode требует pydantic-monty. "
            "Установите: pip install 'fastmcp[code-mode]'. "
            "Откат к BM25."
        )
        from fastmcp.server.transforms.search import BM25SearchTransform

        mcp.add_transform(
            BM25SearchTransform(
                max_results=10,
                always_visible=_vsegda_vidimye,
            )
        )

else:
    logger.info(
        "Поиск инструментов: отключён (все %d+ инструментов видны)",
        len(registry.funktsii),
    )


if __name__ == "__main__":
    mcp.run()
