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

from mcp_russia._shared.http_client import http_otpravit, http_poluchit

from .constants import (
    INSTANTSII_SUDOV,
    KATEGORII_DEL,
    KATEGORII_KAD,
    STATUSY_DEL,
    SUDY_PRYAMYE,
    TIPLY_AKTOV,
)
from .schemas import StoronaDela, SudebnoeDelo, SudebnoeZasedanie, SudebnyyAkt, Sudy


def _opredelit_sud_po_nomeru(nomer: str) -> str:
    """Определить суд по префиксу номера дела."""
    kod = nomer.split("-")[0] if "-" in nomer else nomer[:3]
    return SUDY_PRYAMYE.get(kod, "")


def _opredelit_kategoriyu(nomer: str) -> str:
    """Определить категорию дела по букве номера."""
    if len(nomer) > 4 and nomer[4] == "-":
        letter = nomer[3] if len(nomer) > 3 else ""
        return KATEGORII_KAD.get(letter, "")
    return ""


def _razobrat_rezultaty_poiska(dannye: Any) -> list[SudebnoeDelo]:
    """Разбор результатов поиска дел из API КАД."""
    if isinstance(dannye, dict):
        elementy = dannye.get("Instances", dannye.get("Result", []))
    elif isinstance(dannye, list):
        elementy = dannye
    else:
        return []

    rezultaty = []
    for element in elementy:
        if not isinstance(element, dict):
            continue
        case_info = element.get("CaseInfo", element)
        nomer = case_info.get("CaseNumber", element.get("caseNumber", ""))
        category = _opredelit_kategoriyu(nomer) or case_info.get(
            "Category", element.get("category", "")
        )
        sud_name = case_info.get("Court", element.get("courtName", ""))
        if not sud_name:
            sud_name = _opredelit_sud_po_nomeru(nomer)

        istorcy_raw = case_info.get("Plaintiffs", element.get("plaintiffs", ""))
        if isinstance(istorcy_raw, str):
            istorcy = [s.strip() for s in istorcy_raw.split(",") if s.strip()]
        elif isinstance(istorcy_raw, list):
            istorcy = [s if isinstance(s, str) else str(s) for s in istorcy_raw]
        else:
            istorcy = []

        otvetchiki_raw = case_info.get("Defendants", element.get("defendants", ""))
        if isinstance(otvetchiki_raw, str):
            otvetchiki = [s.strip() for s in otvetchiki_raw.split(",") if s.strip()]
        elif isinstance(otvetchiki_raw, list):
            otvetchiki = [s if isinstance(s, str) else str(s) for s in otvetchiki_raw]
        else:
            otvetchiki = []

        summa = 0.0
        summa_raw = case_info.get("ClaimSum", element.get("claimSum"))
        if summa_raw:
            with contextlib.suppress(ValueError, TypeError):
                summa = float(summa_raw)

        rezultaty.append(
            SudebnoeDelo(
                nomer=nomer,
                kategoriya=category,
                sostoyanie=case_info.get("Status", element.get("status", "")),
                sudya=case_info.get("Judge", element.get("judge", "")),
                nazvanie_suda=sud_name,
                data_vozbuzhdeniya=case_info.get(
                    "RegistrationDate", element.get("registrationDate", "")
                ),
                data_poslednego_akta=case_info.get(
                    "LastDocumentDate", element.get("lastDocumentDate", "")
                ),
                istorcy=istorcy,
                otvetchiki=otvetchiki,
                summa_iska=summa,
            )
        )
    return rezultaty


