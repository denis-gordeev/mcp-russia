#!/usr/bin/env python3
# ruff: noqa: F841, RUF001
"""Генерация диаграмм архитектуры для документации mcp-russia.

Создаёт 4 PNG-диаграммы в docs/concepts/img/:
  - system_overview.png
  - feature_anatomy.png
  - auto_registry_flow.png
  - data_flow.png

Требования: graphviz (brew install graphviz), diagrams (pip install diagrams)
Использование: python scripts/generate_diagrams.py
"""

from __future__ import annotations

import os
from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.generic.blank import Blank
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.programming.flowchart import Action, Decision, StartEnd
from diagrams.programming.framework import FastAPI
from diagrams.programming.language import Python

KATALOG_VYVODA = Path(__file__).resolve().parent.parent / "docs" / "concepts" / "img"
ATRIBUBY_GRAFA = {"fontsize": "14", "bgcolor": "white", "pad": "0.5"}
ATRIBUBY_UZLA = {"fontsize": "11"}
ATRIBUBY_REBRA = {"fontsize": "10"}


def obzor_sistemy() -> None:
    """Диаграмма 1: Высокоуровневая архитектура системы."""
    with Diagram(
        "mcp-russia — Обзор системы",
        filename=str(KATALOG_VYVODA / "system_overview"),
        direction="TB",
        show=False,
        graph_attr=ATRIBUBY_GRAFA,
        node_attr=ATRIBUBY_UZLA,
        edge_attr=ATRIBUBY_REBRA,
    ):
        klient = Client("MCP-клиент\n(Claude, GPT, ...)")

        with Cluster("Корневой сервер mcp-russia"):
            koren = FastAPI("FastMCP\nserver.py")
            reyestr = Python("ReyestrFunktsiy")
            meta = Python("Мета-инструменты\n(spisok, rekomendovat,\nsplanirovat, paket)")
            koren - reyestr
            koren - meta

        klient >> koren

        with Cluster("Экономика и финансы"):
            cbrf = Python("cbrf")
            rosstat = Python("rosstat")
            zakupki = Python("zakupki")
            fns = Python("fns")

        with Cluster("Законодательство и выборы"):
            gosduma = Python("gosduma")
            cekrf = Python("cekrf")
            publikatsii = Python("publikatsii")

        with Cluster("Судебная система и надзор"):
            kad_arbitrazh = Python("kad_arbitrazh")
            rosaudit = Python("rosaudit")
            rospotrebnadzor = Python("rospotrebnadzor")
            roskomnadzor = Python("roskomnadzor")
            fssp = Python("fssp")

        with Cluster("Экология и здравоохранение"):
            rosgidromet = Python("rosgidromet")
            rosvodresursy = Python("rosvodresursy")
            minzdrav = Python("minzdrav")

        with Cluster("Реестры и справочники"):
            rosapi = Python("rosapi")
            rosreestr = Python("rosreestr")
            gibdd = Python("gibdd")
            minobrnauki = Python("minobrnauki")

        with Cluster("Агенты"):
            redator = Python("redator")

        reyestr >> Edge(style="dashed") >> cbrf
        reyestr >> Edge(style="dashed") >> gosduma
        reyestr >> Edge(style="dashed") >> kad_arbitrazh
        reyestr >> Edge(style="dashed") >> cekrf
        reyestr >> Edge(style="dashed") >> rosaudit
        reyestr >> Edge(style="dashed") >> rosgidromet
        reyestr >> Edge(style="dashed") >> zakupki
        reyestr >> Edge(style="dashed") >> redator
        reyestr >> Edge(style="dashed") >> rosapi

        api = Server("Государственные API\n(gosuslugi.ru, rosstat.gov.ru,\ncbr.ru, ...)")

        cbrf >> api
        rosstat >> api
        gosduma >> api
        kad_arbitrazh >> api
        cekrf >> api
        rosaudit >> api
        rosgidromet >> api
        zakupki >> api


def anatomiya_modulya() -> None:
    """Диаграмма 2: Внутреннее строение пакета модуля."""
    with Diagram(
        "Анатомия модуля (data/rosstat/)",
        filename=str(KATALOG_VYVODA / "feature_anatomy"),
        direction="LR",
        show=False,
        graph_attr=ATRIBUBY_GRAFA,
        node_attr=ATRIBUBY_UZLA,
        edge_attr=ATRIBUBY_REBRA,
    ):
        with Cluster("data/rosstat/"):
            init = Python("__init__.py\nFEATURE_META")
            server = FastAPI("server.py\nmcp: FastMCP")
            tools = Python("tools.py\nspisok_regionov()\npoluchit_indikator()")
            client = Python("client.py\nhttp_get() async")
            schemas = Python("schemas.py\nBaseModel")
            constants = Python("constants.py\nROSSTAT_API_BASE")

            server >> Edge(label="регистрирует") >> tools
            tools >> Edge(label="делегирует HTTP") >> client
            client >> Edge(label="возвращает") >> schemas

        shared = Python("_shared/\nhttp_client\nkesh\nformatting")
        api = Server("API Росстата\nrosstat.gov.ru")

        tools >> Edge(style="dashed", label="использует") >> shared
        client >> Edge(style="dashed", label="использует") >> shared
        client >> api


