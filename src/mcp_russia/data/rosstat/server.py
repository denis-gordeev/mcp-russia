"""Сервер модуля Росстата — регистрирует инструменты, ресурсы и промпты.

Без бизнес-логики (ADR-001, правило #4).
"""

from fastmcp import FastMCP

from .prompts import (
    analiz_demografii,
    analiz_regiona,
    analiz_vrp_regionov,
    obzor_inflyatsii,
    obzor_truda,
)
from .resources import istochniki_dannyh, metodologiya, okved, pokazateli, subiekty_rf
from .tools import (
    bezrabotitsa_dannye,
    demografiya,
    dinamika_regiona,
    dokhody_na_dushu,
    indikator_dannye,
    inflyatsiya,
    informatsiya_o_regionye,
    informatsiya_ob_okruge,
    investitsii_po_vidam,
    otraslevaya_struktura_vrp,
    poisk_regiona,
    pokazateli_rosstata,
    promyshlennoe_proizvodstvo,
    spisok_okrugov,
    spisok_regionov,
    sravnenie_okrugov,
    sravnenie_regionov,
    srednyaya_pensiya,
    uroven_bednosti,
    vrp_dannye,
    vvp_dannye,
    zarplata_dannye,
)

mcp = FastMCP("mcp-russia-rosstat")

# Инструменты
mcp.tool(spisok_regionov, tags={"регионы", "справочник"})
mcp.tool(spisok_okrugov, tags={"федеральные-округа", "справочник"})
mcp.tool(poisk_regiona, tags={"регионы", "поиск"})
mcp.tool(informatsiya_o_regionye, tags={"регион", "информация"})
mcp.tool(informatsiya_ob_okruge, tags={"федеральный-округ", "информация"})
mcp.tool(pokazateli_rosstata, tags={"показатели", "справочник"})
mcp.tool(inflyatsiya, tags={"инфляция", "ИПЦ"})
mcp.tool(demografiya, tags={"демография", "население"})
mcp.tool(vrp_dannye, tags={"ВРП", "экономика"})
mcp.tool(vvp_dannye, tags={"ВВП", "экономика"})
mcp.tool(zarplata_dannye, tags={"зарплата", "экономика"})
mcp.tool(bezrabotitsa_dannye, tags={"безработица", "экономика"})
mcp.tool(dokhody_na_dushu, tags={"доходы", "экономика"})
mcp.tool(promyshlennoe_proizvodstvo, tags={"промышленность", "экономика"})
mcp.tool(uroven_bednosti, tags={"бедность", "социальная"})
mcp.tool(srednyaya_pensiya, tags={"пенсия", "социальная"})
mcp.tool(sravnenie_regionov, tags={"сравнение", "регионы"})
mcp.tool(indikator_dannye, tags={"показатель", "ЕМИСС", "универсальный"})
mcp.tool(dinamika_regiona, tags={"динамика", "регионы", "ЕМИСС"})
mcp.tool(otraslevaya_struktura_vrp, tags={"ВРП", "отрасли", "ОКВЭД"})
mcp.tool(investitsii_po_vidam, tags={"инвестиции", "отрасли", "ОКВЭД"})
mcp.tool(sravnenie_okrugov, tags={"сравнение", "федеральные-округа"})

# Ресурсы
mcp.resource("data://istochniki", mime_type="text/plain")(istochniki_dannyh)
mcp.resource("data://metodologiya", mime_type="text/plain")(metodologiya)
mcp.resource("data://pokazateli", mime_type="text/plain")(pokazateli)
mcp.resource("data://okved", mime_type="text/plain")(okved)
mcp.resource("data://subiekty-rf", mime_type="text/plain")(subiekty_rf)

# Промпты
mcp.prompt(analiz_regiona)
mcp.prompt(obzor_inflyatsii)
mcp.prompt(analiz_vrp_regionov)
mcp.prompt(obzor_truda)
mcp.prompt(analiz_demografii)
