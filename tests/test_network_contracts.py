"""Опциональные сетевые контрактные тесты для контроля доступности
внешних источников и изменений схем ответов.

Запускаются только при установленной переменной окружения
MCP_RUSSIA_NETWORK_TESTS=1. Без неё — пропускаются.

Использование:
    MCP_RUSSIA_NETWORK_TESTS=1 make test
    MCP_RUSSIA_NETWORK_TESTS=1 pytest tests/test_network_contracts.py -v
"""

from __future__ import annotations

import os

import pytest

from mcp_russia._shared.http_client import http_poluchit

PROVODIM_SETOVYE_TESTY = os.environ.get("MCP_RUSSIA_NETWORK_TESTS", "") == "1"

ISTOCHNIKI = [
    {
        "imya": "ЦБ РФ (cbr-xml-daily.ru)",
        "adres": "https://www.cbr-xml-daily.ru/daily_json.js",
        "ozhidayemyy_klyuch": "Valute",
        "tip": "json",
    },
    {
        "imya": "Рособрнадзор (аккредитация)",
        "adres": ("https://obrnadzor.gov.ru/opendata/7710542907-FS_ACCRED/data-20240901.json"),
        "ozhidayemyy_tip": (list, dict),
        "tip": "json",
    },
    {
        "imya": "Рособрнадзор (лицензии)",
        "adres": ("https://obrnadzor.gov.ru/opendata/7710542907-FS_LICENSE/data-20240901.json"),
        "ozhidayemyy_tip": (list, dict),
        "tip": "json",
    },
    {
        "imya": "ЕМИСС (fedstat.ru)",
        "adres": "https://www.fedstat.ru/indicator/31074",
        "ozhidayemyy_status": 200,
        "tip": "html",
    },
    {
        "imya": "МВД (открытые данные)",
        "adres": "https://мвд.рф",
        "ozhidayemyy_status": 200,
        "tip": "html",
    },
    {
        "imya": "Open-Meteo (погода Москва)",
        "adres": (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=55.75&longitude=37.62&current_weather=true"
        ),
        "ozhidayemyy_klyuch": "current_weather",
        "tip": "json",
    },
    {
        "imya": "data.gov.ru (портал открытых данных)",
        "adres": "https://data.gov.ru",
        "ozhidayemyy_status": 200,
        "tip": "html",
    },
    {
        "imya": "pravo.gov.ru (правовые акты)",
        "adres": "https://pravo.gov.ru",
        "ozhidayemyy_status": 200,
        "tip": "html",
    },
    {
        "imya": "Росгидромет (Open-Meteo воздух)",
        "adres": (
            "https://air-quality-api.open-meteo.com/v1/air-quality"
            "?latitude=55.75&longitude=37.62&current=pm10"
        ),
        "ozhidayemyy_klyuch": "current",
        "tip": "json",
        "neobyazatelnyy": True,
    },
]


def _propustit_li_test(neobyazatelnyy: bool = False) -> pytest.MarkDecorator:
    if neobyazatelnyy:
        return pytest.mark.skipif(
            not PROVODIM_SETOVYE_TESTY,
            reason="Сетевые тесты отключены (MCP_RUSSIA_NETWORK_TESTS=1)",
        )
    return pytest.mark.skipif(
        not PROVODIM_SETOVYE_TESTY,
        reason="Сетевые тесты отключены (MCP_RUSSIA_NETWORK_TESTS=1)",
    )


@pytest.mark.asyncio
@pytest.mark.skipif(
    not PROVODIM_SETOVYE_TESTY,
    reason="Сетевые тесты отключены (MCP_RUSSIA_NETWORK_TESTS=1)",
)
async def test_istochniki_dostupny() -> None:
    """Проверить доступность всех внешних источников данных."""
    oshibki: list[str] = []
    for istochnik in ISTOCHNIKI:
        try:
            await http_poluchit(istochnik["adres"], taimaut=30.0)
        except Exception as isklyuchenie:
            oshibki.append(f"{istochnik['imya']}: {isklyuchenie}")
    assert not oshibki, "Недоступные источники:\n" + "\n".join(oshibki)


