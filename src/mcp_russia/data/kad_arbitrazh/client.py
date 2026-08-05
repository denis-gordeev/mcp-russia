"""HTTP-клиент для API Картотеки арбитражных дел.

Интеграция с реальными API:
    - Поиск дел: POST https://kad.arbitr.ru/Kad/Search
    - Карточка дела: GET https://kad.arbitr.ru/Kad/Instance/{id}

API КАД является публичным и не требует аутентификации.
Ограничение запросов: будьте уважительны, добавляйте задержки между запросами.
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_otpravit, http_poluchit
from mcp_russia._shared.normalizatsiya import (
    bezopasnaya_stroka,
    bezopasnoe_chislo,
    izvlech_spisok,
    razorvat_stroku_spisok,
)

from .constants import (
    INSTANTSII_SUDOV,
    KATEGORII_DEL,
    KATEGORII_KAD,
    STATUSY_DEL,
    SUDY_PRYAMYE,
    TIPLY_AKTOV,
)
from .schemas import StoronaDela, SudebnoeDelo, SudebnoeZasedanie, SudebnyyAkt, Sudy

logger = logging.getLogger(__name__)


def _opredelit_sud_po_nomeru(nomer: str) -> str:
    """Определить суд по префиксу номера дела."""
    kod = nomer.split("-")[0] if "-" in nomer else nomer[:3]
    return SUDY_PRYAMYE.get(kod, "")


def _opredelit_kategoriyu(nomer: str) -> str:
    """Определить категорию дела по букве номера."""
    if len(nomer) > 4 and nomer[4] == "-":
        bukva = nomer[3] if len(nomer) > 3 else ""
        return KATEGORII_KAD.get(bukva, "")
    return ""


def _razobrat_rezultaty_poiska(dannye: Any) -> list[SudebnoeDelo]:
    """Разбор результатов поиска дел из API КАД."""
    elementy = izvlech_spisok(dannye, "Instances", "Result")

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        dannye_dela = zapis.get("CaseInfo", zapis)
        nomer = bezopasnaya_stroka(dannye_dela.get("CaseNumber") or zapis.get("caseNumber"))
        kategoriya = _opredelit_kategoriyu(nomer) or bezopasnaya_stroka(
            dannye_dela.get("Category") or zapis.get("category")
        )
        nazvanie_suda = bezopasnaya_stroka(dannye_dela.get("Court") or zapis.get("courtName"))
        if not nazvanie_suda:
            nazvanie_suda = _opredelit_sud_po_nomeru(nomer)

        istorcy = razorvat_stroku_spisok(dannye_dela.get("Plaintiffs") or zapis.get("plaintiffs"))
        otvetchiki = razorvat_stroku_spisok(
            dannye_dela.get("Defendants") or zapis.get("defendants")
        )

        summa_syraya = dannye_dela.get("ClaimSum") or zapis.get("claimSum")
        summa = bezopasnoe_chislo(summa_syraya, po_umolchaniyu=0.0) or 0.0

        rezultaty.append(
            SudebnoeDelo(
                nomer=nomer,
                kategoriya=kategoriya,
                sostoyanie=bezopasnaya_stroka(dannye_dela.get("Status") or zapis.get("status")),
                sudya=bezopasnaya_stroka(dannye_dela.get("Judge") or zapis.get("judge")),
                nazvanie_suda=nazvanie_suda,
                data_vozbuzhdeniya=bezopasnaya_stroka(
                    dannye_dela.get("RegistrationDate") or zapis.get("registrationDate")
                ),
                data_poslednego_akta=bezopasnaya_stroka(
                    dannye_dela.get("LastDocumentDate") or zapis.get("lastDocumentDate")
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

    dannye_dela = dannye.get("CaseInfo", dannye.get("Case", dannye))
    if not isinstance(dannye_dela, dict):
        return None
    nomer = bezopasnaya_stroka(dannye_dela.get("CaseNumber") or dannye.get("caseNumber"))
    if not nomer:
        return None

    kategoriya = _opredelit_kategoriyu(nomer) or bezopasnaya_stroka(
        dannye_dela.get("Category") or dannye.get("category")
    )
    nazvanie_suda = bezopasnaya_stroka(dannye_dela.get("Court") or dannye.get("courtName"))
    if not nazvanie_suda:
        nazvanie_suda = _opredelit_sud_po_nomeru(nomer)

    istorcy = razorvat_stroku_spisok(dannye_dela.get("Plaintiffs") or dannye.get("plaintiffs"))
    otvetchiki = razorvat_stroku_spisok(dannye_dela.get("Defendants") or dannye.get("defendants"))

    summa_syraya = dannye_dela.get("ClaimSum") or dannye.get("claimSum")
    summa = bezopasnoe_chislo(summa_syraya, po_umolchaniyu=0.0) or 0.0

    return SudebnoeDelo(
        nomer=nomer,
        kategoriya=kategoriya,
        sostoyanie=bezopasnaya_stroka(dannye_dela.get("Status") or dannye.get("status")),
        sudya=bezopasnaya_stroka(dannye_dela.get("Judge") or dannye.get("judge")),
        nazvanie_suda=nazvanie_suda,
        data_vozbuzhdeniya=bezopasnaya_stroka(
            dannye_dela.get("RegistrationDate") or dannye.get("registrationDate")
        ),
        data_poslednego_akta=bezopasnaya_stroka(
            dannye_dela.get("LastDocumentDate") or dannye.get("lastDocumentDate")
        ),
        istorcy=istorcy,
        otvetchiki=otvetchiki,
        summa_iska=summa,
    )


def _razobrat_akty(dannye: Any, delo_nomer: str) -> list[SudebnyyAkt]:
    """Разбор судебных актов из ответа API КАД."""
    elementy = izvlech_spisok(dannye, "Documents", "Result")

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        dokument = zapis.get("Document", zapis)
        rezultaty.append(
            SudebnyyAkt(
                identifikator=bezopasnaya_stroka(dokument.get("Id") or dokument.get("id")),
                delo_nomer=delo_nomer,
                tip_akta=bezopasnaya_stroka(dokument.get("DocumentType") or dokument.get("type")),
                data_akta=bezopasnaya_stroka(dokument.get("DocumentDate") or dokument.get("date")),
                sud=bezopasnaya_stroka(dokument.get("CourtName") or dokument.get("court")),
                sudya=bezopasnaya_stroka(dokument.get("Judge") or dokument.get("judge")),
                kratkoe_soderzhanie=bezopasnaya_stroka(
                    dokument.get("ShortContent") or dokument.get("summary")
                ),
                rezolyutsiya=bezopasnaya_stroka(
                    dokument.get("Resolution") or dokument.get("resolution")
                ),
                pdf_ssylka=bezopasnaya_stroka(dokument.get("PdfUrl") or dokument.get("pdfUrl")),
            )
        )
    return rezultaty


def _razobrat_storony(dannye: Any, delo_nomer: str) -> list[StoronaDela]:
    """Разбор сторон судебного дела из ответа API КАД."""
    if not isinstance(dannye, dict):
        return []

    rezultaty = []
    for tip_storony, metka_tipa in [("Plaintiffs", "истец"), ("Defendants", "ответчик")]:
        nazvaniya = razorvat_stroku_spisok(dannye.get(tip_storony, []))
        for nazvanie in nazvaniya:
            inn = ""
            if "ИНН" in nazvanie:
                chasti = nazvanie.split("ИНН")
                nazvanie = chasti[0].strip().rstrip(",").strip()
                inn = chasti[1].strip().lstrip(":").strip().split()[0] if len(chasti) > 1 else ""
            rezultaty.append(
                StoronaDela(
                    nazvanie=nazvanie,
                    inn=inn,
                    tip=metka_tipa,
                )
            )
    return rezultaty


async def poisk_del(
    nomer: str = "",
    istorcz: str = "",
    otvetchik: str = "",
    inn: str = "",
    kategoriya: str = "",
    sostoyanie: str = "",
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
        sostoyanie: Статус дела.
        sudya: Фамилия судьи.
        ogranichenie: Максимальное количество результатов.

    Возвращает:
        Список судебных дел.
    """
    storony: list[dict[str, Any]] = []
    if istorcz:
        storony.append({"Name": istorcz, "Type": 1, "ExactMatch": False})
    if otvetchik:
        storony.append({"Name": otvetchik, "Type": 2, "ExactMatch": False})
    if inn:
        storony.append({"Name": inn, "Type": -1, "ExactMatch": True})

    telo: dict[str, Any] = {
        "Page": 1,
        "Count": min(ogranichenie, 25),
        "Courts": [],
        "Judges": [sudya] if sudya else [],
        "DateFrom": None,
        "DateTo": None,
        "Sides": storony,
        "CaseNumber": nomer,
        "WithNewInstances": False,
        "OnlyNew": False,
    }

    try:
        dannye = await http_otpravit(
            "https://kad.arbitr.ru/Kad/Search",
            telo_json=telo,
            zagolovki={"Accept": "application/json", "Referer": "https://kad.arbitr.ru/"},
        )
        return _razobrat_rezultaty_poiska(dannye)
    except Exception:
        logger.exception("Ошибка при поиске дел в КАД")
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
        logger.exception("Ошибка при получении дела %s", nomer)
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
        logger.exception("Ошибка при получении актов по делу %s", nomer)
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
            dokument = dannye.get("Document", dannye)
            return SudebnyyAkt(
                identifikator=bezopasnaya_stroka(dokument.get("Id")) or identifikator_akta,
                delo_nomer=bezopasnaya_stroka(dokument.get("CaseNumber")),
                tip_akta=bezopasnaya_stroka(dokument.get("DocumentType")),
                data_akta=bezopasnaya_stroka(dokument.get("DocumentDate")),
                sud=bezopasnaya_stroka(dokument.get("CourtName")),
                sudya=bezopasnaya_stroka(dokument.get("Judge")),
                kratkoe_soderzhanie=bezopasnaya_stroka(dokument.get("ShortContent")),
                rezolyutsiya=bezopasnaya_stroka(dokument.get("Resolution")),
                pdf_ssylka=bezopasnaya_stroka(dokument.get("PdfUrl")),
            )
    except Exception:
        logger.exception("Ошибка при получении акта %s", identifikator_akta)
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
            elementy = izvlech_spisok(dannye, "Sessions", "Result")
        elif isinstance(dannye, list):
            elementy = dannye
        else:
            return []

        rezultaty = []
        for zapis in elementy:
            if not isinstance(zapis, dict):
                continue
            rezultaty.append(
                SudebnoeZasedanie(
                    identifikator=bezopasnaya_stroka(zapis.get("Id")),
                    delo_nomer=nomer,
                    data_zasedaniya=bezopasnaya_stroka(zapis.get("Date")),
                    vremya=bezopasnaya_stroka(zapis.get("Time")),
                    sudya=bezopasnaya_stroka(zapis.get("Judge")),
                    zala=bezopasnaya_stroka(zapis.get("Hall")),
                    sostoyanie=bezopasnaya_stroka(zapis.get("Status")),
                    rezultaty=bezopasnaya_stroka(zapis.get("Result")),
                )
            )
        return rezultaty
    except Exception:
        logger.exception("Ошибка при получении заседаний по делу %s", nomer)
        return []


async def poisk_sudey(familiya: str = "", nazvanie_suda: str = "") -> list[Sudy]:
    """Поиск судей арбитражных судов.

    Аргументы:
        familiya: Фамилия судьи.
        nazvanie_suda: Наименование суда.

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
        logger.exception("Ошибка при получении сторон дела %s", nomer)
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
