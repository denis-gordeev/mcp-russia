"""Тесты кэша с TTL."""

import time

import pytest

from mcp_russia._shared.cache import KeshSVremenemZhizni, kesh_s_vremenem_zhizni


class TestKeshSVremenemZhizni:
    def test_ustanovka_i_poluchenie(self) -> None:
        cache = KeshSVremenemZhizni(ttl=60)
        cache.set("key", "value")
        assert cache.get("key") == "value"

    def test_poluchenie_otsutstvuyushchego_klyucha(self) -> None:
        cache = KeshSVremenemZhizni(ttl=60)
        assert cache.get("missing") is None

    def test_istekshaya_zapis_vozvrashchaet_none(self) -> None:
        cache = KeshSVremenemZhizni(ttl=0.01)
        cache.set("key", "value")
        time.sleep(0.02)
        assert cache.get("key") is None

    def test_ochistka(self) -> None:
        cache = KeshSVremenemZhizni(ttl=60)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        assert cache.razmer == 0

    def test_vytyesnenie_pri_maks_razmere(self) -> None:
        cache = KeshSVremenemZhizni(ttl=60, maxsize=2)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)  # должен вытеснить самый старый
        assert cache.razmer <= 2

    def test_vytyesnyaet_istekshie_pervymi(self) -> None:
        cache = KeshSVremenemZhizni(ttl=0.01, maxsize=2)
        cache.set("a", 1)
        time.sleep(0.02)  # «a» истекает
        cache.set("b", 2)
        cache.set("c", 3)  # вытесняет истекший «a», а не «b»
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_svoystvo_razmer(self) -> None:
        cache = KeshSVremenemZhizni(ttl=60)
        assert cache.razmer == 0
        cache.set("x", 1)
        assert cache.razmer == 1


class TestDekoratorKeshaSVremenemZhizni:
    @pytest.mark.asyncio
    async def test_keshiruet_rezultat(self) -> None:
        call_count = 0

        @kesh_s_vremenem_zhizni(ttl=60)
        async def fetch_data(key: str) -> str:
            nonlocal call_count
            call_count += 1
            return f"result-{key}"

        result1 = await fetch_data("a")
        result2 = await fetch_data("a")
        assert result1 == "result-a"
        assert result2 == "result-a"
        assert call_count == 1  # второй вызов был из кэша

    @pytest.mark.asyncio
    async def test_raznye_argumenty_raznyy_kesh(self) -> None:
        call_count = 0

        @kesh_s_vremenem_zhizni(ttl=60)
        async def fetch(key: str) -> str:
            nonlocal call_count
            call_count += 1
            return f"result-{key}"

        await fetch("a")
        await fetch("b")
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_istekshiy_kesh_perezaprashivaet(self) -> None:
        call_count = 0

        @kesh_s_vremenem_zhizni(ttl=0.01)
        async def fetch() -> str:
            nonlocal call_count
            call_count += 1
            return "data"

        await fetch()
        time.sleep(0.02)
        await fetch()
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_atribut_kesha_dostupen(self) -> None:
        @kesh_s_vremenem_zhizni(ttl=60)
        async def fetch() -> str:
            return "data"

        assert hasattr(fetch, "cache")
        assert isinstance(fetch.cache, KeshSVremenemZhizni)

    @pytest.mark.asyncio
    async def test_ochistka_kesha(self) -> None:
        call_count = 0

        @kesh_s_vremenem_zhizni(ttl=60)
        async def fetch() -> str:
            nonlocal call_count
            call_count += 1
            return "data"

        await fetch()
        fetch.cache.clear()
        await fetch()
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_imenovannye_argumenty_v_klyuche_kesha(self) -> None:
        call_count = 0

        @kesh_s_vremenem_zhizni(ttl=60)
        async def fetch(uf: str = "SP") -> str:
            nonlocal call_count
            call_count += 1
            return f"data-{uf}"

        await fetch(uf="SP")
        await fetch(uf="RJ")
        await fetch(uf="SP")  # из кэша
        assert call_count == 2
