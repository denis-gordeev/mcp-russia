"""Сервер модуля Россельхознадзор — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (CONTRIBUTING.md, правило #4).
"""

from fastmcp import FastMCP

from . import META_FUNKTSII
from .prompts import analiz_veterinarnoy_proverki, obzor_karantinnoy_obstanovki
from .resources import istochniki_dannyh, struktura_rskhn, zakonodatelstvo_rskhn
from .tools import (
    poisk_karantinnykh_obektov,
    poisk_proverok,
    poisk_registratsiy_produktsii,
    preduprezhdeniya_karantina,
    spisok_kategoriy_proverok,
    spisok_tipov_produktsii,
    spisok_vidov_nadzora,
    spisok_vidov_narusheniy,
    veterinarsnye_sertifikaty,
)

mcp = FastMCP(
    "mcp-russia-rosselkhoznadzor",
    instructions=META_FUNKTSII.opisanie,
    version=META_FUNKTSII.versiya,
)

mcp.tool(spisok_vidov_nadzora, tags={"виды-надзора", "справочник"})
mcp.tool(spisok_kategoriy_proverok, tags={"категории-проверок", "справочник"})
mcp.tool(spisok_vidov_narusheniy, tags={"виды-нарушений", "справочник"})
mcp.tool(spisok_tipov_produktsii, tags={"типы-продукции", "справочник"})
mcp.tool(poisk_proverok, tags={"проверки", "поиск"})
mcp.tool(poisk_karantinnykh_obektov, tags={"карантин", "поиск"})
mcp.tool(poisk_registratsiy_produktsii, tags={"регистрация", "поиск"})
mcp.tool(veterinarsnye_sertifikaty, tags={"ветеринарные-сертификаты", "поиск"})
mcp.tool(preduprezhdeniya_karantina, tags={"предупреждения", "карантин"})

mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://struktura", mime_type="text/plain")(struktura_rskhn)
mcp.resource("data://zakonodatelstvo", mime_type="text/plain")(zakonodatelstvo_rskhn)

mcp.prompt(analiz_veterinarnoy_proverki)
mcp.prompt(obzor_karantinnoy_obstanovki)
