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
    OTKRYTYY_METEO_BAZA,
    OTKRYTYY_METEO_BAZA_KACHESTVA_VOZDUKHA,
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
    SputnikovyyMonitoring,
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
        dannye = await http_poluchit(OTKRYTYY_METEO_BAZA, parametry=parametry)
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
        dannye = await http_poluchit(OTKRYTYY_METEO_BAZA, parametry=parametry)
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
    stantsii = STANCII_MONITORINGA
    if gorod:
        stantsii = [s for s in stantsii if gorod.lower() in s["nazvanie"].lower()]
    if not stantsii:
        stantsii = STANCII_MONITORINGA[:5]

    rezultaty = []
    for stantsiya in stantsii[:5]:
        parametry = {
            "latitude": stantsiya["shirota"],
            "longitude": stantsiya["dolgota"],
            "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone",
            "timezone": "Europe/Moscow",
        }
        try:
            dannye = await http_poluchit(
                OTKRYTYY_METEO_BAZA_KACHESTVA_VOZDUKHA, parametry=parametry
            )
            razobrannye = _razobrat_openmeteo_ekologiyu(dannye, stantsiya)
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
        subiekt: Код или название региона.

    Возвращает:
        Список активных предупреждений.
    """
    stantsii = STANCII_MONITORINGA
    if subiekt:
        stantsii = [
            s
            for s in stantsii
            if subiekt.lower() in s.get("subiekt", "").lower()
            or subiekt.lower() in s.get("nazvanie", "").lower()
        ]
    if not stantsii:
        stantsii = STANCII_MONITORINGA

    preduprezhdeniya = []
    for stantsiya in stantsii[:3]:
        parametry = {
            "latitude": stantsiya["shirota"],
            "longitude": stantsiya["dolgota"],
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "timezone": "Europe/Moscow",
        }
        try:
            dannye = await http_poluchit(OTKRYTYY_METEO_BAZA, parametry=parametry)
            tekushchie = dannye.get("current", {})
            temperatura = tekushchie.get("temperature_2m")
            skorost_vetra = tekushchie.get("wind_speed_10m")
            vmo = tekushchie.get("weather_code", 0)

            if temperatura is not None and temperatura <= -30:
                preduprezhdeniya.append(
                    Preduprezhdenie(
                        tip="moroz",
                        subiekt=stantsiya.get("subiekt", ""),
                        gorod=stantsiya["nazvanie"],
                        opisanie=f"Сильный мороз: {temperatura}°C",
                        uroven_opasnosti="vysokiy",
                    )
                )
            elif temperatura is not None and temperatura >= 35:
                preduprezhdeniya.append(
                    Preduprezhdenie(
                        tip="zhara",
                        subiekt=stantsiya.get("subiekt", ""),
                        gorod=stantsiya["nazvanie"],
                        opisanie=f"Сильная жара: {temperatura}°C",
                        uroven_opasnosti="sredniy",
                    )
                )

            if skorost_vetra is not None and skorost_vetra >= 20:
                preduprezhdeniya.append(
                    Preduprezhdenie(
                        tip="shtorm",
                        subiekt=stantsiya.get("subiekt", ""),
                        gorod=stantsiya["nazvanie"],
                        opisanie=f"Сильный ветер: {skorost_vetra:.1f} м/с",
                        uroven_opasnosti="vysokiy" if skorost_vetra >= 30 else "sredniy",
                    )
                )

            if vmo in (95, 96, 99):
                preduprezhdeniya.append(
                    Preduprezhdenie(
                        tip="uroagan",
                        subiekt=stantsiya.get("subiekt", ""),
                        gorod=stantsiya["nazvanie"],
                        opisanie=f"Гроза ({WMO_KODY_POGODY.get(vmo, '')})",
                        uroven_opasnosti="sredniy" if vmo == 95 else "vysokiy",
                    )
                )
        except Exception:
            continue

    return preduprezhdeniya


async def poluchit_sputnik_dannye(
    subiekt: str = "",
    tip: str = "",
) -> list[SputnikovyyMonitoring]:
    """Заглушка данных спутникового мониторинга.

    Open-Meteo не предоставляет спутниковые снимки. Остаётся заглушкой.

    Аргументы:
        subiekt: Фильтр по региону.
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
    tekushchie = dannye.get("current", {})
    kod_vmo = tekushchie.get("weather_code", 0)
    gradusy_napravleniya_vetra = tekushchie.get("wind_direction_10m", 0)
    opisaniye = WMO_KODY_POGODY.get(kod_vmo, "")

    return PogodaDannye(
        stanciya=svedeniya["kod"],
        gorod=svedeniya["nazvanie"],
        subiekt=svedeniya.get("subiekt", ""),
        temperatura=tekushchie.get("temperature_2m"),
        oshchushchaetsya_kak=tekushchie.get("apparent_temperature"),
        vlazhnost=tekushchie.get("relative_humidity_2m"),
        davlenie=_gpa_v_mmrtst(tekushchie.get("surface_pressure")),
        veter_skorost=tekushchie.get("wind_speed_10m"),
        veter_napravlenie=_gradusy_v_napravlenie(gradusy_napravleniya_vetra),
        osadki=tekushchie.get("precipitation"),
        vidimost=None,
        opisaniye=opisaniye,
        data_vremya=tekushchie.get("time", ""),
    )


