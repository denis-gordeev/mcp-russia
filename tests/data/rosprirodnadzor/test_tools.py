"""Тесты инструментов модуля Росприроднадзор."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosprirodnadzor import tools as rpn_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_vidov_nadzora():
    ctx = _mock_ctx()
    result = await rpn_tools.spisok_vidov_nadzora(ctx)
    assert "надзор" in result.lower() or "экологический" in result.lower()


async def test_spisok_kategoriy_obnv():
    ctx = _mock_ctx()
    result = await rpn_tools.spisok_kategoriy_obnv(ctx)
    assert "категория" in result.lower() or "значительн" in result.lower()


async def test_spisok_vidov_litsenziy_nedra():
    ctx = _mock_ctx()
    result = await rpn_tools.spisok_vidov_litsenziy_nedra(ctx)
    assert "лицензий" in result.lower() or "недр" in result.lower()


async def test_poisk_proverok_empty():
    ctx = _mock_ctx()
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=[]):
        result = await rpn_tools.poisk_proverok(ctx)
    assert isinstance(result, str)


async def test_poisk_proverok_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "nomer": "ПР-2026-001",
            "organizaciya": "ООО «Промышленник»",
            "vid_nadzora": "Государственный экологический надзор",
            "data_nachala": "2026-02-01",
            "data_okonchaniya": "2026-03-01",
            "status": "Завершено",
            "vyavleno_narusheniy": 3,
        },
    ]
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=mock_data):
        result = await rpn_tools.poisk_proverok(ctx)
    assert "Промышленник" in result


async def test_info_proverki_not_found():
    ctx = _mock_ctx()
    with patch.object(rpn_tools.client, "info_proverki", return_value=None):
        result = await rpn_tools.info_proverki("nonexistent", ctx)
    assert "не найдена" in result


async def test_info_proverki_found():
    ctx = _mock_ctx()
    mock_data = {
        "nomer": "ПР-2026-001",
        "organizaciya": "ООО «Промышленник»",
        "vid_nadzora": "Государственный экологический надзор",
        "data_nachala": "2026-02-01",
        "data_okonchaniya": "2026-03-01",
        "status": "Завершено",
        "vyavleno_narusheniy": 3,
    }
    with patch.object(rpn_tools.client, "info_proverki", return_value=mock_data):
        result = await rpn_tools.info_proverki("ПР-2026-001", ctx)
    assert "Промышленник" in result


async def test_poisk_obektov_negativnogo_empty():
    ctx = _mock_ctx()
    with patch.object(rpn_tools.client, "poisk_obektov_negativnogo", return_value=[]):
        result = await rpn_tools.poisk_obektov_negativnogo(ctx)
    assert isinstance(result, str)


async def test_poisk_obektov_negativnogo_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "nomer": "ОНВ-001",
            "nazvanie": "Завод «Химпром»",
            "kategoriya": "I — значительное",
            "region": "Волгоградская область",
            "vid_deyatelnosti": "Химическое производство",
        },
    ]
    with patch.object(rpn_tools.client, "poisk_obektov_negativnogo", return_value=mock_data):
        result = await rpn_tools.poisk_obektov_negativnogo(ctx)
    assert "Химпром" in result


async def test_poisk_litsenziy_nedra_empty():
    ctx = _mock_ctx()
    with patch.object(rpn_tools.client, "poisk_litsenziy_nedra", return_value=[]):
        result = await rpn_tools.poisk_litsenziy_nedra(ctx)
    assert isinstance(result, str)


async def test_poisk_litsenziy_nedra_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "nomer": "ЛЦ-001",
            "vid_litsenzii": "Добыча полезных ископаемых",
            "territory": "ХМАО-Югра",
            "srok_deystviya": "2020–2030",
            "derzhatel": "ПАО «Газпром»",
        },
    ]
    with patch.object(rpn_tools.client, "poisk_litsenziy_nedra", return_value=mock_data):
        result = await rpn_tools.poisk_litsenziy_nedra(ctx)
    assert "Газпром" in result