def _razobrat_kartochka_dela(dannye: Any) -> SudebnoeDelo | None:
    """Разбор карточки судебного дела из API КАД."""
    if not isinstance(dannye, dict):
        return None

    case_info = dannye.get("CaseInfo", dannye.get("Case", dannye))
    nomer = case_info.get("CaseNumber", dannye.get("caseNumber", ""))
    if not nomer:
        return None

    category = _opredelit_kategoriyu(nomer) or case_info.get(
        "Category", dannye.get("category", "")
    )
    sud_name = case_info.get("Court", dannye.get("courtName", ""))
    if not sud_name:
        sud_name = _opredelit_sud_po_nomeru(nomer)

    istorcy_raw = case_info.get("Plaintiffs", dannye.get("plaintiffs", ""))
    if isinstance(istorcy_raw, str):
        istorcy = [s.strip() for s in istorcy_raw.split(",") if s.strip()]
    elif isinstance(istorcy_raw, list):
        istorcy = [s if isinstance(s, str) else str(s) for s in istorcy_raw]
    else:
        istorcy = []

    otvetchiki_raw = case_info.get("Defendants", dannye.get("defendants", ""))
    if isinstance(otvetchiki_raw, str):
        otvetchiki = [s.strip() for s in otvetchiki_raw.split(",") if s.strip()]
    elif isinstance(otvetchiki_raw, list):
        otvetchiki = [s if isinstance(s, str) else str(s) for s in otvetchiki_raw]
    else:
        otvetchiki = []

    summa = 0.0
    summa_raw = case_info.get("ClaimSum", dannye.get("claimSum"))
    if summa_raw:
        with contextlib.suppress(ValueError, TypeError):
            summa = float(summa_raw)

    return SudebnoeDelo(
        nomer=nomer,
        kategoriya=category,
        sostoyanie=case_info.get("Status", dannye.get("status", "")),
        sudya=case_info.get("Judge", dannye.get("judge", "")),
        nazvanie_suda=sud_name,
        data_vozbuzhdeniya=case_info.get("RegistrationDate", dannye.get("registrationDate", "")),
        data_poslednego_akta=case_info.get("LastDocumentDate", dannye.get("lastDocumentDate", "")),
        istorcy=istorcy,
        otvetchiki=otvetchiki,
        summa_iska=summa,
    )


def _razobrat_akty(dannye: Any, delo_number: str) -> list[SudebnyyAkt]:
    """Разбор судебных актов из ответа API КАД."""
    if isinstance(dannye, dict):
        elementy = dannye.get("Documents", dannye.get("Result", []))
    elif isinstance(dannye, list):
        elementy = dannye
    else:
        return []

    rezultaty = []
    for element in elementy:
        if not isinstance(element, dict):
            continue
        doc = element.get("Document", element)
        rezultaty.append(
            SudebnyyAkt(
                identifikator=str(doc.get("Id", doc.get("id", ""))),
                delo_nomer=delo_number,
                tip_akta=doc.get("DocumentType", doc.get("type", "")),
                data_akta=doc.get("DocumentDate", doc.get("date", "")),
                sud=doc.get("CourtName", doc.get("court", "")),
                sudya=doc.get("Judge", doc.get("judge", "")),
                kratkoe_soderzhanie=doc.get("ShortContent", doc.get("summary", "")),
                rezolyutsiya=doc.get("Resolution", doc.get("resolution", "")),
                pdf_ssylka=doc.get("PdfUrl", doc.get("pdfUrl", "")),
            )
        )
    return rezultaty


def _razobrat_storony(dannye: Any, delo_number: str) -> list[StoronaDela]:
    """Разбор сторон судебного дела из ответа API КАД."""
    if not isinstance(dannye, dict):
        return []

    rezultaty = []
    for side_type, tip_label in [("Plaintiffs", "истец"), ("Defendants", "ответчик")]:
        raw = dannye.get(side_type, [])
        if isinstance(raw, str):
            names = [s.strip() for s in raw.split(",") if s.strip()]
        elif isinstance(raw, list):
            names = [s if isinstance(s, str) else str(s) for s in raw]
        else:
            continue
        for name in names:
            inn = ""
            if "ИНН" in name:
                chasti = name.split("ИНН")
                name = chasti[0].strip().rstrip(",").strip()
                inn = chasti[1].strip().lstrip(":").strip().split()[0] if len(chasti) > 1 else ""
            rezultaty.append(
                StoronaDela(
                    nazvanie=name,
                    inn=inn,
                    tip=tip_label,
                )
            )
    return rezultaty