def _razobrat_openmeteo_prognoz(
    dannye: dict[str, Any], svedeniya: dict[str, Any]
) -> list[PrognozDannye]:
    """Разбор ежедневного прогноза Open-Meteo в список PrognozDannye."""
    ezhednevnye = dannye.get("daily", {})
    daty = ezhednevnye.get("time", [])
    temperatura_maks = ezhednevnye.get("temperature_2m_max", [])
    temperatura_min = ezhednevnye.get("temperature_2m_min", [])
    veroyatnost_osadkov = ezhednevnye.get("precipitation_probability_max", [])
    skorost_vetra_maks = ezhednevnye.get("wind_speed_10m_max", [])
    kody_vmo = ezhednevnye.get("weather_code", [])

    rezultaty = []
    for i, stroka_daty in enumerate(daty):
        kod_vmo = kody_vmo[i] if i < len(kody_vmo) else 0
        rezultaty.append(
            PrognozDannye(
                gorod=svedeniya["nazvanie"],
                data=stroka_daty,
                temperatura_dnem=temperatura_maks[i] if i < len(temperatura_maks) else None,
                temperatura_nochyu=temperatura_min[i] if i < len(temperatura_min) else None,
                osadki_veroyatnost=veroyatnost_osadkov[i]
                if i < len(veroyatnost_osadkov)
                else None,
                veter_skorost=skorost_vetra_maks[i] if i < len(skorost_vetra_maks) else None,
                opisaniye=WMO_KODY_POGODY.get(kod_vmo, ""),
            )
        )
    return rezultaty


def _razobrat_openmeteo_ekologiyu(
    dannye: dict[str, Any], svedeniya: dict[str, Any]
) -> list[EkologiyaDannye]:
    """Разбор ответа о качестве воздуха Open-Meteo в список EkologiyaDannye."""
    tekushchie = dannye.get("current", {})
    stroka_vremeni = tekushchie.get("time", "")

    pokazateli_kachestva = [
        ("pm2_5", "PM2.5", 25.0),
        ("pm10", "PM10", 50.0),
        ("carbon_monoxide", "CO", 4.0),
        ("nitrogen_dioxide", "NO₂", 40.0),
        ("sulphur_dioxide", "SO₂", 20.0),
        ("ozone", "O₃", 120.0),
    ]

    rezultaty = []
    for klyuch, nazvanie_pokazatelya, norma in pokazateli_kachestva:
        znachenie_pokazatelya = tekushchie.get(klyuch)
        if znachenie_pokazatelya is not None:
            prevyshenie = znachenie_pokazatelya > norma
            rezultaty.append(
                EkologiyaDannye(
                    gorod=svedeniya["nazvanie"],
                    stanciya=svedeniya["kod"],
                    tip="vozdukh",
                    pokazatel=nazvanie_pokazatelya,
                    znachenie=round(znachenie_pokazatelya, 2),
                    norma_max=norma,
                    norma_min=None,
                    prevyshenie=prevyshenie,
                    data_izmereniya=stroka_vremeni,
                )
            )
    return rezultaty


def _gpa_v_mmrtst(hpa: float | None) -> float | None:
    """Конвертация гектопаскалей в мм рт. ст."""
    if hpa is None:
        return None
    return round(hpa * 0.750062, 1)


def _gradusy_v_napravlenie(gradusy: float) -> str:
    """Преобразование градусов направления ветра в российское компасное направление."""
    napravleniya = [
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
    indeks = round(gradusy / 22.5) % 16
    return napravleniya[indeks]