def potok_avtoobnaruzheniya() -> None:
    """Диаграмма 3: Блок-схема потока автоматического обнаружения."""
    with Diagram(
        "Автообнаружение — Поток обнаружения",
        filename=str(KATALOG_VYVODA / "auto_registry_flow"),
        direction="TB",
        show=False,
        graph_attr=ATRIBUBY_GRAFA,
        node_attr=ATRIBUBY_UZLA,
        edge_attr=ATRIBUBY_REBRA,
    ):
        start = StartEnd("discover(pkg)")
        iter_mod = Action("iter_modules(pkg)")
        proverka_imeni = Decision("имя начинается\nс '_'?")
        propusk = Action("пропустить")
        import_init = Action("import __init__.py")
        proverka_meta = Decision("FEATURE_META\nсуществует?")
        propusk2 = Action("пропустить")
        proverka_auth = Decision("requires_auth\nи env var OK?")
        propusk3 = Action("пропустить\n(молча)")
        import_server = Action("import server.py")
        mount = Action("mount(mcp,\nnamespace=name)")
        end = StartEnd("следующий модуль\nили конец")

        start >> iter_mod >> proverka_imeni
        proverka_imeni >> Edge(label="да") >> propusk >> end
        proverka_imeni >> Edge(label="нет") >> import_init >> proverka_meta
        proverka_meta >> Edge(label="нет") >> propusk2 >> end
        proverka_meta >> Edge(label="да") >> proverka_auth
        proverka_auth >> Edge(label="нет") >> propusk3 >> end
        proverka_auth >> Edge(label="да") >> import_server >> mount >> end


def potok_dannykh() -> None:
    """Диаграмма 4: Конвейер потока данных запрос/ответ."""
    with Diagram(
        "Поток данных — Запрос и ответ",
        filename=str(KATALOG_VYVODA / "data_flow"),
        direction="LR",
        show=False,
        graph_attr={**ATRIBUBY_GRAFA, "nodesep": "0.8"},
        node_attr=ATRIBUBY_UZLA,
        edge_attr=ATRIBUBY_REBRA,
    ):
        polzovatel = Client("Пользователь")
        mcp_klient = Client("MCP-клиент")
        bm25 = Python("Фильтр BM25\n(top-10 инструментов)")

        with Cluster("mcp-russia"):
            tools = Python("tools.py\nоркестрирует")
            client = Python("client.py\nhttpx async")
            ogranichitel = Python("Ограничитель частоты\nскользящее окно")

        api = Server("Гос. API\n(JSON)")

        # Путь запроса
        polzovatel >> Edge(label="вопрос") >> mcp_klient
        mcp_klient >> Edge(label="вызов инструмента") >> bm25
        bm25 >> Edge(label="диспетчеризация") >> tools
        tools >> client >> ogranichitel >> api

        # Путь ответа (обратные метки)
        api >> Edge(label="JSON", style="dashed", color="darkgreen") >> client
        client >> Edge(label="Pydantic", style="dashed", color="darkgreen") >> tools
        tools >> Edge(label="Markdown", style="dashed", color="darkgreen") >> mcp_klient
        mcp_klient >> Edge(label="ответ", style="dashed", color="darkgreen") >> polzovatel

        # Аннотация повторных попыток
        _ = Blank("")
        ogranichitel >> Edge(label="повтор 429/5xx", style="dotted", color="red") >> ogranichitel


def main() -> None:
    KATALOG_VYVODA.mkdir(parents=True, exist_ok=True)
    # библиотека diagrams использует cwd для временных файлов
    iskhodnyy_cwd = os.getcwd()
    os.chdir(KATALOG_VYVODA)
    try:
        obzor_sistemy()
        anatomiya_modulya()
        potok_avtoobnaruzheniya()
        potok_dannykh()
    finally:
        os.chdir(iskhodnyy_cwd)

    sgenerirovannye = sorted(KATALOG_VYVODA.glob("*.png"))
    print(f"Сгенерировано {len(sgenerirovannye)} диаграмм в {KATALOG_VYVODA}/")
    for p in sgenerirovannye:
        print(f"  {p.name}")


if __name__ == "__main__":
    main()
