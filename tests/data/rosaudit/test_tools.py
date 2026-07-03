"""Тесты инструментов модуля Счётная палата РФ."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosaudit import tools as rosaudit_tools


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_napravleniy():
    ctx = _maket_konteksta()
    rezultat = await rosaudit_tools.spisok_napravleniy(ctx)
    assert "Направления контрольной деятельности" in rezultat
    assert "бюджет" in rezultat.lower()


async def test_spisok_tipov_meropriyatiy():
    ctx = _maket_konteksta()
    rezultat = await rosaudit_tools.spisok_tipov_meropriyatiy(ctx)
    assert "Типы контрольных мероприятий" in rezultat
    assert "Проверка" in rezultat


async def test_spisok_subiektov_audita():
    ctx = _maket_konteksta()
    rezultat = await rosaudit_tools.spisok_subiektov_audita(ctx)
    assert "Субъекты" in rezultat
    assert "Федеральные" in rezultat


async def test_poisk_kontrolnyh_meropriyatiy_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rosaudit_tools.client, "poisk_kontrolnyh_meropriyatiy", return_value=[]):
        rezultat = await rosaudit_tools.poisk_kontrolnyh_meropriyatiy(ctx)
    assert "не найдены" in rezultat


async def test_poisk_kontrolnyh_meropriyatiy_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "КМ-2026-001",
            "nazvanie": "Проверка исполнения бюджета",
            "tip": "Проверка",
            "sostoyanie": "Завершено",
            "obiem_sredstv": 1500000000,
        },
    ]
    with patch.object(
        rosaudit_tools.client, "poisk_kontrolnyh_meropriyatiy", return_value=mock_data
    ):
        rezultat = await rosaudit_tools.poisk_kontrolnyh_meropriyatiy(ctx, god=2026)
    assert "КМ-2026-001" in rezultat


async def test_info_kontrolnogo_meropriyatiya_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(
        rosaudit_tools.client, "poluchit_kontrolnoe_meropriyatie", return_value=None
    ):
        rezultat = await rosaudit_tools.info_kontrolnogo_meropriyatiya(
            "nesushchestvuyushchiy", ctx
        )
    assert "не найдено" in rezultat


async def test_info_kontrolnogo_meropriyatiya_nayden():
    ctx = _maket_konteksta()
    mock_data = {
        "nomer": "КМ-2026-001",
        "nazvanie": "Проверка исполнения бюджета",
        "tip": "Проверка",
        "napravlenie": "Контроль исполнения федерального бюджета",
        "data_nachala": "2026-01-15",
        "data_okonchaniya": "2026-03-20",
        "sostoyanie": "Завершено",
        "obiem_sredstv": 1500000000,
    }
    with patch.object(
        rosaudit_tools.client, "poluchit_kontrolnoe_meropriyatie", return_value=mock_data
    ):
        rezultat = await rosaudit_tools.info_kontrolnogo_meropriyatiya("КМ-2026-001", ctx)
    assert "Проверка исполнения бюджета" in rezultat
    assert "2026-01-15" in rezultat


async def test_info_auditorskogo_zaklyucheniya_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(
        rosaudit_tools.client, "poluchit_auditorskoe_zaklyuchenie", return_value=None
    ):
        rezultat = await rosaudit_tools.info_auditorskogo_zaklyucheniya(
            "nesushchestvuyushchiy", ctx
        )
    assert "не найдено" in rezultat


async def test_info_auditorskogo_zaklyucheniya_nayden():
    ctx = _maket_konteksta()
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
        rezultat = await rosaudit_tools.info_auditorskogo_zaklyucheniya("АЗ-2026-001", ctx)
    assert "Заключение" in rezultat
    assert "Минфин" in rezultat


async def test_ispolnenie_byudzheta_nedostupen():
    ctx = _maket_konteksta()
    with patch.object(rosaudit_tools.client, "poluchit_byudzhet_ispolnenie", return_value=None):
        rezultat = await rosaudit_tools.ispolnenie_byudzheta(ctx, period="2024")
    assert "недоступны" in rezultat


async def test_ispolnenie_byudzheta_nayden():
    ctx = _maket_konteksta()
    mock_data = {
        "period": "2025",
        "dohody": 28000.5,
        "raskhody": 31000.2,
        "defitsit": -2999.7,
    }
    with patch.object(
        rosaudit_tools.client, "poluchit_byudzhet_ispolnenie", return_value=mock_data
    ):
        rezultat = await rosaudit_tools.ispolnenie_byudzheta(ctx, period="2025")
    assert "2025" in rezultat
    assert "Доходы" in rezultat


async def test_poisk_narusheniy_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rosaudit_tools.client, "poisk_narusheniy", return_value=[]):
        rezultat = await rosaudit_tools.poisk_narusheniy(ctx, organizaciya="Тест")
    assert "не найдены" in rezultat


async def test_poisk_narusheniy_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "organizaciya": "Минобороны",
            "tip_narusheniya": "Финансовое нарушение",
            "opisanie": "Нецелевое использование средств",
            "summa": 500000,
        },
    ]
    with patch.object(rosaudit_tools.client, "poisk_narusheniy", return_value=mock_data):
        rezultat = await rosaudit_tools.poisk_narusheniy(ctx, organizaciya="Минобороны")
    assert "Минобороны" in rezultat
