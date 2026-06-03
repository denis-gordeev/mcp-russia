"""Тесты инструментов модуля Роскомнадзора."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.roskomnadzor import tools as rkn_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_napravleniy():
    ctx = _mock_ctx()
    result = await rkn_tools.spisok_napravleniy(ctx)
    assert "Надзор в сфере СМИ" in result


async def test_spisok_tipov_licenziy():
    ctx = _mock_ctx()
    result = await rkn_tools.spisok_tipov_licenziy(ctx)
    assert "Интернет-доступ" in result


async def test_spisok_kategoriy_narusheniy():
    ctx = _mock_ctx()
    result = await rkn_tools.spisok_kategoriy_narusheniy(ctx)
    assert "Утечка персональных данных" in result


async def test_spisok_reestrov():
    ctx = _mock_ctx()
    result = await rkn_tools.spisok_reestrov(ctx)
    assert "запрещённых сайтов" in result


async def test_spisok_tipov_smi():
    ctx = _mock_ctx()
    result = await rkn_tools.spisok_tipov_smi(ctx)
    assert "Сетевое издание" in result


async def test_spisok_kategoriy_pd_operatorov():
    ctx = _mock_ctx()
    result = await rkn_tools.spisok_kategoriy_pd_operatorov(ctx)
    assert isinstance(result, str)
    assert len(result) > 0


async def test_info_licenzii_not_found():
    ctx = _mock_ctx()
    with patch.object(rkn_tools.client, "get_licenziya", return_value=None):
        result = await rkn_tools.info_licenzii(ctx, nomer_licenzii="LIC-001")
    assert "не найдена" in result


async def test_poisk_smi_empty():
    ctx = _mock_ctx()
    with patch.object(rkn_tools.client, "get_smi", return_value=[]):
        result = await rkn_tools.poisk_smi(ctx)
    assert "не найдены" in result


async def test_info_operatora_pd_empty():
    ctx = _mock_ctx()
    with patch.object(rkn_tools.client, "get_operator_pd", return_value=[]):
        result = await rkn_tools.info_operatora_pd(ctx)
    assert "не найдены" in result


async def test_poisk_narusheniy_empty():
    ctx = _mock_ctx()
    with patch.object(rkn_tools.client, "get_narusheniya", return_value=[]):
        result = await rkn_tools.poisk_narusheniy(ctx)
    assert "не найдены" in result


async def test_zapisi_reestra_no_id():
    ctx = _mock_ctx()
    result = await rkn_tools.zapisi_reestra(ctx, reestr_code="blocked_sites")
    assert "Укажите ID" in result


async def test_zapisi_reestra_not_found():
    ctx = _mock_ctx()
    with patch.object(rkn_tools.client, "get_zapis_reestra", return_value=None):
        result = await rkn_tools.zapisi_reestra(ctx, reestr_code="blocked_sites", zapisi_id="999")
    assert "не найдена" in result
