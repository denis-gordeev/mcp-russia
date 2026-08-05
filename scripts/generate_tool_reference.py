"""Генерация справочника инструментов из MCP-реестра.

Скрипт собирает данные обо всех зарегистрированных инструментах,
ресурсах и промптах через API FastMCP и выводит структурированный
Markdown-справочник.

Использование:
    uv run python scripts/generate_tool_reference.py
"""

from __future__ import annotations

import asyncio
import importlib
import pkgutil

import mcp_russia.agenty
import mcp_russia.data
from mcp_russia._shared.feature import MetaFunktsii, ReyestrFunktsiy


async def _sobrat_dannye_modulya(imya_modulya: str, put_modulya: str) -> dict[str, object]:
    modul = importlib.import_module(put_modulya)
    metadannye: MetaFunktsii = getattr(modul, "META_FUNKTSII", None)
    server = importlib.import_module(f"{put_modulya}.server").mcp

    instrumenty = []
    for instrument in await server.list_tools():
        parametry = instrument.parameters.get("properties", {})
        obyazatelnye = set(instrument.parameters.get("required", []))
        spisok_parametrov = []
        for imya_param, skhema in parametry.items():
            tip = skhema.get("type", "any")
            obyazatelen = "обязательный" if imya_param in obyazatelnye else "необязательный"
            opisanie_param = skhema.get("description", "")
            spisok_parametrov.append(
                f"    - `{imya_param}` ({tip}, {obyazatelen}): {opisanie_param}"
            )
        instrumenty.append(
            {
                "imya": instrument.name,
                "opisanie": (instrument.description or "").split("\n")[0],
                "parametry": spisok_parametrov,
                "tegi": sorted(instrument.tags) if instrument.tags else [],
            }
        )

    resursy = []
    for resurs in await server.list_resources():
        resursy.append({"uri": str(resurs.uri), "imya": resurs.name or ""})

    prompty = []
    for prompt in await server.list_prompts():
        prompty.append({"imya": prompt.name, "opisanie": prompt.description or ""})

    return {
        "imya": imya_modulya,
        "opisanie": metadannye.opisanie if metadannye else "",
        "versiya": metadannye.versiya if metadannye else "0.0.0",
        "avtorizatsiya": (
            "требуется"
            if metadannye and metadannye.trebuet_autentifikatsii
            else (
                f"опциональная ({metadannye.peremennaya_avt_env})"
                if metadannye and metadannye.peremennaya_avt_env
                else "не требуется"
            )
        ),
        "operatsii_s_avtorizatsiey": (
            metadannye.operatsii_trebuyut_avtorizatsii if metadannye else []
        ),
        "instrumenty": instrumenty,
        "resursy": resursy,
        "prompty": prompty,
    }


async def main() -> None:
    reyestr = ReyestrFunktsiy()
    reyestr.obnaruzhit("mcp_russia.data")
    reyestr.obnaruzhit("mcp_russia.agenty")

    moduli = []
    for bazovyy_paket in (mcp_russia.data, mcp_russia.agenty):
        for svedeniya in pkgutil.iter_modules(
            bazovyy_paket.__path__, bazovyy_paket.__name__ + "."
        ):
            if not svedeniya.ispkg:
                continue
            imya = svedeniya.name.rsplit(".", 1)[-1]
            if imya.startswith("_"):
                continue
            try:
                dannye = await _sobrat_dannye_modulya(imya, svedeniya.name)
                moduli.append(dannye)
            except Exception:
                continue

    vsego_instrumentov = sum(len(m["instrumenty"]) for m in moduli)
    vsego_resursov = sum(len(m["resursy"]) for m in moduli)
    vsego_promptov = sum(len(m["prompty"]) for m in moduli)

    stroki = [
        "# Справочник инструментов mcp-russia",
        "",
        f"{len(moduli)} модулей · {vsego_instrumentov} инструментов · "
        f"{vsego_resursov} ресурсов · {vsego_promptov} промптов",
        "",
        "_Сгенерировано из MCP-реестра. Не редактируйте вручную._",
        "",
    ]

    for modul in sorted(moduli, key=lambda m: m["imya"]):
        stroki.append(f"## `{modul['imya']}` — {modul['opisanie']}")
        stroki.append("")
        stroki.append(f"Версия: {modul['versiya']}")
        stroki.append(f"Авторизация: {modul['avtorizatsiya']}")
        if modul["operatsii_s_avtorizatsiey"]:
            stroki.append(
                f"Операции с авторизацией: "
                f"{', '.join(f'`{o}`' for o in modul['operatsii_s_avtorizatsiey'])}"
            )
        stroki.append("")

        if modul["instrumenty"]:
            stroki.append(f"### Инструменты ({len(modul['instrumenty'])})")
            stroki.append("")
            for inst in modul["instrumenty"]:
                avt_metka = ""
                if inst["imya"] in modul["operatsii_s_avtorizatsiey"]:
                    avt_metka = " *(требуется API-токен)*"
                stroki.append(f"- `{inst['imya']}`{avt_metka}: {inst['opisanie']}")
                for param in inst["parametry"]:
                    stroki.append(param)
                if inst["tegi"]:
                    stroki.append(f"  - Теги: {', '.join(inst['tegi'])}")
            stroki.append("")

        if modul["resursy"]:
            stroki.append(f"### Ресурсы ({len(modul['resursy'])})")
            stroki.append("")
            for res in modul["resursy"]:
                stroki.append(f"- `{res['uri']}`: {res['imya']}")
            stroki.append("")

        if modul["prompty"]:
            stroki.append(f"### Промпты ({len(modul['prompty'])})")
            stroki.append("")
            for prompt in modul["prompty"]:
                stroki.append(f"- `{prompt['imya']}`: {prompt['opisanie']}")
            stroki.append("")

    print("\n".join(stroki))


if __name__ == "__main__":
    asyncio.run(main())
