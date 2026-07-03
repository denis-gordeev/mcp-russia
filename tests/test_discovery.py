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
    async def test_otsutstvuyushchiy_paket_antropic(self) -> None:
        with patch.dict("sys.modules", {"anthropic": None}):
            rezultat = await rekomendovat_instrumenty_impl(
                "расходы правительства", "tekst_kataloga"
            )
            assert "anthropic" in rezultat.lower() or "search_tools" in rezultat

    @pytest.mark.asyncio
    async def test_otsutstvuyushchiy_klyuch_api(self) -> None:
        mock_anthropic = MagicMock()
        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.discovery.KLYUCH_ANTHROPIC_API", ""),
        ):
            rezultat = await rekomendovat_instrumenty_impl(
                "расходы правительства", "tekst_kataloga"
            )
            assert "ANTHROPIC_API_KEY" in rezultat

    @pytest.mark.asyncio
    async def test_uspeshnaya_rekomendatsiya(self) -> None:
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
            patch("mcp_russia._shared.discovery.KLYUCH_ANTHROPIC_API", "test-key"),
        ):
            rezultat = await rekomendovat_instrumenty_impl(
                "расходы правительства", "tekst_kataloga"
            )
            assert "rosstat_poluchit_indikator" in rezultat

    @pytest.mark.asyncio
    async def test_obrabotka_oshibki_api(self) -> None:
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(side_effect=Exception("API timeout"))

        mock_anthropic = MagicMock()
        mock_anthropic.AsyncAnthropic = MagicMock(return_value=mock_client)

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.discovery.KLYUCH_ANTHROPIC_API", "test-key"),
        ):
            rezultat = await rekomendovat_instrumenty_impl(
                "расходы правительства", "tekst_kataloga"
            )
            assert "Ошибка" in rezultat
            assert "search_tools" in rezultat


class TestPostroenieKataloga:
    def setup_method(self) -> None:
        import mcp_russia._shared.discovery as disc

        disc._kesh_kataloga = ""

    def test_postroit_katalog_s_pustym_reestrom(self) -> None:
        mock_registry = MagicMock()
        mock_registry.funktsii = {}
        rezultat = postroit_katalog(mock_registry)
        assert rezultat == ""

    def test_postroit_katalog_keshiruet_rezultat(self) -> None:
        import mcp_russia._shared.discovery as disc

        mock_registry = MagicMock()
        mock_registry.funktsii = {}
        postroit_katalog(mock_registry)

        disc._kesh_kataloga = "cached"
        rezultat = postroit_katalog(mock_registry)
        assert rezultat == "cached"


class TestTransformatsiyaBM25:
    @pytest.mark.asyncio
    async def test_bm25_zamenyaet_spisok_instrumentov(self) -> None:
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
    async def test_bm25_poisk_nakhodit_instrumenty(self) -> None:
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
            rezultat = await c.call_tool("search_tools", {"query": "spisok regionov"})
            tekst = str(rezultat.content)
            assert "spisok_regionov" in tekst

    @pytest.mark.asyncio
    async def test_bm25_vsegda_vidimye_zakrepleny(self) -> None:
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
    async def test_bm25_vyzov_instrumenta_vypolnyaetsya(self) -> None:
        from fastmcp.server.transforms.search import BM25SearchTransform

        server = FastMCP("test")

        @server.tool
        def slozhit(a: int, b: int) -> int:
            """Сложение двух чисел."""
            return a + b

        server.add_transform(BM25SearchTransform(max_results=5))

        async with Client(server) as c:
            rezultat = await c.call_tool(
                "call_tool",
                {"name": "slozhit", "arguments": {"a": 3, "b": 4}},
            )
            tekst = str(rezultat.content)
            assert "7" in tekst


class TestKonfiguratsiyaPoiskaInstrumentov:
    @pytest.mark.asyncio
    async def test_rezhim_none_pokazyvaet_vse_instrumenty(self) -> None:
        from mcp_russia.server import mcp as root_mcp

        async with Client(root_mcp) as c:
            tools = await c.list_tools()
            names = {t.name for t in tools}
            assert "spisok_funktsiy" in names
            assert "rekomendovat_instrumenty" in names
            assert "cbrf_tekushchie_kursy" in names


