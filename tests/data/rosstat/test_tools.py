"""Тесты инструментов модуля Росстат."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosstat import tools as rosstat_tools
from mcp_russia.data.rosstat.schemas import (
    DannyeRegiona,
    DannyeZarplaty,
    IndikatorDannye,
    InvestitsiiPoVidam,
    OtraslevayaStrukturaVRP,
    VRPData,
)


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_regionov():
    ctx = _mock_ctx()
    result = await rosstat_tools.spisok_regionov(ctx)
    assert "Субъект" in result
    assert "Москва" in result


async def test_spisok_regionov_has_many():
    ctx = _mock_ctx()
    result = await rosstat_tools.spisok_regionov(ctx)
    assert "Татарстан" in result
    assert "Краснодар" in result


async def test_spisok_okrugov():
    ctx = _mock_ctx()
    result = await rosstat_tools.spisok_okrugov(ctx)
    assert "Федеральн" in result
    assert "Центральн" in result


async def test_informatsiya_o_regionye():
    ctx = _mock_ctx()
    region = DannyeRegiona(
        kod="77", nazvanie="г. Москва", federalny_okrug="ЦФО", naselenie=13000000
    )
    with patch.object(rosstat_tools.client, "poluchit_dannye_regiona", return_value=region):
        result = await rosstat_tools.informatsiya_o_regionye("77", ctx)
    assert "Москва" in result
    assert "13" in result


async def test_informatsiya_o_regionye_not_found():
    ctx = _mock_ctx()
    with patch.object(rosstat_tools.client, "poluchit_dannye_regiona", return_value=None):
        result = await rosstat_tools.informatsiya_o_regionye("999", ctx)
    assert "не найден" in result


async def test_informatsiya_ob_okruge():
    ctx = _mock_ctx()
    with patch.object(
        rosstat_tools.client,
        "poluchit_federalny_okrug",
        return_value={
            "kod": "CFO",
            "nazvanie": "Центральный федеральный округ",
            "kolichestvo_subiektov": 18,
            "subiekty": ["г. Москва", "Московская область"],
        },
    ):
        result = await rosstat_tools.informatsiya_ob_okruge("CFO", ctx)
    assert "Центральн" in result
    assert "18" in result


async def test_informatsiya_ob_okruge_not_found():
    ctx = _mock_ctx()
    with patch.object(
        rosstat_tools.client,
        "poluchit_federalny_okrug",
        return_value={"error": "не найден"},
    ):
        result = await rosstat_tools.informatsiya_ob_okruge("ZZZ", ctx)
    assert "не найден" in result


async def test_pokazateli_rosstata():
    ctx = _mock_ctx()
    result = await rosstat_tools.pokazateli_rosstata(ctx)
    assert "показател" in result.lower()
    assert "населени" in result or "naselenie" in result


async def test_inflyaciya_fallback():
    result = await rosstat_tools.inflyaciya(god="2025")
    assert "Инфляц" in result or "ИПЦ" in result
    assert "2025" in result


async def test_inflyaciya_with_data():
    mock_data = [
        {"period": "2025-01", "ipcz_mesyac": 0.5, "ipcz_nakoplenny": 0.5, "ipcz_god": 9.9},
    ]
    with patch.object(rosstat_tools.client, "poluchit_inflyaciyu", return_value=mock_data):
        result = await rosstat_tools.inflyaciya(god="2025")
    assert "2025-01" in result


async def test_demografiya_fallback():
    result = await rosstat_tools.demografiya(region="")
    assert "Демограф" in result
    assert "Росси" in result


async def test_demografiya_with_data():
    mock_data = [
        {"period": "2025-01", "naselenie": 146000000, "rozhdaemost": 9.0, "smertnost": 12.5},
    ]
    with patch.object(rosstat_tools.client, "poluchit_demografiyu", return_value=mock_data):
        result = await rosstat_tools.demografiya(region="")
    assert "146" in result or "2025-01" in result


async def test_demografiya_with_region():
    result = await rosstat_tools.demografiya(region="77")
    assert "77" in result


async def test_constants_subiekty_count():
    from mcp_russia.data.rosstat.constants import SUBIEKTY_RF

    assert len(SUBIEKTY_RF) >= 85


async def test_constants_emiss_kody():
    from mcp_russia.data.rosstat.constants import EMISS_KODY_POKAZATELEY

    assert "ipcz" in EMISS_KODY_POKAZATELEY
    assert "naselenie" in EMISS_KODY_POKAZATELEY
    assert "vrp" in EMISS_KODY_POKAZATELEY
    assert "zarplata" in EMISS_KODY_POKAZATELEY
    assert "selkoe_khozyaystvo" in EMISS_KODY_POKAZATELEY
    assert "stroitelstvo" in EMISS_KODY_POKAZATELEY


async def test_constants_emiss_kody_complete():
    from mcp_russia.data.rosstat.constants import EMISS_KODY_POKAZATELEY, KLYUCHEVYE_INDIKATORY

    indicator_codes = {p["kod"] for p in KLYUCHEVYE_INDIKATORY}
    for code in indicator_codes:
        assert code in EMISS_KODY_POKAZATELEY, (
            f"KLYUCHEVYE_INDIKATORY code '{code}' missing from EMISS_KODY_POKAZATELEY"
        )


async def test_constants_regionalnye_pokazateli():
    from mcp_russia.data.rosstat.constants import REGIONALNYE_POKAZATELI

    assert "vrp" in REGIONALNYE_POKAZATELI
    assert "zarplata" in REGIONALNYE_POKAZATELI
    assert "naselenie" in REGIONALNYE_POKAZATELI


async def test_vrp_dannye_fallback():
    result = await rosstat_tools.vrp_dannye(region="77")
    assert "ВРП" in result or "Валовой" in result


async def test_vrp_dannye_with_data():
    mock_data = [
        VRPData(period="2023", region="г. Москва", vrp=25400.5, vrp_na_dushu=1953.8),
    ]
    with patch.object(rosstat_tools.client, "poluchit_vrp", return_value=mock_data):
        result = await rosstat_tools.vrp_dannye(region="77", god="2023")
    assert "2023" in result
    assert "Москва" in result


async def test_vrp_dannye_empty():
    with patch.object(rosstat_tools.client, "poluchit_vrp", return_value=[]):
        result = await rosstat_tools.vrp_dannye()
    assert "Валовой" in result or "ВРП" in result


async def test_zarplata_dannye_fallback():
    result = await rosstat_tools.zarplata_dannye(region="77")
    assert "заработ" in result.lower()


async def test_zarplata_dannye_with_data():
    mock_data = [
        DannyeZarplaty(
            period="2024",
            region="г. Москва",
            nominalnaya_zp=125000.0,
            realnaya_zp_change=-1.5,
        ),
    ]
    with patch.object(rosstat_tools.client, "poluchit_zarplatu", return_value=mock_data):
        result = await rosstat_tools.zarplata_dannye(region="77", god="2024")
    assert "2024" in result
    assert "Москва" in result


async def test_zarplata_dannye_empty():
    with patch.object(rosstat_tools.client, "poluchit_zarplatu", return_value=[]):
        result = await rosstat_tools.zarplata_dannye()
    assert "Заработ" in result or "заработ" in result.lower()


async def test_sravnenie_regionov_invalid_pokazatel():
    ctx = _mock_ctx()
    result = await rosstat_tools.sravnenie_regionov("invalid_code", ctx)
    assert "не поддерживается" in result


async def test_sravnenie_regionov_with_data():
    ctx = _mock_ctx()
    mock_data = [
        {"region": "г. Москва", "kod": "77", "znachenie": 25400.5, "period": "2023"},
        {"region": "Тюменская область", "kod": "72", "znachenie": 8900.3, "period": "2023"},
    ]
    with patch.object(rosstat_tools.client, "poluchit_sravnenie_regionov", return_value=mock_data):
        result = await rosstat_tools.sravnenie_regionov("vrp", ctx)
    assert "Москва" in result
    assert "Тюмен" in result
    assert "Рейтинг" in result


async def test_sravnenie_regionov_empty():
    ctx = _mock_ctx()
    with patch.object(rosstat_tools.client, "poluchit_sravnenie_regionov", return_value=[]):
        result = await rosstat_tools.sravnenie_regionov("vrp", ctx)
    assert "недоступны" in result or "ВРП" in result


async def test_indikator_dannye_fallback():
    result = await rosstat_tools.indikator_dannye(kod="ipcz")
    assert "ИПЦ" in result or "Инфляц" in result or "31088" in result


async def test_indikator_dannye_with_data():
    mock_data = [
        IndikatorDannye(
            kod_emiss="31088",
            nazvanie="Индекс потребительских цен (инфляция)",
            period="2025-01",
            znachenie=105.2,
            edinitsa="%",
            region="",
        ),
    ]
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=mock_data):
        result = await rosstat_tools.indikator_dannye(kod="ipcz")
    assert "2025-01" in result
    assert "105" in result


async def test_indikator_dannye_with_region():
    mock_data = [
        IndikatorDannye(
            kod_emiss="24140",
            nazvanie="Средняя заработная плата",
            period="2024",
            znachenie=85000.0,
            edinitsa="руб.",
            region="г. Москва",
        ),
    ]
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=mock_data):
        result = await rosstat_tools.indikator_dannye(kod="zarplata", region="77", god="2024")
    assert "Москва" in result


async def test_indikator_dannye_empty():
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=[]):
        result = await rosstat_tools.indikator_dannye(kod="ipcz")
    assert "недоступны" in result or "31088" in result


async def test_indikator_dannye_emiss_code_direct():
    mock_data = [
        IndikatorDannye(
            kod_emiss="99999",
            nazvanie="Тестовый показатель",
            period="2024",
            znachenie=42.0,
            edinitsa="шт.",
            region="",
        ),
    ]
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=mock_data):
        result = await rosstat_tools.indikator_dannye(kod="99999")
    assert "99999" in result


async def test_constants_subiekty_no_duplicates():
    from mcp_russia.data.rosstat.constants import SUBIEKTY_RF

    codes = [r["kod"] for r in SUBIEKTY_RF]
    dups = [c for c in codes if codes.count(c) > 1]
    assert len(codes) == len(set(codes)), f"Дубликаты кодов: {dups}"


async def test_otraslevaya_struktura_vrp_fallback():
    result = await rosstat_tools.otraslevaya_struktura_vrp(region="77")
    assert "ОКВЭД" in result or "отраслев" in result.lower()


async def test_otraslevaya_struktura_vrp_with_data():
    mock_data = [
        OtraslevayaStrukturaVRP(
            region="г. Москва",
            period="2023",
            otrasl="Обрабатывающие производства",
            kod_okved="C",
            dolya_vvp=18.5,
            vrp=4700.0,
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_otraslevuyu_strukturu_vrp", return_value=mock_data
    ):
        result = await rosstat_tools.otraslevaya_struktura_vrp(region="77", god="2023")
    assert "C" in result
    assert "Обрабатыва" in result


async def test_otraslevaya_struktura_vrp_empty():
    with patch.object(rosstat_tools.client, "poluchit_otraslevuyu_strukturu_vrp", return_value=[]):
        result = await rosstat_tools.otraslevaya_struktura_vrp()
    assert "ОКВЭД" in result or "27103" in result


async def test_investitsii_po_vidam_fallback():
    result = await rosstat_tools.investitsii_po_vidam(region="77")
    assert "инвестиц" in result.lower() or "ОКВЭД" in result


async def test_investitsii_po_vidam_with_data():
    mock_data = [
        InvestitsiiPoVidam(
            region="г. Москва",
            period="2023",
            vid_deyatelnosti="Обрабатывающие производства",
            kod_okved="C",
            investitsii=3200.0,
            dolya=15.3,
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_investitsii_po_vidam", return_value=mock_data
    ):
        result = await rosstat_tools.investitsii_po_vidam(region="77", god="2023")
    assert "C" in result
    assert "Обрабатыва" in result


async def test_investitsii_po_vidam_empty():
    with patch.object(rosstat_tools.client, "poluchit_investitsii_po_vidam", return_value=[]):
        result = await rosstat_tools.investitsii_po_vidam()
    assert "инвестиц" in result.lower() or "24145" in result


async def test_constants_otraslevaya_struktura():
    from mcp_russia.data.rosstat.constants import OTRASLEVAYA_STRUKTURA_VRP

    assert len(OTRASLEVAYA_STRUKTURA_VRP) >= 19
    codes = [o["kod"] for o in OTRASLEVAYA_STRUKTURA_VRP]
    assert "A" in codes
    assert "F" in codes
    assert "S" in codes


async def test_constants_vidy_deyatelnosti_investitsii():
    from mcp_russia.data.rosstat.constants import VIDY_DEYATELNOSTI_INVESTITSII

    assert len(VIDY_DEYATELNOSTI_INVESTITSII) >= 19
    codes = [v["kod"] for v in VIDY_DEYATELNOSTI_INVESTITSII]
    assert "A" in codes
    assert "F" in codes


async def test_constants_new_emiss_kody():
    from mcp_russia.data.rosstat.constants import EMISS_KODY_POKAZATELEY

    assert "vneshnetorgovyy_oborot" in EMISS_KODY_POKAZATELEY
    assert "proizvodstvo_elektroenergii" in EMISS_KODY_POKAZATELEY
    assert "gruzooborot_transporta" in EMISS_KODY_POKAZATELEY
    assert "nauka_i_innovatsii" in EMISS_KODY_POKAZATELEY
    assert "struktura_vrp" in EMISS_KODY_POKAZATELEY


async def test_constants_new_regionalnye_pokazateli():
    from mcp_russia.data.rosstat.constants import REGIONALNYE_POKAZATELI

    assert "selkoe_khozyaystvo" in REGIONALNYE_POKAZATELI
    assert "stroitelstvo" in REGIONALNYE_POKAZATELI
    assert "migratsiya" in REGIONALNYE_POKAZATELI
    assert "estestvennyy_prirost" in REGIONALNYE_POKAZATELI
