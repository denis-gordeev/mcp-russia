"""Тесты кэша с TTL."""

import time

import pytest

from mcp_russia._shared.cache import KeshSVremenemZhizni, kesh_s_vremenem_zhizni


class TestKeshSVremenemZhizni:
    def test_ustanovka_i_poluchenie(self) -> None:
        kesh = KeshSVremenemZhizni(vremya_zhizni=60)
        kesh.ustanovit("klyuch", "znachenie")
        assert kesh.poluchit("klyuch") == "znachenie"

    def test_poluchenie_otsutstvuyushchego_klyucha(self) -> None:
        kesh = KeshSVremenemZhizni(vremya_zhizni=60)
        assert kesh.poluchit("otsutstvuyushchiy") is None

    def test_istekshaya_zapis_vozvrashchaet_nichego(self) -> None:
        kesh = KeshSVremenemZhizni(vremya_zhizni=0.01)
        kesh.ustanovit("klyuch", "znachenie")
        time.sleep(0.02)
        assert kesh.poluchit("klyuch") is None

    def test_ochistka(self) -> None:
        kesh = KeshSVremenemZhizni(vremya_zhizni=60)
        kesh.ustanovit("a", 1)
        kesh.ustanovit("b", 2)
        kesh.ochistit()
        assert kesh.razmer == 0

    def test_vytyesnenie_pri_maks_razmere(self) -> None:
        kesh = KeshSVremenemZhizni(vremya_zhizni=60, maks_razmer=2)
        kesh.ustanovit("a", 1)
        kesh.ustanovit("b", 2)
        kesh.ustanovit("c", 3)  # должен вытеснить самый старый
        assert kesh.razmer <= 2

    def test_vytyesnyaet_istekshie_pervymi(self) -> None:
        kesh = KeshSVremenemZhizni(vremya_zhizni=0.01, maks_razmer=2)
        kesh.ustanovit("a", 1)
        time.sleep(0.02)  # «a» истекает
        kesh.ustanovit("b", 2)
        kesh.ustanovit("c", 3)  # вытесняет истекший «a», а не «b»
        assert kesh.poluchit("b") == 2
        assert kesh.poluchit("c") == 3

    def test_svoystvo_razmer(self) -> None:
        kesh = KeshSVremenemZhizni(vremya_zhizni=60)
        assert kesh.razmer == 0
        kesh.ustanovit("x", 1)
        assert kesh.razmer == 1


class TestDekoratorKeshaSVremenemZhizni:
    @pytest.mark.asyncio
    async def test_keshiruet_rezultat(self) -> None:
        schetchik_vyzovov = 0

        @kesh_s_vremenem_zhizni(vremya_zhizni=60)
        async def poluchit_dannye(klyuch: str) -> str:
            nonlocal schetchik_vyzovov
            schetchik_vyzovov += 1
            return f"rezultat-{klyuch}"

        rezultat1 = await poluchit_dannye("a")
        rezultat2 = await poluchit_dannye("a")
        assert rezultat1 == "rezultat-a"
        assert rezultat2 == "rezultat-a"
        assert schetchik_vyzovov == 1  # второй вызов был из кэша

    @pytest.mark.asyncio
    async def test_raznye_argumenty_raznyy_kesh(self) -> None:
        schetchik_vyzovov = 0

        @kesh_s_vremenem_zhizni(vremya_zhizni=60)
        async def poluchit(klyuch: str) -> str:
            nonlocal schetchik_vyzovov
            schetchik_vyzovov += 1
            return f"rezultat-{klyuch}"

        await poluchit("a")
        await poluchit("b")
        assert schetchik_vyzovov == 2

    @pytest.mark.asyncio
    async def test_istekshiy_kesh_perezaprashivaet(self) -> None:
        schetchik_vyzovov = 0

        @kesh_s_vremenem_zhizni(vremya_zhizni=0.01)
        async def poluchit() -> str:
            nonlocal schetchik_vyzovov
            schetchik_vyzovov += 1
            return "dannye"

        await poluchit()
        time.sleep(0.02)
        await poluchit()
        assert schetchik_vyzovov == 2

    @pytest.mark.asyncio
    async def test_atribut_kesha_dostupen(self) -> None:
        @kesh_s_vremenem_zhizni(vremya_zhizni=60)
        async def poluchit() -> str:
            return "dannye"

        assert hasattr(poluchit, "kesh")
        assert isinstance(poluchit.kesh, KeshSVremenemZhizni)

    @pytest.mark.asyncio
    async def test_ochistka_kesha(self) -> None:
        schetchik_vyzovov = 0

        @kesh_s_vremenem_zhizni(vremya_zhizni=60)
        async def poluchit() -> str:
            nonlocal schetchik_vyzovov
            schetchik_vyzovov += 1
            return "dannye"

        await poluchit()
        poluchit.kesh.ochistit()
        await poluchit()
        assert schetchik_vyzovov == 2

    @pytest.mark.asyncio
    async def test_imenovannye_argumenty_v_klyuche_kesha(self) -> None:
        schetchik_vyzovov = 0

        @kesh_s_vremenem_zhizni(vremya_zhizni=60)
        async def poluchit(subiekt: str = "77") -> str:
            nonlocal schetchik_vyzovov
            schetchik_vyzovov += 1
            return f"dannye-{subiekt}"

        await poluchit(subiekt="77")
        await poluchit(subiekt="16")
        await poluchit(subiekt="77")  # из кэша
        assert schetchik_vyzovov == 2
