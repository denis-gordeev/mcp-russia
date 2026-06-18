"""HTTP-клиент для API Картотеки арбитражных дел.

Интеграция с реальными API:
    - Поиск дел: POST https://kad.arbitr.ru/Kad/Search
    - Карточка дела: GET https://kad.arbitr.ru/Kad/Instance/{id}

API КАД является публичным и не требует аутентификации.
Ограничение запросов: будьте уважительны, добавляйте задержки между запросами.
"""

from __future__ import annotations

import contextlib
from typing import Any

from mcp_russia._shared.http_client import http_get, http_post

from .constants import (
    INSTANTSII_SUDOV,
    KATEGORII_DEL,
    KATEGORII_KAD,
    STATUSY_DEL,
    SUDY_PRYAMYE,
    TIPLY_AKTOV,
)
from .schemas import StoronaDela, SudebnoeDelo, SudebnoeZasedanie, SudebnyyAkt, Sudy


def _opredelit_sud_po_nomeru(number: str) -> str:
    """Определить суд по префиксу номера дела."""
    kod = number.split("-")[0] if "-" in number else number[:3]
    return SUDY_PRYAMYE.get(kod, "")


def _opredelit_kategoriyu(number: str) -> str:
    """Определить категорию дела по букве номера."""
    if len(number) > 4 and number[4] == "-":
        letter = number[3] if len(number) > 3 else ""
        return KATEGORII_KAD.get(letter, "")
    return ""


def _parse_rezultaty_poiska(data: Any) -> list[SudebnoeDelo]:
    """Разбор результатов поиска дел из API КАД."""
    if isinstance(data, dict):
        items = data.get("Instances", data.get("Result", []))
    elif isinstance(data, list):
        items = data
    else:
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        case_info = item.get("CaseInfo", item)
        number = case_info.get("CaseNumber", item.get("caseNumber", ""))
        category = _opredelit_kategoriyu(number) or case_info.get(
            "Category", item.get("category", "")
        )
        sud_name = case_info.get("Court", item.get("courtName", ""))
        if not sud_name:
            sud_name = _opredelit_sud_po_nomeru(number)

        istorcy_raw = case_info.get("Plaintiffs", item.get("plaintiffs", ""))
        if isinstance(istorcy_raw, str):
            istorcy = [s.strip() for s in istorcy_raw.split(",") if s.strip()]
        elif isinstance(istorcy_raw, list):
            istorcy = [s if isinstance(s, str) else str(s) for s in istorcy_raw]
        else:
            istorcy = []

        otvetchiki_raw = case_info.get("Defendants", item.get("defendants", ""))
        if isinstance(otvetchiki_raw, str):
            otvetchiki = [s.strip() for s in otvetchiki_raw.split(",") if s.strip()]
        elif isinstance(otvetchiki_raw, list):
            otvetchiki = [s if isinstance(s, str) else str(s) for s in otvetchiki_raw]
        else:
            otvetchiki = []

        summa = 0.0
        summa_raw = case_info.get("ClaimSum", item.get("claimSum"))
        if summa_raw:
            with contextlib.suppress(ValueError, TypeError):
                summa = float(summa_raw)

        results.append(
            SudebnoeDelo(
                number=number,
                category=category,
                status=case_info.get("Status", item.get("status", "")),
                sudya=case_info.get("Judge", item.get("judge", "")),
                nazvanie_suda=sud_name,
                data_vozbuzhdeniya=case_info.get(
                    "RegistrationDate", item.get("registrationDate", "")
                ),
                data_poslednego_akta=case_info.get(
                    "LastDocumentDate", item.get("lastDocumentDate", "")
                ),
                istorcy=istorcy,
                otvetchiki=otvetchiki,
                summa_iska=summa,
            )
        )
    return results


