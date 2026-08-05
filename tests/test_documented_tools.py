"""Сверка вызовов в документации с фактическим MCP-реестром."""  # noqa: RUF002

from __future__ import annotations

import ast
import importlib
import pkgutil
import re
from pathlib import Path

import pytest

import mcp_russia.agenty
import mcp_russia.data

KOREN_PROEKTA = Path(__file__).parents[1]
VYZOV_RE = re.compile(r"(?<![\w])(?P<imya>[a-z][a-z0-9_]{2,})\((?P<argumenty>[^()\n]*)\)")
IMENOVANNYY_ARGUMENT_RE = re.compile(r"\b(?P<imya>[a-z][a-z0-9_]*)\s*=")
PAKETNYY_VYZOV_RE = re.compile(
    r'"imya_instrumenta"\s*:\s*"(?P<imya>[a-z][a-z0-9_]*)"\s*,\s*'
    r'"argumenty"\s*:\s*\{(?P<argumenty>[^{}]*)\}'
)
JSON_ARGUMENT_RE = re.compile(r'"(?P<imya>[a-z][a-z0-9_]*)"\s*:')
OBRATNAYA_KAVYCHKA_RE = re.compile(r"`(?P<imya>[a-z][a-z0-9_]+)`")
MODUL_INSTRUMENT_RE = re.compile(
    r"###\s+`(?P<modul>[a-z][a-z0-9_]*)`\s+.*?\((?P<kolichestvo>\d+)\s+инструмент"
)
STROKA_TABLITSY_INSTRUMENTA_RE = re.compile(r"^\|\s*`(?P<imya>[a-z][a-z0-9_]+)`\s*\|")
PLANIRUEMYY_RE = re.compile(r"\*\(планируемый\)\*|\*\(инструмент недоступен\)\*")
PUT_FEATURES = KOREN_PROEKTA / "docs" / "reference" / "features.md"
PUT_SMART_TOOLS = KOREN_PROEKTA / "docs" / "reference" / "smart-tools.md"
ISPYTATELNYE_MODULI = {
    "spisok_funktsiy",
    "rekomendovat_instrumenty",
    "splanirovat_zapros",
    "vypolnit_paket",
}


async def _sobrat_katalog() -> tuple[dict[str, set[str]], dict[str, dict[str, set[str]]]]:
    """Собрать публичные имена и параметры прямо из FastMCP-серверов модулей."""
    publichnyy_katalog: dict[str, set[str]] = {}
    lokalnye_katalogi: dict[str, dict[str, set[str]]] = {}

    for bazovyy_paket in (mcp_russia.data, mcp_russia.agenty):
        for svedeniya in pkgutil.iter_modules(
            bazovyy_paket.__path__, bazovyy_paket.__name__ + "."
        ):
            if not svedeniya.ispkg:
                continue

            imya_modulya = svedeniya.name.rsplit(".", 1)[-1]
            server = importlib.import_module(f"{svedeniya.name}.server").mcp
            lokalnye_katalogi[imya_modulya] = {}

            for instrument in await server.list_tools():
                parametry = set(instrument.parameters.get("properties", {}))
                lokalnye_katalogi[imya_modulya][instrument.name] = parametry
                publichnyy_katalog[f"{imya_modulya}_{instrument.name}"] = parametry

    from mcp_russia.server import mcp

    for instrument in await mcp.list_tools():
        publichnyy_katalog[instrument.name] = set(instrument.parameters.get("properties", {}))

    return publichnyy_katalog, lokalnye_katalogi


def _proverit_vyzov(
    oshibki: list[str],
    istochnik: str,
    imya: str,
    argumenty: set[str],
    katalog: dict[str, set[str]],
) -> None:
    if imya not in katalog:
        oshibki.append(f"{istochnik}: инструмент {imya!r} не зарегистрирован")
        return

    lishnie = argumenty - katalog[imya]
    if lishnie:
        oshibki.append(
            f"{istochnik}: у {imya!r} нет параметров {sorted(lishnie)!r}"  # noqa: RUF001
        )


