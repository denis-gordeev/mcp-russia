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
    with patch.object(rkn_tools.client, "poisk_licenziy", return_value=[]):
        result = await rkn_tools.info_licenzii(ctx, nomer_licenzii="LIC-001")
    assert "не найдена" in result


async def test_info_licenzii_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "nomer": "LIC-001",
            "organizaciya": "ООО Тест",
            "tip_licenzii": "Интернет-доступ",
            "data_vydachi": "2023-01-01",
            "data_okonchaniya": "2028-01-01",
            "status": "Действует",
            "territoriya": "Российская Федерация",
            "istochnik": "Реестр лицензий (rkn.gov.ru)",
        }
    ]
    with patch.object(rkn_tools.client, "poisk_licenziy", return_value=mock_data):
        result = await rkn_tools.info_licenzii(ctx, nomer_licenzii="LIC-001")
    assert "LIC-001" in result
    assert "ООО Тест" in result


async def test_poisk_smi_empty():
    ctx = _mock_ctx()
    with patch.object(rkn_tools.client, "poisk_smi", return_value=[]):
        result = await rkn_tools.poisk_smi(ctx)
    assert "не найдены" in result


async def test_info_operatora_pd_empty():
    ctx = _mock_ctx()
    with patch.object(rkn_tools.client, "poisk_operatora_pd", return_value=[]):
        result = await rkn_tools.info_operatora_pd(ctx)
    assert "не найдены" in result


async def test_info_operatora_pd_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "naimenovanie": "ООО Тест",
            "inn": "7710563663",
            "kategoriya": "Коммерческие организации",
            "tsel_obrabotki": "Кадровый учёт",
            "status": "Зарегистрирован",
        }
    ]
    with patch.object(rkn_tools.client, "poisk_operatora_pd", return_value=mock_data):
        result = await rkn_tools.info_operatora_pd(ctx, inn="7710563663")
    assert "ООО Тест" in result


async def test_proverka_blokirovki_not_blocked():
    ctx = _mock_ctx()
    with patch.object(
        rkn_tools.client,
        "proverka_blokirovki",
        return_value={"domain": "example.com", "blokirovka": False, "istochnik": "ЕАИС"},
    ):
        result = await rkn_tools.proverka_blokirovki(ctx, domen="example.com")
    assert "НЕ найден" in result


async def test_proverka_blokirovki_blocked():
    ctx = _mock_ctx()
    with patch.object(
        rkn_tools.client,
        "proverka_blokirovki",
        return_value={
            "domain": "blocked-site.ru",
            "blokirovka": True,
            "osnovanie": "Экстремистские материалы",
            "data_vklyucheniya": "2024-01-01",
            "organy": "Роскомнадзор",
        },
    ):
        result = await rkn_tools.proverka_blokirovki(ctx, domen="blocked-site.ru")
    assert "ЗАБЛОКИРОВАН" in result


async def test_poisk_ori_empty():
    ctx = _mock_ctx()
    with patch.object(rkn_tools.client, "poisk_ori", return_value=[]):
        result = await rkn_tools.poisk_ori(ctx)
    assert "не найдены" in result


async def test_zapisi_reestra_found():
    ctx = _mock_ctx()
    result = await rkn_tools.zapisi_reestra(ctx, kod_reestra="zapreshchennye_sayty")
    assert "запрещённых сайтов" in result


async def test_zapisi_reestra_not_found():
    ctx = _mock_ctx()
    result = await rkn_tools.zapisi_reestra(ctx, kod_reestra="nonexistent")
    assert "не найден" in result