def _parse_kartochka_dela(data: Any) -> SudebnoeDelo | None:
    """Разбор карточки судебного дела из API КАД."""
    if not isinstance(data, dict):
        return None

    case_info = data.get("CaseInfo", data.get("Case", data))
    number = case_info.get("CaseNumber", data.get("caseNumber", ""))
    if not number:
        return None

    category = _opredelit_kategoriyu(number) or case_info.get("Category", data.get("category", ""))
    sud_name = case_info.get("Court", data.get("courtName", ""))
    if not sud_name:
        sud_name = _opredelit_sud_po_nomeru(number)

    istorcy_raw = case_info.get("Plaintiffs", data.get("plaintiffs", ""))
    if isinstance(istorcy_raw, str):
        istorcy = [s.strip() for s in istorcy_raw.split(",") if s.strip()]
    elif isinstance(istorcy_raw, list):
        istorcy = [s if isinstance(s, str) else str(s) for s in istorcy_raw]
    else:
        istorcy = []

    otvetchiki_raw = case_info.get("Defendants", data.get("defendants", ""))
    if isinstance(otvetchiki_raw, str):
        otvetchiki = [s.strip() for s in otvetchiki_raw.split(",") if s.strip()]
    elif isinstance(otvetchiki_raw, list):
        otvetchiki = [s if isinstance(s, str) else str(s) for s in otvetchiki_raw]
    else:
        otvetchiki = []

    summa = 0.0
    summa_raw = case_info.get("ClaimSum", data.get("claimSum"))
    if summa_raw:
        with contextlib.suppress(ValueError, TypeError):
            summa = float(summa_raw)

    return SudebnoeDelo(
        number=number,
        category=category,
        status=case_info.get("Status", data.get("status", "")),
        sudya=case_info.get("Judge", data.get("judge", "")),
        nazvanie_suda=sud_name,
        data_vozbuzhdeniya=case_info.get("RegistrationDate", data.get("registrationDate", "")),
        data_poslednego_akta=case_info.get("LastDocumentDate", data.get("lastDocumentDate", "")),
        istorcy=istorcy,
        otvetchiki=otvetchiki,
        summa_iska=summa,
    )


def _parse_akty(data: Any, delo_number: str) -> list[SudebnyyAkt]:
    """Разбор судебных актов из ответа API КАД."""
    if isinstance(data, dict):
        items = data.get("Documents", data.get("Result", []))
    elif isinstance(data, list):
        items = data
    else:
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        doc = item.get("Document", item)
        results.append(
            SudebnyyAkt(
                id=str(doc.get("Id", doc.get("id", ""))),
                delo_number=delo_number,
                tip_akta=doc.get("DocumentType", doc.get("type", "")),
                data_akta=doc.get("DocumentDate", doc.get("date", "")),
                sud=doc.get("CourtName", doc.get("court", "")),
                sudya=doc.get("Judge", doc.get("judge", "")),
                kratkoe_soderzhanie=doc.get("ShortContent", doc.get("summary", "")),
                rezolyutsiya=doc.get("Resolution", doc.get("resolution", "")),
                pdf_url=doc.get("PdfUrl", doc.get("pdfUrl", "")),
            )
        )
    return results


def _parse_storony(data: Any, delo_number: str) -> list[StoronaDela]:
    """Разбор сторон судебного дела из ответа API КАД."""
    if not isinstance(data, dict):
        return []

    results = []
    for side_type, tip_label in [("Plaintiffs", "истец"), ("Defendants", "ответчик")]:
        raw = data.get(side_type, [])
        if isinstance(raw, str):
            names = [s.strip() for s in raw.split(",") if s.strip()]
        elif isinstance(raw, list):
            names = [s if isinstance(s, str) else str(s) for s in raw]
        else:
            continue
        for name in names:
            inn = ""
            if "ИНН" in name:
                parts = name.split("ИНН")
                name = parts[0].strip().rstrip(",").strip()
                inn = parts[1].strip().lstrip(":").strip().split()[0] if len(parts) > 1 else ""
            results.append(
                StoronaDela(
                    nazvanie=name,
                    inn=inn,
                    tip=tip_label,
                )
            )
    return results


