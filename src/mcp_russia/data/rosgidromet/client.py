"""HTTP-клиент для модуля Росгидромета.

Интеграция через Open-Meteo (https://open-meteo.com):
    - Текущая погода: /v1/forecast?current_weather=true
    - Прогноз: /v1/forecast?daily=...
    - Качество воздуха: /v1/air-quality?current=...

Open-Meteo бесплатен, не требует API-ключа и покрывает города России.
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_poluchit

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
    EkologiyaDannye,
    PogodaDannye,
    Preduprezhdenie,
    PrognozDannye,
    SputnikMonitoring,
)


def _nayti_stantsiyu(kod: str) -> dict[str, Any] | None:
    """Поиск станции мониторинга по коду."""
    for s in STANCII_MONITORINGA:
        if s["kod"] == kod:
            return s
    return None


async def poluchit_pogodu(stanciya: str = "77") -> PogodaDannye | None:
    """Получение текущих данных о погоде через API Open-Meteo.

    Аргументы:
        stanciya: Код станции (по умолчанию: Москва — 77).

    Возвращает:
        Данные о текущей погоде или None.
    """
    svedeniya = _nayti_stantsiyu(stanciya)
    if not svedeniya:
        return None

    parametry = {
        "latitude": svedeniya["shirota"],
        "longitude": svedeniya["dolgota"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m,surface_pressure",
        "timezone": "Europe/Moscow",
    }
    try:
        dannye = await http_poluchit(OPEN_METEO_BASE, parametry=parametry)
        return _razobrat_openmeteo_pogodu(dannye, svedeniya)
    except Exception:
        return None


async def poluchit_prognoz(
    stanciya: str = "77",
    dni: int = 3,
) -> list[PrognozDannye]:
    """Получение прогноза погоды через API Open-Meteo.

    Аргументы:
        stanciya: Код станции.
        dni: Количество дней прогноза (1-16).

    Возвращает:
        Список данных прогноза.
    """
    svedeniya = _nayti_stantsiyu(stanciya)
    if not svedeniya:
        return []

    parametry = {
        "latitude": svedeniya["shirota"],
        "longitude": svedeniya["dolgota"],
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
        "timezone": "Europe/Moscow",
        "forecast_days": min(max(dni, 1), 16),
    }
    try:
        dannye = await http_poluchit(OPEN_METEO_BASE, parametry=parametry)
        return _razobrat_openmeteo_prognoz(dannye, svedeniya)
    except Exception:
        return []


async def poluchit_ekologiyu(
    gorod: str = "",
    tip: str = "",
) -> list[EkologiyaDannye]:
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

    rezultaty = []
    for station in stations[:5]:
        parametry = {
            "latitude": station["shirota"],
            "longitude": station["dolgota"],
            "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone",
            "timezone": "Europe/Moscow",
        }
        try:
            dannye = await http_poluchit(OPEN_METEO_AIR_QUALITY_BASE, parametry=parametry)
            razobrannye = _razobrat_openmeteo_ekologiyu(dannye, station)
            rezultaty.extend(razobrannye)
        except Exception:
            continue

    if tip:
        rezultaty = [r for r in rezultaty if r.tip == tip]

    return rezultaty


async def poluchit_preduprezhdeniya(subiekt: str = "") -> list[Preduprezhdenie]:
    """Получение активных предупреждений о погоде.

    Open-Meteo не предоставляет данные о предупреждениях. Эта функция
    проверяет текущие погодные условия и генерирует предупреждения для экстремальных значений.

    Аргументы:
        region: Код или название региона.

    Возвращает:
        Список активных предупреждений.
    """
    stations = STANCII_MONITORINGA
    if subiekt:
        stations = [
            s
            for s in stations
            if subiekt.lower() in s.get("subiekt", "").lower()
            or subiekt.lower() in s.get("nazvanie", "").lower()
        ]
    if not stations:
        stations = STANCII_MONITORINGA

    warnings = []
    for station in stations[:3]:
        parametry = {
            "latitude": station["shirota"],
            "longitude": station["dolgota"],
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "timezone": "Europe/Moscow",
        }
        try:
            dannye = await http_poluchit(OPEN_METEO_BASE, parametry=parametry)
            current = dannye.get("current", {})
            temperatura = current.get("temperature_2m")
            wind = current.get("wind_speed_10m")
            wmo = current.get("weather_code", 0)

            if temperatura is not None and temperatura <= -30:
                warnings.append(
                    Preduprezhdenie(
                        tip="moroz",
                        subiekt=station.get("subiekt", ""),
                        gorod=station["nazvanie"],
                        opisanie=f"Сильный мороз: {temperatura}°C",
                        uroven_opasnosti="vysokiy",
                    )
                )
            elif temperatura is not None and temperatura >= 35:
                warnings.append(
                    Preduprezhdenie(
                        tip="zhara",
                        subiekt=station.get("subiekt", ""),
                        gorod=station["nazvanie"],
                        opisanie=f"Сильная жара: {temperatura}°C",
                        uroven_opasnosti="sredniy",
                    )
                )

            if wind is not None and wind >= 20:
                warnings.append(
                    Preduprezhdenie(
                        tip="shtorm",
                        subiekt=station.get("subiekt", ""),
                        gorod=station["nazvanie"],
                        opisanie=f"Сильный ветер: {wind:.1f} м/с",
                        uroven_opasnosti="vysokiy" if wind >= 30 else "sredniy",
                    )
                )

            if wmo in (95, 96, 99):
                warnings.append(
                    Preduprezhdenie(
                        tip="uroagan",
                        subiekt=station.get("subiekt", ""),
                        gorod=station["nazvanie"],
                        opisanie=f"Гроза ({WMO_KODY_POGODY.get(wmo, '')})",
                        uroven_opasnosti="sredniy" if wmo == 95 else "vysokiy",
                    )
                )
        except Exception:
            continue

    return warnings


async def poluchit_sputnik_dannye(
    subiekt: str = "",
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


def poluchit_spisok_stantsiy() -> list[dict[str, Any]]:
    """Возвращает список мониторинговых станций."""
    return STANCII_MONITORINGA


def poluchit_spisok_tipov_meteo() -> list[dict[str, str]]:
    """Возвращает список типов метеорологических данных."""
    return TIPY_METEODANNYKH


def poluchit_spisok_tipov_eko() -> list[dict[str, str]]:
    """Возвращает список типов экологических данных."""
    return TIPY_EKODANNYKH


def poluchit_spisok_tipov_preduprezhdeniy() -> list[dict[str, str]]:
    """Возвращает список типов предупреждений."""
    return TIPY_PREDUPREZHDENIY


# --- Разборщики ответов Open-Meteo ---


def _razobrat_openmeteo_pogodu(dannye: dict[str, Any], svedeniya: dict[str, Any]) -> PogodaDannye:
    """Разбор ответа прогноза Open-Meteo в PogodaDannye."""
    current = dannye.get("current", {})
    wmo_code = current.get("weather_code", 0)
    wind_dir_deg = current.get("wind_direction_10m", 0)
    opisaniye = WMO_KODY_POGODY.get(wmo_code, "")

    return PogodaDannye(
        stanciya=svedeniya["kod"],
        gorod=svedeniya["nazvanie"],
        subiekt=svedeniya.get("subiekt", ""),
        temperatura=current.get("temperature_2m"),
        oshchushchaetsya_kak=current.get("apparent_temperature"),
        vlazhnost=current.get("relative_humidity_2m"),
        davlenie=_gpa_v_mmrtst(current.get("surface_pressure")),
        veter_skorost=current.get("wind_speed_10m"),
        veter_napravlenie=_gradusy_v_napravlenie(wind_dir_deg),
        osadki=current.get("precipitation"),
        vidimost=None,
        opisaniye=opisaniye,
        data_vremya=current.get("time", ""),
    )


def _razobrat_openmeteo_prognoz(
    dannye: dict[str, Any], svedeniya: dict[str, Any]
) -> list[PrognozDannye]:
    """Разбор ежедневного прогноза Open-Meteo в список PrognozDannye."""
    daily = dannye.get("daily", {})
    dates = daily.get("time", [])
    t_max = daily.get("temperature_2m_max", [])
    t_min = daily.get("temperature_2m_min", [])
    precip_prob = daily.get("precipitation_probability_max", [])
    wind_max = daily.get("wind_speed_10m_max", [])
    wmo_codes = daily.get("weather_code", [])

    rezultaty = []
    for i, date_str in enumerate(dates):
        wmo_code = wmo_codes[i] if i < len(wmo_codes) else 0
        rezultaty.append(
            PrognozDannye(
                gorod=svedeniya["nazvanie"],
                data=date_str,
                temperatura_dnem=t_max[i] if i < len(t_max) else None,
                temperatura_nochyu=t_min[i] if i < len(t_min) else None,
                osadki_veroyatnost=precip_prob[i] if i < len(precip_prob) else None,
                veter_skorost=wind_max[i] if i < len(wind_max) else None,
                opisaniye=WMO_KODY_POGODY.get(wmo_code, ""),
            )
        )
    return rezultaty


def _razobrat_openmeteo_ekologiyu(
    dannye: dict[str, Any], svedeniya: dict[str, Any]
) -> list[EkologiyaDannye]:
    """Разбор ответа о качестве воздуха Open-Meteo в список EkologiyaDannye."""
    current = dannye.get("current", {})
    time_str = current.get("time", "")

    indicators = [
        ("pm2_5", "PM2.5", 25.0),
        ("pm10", "PM10", 50.0),
        ("carbon_monoxide", "CO", 4.0),
        ("nitrogen_dioxide", "NO₂", 40.0),
        ("sulphur_dioxide", "SO₂", 20.0),
        ("ozone", "O₃", 120.0),
    ]

    rezultaty = []
    for key, name, norma in indicators:
        value = current.get(key)
        if value is not None:
            prevyshenie = value > norma
            rezultaty.append(
                EkologiyaDannye(
                    gorod=svedeniya["nazvanie"],
                    stanciya=svedeniya["kod"],
                    tip="vozdukh",
                    pokazatel=name,
                    znachenie=round(value, 2),
                    norma_max=norma,
                    norma_min=None,
                    prevyshenie=prevyshenie,
                    data_izmereniya=time_str,
                )
            )
    return rezultaty


def _gpa_v_mmrtst(hpa: float | None) -> float | None:
    """Конвертация гектопаскалей в мм рт. ст."""
    if hpa is None:
        return None
    return round(hpa * 0.750062, 1)


def _gradusy_v_napravlenie(deg: float) -> str:
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
