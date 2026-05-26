"""mcp-russia root server — auto-discovers and mounts all features.

This file uses FeatureRegistry for zero-touch feature onboarding.
You should NEVER need to edit this file to add a new feature.
Just create a new directory following the convention in ADR-001/002.

Usage:
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

from ._shared.batch import build_dispatch, execute_batch
from ._shared.feature import FeatureRegistry
from ._shared.lifespan import http_lifespan
from .settings import TOOL_SEARCH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("mcp-russia")


# ---------------------------------------------------------------------------
# Middleware — lightweight request logging
# ---------------------------------------------------------------------------
class RequestLoggingMiddleware(Middleware):
    """Log all tool calls, resource reads, and prompt requests."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        name = context.message.name
        logger.info("Tool call: %s", name)
        start = time.monotonic()
        result = await call_next(context)
        elapsed = time.monotonic() - start
        logger.info("Tool %s completed in %.2fs", name, elapsed)
        return result

    async def on_read_resource(
        self,
        context: MiddlewareContext[mt.ReadResourceRequestParams],
        call_next: CallNext[mt.ReadResourceRequestParams, ResourceResult],
    ) -> ResourceResult:
        uri = context.message.uri
        logger.info("Resource read: %s", uri)
        return await call_next(context)

    async def on_get_prompt(
        self,
        context: MiddlewareContext[mt.GetPromptRequestParams],
        call_next: CallNext[mt.GetPromptRequestParams, PromptResult],
    ) -> PromptResult:
        name = context.message.name
        logger.info("Prompt get: %s", name)
        return await call_next(context)


# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

# Create the root server
mcp = FastMCP("mcp-russia", lifespan=http_lifespan)

# Add middleware
mcp.add_middleware(RequestLoggingMiddleware())

# Auto-discover and mount all features
registry = FeatureRegistry()
registry.discover("mcp_brasil.data")
registry.discover("mcp_brasil.agentes")
registry.mount_all(mcp)

logger.info("\n%s", registry.summary())

# Build batch dispatch table for executar_lote
build_dispatch(registry)


# Expose a meta-tool for introspection
@mcp.tool(tags={"meta", "discovery"})
def listar_features() -> str:
    """Список всех доступных функций (API) в mcp-russia.

    Используйте этот инструмент, чтобы узнать, какие государственные API
    подключены и какие инструменты предоставляет каждая функция.

    Returns:
        Сводка активных функций с описанием и статусом аутентификации.
    """
    return registry.summary()


@mcp.tool(tags={"meta", "discovery"})
async def recomendar_tools(query: str, ctx: Context) -> str:
    """Рекомендует релевантные инструменты по запросу на естественном языке.

    Использует ИИ для понимания намерения и подбора наиболее подходящих
    инструментов mcp-russia с объяснением, когда и как их применять.

    Args:
        query: Вопрос или описание потребности
               (напр.: «нужны данные о расходах федерального бюджета»).
    """
    from ._shared.discovery import build_catalog, recomendar_tools_impl

    await ctx.info(f"Поиск рекомендаций для: {query}")
    catalog = build_catalog(registry)
    return await recomendar_tools_impl(query, catalog)


@mcp.tool(tags={"meta", "discovery", "планирование"})
async def planejar_consulta(query: str, ctx: Context) -> str:
    """Создаёт план выполнения для сложных запросов.

    Анализирует вопрос, определяет, какие инструменты использовать,
    в каком порядке, и какие этапы зависят от других. Полезно для запросов,
    требующих нескольких комбинированных вызовов.

    Args:
        query: Вопрос на естественном языке
               (напр.: «сравните расходы депутата X со средним значением»).
    """
    from ._shared.discovery import build_catalog
    from ._shared.planner import planejar_consulta_impl

    await ctx.info(f"Планирование запроса: {query}")
    catalog = build_catalog(registry)
    return await planejar_consulta_impl(query, catalog)


@mcp.tool(tags={"meta", "batch"})
async def executar_lote(consultas: list[dict[str, object]], ctx: Context) -> str:
    """Выполняет несколько инструментов за один вызов, параллельно.

    Используйте для ускорения, когда нужны данные из нескольких источников
    или с разными параметрами одновременно.

    Каждый запрос должен содержать полное имя инструмента (с пространством
    имён, напр.: «gosduma_poisk_deputata») и его аргументы.

    Args:
        consultas: Список запросов. Каждый элемент — объект с:
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
    await ctx.info(f"Выполнение пакета из {len(consultas)} запрос(ов)...")
    return await execute_batch(consultas, ctx)


# ---------------------------------------------------------------------------
# Tool Search Transform — configurable via MCP_RUSSIA_TOOL_SEARCH
# ---------------------------------------------------------------------------
_always_visible = [
    "listar_features",
    "recomendar_tools",
    "planejar_consulta",
    "executar_lote",
]

if TOOL_SEARCH == "bm25":
    from fastmcp.server.transforms.search import BM25SearchTransform

    mcp.add_transform(
        BM25SearchTransform(
            max_results=10,
            always_visible=_always_visible,
        )
    )
    logger.info("Tool search: BM25 (search_tools + call_tool)")

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
        logger.info("Tool search: CodeMode (experimental)")
    except ImportError:
        logger.warning(
            "CodeMode requires pydantic-monty. "
            "Install with: pip install 'fastmcp[code-mode]'. "
            "Falling back to BM25."
        )
        from fastmcp.server.transforms.search import BM25SearchTransform

        mcp.add_transform(
            BM25SearchTransform(
                max_results=10,
                always_visible=_always_visible,
            )
        )

else:
    logger.info("Tool search: none (all %d+ tools visible)", len(registry.features))


if __name__ == "__main__":
    mcp.run()