async def poisk_del(
    nomer: str = "",
    istorcz: str = "",
    otvetchik: str = "",
    inn: str = "",
    kategoriya: str = "",
    status: str = "",
    sudya: str = "",
    ogranichenie: int = 20,
) -> list[SudebnoeDelo]:
    """Поиск дел в Картотеке арбитражных дел через API kad.arbitr.ru.

    Аргументы:
        nomer: Номер дела (например, 'А40-12345/2024').
        istorcz: Название истца.
        otvetchik: Название ответчика.
        inn: ИНН участника.
        kategoriya: Категория дела.
        status: Статус дела.
        sudya: Фамилия судьи.
        ogranichenie: Максимальное количество результатов.

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

    telo: dict[str, Any] = {
        "Page": 1,
        "Count": min(ogranichenie, 25),
        "Courts": [],
        "Judges": [sudya] if sudya else [],
        "DateFrom": None,
        "DateTo": None,
        "Sides": sides,
        "CaseNumber": nomer,
        "WithNewInstances": False,
        "OnlyNew": False,
    }

    try:
        dannye = await http_otpravit(
            "https://kad.arbitr.ru/Kad/Search",
            json_body=telo,
            zagolovki={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        return _razobrat_rezultaty_poiska(dannye)
    except Exception:
        return []


async def info_dela(nomer: str) -> SudebnoeDelo | None:
    """Получить подробную информацию о судебном деле.

    Аргументы:
        nomer: Номер дела.

    Возвращает:
        Данные дела или None.
    """
    try:
        dannye = await http_poluchit(
            f"https://kad.arbitr.ru/Kad/Case/{nomer}",
            zagolovki={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        return _razobrat_kartochka_dela(dannye)
    except Exception:
        return None


async def akty_po_delu(nomer: str) -> list[SudebnyyAkt]:
    """Получить судебные акты по делу.

    Аргументы:
        nomer: Номер дела.

    Возвращает:
        Список судебных актов.
    """
    try:
        dannye = await http_poluchit(
            f"https://kad.arbitr.ru/Kad/Documents/{nomer}",
            zagolovki={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        return _razobrat_akty(dannye, nomer)
    except Exception:
        return []


async def info_akta(identifikator_akta: str) -> SudebnyyAkt | None:
    """Получить подробную информацию о судебном акте.

    Аргументы:
        identifikator_akta: Идентификатор судебного акта.

    Возвращает:
        Данные акта или None.
    """
    try:
        dannye = await http_poluchit(
            f"https://kad.arbitr.ru/Kad/Document/{identifikator_akta}",
            zagolovki={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        if isinstance(dannye, dict):
            doc = dannye.get("Document", dannye)
            return SudebnyyAkt(
                identifikator=str(doc.get("Id", identifikator_akta)),
                delo_nomer=doc.get("CaseNumber", ""),
                tip_akta=doc.get("DocumentType", ""),
                data_akta=doc.get("DocumentDate", ""),
                sud=doc.get("CourtName", ""),
                sudya=doc.get("Judge", ""),
                kratkoe_soderzhanie=doc.get("ShortContent", ""),
                rezolyutsiya=doc.get("Resolution", ""),
                pdf_ssylka=doc.get("PdfUrl", ""),
            )
    except Exception:
        pass
    return None


async def zasedaniya_po_delu(nomer: str) -> list[SudebnoeZasedanie]:
    """Получить информацию о заседаниях по делу.

    Аргументы:
        nomer: Номер дела.

    Возвращает:
        Список заседаний.
    """
    try:
        dannye = await http_poluchit(
            f"https://kad.arbitr.ru/Kad/Sessions/{nomer}",
            zagolovki={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        if isinstance(dannye, dict):
            elementy = dannye.get("Sessions", dannye.get("Result", []))
        elif isinstance(dannye, list):
            elementy = dannye
        else:
            return []

        rezultaty = []
        for element in elementy:
            if not isinstance(element, dict):
                continue
            rezultaty.append(
                SudebnoeZasedanie(
                    identifikator=str(element.get("Id", "")),
                    delo_nomer=nomer,
                    data_zasedaniya=element.get("Date", ""),
                    vremya=element.get("Time", ""),
                    sudya=element.get("Judge", ""),
                    zala=element.get("Hall", ""),
                    sostoyanie=element.get("Status", ""),
                    rezultaty=element.get("Result", ""),
                )
            )
        return rezultaty
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


async def storony_dela(nomer: str) -> list[StoronaDela]:
    """Получить стороны судебного дела.

    Аргументы:
        nomer: Номер дела.

    Возвращает:
        Список сторон (истцы и ответчики).
    """
    try:
        dannye = await http_poluchit(
            f"https://kad.arbitr.ru/Kad/Sides/{nomer}",
            zagolovki={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        return _razobrat_storony(dannye, nomer)
    except Exception:
        return []


def poluchit_instantsii() -> list[dict[str, str]]:
    """Вернуть справочник инстанций судов."""
    return INSTANTSII_SUDOV


def poluchit_kategorii_del() -> list[dict[str, str]]:
    """Вернуть справочник категорий дел."""
    return KATEGORII_DEL


def poluchit_statusy_del() -> list[dict[str, str]]:
    """Вернуть справочник статусов дел."""
    return STATUSY_DEL


def poluchit_tipy_aktov() -> list[dict[str, str]]:
    """Вернуть справочник типов актов."""
    return TIPLY_AKTOV
