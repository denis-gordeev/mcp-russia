"""Tool functions for the Росводресурсы feature.

Tools for accessing water resources, hydrological, and reservoir data.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_number_br, markdown_table

from . import client


async def spisok_basseynovykh_okrugov(ctx: Context) -> str:
    """Получить список бассейновых округов РФ.

    Returns:
        Список бассейновых округов.
    """
    await ctx.info("Запрос списка бассейновых округов...")
    okruga = client.get_basseynovye_okruga_list()

    rows = [(o["code"], o["name"]) for o in okruga]
    header = "**Бассейновые округа Российской Федерации**\n\n"
    return header + markdown_table(["Код", "Бассейновый округ"], rows)


async def spisok_tipov_vodnykh_obektov(ctx: Context) -> str:
    """Получить список типов водных объектов.

    Returns:
        Список типов водных объектов.
    """
    await ctx.info("Запрос списка типов водных объектов...")
    tipy = client.get_tipy_vodnykh_obektov_list()
    gidro = client.get_tipy_gidro_list()

    lines = ["**Типы водных объектов**\n"]
    rows = [(t["code"], t["name"]) for t in tipy]
    lines.append(markdown_table(["Код", "Тип"], rows))

    lines.append("\n**Типы гидрологических данных**\n")
    rows = [(g["code"], g["name"]) for g in gidro]
    lines.append(markdown_table(["Код", "Тип"], rows))

    return "\n".join(lines)


async def spisok_vodokhranilishch(ctx: Context) -> str:
    """Получить список крупных водохранилищ.

    Returns:
        Список крупных водохранилищ.
    """
    await ctx.info("Запрос списка водохранилищ...")
    vodokhr = client.get_vodokhranilishcha_list()

    rows = [(v["code"], v["name"], v["region"]) for v in vodokhr]
    header = "**Крупные водохранилища РФ**\n\n"
    return header + markdown_table(["Код", "Водохранилище", "Регион"], rows)


async def info_vodnogo_obekta(code: str, ctx: Context) -> str:
    """Получить информацию о водном объекте по коду.

    Args:
        code: Код водного объекта из Государственного водного реестра.

    Returns:
        Информация о водном объекте.
    """
    await ctx.info(f"Запрос информации о водном объекте {code}...")
    data = await client.buscar_vodnyy_obekt(code)

    if not data:
        return (
            f"Водный объект с кодом '{code}' не найден.\n\n"
            f"Проверьте код в Государственном водном реестре: text.water.ru"
        )

    lines = [
        f"**{data.name}**",
        f"- Тип: {data.tip}",
        f"- Бассейн: {data.basseyn}",
    ]
    if data.dlinna_km:
        lines.append(f"- Длина: {format_number_br(data.dlinna_km, 1)} км")
    if data.ploshchad_km2:
        lines.append(f"- Площадь: {format_number_br(data.ploshchad_km2, 1)} км²")
    if data.region:
        lines.append(f"- Регион: {data.region}")
    if data.opisaniye:
        lines.append(f"- Описание: {data.opisaniye}")
    lines.append("- Источник: Росводресурсы (rosvodresursy.ru)")
    return "\n".join(lines)


async def gidro_monitoring(post: str = "", ctx: Context | None = None) -> str:
    """Получить данные гидрологического мониторинга.

    Args:
        post: Код гидрологического поста (необязательно).

    Returns:
        Гидрологические данные.
    """
    if not post:
        return (
            "**Гидрологический мониторинг**\n\n"
            "Для получения данных укажите код гидрологического поста.\n"
            "Данные доступны на сайте Росводресурсов: rosvodresursy.ru"
        )

    data = await client.buscar_gidro_post(post)

    if not data:
        return (
            f"Данные гидрологического поста '{post}' недоступны.\n\n"
            f"Проверьте код поста на сайте Росводресурсов."
        )

    lines = [
        f"**Гидрологический пост: {data.post}**",
        f"- Водный объект: {data.vodnyy_obekt}",
        f"- Дата измерения: {data.data_izmereniya}",
    ]
    if data.uroven is not None:
        lines.append(f"- Уровень воды: {format_number_br(data.uroven, 2)} м")
    if data.raskhod is not None:
        lines.append(f"- Расход воды: {format_number_br(data.raskhod, 2)} м³/с")
    if data.temperatura is not None:
        lines.append(f"- Температура воды: {format_number_br(data.temperatura, 1)}°C")
    if data.ledovaya_obstanovka:
        lines.append(f"- Ледовая обстановка: {data.ledovaya_obstanovka}")
    if data.preduprezhdenie:
        lines.append(f"- ⚠️ Предупреждение: {data.preduprezhdenie}")
    lines.append("- Источник: Росводресурсы / Гидромониторинг")
    return "\n".join(lines)


async def info_vodokhranilishcha(code: str, ctx: Context) -> str:
    """Получить информацию о водохранилище по коду.

    Args:
        code: Код водохранилища.

    Returns:
        Информация о водохранилище.
    """
    await ctx.info(f"Запрос информации о водохранилище {code}...")
    data = await client.buscar_vodokhranilishche(code)

    if not data:
        return (
            f"Водохранилище с кодом '{code}' не найдено.\n\n"
            f"Используйте spisok_vodokhranilishch() для списка водохранилищ."
        )

    lines = [
        f"**{data.name}** ({data.region})",
    ]
    if data.obiem_km3:
        lines.append(f"- Объём: {format_number_br(data.obiem_km3, 2)} км³")
    if data.ploshchad_km2:
        lines.append(f"- Площадь: {format_number_br(data.ploshchad_km2, 1)} км²")
    if data.uroven_m is not None:
        lines.append(f"- Уровень: {format_number_br(data.uroven_m, 2)} м")
    if data.priznak_napolneniya:
        lines.append(f"- Наполнение: {data.priznak_napolneniya}")
    if data.data_izmereniya:
        lines.append(f"- Дата измерения: {data.data_izmereniya}")
    lines.append("- Источник: Росводресурсы (rosvodresursy.ru)")
    return "\n".join(lines)


async def vodopolzovanie_regionov(
    region: str = "",
    god: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить данные о водопользовании по регионам.

    Args:
        region: Регион (необязательно).
        god: Год (необязательно).

    Returns:
        Данные о водопользовании.
    """
    data = await client.buscar_vodopolzovanie(region=region, god=god)

    if not data:
        filters = []
        if region:
            filters.append(f"регион: {region}")
        if god:
            filters.append(f"год: {god}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Данные о водопользовании{filter_text} недоступны.\n\n"
            f"Данные доступны на сайте Росводресурсов: rosvodresursy.ru"
        )

    lines = [f"**Водопользование** — записей: {len(data)}\n"]
    for v in data[:10]:
        lines.append(f"**{v.region}** ({v.god})")
        if v.zabrano_vody_km3:
            lines.append(
                f"- Забрано воды: {format_number_br(v.zabrano_vody_km3, 3)} км³"
            )
        if v.ispolzovano_vody_km3:
            lines.append(
                f"- Использовано: {format_number_br(v.ispolzovano_vody_km3, 3)} км³"
            )
        if v.sbrosheno_stokov_km3:
            lines.append(
                f"- Сброшено стоков: {format_number_br(v.sbrosheno_stokov_km3, 3)} км³"
            )
        if v.istochnik:
            lines.append(f"- Источник: {v.istochnik}")
        if v.naznachenie:
            lines.append(f"- Назначение: {v.naznachenie}")
        lines.append("")

    if len(data) > 10:
        lines.append(f"\n... и ещё {len(data) - 10} записей")

    lines.append("- Источник: Росводресурсы (rosvodresursy.ru)")
    return "\n".join(lines)