async def poisk_del(
    number: str = "",
    istorcz: str = "",
    otvetchik: str = "",
    inn: str = "",
    category: str = "",
    status: str = "",
    sudya: str = "",
    limit: int = 20,
) -> list[SudebnoeDelo]:
    """Поиск дел в Картотеке арбитражных дел через API kad.arbitr.ru.

    Аргументы:
        number: Номер дела (например, 'А40-12345/2024').
        istorcz: Название истца.
        otvetchik: Название ответчика.
        inn: ИНН участника.
        category: Категория дела.
        status: Статус дела.
        sudya: Фамилия судьи.
        limit: Максимальное количество результатов.

    Возвращает:
        Список судебных дел.
    """
    sides: list[dict[str, Any]] = []
    if istorcz:
        sides.append({"Name": istorcz, "Type": 1, "ExactMatch": False})
    if otvetchik:
        sides.append({"Name": otvetchik, "Type": 2, "ExactMatch": False})
    if inn:
        sides.append({"Name": inn, "Type": -1, "ExactMatch": True})

    body: dict[str, Any] = {
        "Page": 1,
        "Count": min(limit, 25),
        "Courts": [],
        "Judges": [sudya] if sudya else [],
        "DateFrom": None,
        "DateTo": None,
        "Sides": sides,
        "CaseNumber": number,
        "WithNewInstances": False,
        "OnlyNew": False,
    }

    try:
        data = await http_post(
            "https://kad.arbitr.ru/Kad/Search",
            json_body=body,
            headers={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        return _parse_rezultaty_poiska(data)
    except Exception:
        return []


async def info_dela(number: str) -> SudebnoeDelo | None:
    """Получить подробную информацию о судебном деле.

    Аргументы:
        number: Номер дела.

    Возвращает:
        Данные дела или None.
    """
    try:
        data = await http_get(
            f"https://kad.arbitr.ru/Kad/Case/{number}",
            headers={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        return _parse_kartochka_dela(data)
    except Exception:
        return None


async def akty_po_delu(number: str) -> list[SudebnyyAkt]:
    """Получить судебные акты по делу.

    Аргументы:
        number: Номер дела.

    Возвращает:
        Список судебных актов.
    """
    try:
        data = await http_get(
            f"https://kad.arbitr.ru/Kad/Documents/{number}",
            headers={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        return _parse_akty(data, number)
    except Exception:
        return []


async def info_akta(id_akta: str) -> SudebnyyAkt | None:
    """Получить подробную информацию о судебном акте.

    Аргументы:
        id_akta: Идентификатор судебного акта.

    Возвращает:
        Данные акта или None.
    """
    try:
        data = await http_get(
            f"https://kad.arbitr.ru/Kad/Document/{id_akta}",
            headers={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        if isinstance(data, dict):
            doc = data.get("Document", data)
            return SudebnyyAkt(
                id=str(doc.get("Id", id_akta)),
                delo_number=doc.get("CaseNumber", ""),
                tip_akta=doc.get("DocumentType", ""),
                data_akta=doc.get("DocumentDate", ""),
                sud=doc.get("CourtName", ""),
                sudya=doc.get("Judge", ""),
                kratkoe_soderzhanie=doc.get("ShortContent", ""),
                rezolyutsiya=doc.get("Resolution", ""),
                pdf_url=doc.get("PdfUrl", ""),
            )
    except Exception:
        pass
    return None


async def zasedaniya_po_delu(number: str) -> list[SudebnoeZasedanie]:
    """Получить информацию о заседаниях по делу.

    Аргументы:
        number: Номер дела.

    Возвращает:
        Список заседаний.
    """
    try:
        data = await http_get(
            f"https://kad.arbitr.ru/Kad/Sessions/{number}",
            headers={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        if isinstance(data, dict):
            items = data.get("Sessions", data.get("Result", []))
        elif isinstance(data, list):
            items = data
        else:
            return []

        results = []
        for item in items:
            if not isinstance(item, dict):
                continue
            results.append(
                SudebnoeZasedanie(
                    id=str(item.get("Id", "")),
                    delo_number=number,
                    data_zasedaniya=item.get("Date", ""),
                    vremya=item.get("Time", ""),
                    sudya=item.get("Judge", ""),
                    zala=item.get("Hall", ""),
                    status=item.get("Status", ""),
                    rezultaty=item.get("Result", ""),
                )
            )
        return results
    except Exception:
        return []


async def poisk_sudey(familiya: str = "", sud_name: str = "") -> list[Sudy]:
    """Поиск судей арбитражных судов.

    Аргументы:
        familiya: Фамилия судьи.
        sud_name: Наименование суда.

    Возвращает:
        Список судей.
    """
    return []


async def storony_dela(number: str) -> list[StoronaDela]:
    """Получить стороны судебного дела.

    Аргументы:
        number: Номер дела.

    Возвращает:
        Список сторон (истцы и ответчики).
    """
    try:
        data = await http_get(
            f"https://kad.arbitr.ru/Kad/Sides/{number}",
            headers={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        return _parse_storony(data, number)
    except Exception:
        return []


def get_instantsii() -> list[dict[str, str]]:
    """Вернуть справочник инстанций судов."""
    return INSTANTSII_SUDOV


def get_kategorii_del() -> list[dict[str, str]]:
    """Вернуть справочник категорий дел."""
    return KATEGORII_DEL


def get_statusy_del() -> list[dict[str, str]]:
    """Вернуть справочник статусов дел."""
    return STATUSY_DEL


def get_tipy_aktov() -> list[dict[str, str]]:
    """Вернуть справочник типов актов."""
    return TIPLY_AKTOV
