"""Тесты инструментов модуля Минобрнауки."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.minobrnauki import tools as minobrnauki_tools


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_tipov_vuzov():
    ctx = _maket_konteksta()
    result = await minobrnauki_tools.spisok_tipov_vuzov(ctx=ctx)
    assert "Университет" in result


async def test_spisok_form_obucheniya():
    ctx = _maket_konteksta()
    result = await minobrnauki_tools.spisok_form_obucheniya(ctx=ctx)
    assert "Очная" in result


async def test_spisok_urovney_obrazovaniya():
    ctx = _maket_konteksta()
    result = await minobrnauki_tools.spisok_urovney_obrazovaniya(ctx=ctx)
    assert "Бакалавриат" in result


async def test_spisok_otrasley_nauki():
    ctx = _maket_konteksta()
    result = await minobrnauki_tools.spisok_otrasley_nauki(ctx=ctx)
    assert "Естественные" in result or "естественные" in result


async def test_spisok_tipov_grantov():
    ctx = _maket_konteksta()
    result = await minobrnauki_tools.spisok_tipov_grantov(ctx=ctx)
    assert "РНФ" in result


async def test_spisok_statusov_akkreditatsii():
    ctx = _maket_konteksta()
    result = await minobrnauki_tools.spisok_statusov_akkreditatsii(ctx=ctx)
    assert "Действует" in result


async def test_spisok_federalnyh_okrugov():
    ctx = _maket_konteksta()
    result = await minobrnauki_tools.spisok_federalnyh_okrugov(ctx=ctx)
    assert "Центральный" in result


async def test_info_vuza_by_name():
    ctx = _maket_konteksta()
    mock_data = {
        "nazvanie": "МГУ имени М.В. Ломоносова",
        "inn": "7710563663",
        "tip": "университет",
        "gorod": "Москва",
        "subiekt": "г. Москва",
        "status_akkreditatsii": "Действует",
        "data_akkreditatsii": "2020-01-01",
        "srok_deystviya": "2026-01-01",
        "nomer_svidetelstva": "1234",
        "adres": "Москва, Ленинские горы",
        "sayt": "https://msu.ru",
        "istochnik": "Рособрнадзор (obrnadzor.gov.ru)",
    }
    with patch.object(
        minobrnauki_tools.client, "poisk_akreditovannyh_vuzov", return_value=[mock_data]
    ):
        result = await minobrnauki_tools.info_vuza(ctx=ctx, nazvanie="МГУ")
    assert "МГУ" in result
    assert "Действует" in result


async def test_info_vuza_by_inn():
    ctx = _maket_konteksta()
    mock_data = {
        "nazvanie": "МФТИ",
        "inn": "5032003607",
        "tip": "университет",
        "status_akkreditatsii": "Действует",
    }
    with patch.object(minobrnauki_tools.client, "info_akkreditacii", return_value=mock_data):
        result = await minobrnauki_tools.info_vuza(ctx=ctx, inn="5032003607")
    assert "МФТИ" in result


async def test_info_vuza_ne_nayden():
    ctx = _maket_konteksta()
    with (
        patch.object(minobrnauki_tools.client, "poisk_akreditovannyh_vuzov", return_value=[]),
        patch.object(minobrnauki_tools.client, "info_akkreditacii", return_value=None),
    ):
        result = await minobrnauki_tools.info_vuza(ctx=ctx, nazvanie="НесуществующийВУЗ")
    assert "не найден" in result


async def test_programmy_vuza_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(minobrnauki_tools.client, "poisk_akreditovannyh_vuzov", return_value=[]):
        result = await minobrnauki_tools.programmy_vuza(ctx=ctx, vuz="НесуществующийВУЗ")
    assert "не найден" in result


async def test_granty_i_isledovaniya():
    ctx = _maket_konteksta()
    result = await minobrnauki_tools.granty_i_isledovaniya(ctx=ctx)
    assert "РНФ" in result


async def test_reyting_vuzov_pustoy():
    ctx = _maket_konteksta()
    with patch.object(minobrnauki_tools.client, "poluchit_reyting", return_value=[]):
        result = await minobrnauki_tools.reyting_vuzov(ctx=ctx, god=2024)
    assert "не получен" in result or "vuz.minobrnauki" in result


async def test_aspirantura():
    ctx = _maket_konteksta()
    result = await minobrnauki_tools.aspirantura(ctx=ctx)
    assert "аспирант" in result.lower()


async def test_poisk_licenziy_pustoy():
    ctx = _maket_konteksta()
    with patch.object(minobrnauki_tools.client, "poisk_licenziy", return_value=[]):
        result = await minobrnauki_tools.poisk_licenziy(ctx=ctx, inn="1234567890")
    assert "не найдены" in result


async def test_poisk_licenziy_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer_licenzii": "1234",
            "nazvanie": "МГУ",
            "status_licenzii": "Действует",
            "srok_deystviya": "2026-01-01",
        }
    ]
    with patch.object(minobrnauki_tools.client, "poisk_licenziy", return_value=mock_data):
        result = await minobrnauki_tools.poisk_licenziy(ctx=ctx, inn="7710563663")
    assert "МГУ" in result
    assert "1234" in result
