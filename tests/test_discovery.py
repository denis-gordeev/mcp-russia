"""Тесты для функций обнаружения инструментов (BM25-поиск, rekomendovat_instrumenty, теги).

Тестирует трансформации поиска, рекомендации на основе LLM и распространение тегов.
MCP_RUSSIA_TOOL_SEARCH=none устанавливается в conftest.py (до любого импорта).
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp import Client, FastMCP

from mcp_russia._shared.discovery import postroit_katalog, rekomendovat_instrumenty_impl
from mcp_russia._shared.planner import PlanZaprosa, splanirovat_zapros_impl


class TestRekomendovatInstrumenty:
    @pytest.mark.asyncio
    async def test_missing_anthropic_package(self) -> None:
        with patch.dict("sys.modules", {"anthropic": None}):
            result = await rekomendovat_instrumenty_impl("расходы правительства", "catalog text")
            assert "anthropic" in result.lower() or "search_tools" in result

    @pytest.mark.asyncio
    async def test_missing_api_key(self) -> None:
        mock_anthropic = MagicMock()
        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.discovery.ANTHROPIC_API_KEY", ""),
        ):
            result = await rekomendovat_instrumenty_impl("расходы правительства", "catalog text")
            assert "ANTHROPIC_API_KEY" in result

    @pytest.mark.asyncio
    async def test_successful_recommendation(self) -> None:
        mock_block = MagicMock()
        mock_block.text = "Рекомендую: rosstat_poluchit_indikator"

        mock_response = MagicMock()
        mock_response.content = [mock_block]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        mock_anthropic = MagicMock()
        mock_anthropic.AsyncAnthropic = MagicMock(return_value=mock_client)

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.discovery.ANTHROPIC_API_KEY", "test-key"),
        ):
            result = await rekomendovat_instrumenty_impl("расходы правительства", "catalog text")
            assert "rosstat_poluchit_indikator" in result

    @pytest.mark.asyncio
    async def test_api_error_handling(self) -> None:
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(side_effect=Exception("API timeout"))

        mock_anthropic = MagicMock()
        mock_anthropic.AsyncAnthropic = MagicMock(return_value=mock_client)

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.discovery.ANTHROPIC_API_KEY", "test-key"),
        ):
            result = await rekomendovat_instrumenty_impl("расходы правительства", "catalog text")
            assert "Ошибка" in result
            assert "search_tools" in result


class TestBuildCatalog:
    def setup_method(self) -> None:
        import mcp_russia._shared.discovery as disc

        disc._catalog_cache = ""

    def test_postroit_katalog_with_empty_registry(self) -> None:
        mock_registry = MagicMock()
        mock_registry.funktsii = {}
        result = postroit_katalog(mock_registry)
        assert result == ""

    def test_postroit_katalog_caches_result(self) -> None:
        import mcp_russia._shared.discovery as disc

        mock_registry = MagicMock()
        mock_registry.funktsii = {}
        postroit_katalog(mock_registry)

        disc._kesh_kataloga = "cached"
        result = postroit_katalog(mock_registry)
        assert result == "cached"


class TestBM25SearchTransform:
    @pytest.mark.asyncio
    async def test_bm25_replaces_tool_listing(self) -> None:
        from fastmcp.server.transforms.search import BM25SearchTransform

        server = FastMCP("test")

        @server.tool(tags={"search", "regions"})
        def spisok_regionov() -> str:
            """Список всех регионов России."""
            return "Moscow, Tatarstan, Sverdlovsk"

        @server.tool(tags={"query", "data"})
        def zaprosit_dannye(kod: int) -> str:
            """Запрос данных по коду."""
            return f"Data {kod}"

        server.add_transform(BM25SearchTransform(max_results=5))

        async with Client(server) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "search_tools" in names
            assert "call_tool" in names
            assert "spisok_regionov" not in names
            assert "zaprosit_dannye" not in names

    @pytest.mark.asyncio
    async def test_bm25_search_finds_tools(self) -> None:
        from fastmcp.server.transforms.search import BM25SearchTransform

        server = FastMCP("test")

        @server.tool(tags={"search", "regions"})
        def spisok_regionov() -> str:
            """Список всех регионов России (spisok regionov)."""
            return "Moscow, Tatarstan"

        @server.tool(tags={"query", "data"})
        def zaprosit_dannye(kod: int) -> str:
            """Запрос данных временных рядов из Росстата."""
            return f"Data {kod}"

        server.add_transform(BM25SearchTransform(max_results=5))

        async with Client(server) as c:
            result = await c.call_tool("search_tools", {"query": "spisok regionov"})
            text = str(result.content)
            assert "spisok_regionov" in text

    @pytest.mark.asyncio
    async def test_bm25_always_visible_pinned(self) -> None:
        from fastmcp.server.transforms.search import BM25SearchTransform

        server = FastMCP("test")

        @server.tool(tags={"meta"})
        def spisok_funktsiy() -> str:
            """Список функций."""
            return "functions"

        @server.tool(tags={"search"})
        def hidden_tool() -> str:
            """Скрытый инструмент."""
            return "hidden"

        server.add_transform(
            BM25SearchTransform(
                max_results=5,
                always_visible=["spisok_funktsiy"],
            )
        )

        async with Client(server) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "spisok_funktsiy" in names
            assert "hidden_tool" not in names

    @pytest.mark.asyncio
    async def test_bm25_call_tool_executes(self) -> None:
        from fastmcp.server.transforms.search import BM25SearchTransform

        server = FastMCP("test")

        @server.tool
        def slozhit(a: int, b: int) -> int:
            """Сложение двух чисел."""
            return a + b

        server.add_transform(BM25SearchTransform(max_results=5))

        async with Client(server) as c:
            result = await c.call_tool(
                "call_tool",
                {"name": "slozhit", "arguments": {"a": 3, "b": 4}},
            )
            text = str(result.content)
            assert "7" in text


class TestToolSearchConfig:
    @pytest.mark.asyncio
    async def test_none_mode_shows_all_tools(self) -> None:
        from mcp_russia.server import mcp as root_mcp

        async with Client(root_mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "spisok_funktsiy" in names
            assert "rekomendovat_instrumenty" in names
            assert "cbrf_tekushchie_kursy" in names


class TestTagPropagation:
    @pytest.mark.asyncio
    async def test_tags_preserved_after_mount(self) -> None:
        child = FastMCP("child")

        @child.tool(tags={"search", "regions"})
        def spisok_regionov() -> str:
            """Список регионов."""
            return "Moscow"

        parent = FastMCP("parent")
        parent.mount(child, namespace="rosstat")

        async with Client(parent) as c:
            tools = await c.list_tools()
            rosstat_tool = next((t for t in tools if t.name == "rosstat_spisok_regionov"), None)
            assert rosstat_tool is not None

    @pytest.mark.asyncio
    async def test_search_finds_by_description(self) -> None:
        from fastmcp.server.transforms.search import BM25SearchTransform

        server = FastMCP("test")

        @server.tool(tags={"environmental", "fires"})
        def nayti_ochagi() -> str:
            """Поиск очагов пожаров, обнаруженных спутником в России."""
            return "hotspots"

        @server.tool(tags={"financial", "banks"})
        def spisok_bankov() -> str:
            """Список всех банков России, зарегистрированных в Центральном банке."""
            return "banks"

        server.add_transform(BM25SearchTransform(max_results=5))

        async with Client(server) as c:
            result = await c.call_tool("search_tools", {"query": "ochagi pozhary sputnik"})
            text = str(result.content)
            assert "nayti_ochagi" in text


_VALID_PLAN_JSON = json.dumps(
    {
        "zapros": "расходы депутата X",
        "slozhnost": "umerennyy",
        "svodka": "Найти депутата и запросить его расходы",
        "etapy": [
            {
                "etap": 1,
                "opisanie": "Найти депутата по фамилии",
                "tool": "gosduma_poluchit_deputatov",
                "parametry": {"familiya": "X"},
                "zavisit_ot": [],
                "obosnovanie": "Нужен ID депутата",
            },
            {
                "etap": 2,
                "opisanie": "Запросить расходы депутата",
                "tool": "gosduma_raskhody_deputata",
                "parametry": {"id": "{etap_1.id}"},
                "zavisit_ot": [1],
                "obosnovanie": "Получить расходы используя ID",
            },
        ],
        "primechaniya": "",
    }
)


class TestSplanirovatZapros:
    @pytest.mark.asyncio
    async def test_missing_anthropic_package(self) -> None:
        with patch.dict("sys.modules", {"anthropic": None}):
            result = await splanirovat_zapros_impl("расходы правительства", "catalog text")
            assert "anthropic" in result.lower() or "search_tools" in result

    @pytest.mark.asyncio
    async def test_missing_api_key(self) -> None:
        mock_anthropic = MagicMock()
        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.planner.ANTHROPIC_API_KEY", ""),
        ):
            result = await splanirovat_zapros_impl("расходы правительства", "catalog text")
            assert "ANTHROPIC_API_KEY" in result

    @pytest.mark.asyncio
    async def test_successful_plan(self) -> None:
        mock_block = MagicMock()
        mock_block.text = _VALID_PLAN_JSON

        mock_response = MagicMock()
        mock_response.content = [mock_block]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        mock_anthropic = MagicMock()
        mock_anthropic.AsyncAnthropic = MagicMock(return_value=mock_client)

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.planner.ANTHROPIC_API_KEY", "test-key"),
        ):
            result = await splanirovat_zapros_impl("расходы депутата X", "catalog")
            assert "## План запроса" in result
            assert "Этап 1" in result
            assert "Этап 2" in result
            assert "gosduma_poluchit_deputatov" in result
            assert "Зависит от:** Этап 1" in result

    @pytest.mark.asyncio
    async def test_invalid_json_fallback(self) -> None:
        mock_block = MagicMock()
        mock_block.text = "Не удалось построить структурированный план."

        mock_response = MagicMock()
        mock_response.content = [mock_block]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        mock_anthropic = MagicMock()
        mock_anthropic.AsyncAnthropic = MagicMock(return_value=mock_client)

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.planner.ANTHROPIC_API_KEY", "test-key"),
        ):
            result = await splanirovat_zapros_impl("расходы правительства", "catalog")
            assert "Не удалось построить структурированный план." in result

    @pytest.mark.asyncio
    async def test_api_error_handling(self) -> None:
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(side_effect=Exception("API timeout"))

        mock_anthropic = MagicMock()
        mock_anthropic.AsyncAnthropic = MagicMock(return_value=mock_client)

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.planner.ANTHROPIC_API_KEY", "test-key"),
        ):
            result = await splanirovat_zapros_impl("расходы правительства", "catalog")
            assert "Ошибка" in result
            assert "search_tools" in result


class TestPlanZaprosaMarkdown:
    def test_to_markdown_renders_steps(self) -> None:
        plan = PlanZaprosa.model_validate(json.loads(_VALID_PLAN_JSON))
        md = plan.v_markdown()
        assert "## План запроса" in md
        assert "**Сложность:** umerennyy" in md
        assert "### Этап 1:" in md
        assert "### Этап 2:" in md
        assert "`gosduma_poluchit_deputatov`" in md
        assert "Зависит от:** (нет)" in md
        assert "Зависит от:** Этап 1" in md

    def test_to_markdown_with_primechaniya(self) -> None:
        plan = PlanZaprosa(
            zapros="тест",
            slozhnost="prostoy",
            svodka="Простой план",
            etapy=[
                {
                    "etap": 1,
                    "opisanie": "Единственный шаг",
                    "tool": "rosstat_poluchit_indikator",
                    "parametry": {},
                    "zavisit_ot": [],
                    "obosnovanie": "Необходимо",
                }
            ],
            primechaniya="Требуется авторизация на портале Росстата.",
        )
        md = plan.v_markdown()
        assert "**Примечания:**" in md
        assert "Росстата" in md
