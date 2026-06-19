"""HTTP-клиент для модуля Росгидромета.

Интеграция через Open-Meteo (https://open-meteo.com):
    - Текущая погода: /v1/forecast?current_weather=true
    - Прогноз: /v1/forecast?daily=...
    - Качество воздуха: /v1/air-quality?current=...

Open-Meteo бесплатен, не требует API-ключа и покрывает города России.
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_get

from .constants import (
    OPEN_METEO_AIR_QUALITY_BASE,
    OPEN_METEO_BASE,
    STANCII_MONITORINGA,
    TIPY_EKODANNYKH,
    TIPY_METEODANNYKH,
    TIPY_PREDUPREZHDENIY,
    WMO_KODY_POGODY,
)
from .schemas import (
    EkologiyaData,
    PogodaData,
    Preduprezhdenie,
    PrognozData,
    SputnikMonitoring,
)


def _find_stanciya(code: str) -> dict[str, Any] | None:
    """Поиск станции мониторинга по коду."""
    for s in STANCII_MONITORINGA:
        if s["kod"] == code:
            return s
    return None


async def poluchit_pogodu(stanciya: str = "77") -> PogodaData | None:
    """Получение текущих данных о погоде через API Open-Meteo.

    Аргументы:
        stanciya: Код станции (по умолчанию: Москва — 77).

    Возвращает:
        Данные о текущей погоде или None.
    """
    info = _find_stanciya(stanciya)
    if not info:
        return None

    params = {
        "latitude": info["shirota"],
        "longitude": info["dolgota"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m,surface_pressure",
        "timezone": "Europe/Moscow",
    }
    try:
        data = await http_get(OPEN_METEO_BASE, params=params)
        return _parse_openmeteo_pogoda(data, info)
    except Exception:
        return None


async def poluchit_prognoz(
    stanciya: str = "77",
    dni: int = 3,
) -> list[PrognozData]:
    """Получение прогноза погоды через API Open-Meteo.

    Аргументы:
        stanciya: Код станции.
        dni: Количество дней прогноза (1-16).

    Возвращает:
        Список данных прогноза.
    """
    info = _find_stanciya(stanciya)
    if not info:
        return []

    params = {
        "latitude": info["shirota"],
        "longitude": info["dolgota"],
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
        "timezone": "Europe/Moscow",
        "forecast_days": min(max(dni, 1), 16),
    }
    try:
        data = await http_get(OPEN_METEO_BASE, params=params)
        return _parse_openmeteo_prognoz(data, info)
    except Exception:
        return []


async def poluchit_ekologiyu(
    gorod: str = "",
    tip: str = "",
) -> list[EkologiyaData]:
    """Получение данных о качестве воздуха через API Open-Meteo Air Quality.

    Аргументы:
        gorod: Фильтр по названию города (сопоставляется с названиями станций).
        tip: Фильтр по типу данных (пока поддерживается только 'vozdukh').

    Возвращает:
        Список экологических данных.
    """
    stations = STANCII_MONITORINGA
    if gorod:
        stations = [s for s in stations if gorod.lower() in s["nazvanie"].lower()]
    if not stations:
        stations = STANCII_MONITORINGA[:5]

    results = []
    for station in stations[:5]:
        params = {
            "latitude": station["shirota"],
            "longitude": station["dolgota"],
            "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone",
            "timezone": "Europe/Moscow",
        }
        try:
            data = await http_get(OPEN_METEO_AIR_QUALITY_BASE, params=params)
            parsed = _parse_openmeteo_ekologiya(data, station)
            results.extend(parsed)
        except Exception:
            continue

    if tip:
        results = [r for r in results if r.tip == tip]

    return results


async def poluchit_preduprezhdeniya(region: str = "") -> list[Preduprezhdenie]:
    """Получение активных предупреждений о погоде.

    Open-Meteo не предоставляет данные о предупреждениях. Эта функция
    проверяет текущие погодные условия и генерирует предупреждения для экстремальных значений.

    Аргументы:
        region: Код или название региона.

    Возвращает:
        Список активных предупреждений.
    """
    stations = STANCII_MONITORINGA
    if region:
        stations = [
            s
            for s in stations
            if region.lower() in s.get("region", "").lower()
            or region.lower() in s.get("nazvanie", "").lower()
        ]
    if not stations:
        stations = STANCII_MONITORINGA

    warnings = []
    for station in stations[:3]:
        params = {
            "latitude": station["shirota"],
            "longitude": station["dolgota"],
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "timezone": "Europe/Moscow",
        }
        try:
            data = await http_get(OPEN_METEO_BASE, params=params)
            current = data.get("current", {})
            temp = current.get("temperature_2m")
            wind = current.get("wind_speed_10m")
            wmo = current.get("weather_code", 0)

            if temp is not None and temp <= -30:
                warnings.append(
                    Preduprezhdenie(
                        tip="moroz",
                        region=station.get("region", ""),
                        gorod=station["nazvanie"],
                        opisanie=f"Сильный мороз: {temp}°C",
                        uroven_opasnosti="vysokiy",
                    )
                )
            elif temp is not None and temp >= 35:
                warnings.append(
                    Preduprezhdenie(
                        tip="zhara",
                        region=station.get("region", ""),
                        gorod=station["nazvanie"],
                        opisanie=f"Сильная жара: {temp}°C",
                        uroven_opasnosti="sredniy",
                    )
                )

            if wind is not None and wind >= 20:
                warnings.append(
                    Preduprezhdenie(
                        tip="shtorm",
                        region=station.get("region", ""),
                        gorod=station["nazvanie"],
                        opisanie=f"Сильный ветер: {wind:.1f} м/с",
                        uroven_opasnosti="vysokiy" if wind >= 30 else "sredniy",
                    )
                )

            if wmo in (95, 96, 99):
                warnings.append(
                    Preduprezhdenie(
                        tip="urogan",
                        region=station.get("region", ""),
                        gorod=station["nazvanie"],
                        opisanie=f"Гроза ({WMO_KODY_POGODY.get(wmo, '')})",
                        uroven_opasnosti="sredniy" if wmo == 95 else "vysokiy",
                    )
                )
        except Exception:
            continue

    return warnings


async def poluchit_sputnik_dannye(
    region: str = "",
    tip: str = "",
) -> list[SputnikMonitoring]:
    """Заглушка данных спутникового мониторинга.

    Open-Meteo не предоставляет спутниковые снимки. Остаётся заглушкой.

    Аргументы:
        region: Фильтр по региону.
        tip: Тип данных (lesa, voda, pozhary, snezhnyy_pokrov).

    Возвращает:
        Пустой список — спутниковые данные недоступны через текущий API.
    """
    return []


def get_stancii_list() -> list[dict[str, Any]]:
    """Возвращает список мониторинговых станций."""
    return STANCII_MONITORINGA


def get_tipy_meteo_list() -> list[dict[str, str]]:
    """Возвращает список типов метеорологических данных."""
    return TIPY_METEODANNYKH


def get_tipy_eko_list() -> list[dict[str, str]]:
    """Возвращает список типов экологических данных."""
    return TIPY_EKODANNYKH


def get_tipy_preduprezhdeniy_list() -> list[dict[str, str]]:
    """Возвращает список типов предупреждений."""
    return TIPY_PREDUPREZHDENIY


# --- Разборщики ответов Open-Meteo ---


def _parse_openmeteo_pogoda(data: dict[str, Any], info: dict[str, Any]) -> PogodaData:
    """Разбор ответа прогноза Open-Meteo в PogodaData."""
    current = data.get("current", {})
    wmo_code = current.get("weather_code", 0)
    wind_dir_deg = current.get("wind_direction_10m", 0)
    opisaniye = WMO_KODY_POGODY.get(wmo_code, "")

    return PogodaData(
        stanciya=info["kod"],
        gorod=info["nazvanie"],
        region=info.get("region", ""),
        temperatura=current.get("temperature_2m"),
        oshchushchaetsya_kak=current.get("apparent_temperature"),
        vlazhnost=current.get("relative_humidity_2m"),
        davlenie=_hpa_to_mmhg(current.get("surface_pressure")),
        veter_skorost=current.get("wind_speed_10m"),
        veter_napravlenie=_deg_to_napravlenie(wind_dir_deg),
        osadki=current.get("precipitation"),
        vidimost=None,
        opisaniye=opisaniye,
        data_vremya=current.get("time", ""),
    )


def _parse_openmeteo_prognoz(data: dict[str, Any], info: dict[str, Any]) -> list[PrognozData]:
    """Разбор ежедневного прогноза Open-Meteo в список PrognozData."""
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    t_max = daily.get("temperature_2m_max", [])
    t_min = daily.get("temperature_2m_min", [])
    precip_prob = daily.get("precipitation_probability_max", [])
    wind_max = daily.get("wind_speed_10m_max", [])
    wmo_codes = daily.get("weather_code", [])

    results = []
    for i, date_str in enumerate(dates):
        wmo_code = wmo_codes[i] if i < len(wmo_codes) else 0
        results.append(
            PrognozData(
                gorod=info["nazvanie"],
                data=date_str,
                temperatura_dnem=t_max[i] if i < len(t_max) else None,
                temperatura_nochyu=t_min[i] if i < len(t_min) else None,
                osadki_veroyatnost=precip_prob[i] if i < len(precip_prob) else None,
                veter_skorost=wind_max[i] if i < len(wind_max) else None,
                opisaniye=WMO_KODY_POGODY.get(wmo_code, ""),
            )
        )
    return results


def _parse_openmeteo_ekologiya(data: dict[str, Any], info: dict[str, Any]) -> list[EkologiyaData]:
    """Разбор ответа о качестве воздуха Open-Meteo в список EkologiyaData."""
    current = data.get("current", {})
    time_str = current.get("time", "")

    indicators = [
        ("pm2_5", "PM2.5", 25.0),
        ("pm10", "PM10", 50.0),
        ("carbon_monoxide", "CO", 4.0),
        ("nitrogen_dioxide", "NO₂", 40.0),
        ("sulphur_dioxide", "SO₂", 20.0),
        ("ozone", "O₃", 120.0),
    ]

    results = []
    for key, name, norma in indicators:
        value = current.get(key)
        if value is not None:
            prevyshenie = value > norma
            results.append(
                EkologiyaData(
                    gorod=info["nazvanie"],
                    stanciya=info["kod"],
                    tip="vozdukh",
                    pokazatel=name,
                    znachenie=round(value, 2),
                    norma_max=norma,
                    norma_min=None,
                    prevyshenie=prevyshenie,
                    data_izmereniya=time_str,
                )
            )
    return results


def _hpa_to_mmhg(hpa: float | None) -> float | None:
    """Конвертация гектопаскалей в мм рт. ст."""
    if hpa is None:
        return None
    return round(hpa * 0.750062, 1)


def _deg_to_napravlenie(deg: float) -> str:
    """Преобразование градусов направления ветра в российское компасное направление."""
    directions = [
        "С",
        "ССВ",
        "СВ",
        "ВСВ",
        "В",
        "ВЮВ",
        "ЮВ",
        "ЮЮВ",
        "Ю",
        "ЮЮЗ",
        "ЮЗ",
        "ЗЮЗ",
        "З",
        "ЗСЗ",
        "СЗ",
        "ССЗ",
    ]
    idx = round(deg / 22.5) % 16
    return directions[idx]
