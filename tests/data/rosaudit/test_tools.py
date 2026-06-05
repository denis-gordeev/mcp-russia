"""Тесты инструментов модуля Счётная палата РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosaudit import tools as rosaudit_tools


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_napravleniy():
    ctx = _mock_ctx()
    result = await rosaudit_tools.spisok_napravleniy(ctx)
    assert "Направления контрольной деятельности" in result
    assert "бюджет" in result.lower()


async def test_spisok_tipov_meropriyatiy():
    ctx = _mock_ctx()
    result = await rosaudit_tools.spisok_tipov_meropriyatiy(ctx)
    assert "Типы контрольных мероприятий" in result
    assert "Проверка" in result


async def test_spisok_subiektov_audita():
    ctx = _mock_ctx()
    result = await rosaudit_tools.spisok_subiektov_audita(ctx)
    assert "Субъекты" in result
    assert "Федеральные" in result


async def test_poisk_kontrolnyh_meropriyatiy_empty():
    ctx = _mock_ctx()
    with patch.object(rosaudit_tools.client, "poisk_kontrolnyh_meropriyatiy", return_value=[]):
        result = await rosaudit_tools.poisk_kontrolnyh_meropriyatiy(ctx)
    assert "не найдены" in result


async def test_poisk_kontrolnyh_meropriyatiy_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "nomer": "КМ-2026-001",
            "nazvanie": "Проверка исполнения бюджета",
            "tip": "Проверка",
            "status": "Завершено",
            "obiem_sredstv": 1500000000,
        },
    ]
    with patch.object(
        rosaudit_tools.client, "poisk_kontrolnyh_meropriyatiy", return_value=mock_data
    ):
        result = await rosaudit_tools.poisk_kontrolnyh_meropriyatiy(ctx, god=2026)
    assert "КМ-2026-001" in result


async def test_info_kontrolnogo_meropriyatiya_not_found():
    ctx = _mock_ctx()
    with patch.object(
        rosaudit_tools.client, "poluchit_kontrolnoe_meropriyatie", return_value=None
    ):
        result = await rosaudit_tools.info_kontrolnogo_meropriyatiya("nonexistent", ctx)
    assert "не найдено" in result


async def test_info_kontrolnogo_meropriyatiya_found():
    ctx = _mock_ctx()
    mock_data = {
        "nomer": "КМ-2026-001",
        "nazvanie": "Проверка исполнения бюджета",
        "tip": "Проверка",
        "napravlenie": "Контроль исполнения федерального бюджета",
        "data_nachala": "2026-01-15",
        "data_okonchaniya": "2026-03-20",
        "status": "Завершено",
        "obiem_sredstv": 1500000000,
    }
    with patch.object(
        rosaudit_tools.client, "poluchit_kontrolnoe_meropriyatie", return_value=mock_data
    ):
        result = await rosaudit_tools.info_kontrolnogo_meropriyatiya("КМ-2026-001", ctx)
    assert "Проверка исполнения бюджета" in result
    assert "2026-01-15" in result


async def test_info_auditorskogo_zaklyucheniya_not_found():
    ctx = _mock_ctx()
    with patch.object(
        rosaudit_tools.client, "poluchit_auditorskoe_zaklyuchenie", return_value=None
    ):
        result = await rosaudit_tools.info_auditorskogo_zaklyucheniya("nonexistent", ctx)
    assert "не найдено" in result


async def test_info_auditorskogo_zaklyucheniya_found():
    ctx = _mock_ctx()
    mock_data = {
        "nomer": "АЗ-2026-001",
        "nazvanie": "Заключение по проверке Минфина",
        "data_publikacii": "2026-04-01",
        "obekt_audita": "Минфин России",
        "napravlenie": "Контроль исполнения бюджета",
        "vyavleno_narusheniy": 5,
        "summa_narusheniy": 2000000,
    }
    with patch.object(
        rosaudit_tools.client, "poluchit_auditorskoe_zaklyuchenie", return_value=mock_data
    ):
        result = await rosaudit_tools.info_auditorskogo_zaklyucheniya("АЗ-2026-001", ctx)
    assert "Заключение" in result
    assert "Минфин" in result


async def test_ispolnenie_byudzheta_unavailable():
    ctx = _mock_ctx()
    with patch.object(rosaudit_tools.client, "poluchit_byudzhet_ispolnenie", return_value=None):
        result = await rosaudit_tools.ispolnenie_byudzheta(ctx, period="2024")
    assert "недоступны" in result


async def test_ispolnenie_byudzheta_found():
    ctx = _mock_ctx()
    mock_data = {
        "period": "2025",
        "dohody": 28000.5,
        "raskhody": 31000.2,
        "deficit": -2999.7,
    }
    with patch.object(
        rosaudit_tools.client, "poluchit_byudzhet_ispolnenie", return_value=mock_data
    ):
        result = await rosaudit_tools.ispolnenie_byudzheta(ctx, period="2025")
    assert "2025" in result
    assert "Доходы" in result


async def test_poisk_narusheniy_empty():
    ctx = _mock_ctx()
    with patch.object(rosaudit_tools.client, "poisk_narusheniy", return_value=[]):
        result = await rosaudit_tools.poisk_narusheniy(ctx, organizaciya="Тест")
    assert "не найдены" in result


async def test_poisk_narusheniy_found():
    ctx = _mock_ctx()
    mock_data = [
        {
            "organizaciya": "Минобороны",
            "tip_narusheniya": "Финансовое нарушение",
            "opisanie": "Нецелевое использование средств",
            "summa": 500000,
        },
    ]
    with patch.object(rosaudit_tools.client, "poisk_narusheniy", return_value=mock_data):
        result = await rosaudit_tools.poisk_narusheniy(ctx, organizaciya="Минобороны")
    assert "Минобороны" in result
