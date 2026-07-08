"""Интеграционные тесты модуля официальных документов с fastmcp.Client."""

import pytest
from fastmcp import Client

from mcp_russia.agenty.deloproizvodstvo.server import mcp


class TestInstrumentyZaregistrirovany:
    @pytest.mark.asyncio
    async def test_vse_5_instrumentov_zaregistrirovany(self) -> None:
        async with Client(mcp) as c:
            spisok_instrumentov = await c.list_tools()
            imena = {t.name for t in spisok_instrumentov}
            ozhidayemyy = {
                "formatirovat_data_extenso",
                "generirovat_numeraciyu",
                "konsulitirovat_obrashchenie",
                "validirovat_dokument",
                "spisok_tipov_dokumentov",
            }
            assert ozhidayemyy.issubset(imena), f"Отсутствуют: {ozhidayemyy - imena}"

    @pytest.mark.asyncio
    async def test_instrumenty_imeyut_docstringi(self) -> None:
        async with Client(mcp) as c:
            spisok_instrumentov = await c.list_tools()
            for instrument in spisok_instrumentov:
                assert instrument.description, f"Инструмент {instrument.name} не имеет описания"


class TestResursyZaregistrirovany:
    @pytest.mark.asyncio
    async def test_vse_resursy_zaregistrirovany(self) -> None:
        async with Client(mcp) as c:
            resursy = await c.list_resources()
            adresa_uri = {str(r.uri) for r in resursy}
            ozhidayemyy = {
                "shablon://pismo",
                "shablon://prikaz",
                "shablon://rasporyazhenie",
                "shablon://akt",
                "shablon://spravka",
                "shablon://protokol",
                "shablon://dokladnaya_zapiska",
                "normy://manual",
                "normy://obrashcheniya",
                "normy://zaklyuchitelnye",
            }
            assert ozhidayemyy.issubset(adresa_uri), f"Отсутствуют: {ozhidayemyy - adresa_uri}"


class TestPromptyZaregistrirovany:
    @pytest.mark.asyncio
    async def test_vse_prompty_zaregistrirovany(self) -> None:
        async with Client(mcp) as c:
            prompty = await c.list_prompts()
            imena = {p.name for p in prompty}
            ozhidayemyy = {
                "redaktor_pismo",
                "redaktor_prikaz",
                "redaktor_rasporyazhenie",
                "redaktor_akt",
                "redaktor_spravka",
                "redaktor_protokol",
                "redaktor_dokladnaya_zapiska",
            }
            assert ozhidayemyy.issubset(imena), f"Отсутствуют: {ozhidayemyy - imena}"


class TestVypolnenieInstrumentov:
    @pytest.mark.asyncio
    async def test_formatirovat_data_e2e(self) -> None:
        async with Client(mcp) as c:
            rezultat = await c.call_tool(
                "formatirovat_data_extenso",
                {"gorod": "Санкт-Петербург"},
            )
            assert "г. Санкт-Петербург" in rezultat.data

    @pytest.mark.asyncio
    async def test_generirovat_numeraciyu_e2e(self) -> None:
        async with Client(mcp) as c:
            rezultat = await c.call_tool(
                "generirovat_numeraciyu",
                {"tip": "письмо", "nomer": 42, "god": 2026, "otdel": "Д-15"},
            )
            assert "ПИСЬМО № 42/2026/Д-15" in rezultat.data

    @pytest.mark.asyncio
    async def test_konsulitirovat_obrashchenie_e2e(self) -> None:
        async with Client(mcp) as c:
            rezultat = await c.call_tool(
                "konsulitirovat_obrashchenie",
                {"dolzhnost": "Губернатор"},
            )
            assert "Уважаемый господин Губернатор" in rezultat.data

    @pytest.mark.asyncio
    async def test_spisok_tipov_e2e(self) -> None:
        async with Client(mcp) as c:
            rezultat = await c.call_tool("spisok_tipov_dokumentov", {})
            assert "приказ" in rezultat.data
            assert "письмо" in rezultat.data


class TestVypolnenieResursov:
    @pytest.mark.asyncio
    async def test_chtenie_shablona_pismo(self) -> None:
        async with Client(mcp) as c:
            soderzhimoe = await c.read_resource("shablon://pismo")
            tekst = soderzhimoe[0].text if hasattr(soderzhimoe[0], "text") else str(soderzhimoe[0])
            assert "ПИСЬМО" in tekst or "ОФИЦИАЛЬНОЕ ПИСЬМО" in tekst

    @pytest.mark.asyncio
    async def test_chtenie_shablona_prikaz(self) -> None:
        async with Client(mcp) as c:
            soderzhimoe = await c.read_resource("shablon://prikaz")
            tekst = soderzhimoe[0].text if hasattr(soderzhimoe[0], "text") else str(soderzhimoe[0])
            assert "ПРИКАЗ" in tekst

    @pytest.mark.asyncio
    async def test_chtenie_normas_manual(self) -> None:
        async with Client(mcp) as c:
            soderzhimoe = await c.read_resource("normy://manual")
            tekst = soderzhimoe[0].text if hasattr(soderzhimoe[0], "text") else str(soderzhimoe[0])
            assert "ГОСТ" in tekst or "единообразие" in tekst.lower()

    @pytest.mark.asyncio
    async def test_chtenie_normas_obrashcheniya(self) -> None:
        async with Client(mcp) as c:
            soderzhimoe = await c.read_resource("normy://obrashcheniya")
            tekst = soderzhimoe[0].text if hasattr(soderzhimoe[0], "text") else str(soderzhimoe[0])
            assert "Президент" in tekst or "Уважаемый" in tekst


class TestVypolneniePromtov:
    @pytest.mark.asyncio
    async def test_prompt_pismo(self) -> None:
        async with Client(mcp) as c:
            rezultat = await c.get_prompt(
                "redaktor_pismo",
                arguments={
                    "adresat": "Иванов Иван Иванович",
                    "dolzhnost_adresata": "Министр",
                    "tema": "Согласование проекта",
                },
            )
            soobshcheniya = rezultat.messages
            assert len(soobshcheniya) == 2
            assert "ПИСЬМО" in soobshcheniya[0].content.text
            assert "Согласование проекта" in soobshcheniya[0].content.text

    @pytest.mark.asyncio
    async def test_prompt_prikaz(self) -> None:
        async with Client(mcp) as c:
            rezultat = await c.get_prompt(
                "redaktor_prikaz",
                arguments={"tema": "О проведении инвентаризации"},
            )
            soobshcheniya = rezultat.messages
            assert len(soobshcheniya) == 2
            assert "ПРИКАЗ" in soobshcheniya[0].content.text
            assert "инвентаризации" in soobshcheniya[0].content.text
