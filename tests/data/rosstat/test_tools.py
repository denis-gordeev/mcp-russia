"""Тесты инструментов модуля Росстат."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosstat import tools as rosstat_tools
from mcp_russia.data.rosstat.schemas import (
    DannyeRegiona,
    DannyeZarplaty,
    IndikatorDannye,
    InvestitsiiPoVidam,
    OtraslevayaStrukturaVRP,
    VRPDannye,
)


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_regionov():
    kontekst = _maket_konteksta()
    rezultat = await rosstat_tools.spisok_regionov(kontekst)
    assert "Субъект" in rezultat
    assert "Москва" in rezultat


async def test_spisok_regionov_imeet_mnogo():
    kontekst = _maket_konteksta()
    rezultat = await rosstat_tools.spisok_regionov(kontekst)
    assert "Татарстан" in rezultat
    assert "Краснодар" in rezultat


async def test_spisok_okrugov():
    kontekst = _maket_konteksta()
    rezultat = await rosstat_tools.spisok_okrugov(kontekst)
    assert "Федеральн" in rezultat
    assert "Центральн" in rezultat


async def test_informatsiya_o_regionye():
    kontekst = _maket_konteksta()
    subiekt = DannyeRegiona(
        kod="77", nazvanie="г. Москва", federalny_okrug="ЦФО", naselenie=13000000
    )
    with patch.object(rosstat_tools.client, "poluchit_dannye_regiona", return_value=subiekt):
        rezultat = await rosstat_tools.informatsiya_o_regionye("77", kontekst)
    assert "Москва" in rezultat
    assert "13" in rezultat


async def test_informatsiya_o_regionye_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(rosstat_tools.client, "poluchit_dannye_regiona", return_value=None):
        rezultat = await rosstat_tools.informatsiya_o_regionye("999", kontekst)
    assert "не найден" in rezultat


async def test_informatsiya_ob_okruge():
    kontekst = _maket_konteksta()
    with patch.object(
        rosstat_tools.client,
        "poluchit_federalny_okrug",
        return_value={
            "kod": "ЦФО",
            "nazvanie": "Центральный федеральный округ",
            "kolichestvo_subiektov": 18,
            "subiekty": ["г. Москва", "Московская область"],
        },
    ):
        rezultat = await rosstat_tools.informatsiya_ob_okruge("ЦФО", kontekst)
    assert "Центральн" in rezultat
    assert "18" in rezultat


async def test_informatsiya_ob_okruge_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(
        rosstat_tools.client,
        "poluchit_federalny_okrug",
        return_value={"oshibka": "не найден"},
    ):
        rezultat = await rosstat_tools.informatsiya_ob_okruge("ZZZ", kontekst)
    assert "не найден" in rezultat


async def test_pokazateli_rosstata():
    kontekst = _maket_konteksta()
    rezultat = await rosstat_tools.pokazateli_rosstata(kontekst)
    assert "показател" in rezultat.lower()
    assert "населени" in rezultat or "naselenie" in rezultat


async def test_inflyatsiya_zapasnoy():
    rezultat = await rosstat_tools.inflyatsiya(god="2025")
    assert "Инфляц" in rezultat or "ИПЦ" in rezultat
    assert "2025" in rezultat


async def test_inflyatsiya_s_dannymi():
    maket_dannykh = [
        {"period": "2025-01", "ipcz_mesyac": 0.5, "ipcz_nakoplenny": 0.5, "ipcz_god": 9.9},
    ]
    with patch.object(rosstat_tools.client, "poluchit_inflyatsiyu", return_value=maket_dannykh):
        rezultat = await rosstat_tools.inflyatsiya(god="2025")
    assert "2025-01" in rezultat


async def test_demografiya_zapasnoy():
    rezultat = await rosstat_tools.demografiya(subiekt="")
    assert "Демограф" in rezultat
    assert "Росси" in rezultat


async def test_demografiya_s_dannymi():
    maket_dannykh = [
        {"period": "2025-01", "naselenie": 146000000, "rozhdaemost": 9.0, "smertnost": 12.5},
    ]
    with patch.object(rosstat_tools.client, "poluchit_demografiyu", return_value=maket_dannykh):
        rezultat = await rosstat_tools.demografiya(subiekt="")
    assert "146" in rezultat or "2025-01" in rezultat


async def test_demografiya_s_regionom():
    rezultat = await rosstat_tools.demografiya(subiekt="77")
    assert "77" in rezultat


async def test_constants_subiekty_kolichestvo():
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


async def test_constants_emiss_kody_polnyy():
    from mcp_russia.data.rosstat.constants import EMISS_KODY_POKAZATELEY, KLYUCHEVYE_INDIKATORY

    kody_indikatorov = {p["kod"] for p in KLYUCHEVYE_INDIKATORY}
    for kod in kody_indikatorov:
        assert kod in EMISS_KODY_POKAZATELEY, (
            f"KLYUCHEVYE_INDIKATORY код '{kod}' отсутствует в EMISS_KODY_POKAZATELEY"
        )


async def test_constants_regionalnye_pokazateli():
    from mcp_russia.data.rosstat.constants import REGIONALNYE_POKAZATELI

    assert "vrp" in REGIONALNYE_POKAZATELI
    assert "zarplata" in REGIONALNYE_POKAZATELI
    assert "naselenie" in REGIONALNYE_POKAZATELI


async def test_vrp_dannye_zapasnoy():
    rezultat = await rosstat_tools.vrp_dannye(subiekt="77")
    assert "ВРП" in rezultat or "Валовой" in rezultat


async def test_vrp_dannye_s_dannymi():
    maket_dannykh = [
        VRPDannye(period="2023", subiekt="г. Москва", vrp=25400.5, vrp_na_dushu=1953.8),
    ]
    with patch.object(rosstat_tools.client, "poluchit_vrp", return_value=maket_dannykh):
        rezultat = await rosstat_tools.vrp_dannye(subiekt="77", god="2023")
    assert "2023" in rezultat
    assert "Москва" in rezultat


async def test_vrp_dannye_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_vrp", return_value=[]):
        rezultat = await rosstat_tools.vrp_dannye()
    assert "Валовой" in rezultat or "ВРП" in rezultat


async def test_zarplata_dannye_zapasnoy():
    rezultat = await rosstat_tools.zarplata_dannye(subiekt="77")
    assert "заработ" in rezultat.lower()


async def test_zarplata_dannye_s_dannymi():
    maket_dannykh = [
        DannyeZarplaty(
            period="2024",
            subiekt="г. Москва",
            nominalnaya_zp=125000.0,
            realnaya_zp_izmenenie=-1.5,
        ),
    ]
    with patch.object(rosstat_tools.client, "poluchit_zarplatu", return_value=maket_dannykh):
        rezultat = await rosstat_tools.zarplata_dannye(subiekt="77", god="2024")
    assert "2024" in rezultat
    assert "Москва" in rezultat


async def test_zarplata_dannye_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_zarplatu", return_value=[]):
        rezultat = await rosstat_tools.zarplata_dannye()
    assert "Заработ" in rezultat or "заработ" in rezultat.lower()


async def test_sravnenie_regionov_nekorrektnyy_pokazatel():
    kontekst = _maket_konteksta()
    rezultat = await rosstat_tools.sravnenie_regionov("nekorrektnyy_kod", kontekst)
    assert "не поддерживается" in rezultat


async def test_sravnenie_regionov_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {"subiekt": "г. Москва", "kod": "77", "znachenie": 25400.5, "period": "2023"},
        {"subiekt": "Тюменская область", "kod": "72", "znachenie": 8900.3, "period": "2023"},
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_sravnenie_regionov", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.sravnenie_regionov("vrp", kontekst)
    assert "Москва" in rezultat
    assert "Тюмен" in rezultat
    assert "Рейтинг" in rezultat


async def test_sravnenie_regionov_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rosstat_tools.client, "poluchit_sravnenie_regionov", return_value=[]):
        rezultat = await rosstat_tools.sravnenie_regionov("vrp", kontekst)
    assert "недоступны" in rezultat or "ВРП" in rezultat


async def test_indikator_dannye_zapasnoy():
    rezultat = await rosstat_tools.indikator_dannye(kod="ipcz")
    assert "ИПЦ" in rezultat or "Инфляц" in rezultat or "31074" in rezultat


async def test_indikator_dannye_s_dannymi():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="31074",
            nazvanie="Индекс потребительских цен (инфляция)",
            period="2025-01",
            znachenie=105.2,
            edinitsa="%",
            subiekt="",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.indikator_dannye(kod="ipcz")
    assert "2025-01" in rezultat
    assert "105" in rezultat


async def test_indikator_dannye_s_regionom():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="58701",
            nazvanie="Средняя заработная плата",
            period="2024",
            znachenie=85000.0,
            edinitsa="руб.",
            subiekt="г. Москва",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.indikator_dannye(kod="zarplata", subiekt="77", god="2024")
    assert "Москва" in rezultat


async def test_indikator_dannye_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=[]):
        rezultat = await rosstat_tools.indikator_dannye(kod="ipcz")
    assert "недоступны" in rezultat or "31074" in rezultat


async def test_indikator_dannye_emiss_code_direct():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="99999",
            nazvanie="Тестовый показатель",
            period="2024",
            znachenie=42.0,
            edinitsa="шт.",
            subiekt="",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.indikator_dannye(kod="99999")
    assert "99999" in rezultat


async def test_dinamika_regiona_s_dannymi():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="58701",
            nazvanie="Средняя заработная плата",
            period="2023",
            znachenie=80000.0,
            edinitsa="руб.",
            subiekt="г. Москва",
        ),
        IndikatorDannye(
            kod_emiss="58701",
            nazvanie="Средняя заработная плата",
            period="2024",
            znachenie=88000.0,
            edinitsa="руб.",
            subiekt="г. Москва",
        ),
        IndikatorDannye(
            kod_emiss="58701",
            nazvanie="Средняя заработная плата",
            period="2022",
            znachenie=70000.0,
            edinitsa="руб.",
            subiekt="г. Москва",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ) as klient:
        rezultat = await rosstat_tools.dinamika_regiona(
            "zarplata", "77", god_nachalo="2023", god_konets="2024"
        )

    klient.assert_awaited_once_with(kod="zarplata", subiekt="77")
    assert "Москва" in rezultat
    assert "2022" not in rezultat
    assert rezultat.index("2023") < rezultat.index("2024")
    assert "+10.00%" in rezultat


async def test_dinamika_regiona_proveryaet_argumenty():
    rezultat = await rosstat_tools.dinamika_regiona("neizvestnyy", "77")
    assert "не поддерживается" in rezultat

    rezultat = await rosstat_tools.dinamika_regiona("zarplata", "999")
    assert "не найден" in rezultat

    rezultat = await rosstat_tools.dinamika_regiona(
        "zarplata", "77", god_nachalo="2025", god_konets="2024"
    )
    assert "не может быть больше" in rezultat


async def test_dinamika_regiona_pustoy_rezultat():
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=[]):
        rezultat = await rosstat_tools.dinamika_regiona("vrp", "77")
    assert "Данные за выбранный период временно недоступны" in rezultat
    assert "61497" in rezultat


async def test_constants_subiekty_bez_dublikatov():
    from mcp_russia.data.rosstat.constants import SUBIEKTY_RF

    kody = [r["kod"] for r in SUBIEKTY_RF]
    dublikaty = [k for k in kody if kody.count(k) > 1]
    assert len(kody) == len(set(kody)), f"Дубликаты кодов: {dublikaty}"


async def test_otraslevaya_struktura_vrp_zapasnoy():
    rezultat = await rosstat_tools.otraslevaya_struktura_vrp(subiekt="77")
    assert "ОКВЭД" in rezultat or "отраслев" in rezultat.lower()


async def test_otraslevaya_struktura_vrp_s_dannymi():
    maket_dannykh = [
        OtraslevayaStrukturaVRP(
            subiekt="г. Москва",
            period="2023",
            otrasl="Обрабатывающие производства",
            kod_okved="C",
            dolya_vvp=18.5,
            vrp=4700.0,
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_otraslevuyu_strukturu_vrp", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.otraslevaya_struktura_vrp(subiekt="77", god="2023")
    assert "C" in rezultat
    assert "Обрабатыва" in rezultat


async def test_otraslevaya_struktura_vrp_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_otraslevuyu_strukturu_vrp", return_value=[]):
        rezultat = await rosstat_tools.otraslevaya_struktura_vrp()
    assert "ОКВЭД" in rezultat or "59450" in rezultat


async def test_investitsii_po_vidam_zapasnoy():
    rezultat = await rosstat_tools.investitsii_po_vidam(subiekt="77")
    assert "инвестиц" in rezultat.lower() or "ОКВЭД" in rezultat


async def test_investitsii_po_vidam_s_dannymi():
    maket_dannykh = [
        InvestitsiiPoVidam(
            subiekt="г. Москва",
            period="2023",
            vid_deyatelnosti="Обрабатывающие производства",
            kod_okved="C",
            investitsii=3200.0,
            dolya=15.3,
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_investitsii_po_vidam", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.investitsii_po_vidam(subiekt="77", god="2023")
    assert "C" in rezultat
    assert "Обрабатыва" in rezultat


async def test_investitsii_po_vidam_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_investitsii_po_vidam", return_value=[]):
        rezultat = await rosstat_tools.investitsii_po_vidam()
    assert "инвестиц" in rezultat.lower() or "33644" in rezultat


async def test_constants_otraslevaya_struktura():
    from mcp_russia.data.rosstat.constants import OTRASLEVAYA_STRUKTURA_VRP

    assert len(OTRASLEVAYA_STRUKTURA_VRP) >= 19
    kody = [o["kod"] for o in OTRASLEVAYA_STRUKTURA_VRP]
    assert "A" in kody
    assert "F" in kody
    assert "S" in kody


async def test_constants_vidy_deyatelnosti_investitsii():
    from mcp_russia.data.rosstat.constants import VIDY_DEYATELNOSTI_INVESTITSII

    assert len(VIDY_DEYATELNOSTI_INVESTITSII) >= 19
    kody = [v["kod"] for v in VIDY_DEYATELNOSTI_INVESTITSII]
    assert "A" in kody
    assert "F" in kody


async def test_constants_novyy_emiss_kody():
    from mcp_russia.data.rosstat.constants import EMISS_KODY_POKAZATELEY

    assert "vneshnetorgovyy_oborot" in EMISS_KODY_POKAZATELEY
    assert "proizvodstvo_elektroenergii" in EMISS_KODY_POKAZATELEY
    assert "gruzooborot_transporta" in EMISS_KODY_POKAZATELEY
    assert "nauka_i_innovatsii" in EMISS_KODY_POKAZATELEY
    assert "struktura_vrp" in EMISS_KODY_POKAZATELEY


async def test_constants_novyy_regionalnye_pokazateli():
    from mcp_russia.data.rosstat.constants import REGIONALNYE_POKAZATELI

    assert "selkoe_khozyaystvo" in REGIONALNYE_POKAZATELI
    assert "stroitelstvo" in REGIONALNYE_POKAZATELI
    assert "migratsiya" in REGIONALNYE_POKAZATELI
    assert "estestvennyy_prirost" in REGIONALNYE_POKAZATELI


async def test_sravnenie_okrugov_nekorrektnyy_pokazatel():
    kontekst = _maket_konteksta()
    rezultat = await rosstat_tools.sravnenie_okrugov("nekorrektnyy_kod", kontekst)
    assert "не поддерживается" in rezultat


async def test_sravnenie_okrugov_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {"subiekt": "г. Москва", "kod": "77", "znachenie": 25400.5, "period": "2023"},
        {"subiekt": "Московская область", "kod": "50", "znachenie": 4700.3, "period": "2023"},
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_sravnenie_regionov", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.sravnenie_okrugov("vrp", kontekst)
    assert "ЦФО" in rezultat or "Центральн" in rezultat
    assert "Рейтинг" in rezultat


async def test_sravnenie_okrugov_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rosstat_tools.client, "poluchit_sravnenie_regionov", return_value=[]):
        rezultat = await rosstat_tools.sravnenie_okrugov("vrp", kontekst)
    assert "недоступны" in rezultat or "ВРП" in rezultat


async def test_vvp_dannye_s_dannymi():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="60201",
            nazvanie="Валовой внутренний продукт",
            period="2024",
            znachenie=187000.0,
            edinitsa="млрд руб.",
            subiekt="",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.vvp_dannye(god="2024")
    assert "ВВП" in rezultat
    assert "187" in rezultat


async def test_vvp_dannye_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=[]):
        rezultat = await rosstat_tools.vvp_dannye()
    assert "60201" in rezultat


async def test_bezrabotitsa_dannye_s_dannymi():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="43062",
            nazvanie="Уровень безработицы",
            period="2024",
            znachenie=3.2,
            edinitsa="%",
            subiekt="",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.bezrabotitsa_dannye()
    assert "безработиц" in rezultat
    assert "3" in rezultat


async def test_bezrabotitsa_dannye_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=[]):
        rezultat = await rosstat_tools.bezrabotitsa_dannye()
    assert "43062" in rezultat


async def test_dokhody_na_dushu_s_dannymi():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="57039",
            nazvanie="Среднедушевые денежные доходы",
            period="2024",
            znachenie=45600.0,
            edinitsa="руб./мес.",
            subiekt="",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.dokhody_na_dushu()
    assert "доход" in rezultat
    assert "45" in rezultat


async def test_dokhody_na_dushu_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=[]):
        rezultat = await rosstat_tools.dokhody_na_dushu()
    assert "57039" in rezultat


async def test_promyshlennoe_proizvodstvo_s_dannymi():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="43045",
            nazvanie="Индекс промышленного производства",
            period="2024",
            znachenie=103.5,
            edinitsa="%",
            subiekt="",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.promyshlennoe_proizvodstvo()
    assert "промышленн" in rezultat
    assert "103" in rezultat


async def test_promyshlennoe_proizvodstvo_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=[]):
        rezultat = await rosstat_tools.promyshlennoe_proizvodstvo()
    assert "43045" in rezultat


async def test_uroven_bednosti_s_dannymi():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="33460",
            nazvanie="Уровень бедности",
            period="2024",
            znachenie=9.8,
            edinitsa="%",
            subiekt="",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.uroven_bednosti()
    assert "бедност" in rezultat
    assert "9" in rezultat


async def test_uroven_bednosti_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=[]):
        rezultat = await rosstat_tools.uroven_bednosti()
    assert "33460" in rezultat


async def test_srednyaya_pensiya_s_dannymi():
    maket_dannykh = [
        IndikatorDannye(
            kod_emiss="60440",
            nazvanie="Средний размер назначенных пенсий",
            period="2024",
            znachenie=21500.0,
            edinitsa="руб.",
            subiekt="",
        ),
    ]
    with patch.object(
        rosstat_tools.client, "poluchit_indikator_dannye", return_value=maket_dannykh
    ):
        rezultat = await rosstat_tools.srednyaya_pensiya()
    assert "пенси" in rezultat
    assert "21" in rezultat


async def test_srednyaya_pensiya_pustoy():
    with patch.object(rosstat_tools.client, "poluchit_indikator_dannye", return_value=[]):
        rezultat = await rosstat_tools.srednyaya_pensiya()
    assert "60440" in rezultat