@pytest.mark.asyncio
@pytest.mark.skipif(
    not PROVODIM_SETOVYE_TESTY,
    reason="Сетевые тесты отключены (MCP_RUSSIA_NETWORK_TESTS=1)",
)
async def test_json_skhemy_otvetov() -> None:
    """Проверить, что JSON-источники возвращают ожидаемую структуру."""
    oshibki: list[str] = []
    for istochnik in ISTOCHNIKI:
        if istochnik["tip"] != "json":
            continue
        try:
            otvet = await http_poluchit(istochnik["adres"], taimaut=30.0)
        except Exception as isklyuchenie:
            oshibki.append(f"{istochnik['imya']}: запрос не удался — {isklyuchenie}")
            continue
        if "ozhidayemyy_klyuch" in istochnik:
            if not isinstance(otvet, dict):
                oshibki.append(f"{istochnik['imya']}: ответ не dict, а {type(otvet).__name__}")
                continue
            klyuch = istochnik["ozhidayemyy_klyuch"]
            if klyuch not in otvet:
                oshibki.append(f"{istochnik['imya']}: ключ '{klyuch}' отсутствует в ответе")
            if "ozhidayemyy_tip" in istochnik and not isinstance(
                otvet, istochnik["ozhidayemyy_tip"]
            ):
                oshibki.append(
                    f"{istochnik['imya']}: тип {type(otvet).__name__} "
                    f"не совпадает с ожидаемым {istochnik['ozhidayemyy_tip']}"
                )
    assert not oshibki, "Ошибки схем ответов:\n" + "\n".join(oshibki)


@pytest.mark.asyncio
@pytest.mark.skipif(
    not PROVODIM_SETOVYE_TESTY,
    reason="Сетевые тесты отключены (MCP_RUSSIA_NETWORK_TESTS=1)",
)
async def test_tsr_osobennosti_otveta() -> None:
    """Контрактный тест: ЦБ РФ возвращает корректные курсы валют."""
    otvet = await http_poluchit("https://www.cbr-xml-daily.ru/daily_json.js", taimaut=30.0)
    assert isinstance(otvet, dict), "Ответ ЦБ РФ не dict"
    assert "Valute" in otvet, "Ключ 'Valute' отсутствует в ответе ЦБ РФ"
    valyuty = otvet["Valute"]
    assert isinstance(valyuty, dict), "Valute не dict"
    assert "USD" in valyuty, "USD отсутствует в справочнике валют"
    usd = valyuty["USD"]
    assert "Value" in usd, "Ключ 'Value' отсутствует в записи USD"
    assert isinstance(usd["Value"], (int, float)), "Value USD не число"
    assert usd["Value"] > 0, "Курс USD неположительный"


@pytest.mark.asyncio
@pytest.mark.skipif(
    not PROVODIM_SETOVYE_TESTY,
    reason="Сетевые тесты отключены (MCP_RUSSIA_NETWORK_TESTS=1)",
)
async def test_obrnadzor_akkr_kontrakt() -> None:
    """Контрактный тест: Рособрнадзор возвращает список аккредитации."""
    otvet = await http_poluchit(
        "https://obrnadzor.gov.ru/opendata/7710542907-FS_ACCRED/data-20240901.json",
        taimaut=30.0,
    )
    assert isinstance(otvet, list), "Ответ Рособрнадзор не list"
    if otvet:
        pervaya_zapis = otvet[0]
        assert isinstance(pervaya_zapis, dict), "Запись не dict"
        for klyuch in ("inn", "fullName"):
            assert klyuch in pervaya_zapis, f"Ключ '{klyuch}' отсутствует в записи аккредитации"


@pytest.mark.asyncio
@pytest.mark.skipif(
    not PROVODIM_SETOVYE_TESTY,
    reason="Сетевые тесты отключены (MCP_RUSSIA_NETWORK_TESTS=1)",
)
async def test_open_meteo_kontrakt() -> None:
    """Контрактный тест: Open-Meteo возвращает текущую погоду."""
    otvet = await http_poluchit(
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=55.75&longitude=37.62&current_weather=true",
        taimaut=30.0,
    )
    assert isinstance(otvet, dict), "Ответ Open-Meteo не dict"
    assert "current_weather" in otvet, "Ключ 'current_weather' отсутствует"
    pogoda = otvet["current_weather"]
    assert "temperature" in pogoda, "Ключ 'temperature' отсутствует в погоде"
    assert isinstance(pogoda["temperature"], (int, float)), "temperature не число"