@pytest.mark.asyncio
async def test_vyzovy_v_primerah_sootvetstvuyut_mcp_reyestru() -> None:
    publichnyy_katalog, _ = await _sobrat_katalog()
    oshibki: list[str] = []

    for put in sorted((KOREN_PROEKTA / "docs" / "examples").glob("*.md")):
        tekst = put.read_text(encoding="utf-8")
        for nomer_stroki, stroka in enumerate(tekst.splitlines(), start=1):
            for sovpadenie in VYZOV_RE.finditer(stroka):
                imya = sovpadenie.group("imya")
                if "_" not in imya:
                    continue
                argumenty = {
                    zapis.group("imya")
                    for zapis in IMENOVANNYY_ARGUMENT_RE.finditer(sovpadenie.group("argumenty"))
                }
                _proverit_vyzov(
                    oshibki,
                    f"{put.relative_to(KOREN_PROEKTA)}:{nomer_stroki}",
                    imya,
                    argumenty,
                    publichnyy_katalog,
                )

        for sovpadenie in PAKETNYY_VYZOV_RE.finditer(tekst):
            argumenty = {
                zapis.group("imya")
                for zapis in JSON_ARGUMENT_RE.finditer(sovpadenie.group("argumenty"))
            }
            nomer_stroki = tekst.count("\n", 0, sovpadenie.start()) + 1
            _proverit_vyzov(
                oshibki,
                f"{put.relative_to(KOREN_PROEKTA)}:{nomer_stroki}",
                sovpadenie.group("imya"),
                argumenty,
                publichnyy_katalog,
            )

    assert not oshibki, "Ошибки в примерах MCP-вызовов:\n" + "\n".join(oshibki)


def _stroki_iz_ast(derevo: ast.AST) -> str:
    return "\n".join(
        uzel.value
        for uzel in ast.walk(derevo)
        if isinstance(uzel, ast.Constant) and isinstance(uzel.value, str)
    )


@pytest.mark.asyncio
async def test_vyzovy_v_promptah_sootvetstvuyut_lokalnomu_reyestru() -> None:
    _, lokalnye_katalogi = await _sobrat_katalog()
    oshibki: list[str] = []

    for put in sorted((KOREN_PROEKTA / "src" / "mcp_russia").glob("**/prompts.py")):
        imya_modulya = put.parent.name
        katalog = lokalnye_katalogi[imya_modulya]
        tekst = _stroki_iz_ast(ast.parse(put.read_text(encoding="utf-8")))

        for sovpadenie in VYZOV_RE.finditer(tekst):
            argumenty = {
                zapis.group("imya")
                for zapis in IMENOVANNYY_ARGUMENT_RE.finditer(sovpadenie.group("argumenty"))
            }
            _proverit_vyzov(
                oshibki,
                str(put.relative_to(KOREN_PROEKTA)),
                sovpadenie.group("imya"),
                argumenty,
                katalog,
            )

    assert not oshibki, "Ошибки в MCP-вызовах промптов:\n" + "\n".join(oshibki)


@pytest.mark.asyncio
async def test_istruikmenty_v_osnovnykh_dokumentakh_sootvetstvuyut_reyestru() -> None:
    publichnyy_katalog, lokalnye_katalogi = await _sobrat_katalog()
    izvestnye_moduli = set(lokalnye_katalogi.keys())
    oshibki: list[str] = []

    for put_dokumenta in [PUT_SMART_TOOLS]:
        if not put_dokumenta.exists():
            continue
        tekst = put_dokumenta.read_text(encoding="utf-8")

        for nomer_stroki, stroka in enumerate(tekst.splitlines(), start=1):
            for sovpadenie in OBRATNAYA_KAVYCHKA_RE.finditer(stroka):
                imya = sovpadenie.group("imya")
                if "_" not in imya:
                    continue
                chast_do_podcherkivaniya = imya.split("_")[0]
                if chast_do_podcherkivaniya not in izvestnye_moduli:
                    continue
                if PLANIRUEMYY_RE.search(stroka):
                    continue
                if imya not in publichnyy_katalog:
                    oshibki.append(
                        f"{put_dokumenta.relative_to(KOREN_PROEKTA)}:{nomer_stroki}: "
                        f"инструмент {imya!r} не зарегистрирован"
                    )

    for put_primera in sorted((KOREN_PROEKTA / "docs" / "examples").glob("*.md")):
        tekst = put_primera.read_text(encoding="utf-8")
        for nomer_stroki, stroka in enumerate(tekst.splitlines(), start=1):
            for sovpadenie in OBRATNAYA_KAVYCHKA_RE.finditer(stroka):
                imya = sovpadenie.group("imya")
                if "_" not in imya:
                    continue
                chast_do_podcherkivaniya = imya.split("_")[0]
                if chast_do_podcherkivaniya not in izvestnye_moduli:
                    continue
                if PLANIRUEMYY_RE.search(stroka):
                    continue
                if imya not in publichnyy_katalog:
                    oshibki.append(
                        f"{put_primera.relative_to(KOREN_PROEKTA)}:{nomer_stroki}: "
                        f"инструмент {imya!r} не зарегистрирован"
                    )

    assert not oshibki, "Ошибки в именах инструментов документации:\n" + "\n".join(oshibki)