class TestRasprostranenieTegov:
    @pytest.mark.asyncio
    async def test_tegi_sokhranyayutsya_posle_montirovaniya(self) -> None:
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
    async def test_poisk_nakhodit_po_opisaniyu(self) -> None:
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
            rezultat = await c.call_tool("search_tools", {"query": "ochagi pozhary sputnik"})
            tekst = str(rezultat.content)
            assert "nayti_ochagi" in tekst


_VALID_PLAN_JSON = json.dumps(
    {
        "zapros": "расходы депутата X",
        "slozhnost": "umerennyy",
        "svodka": "Найти депутата и запросить его расходы",
        "etapy": [
            {
                "etap": 1,
                "opisanie": "Найти депутата по фамилии",
                "instrument": "gosduma_poluchit_deputatov",
                "parametry": {"familiya": "X"},
                "zavisit_ot": [],
                "obosnovanie": "Нужен ID депутата",
            },
            {
                "etap": 2,
                "opisanie": "Запросить расходы депутата",
                "instrument": "gosduma_raskhody_deputata",
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
    async def test_otsutstvuyushchiy_paket_antropic(self) -> None:
        with patch.dict("sys.modules", {"anthropic": None}):
            rezultat = await splanirovat_zapros_impl("расходы правительства", "tekst_kataloga")
            assert "anthropic" in rezultat.lower() or "search_tools" in rezultat

    @pytest.mark.asyncio
    async def test_otsutstvuyushchiy_klyuch_api(self) -> None:
        mock_anthropic = MagicMock()
        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.planner.KLYUCH_ANTHROPIC_API", ""),
        ):
            rezultat = await splanirovat_zapros_impl("расходы правительства", "tekst_kataloga")
            assert "ANTHROPIC_API_KEY" in rezultat

    @pytest.mark.asyncio
    async def test_uspeshnyy_plan(self) -> None:
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
            patch("mcp_russia._shared.planner.KLYUCH_ANTHROPIC_API", "test-key"),
        ):
            rezultat = await splanirovat_zapros_impl("расходы депутата X", "catalog")
            assert "## План запроса" in rezultat
            assert "Этап 1" in rezultat
            assert "Этап 2" in rezultat
            assert "gosduma_poluchit_deputatov" in rezultat
            assert "Зависит от:** Этап 1" in rezultat

    @pytest.mark.asyncio
    async def test_rezervnyy_variant_pri_nekorrektnom_json(self) -> None:
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
            patch("mcp_russia._shared.planner.KLYUCH_ANTHROPIC_API", "test-key"),
        ):
            rezultat = await splanirovat_zapros_impl("расходы правительства", "catalog")
            assert "Не удалось построить структурированный план." in rezultat

    @pytest.mark.asyncio
    async def test_obrabotka_oshibki_api(self) -> None:
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(side_effect=Exception("API timeout"))

        mock_anthropic = MagicMock()
        mock_anthropic.AsyncAnthropic = MagicMock(return_value=mock_client)

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch("mcp_russia._shared.planner.KLYUCH_ANTHROPIC_API", "test-key"),
        ):
            rezultat = await splanirovat_zapros_impl("расходы правительства", "catalog")
            assert "Ошибка" in rezultat
            assert "search_tools" in rezultat


class TestPlanZaprosaVMarkdown:
    def test_v_markdown_otobrazhaet_etapy(self) -> None:
        plan = PlanZaprosa.model_validate(json.loads(_VALID_PLAN_JSON))
        md = plan.v_markdown()
        assert "## План запроса" in md
        assert "**Сложность:** umerennyy" in md
        assert "### Этап 1:" in md
        assert "### Этап 2:" in md
        assert "`gosduma_poluchit_deputatov`" in md
        assert "Зависит от:** (нет)" in md
        assert "Зависит от:** Этап 1" in md

    def test_v_markdown_s_primechaniyami(self) -> None:
        plan = PlanZaprosa(
            zapros="тест",
            slozhnost="prostoy",
            svodka="Простой план",
            etapy=[
                {
                    "etap": 1,
                    "opisanie": "Единственный шаг",
                    "instrument": "rosstat_poluchit_indikator",
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