@pytest.mark.asyncio
async def test_instrumenty_v_iskhodnom_kode_sootvetstvuyut_reyestru() -> None:
    publichnyy_katalog, _ = await _sobrat_katalog()
    oshibki: list[str] = []

    for put_modulya in sorted((KOREN_PROEKTA / "src" / "mcp_russia").glob("**/*.py")):
        tekst = _stroki_iz_ast(ast.parse(put_modulya.read_text(encoding="utf-8")))
        imya_fayla = put_modulya.relative_to(KOREN_PROEKTA)

        for sovpadenie in VYZOV_RE.finditer(tekst):
            imya = sovpadenie.group("imya")
            if "_" not in imya:
                continue
            if imya not in publichnyy_katalog:
                continue
            argumenty = {
                zapis.group("imya")
                for zapis in IMENOVANNYY_ARGUMENT_RE.finditer(sovpadenie.group("argumenty"))
            }
            _proverit_vyzov(oshibki, str(imya_fayla), imya, argumenty, publichnyy_katalog)

    assert not oshibki, "Ошибки в MCP-вызовах исходного кода:\n" + "\n".join(oshibki)


@pytest.mark.asyncio
async def test_kolichestva_instrumentov_v_features_md_sootvetstvuyut_reyestru() -> None:
    _, lokalnye_katalogi = await _sobrat_katalog()
    oshibki: list[str] = []

    if not PUT_FEATURES.exists():
        pytest.skip("features.md не найден")

    tekst = PUT_FEATURES.read_text(encoding="utf-8")
    for sovpadenie in MODUL_INSTRUMENT_RE.finditer(tekst):
        imya_modulya = sovpadenie.group("modul")
        ozhidaemoe = int(sovpadenie.group("kolichestvo"))
        if imya_modulya not in lokalnye_katalogi:
            oshibki.append(f"модуль {imya_modulya!r} не найден в реестре")
            continue
        fakticheskoe = len(lokalnye_katalogi[imya_modulya])
        if fakticheskoe != ozhidaemoe:
            oshibki.append(
                f"модуль {imya_modulya!r}: указано {ozhidaemoe} инструментов, "
                f"фактически {fakticheskoe}"
            )

    assert not oshibki, "Несоответствие количества инструментов:\n" + "\n".join(oshibki)


@pytest.mark.asyncio
async def test_imena_instrumentov_v_features_md_sootvetstvuyut_reyestru() -> None:
    _, lokalnye_katalogi = await _sobrat_katalog()
    oshibki: list[str] = []

    if not PUT_FEATURES.exists():
        pytest.skip("features.md не найден")

    tekst = PUT_FEATURES.read_text(encoding="utf-8")
    tekushchiy_modul: str | None = None

    for nomer_stroki, stroka in enumerate(tekst.splitlines(), start=1):
        zagolovok = MODUL_INSTRUMENT_RE.search(stroka)
        if zagolovok:
            tekushchiy_modul = zagolovok.group("modul")
            continue

        if tekushchiy_modul is None or tekushchiy_modul not in lokalnye_katalogi:
            continue

        if stroka.startswith("---"):
            tekushchiy_modul = None
            continue

        sovpadenie = STROKA_TABLITSY_INSTRUMENTA_RE.match(stroka)
        if not sovpadenie:
            continue

        imya = sovpadenie.group("imya")
        if PLANIRUEMYY_RE.search(stroka):
            continue
        if imya not in lokalnye_katalogi[tekushchiy_modul]:
            oshibki.append(
                f"features.md:{nomer_stroki}: инструмент {imya!r} "
                f"не найден в модуле {tekushchiy_modul!r}"
            )

    assert not oshibki, "Несоответствие имён инструментов в features.md:\n" + "\n".join(oshibki)
