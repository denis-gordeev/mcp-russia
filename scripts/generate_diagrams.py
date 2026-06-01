#!/usr/bin/env python3
# ruff: noqa: F841, RUF001
"""Generate architecture diagrams for mcp-russia documentation.

Produces 4 PNG diagrams in docs/concepts/img/:
  - system_overview.png
  - feature_anatomy.png
  - auto_registry_flow.png
  - data_flow.png

Requirements: graphviz (brew install graphviz), diagrams (pip install diagrams)
Usage: python scripts/generate_diagrams.py
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

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "concepts" / "img"
GRAPH_ATTR = {"fontsize": "14", "bgcolor": "white", "pad": "0.5"}
NODE_ATTR = {"fontsize": "11"}
EDGE_ATTR = {"fontsize": "10"}


def system_overview() -> None:
    """Diagram 1: High-level system architecture."""
    with Diagram(
        "mcp-russia — System Overview",
        filename=str(OUTPUT_DIR / "system_overview"),
        direction="TB",
        show=False,
        graph_attr=GRAPH_ATTR,
        node_attr=NODE_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        client = Client("MCP Client\n(Claude, GPT, ...)")

        with Cluster("mcp-russia Root Server"):
            root = FastAPI("FastMCP\nserver.py")
            registry = Python("FeatureRegistry")
            meta = Python("Мета-инструменты\n(spisok, rekomendovat,\nsplanirovat, paket)")
            root - registry
            root - meta

        client >> root

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

        registry >> Edge(style="dashed") >> cbrf
        registry >> Edge(style="dashed") >> gosduma
        registry >> Edge(style="dashed") >> kad_arbitrazh
        registry >> Edge(style="dashed") >> cekrf
        registry >> Edge(style="dashed") >> rosaudit
        registry >> Edge(style="dashed") >> rosgidromet
        registry >> Edge(style="dashed") >> zakupki
        registry >> Edge(style="dashed") >> redator
        registry >> Edge(style="dashed") >> rosapi

        apis = Server("Государственные API\n(gosuslugi.ru, rosstat.gov.ru,\ncbr.ru, ...)")

        cbrf >> apis
        rosstat >> apis
        gosduma >> apis
        kad_arbitrazh >> apis
        cekrf >> apis
        rosaudit >> apis
        rosgidromet >> apis
        zakupki >> apis


def feature_anatomy() -> None:
    """Diagram 2: Internal structure of a feature package."""
    with Diagram(
        "Анатомия feature-пакета (data/rosstat/)",
        filename=str(OUTPUT_DIR / "feature_anatomy"),
        direction="LR",
        show=False,
        graph_attr=GRAPH_ATTR,
        node_attr=NODE_ATTR,
        edge_attr=EDGE_ATTR,
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

        shared = Python("_shared/\nhttp_client\ncache\nformatting")
        api = Server("API Росстата\nrosstat.gov.ru")

        tools >> Edge(style="dashed", label="использует") >> shared
        client >> Edge(style="dashed", label="использует") >> shared
        client >> api


def auto_registry_flow() -> None:
    """Diagram 3: Auto-registry discovery flowchart."""
    with Diagram(
        "Auto-Registry — Поток обнаружения",
        filename=str(OUTPUT_DIR / "auto_registry_flow"),
        direction="TB",
        show=False,
        graph_attr=GRAPH_ATTR,
        node_attr=NODE_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        start = StartEnd("discover(pkg)")
        iter_mod = Action("iter_modules(pkg)")
        skip_check = Decision("имя начинается\nс '_'?")
        skip = Action("пропустить")
        import_init = Action("import __init__.py")
        meta_check = Decision("FEATURE_META\nсуществует?")
        skip2 = Action("пропустить")
        auth_check = Decision("requires_auth\nи env var OK?")
        skip3 = Action("пропустить\n(молча)")
        import_server = Action("import server.py")
        mount = Action("mount(mcp,\nnamespace=name)")
        end = StartEnd("следующий модуль\nили конец")

        start >> iter_mod >> skip_check
        skip_check >> Edge(label="да") >> skip >> end
        skip_check >> Edge(label="нет") >> import_init >> meta_check
        meta_check >> Edge(label="нет") >> skip2 >> end
        meta_check >> Edge(label="да") >> auth_check
        auth_check >> Edge(label="нет") >> skip3 >> end
        auth_check >> Edge(label="да") >> import_server >> mount >> end


def data_flow() -> None:
    """Diagram 4: Request/response data flow pipeline."""
    with Diagram(
        "Поток данных — Запрос и ответ",
        filename=str(OUTPUT_DIR / "data_flow"),
        direction="LR",
        show=False,
        graph_attr={**GRAPH_ATTR, "nodesep": "0.8"},
        node_attr=NODE_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        user = Client("Пользователь")
        mcp_client = Client("MCP Client")
        bm25 = Python("BM25 Filter\n(top-10 tools)")

        with Cluster("mcp-russia"):
            tools = Python("tools.py\nоркестрирует")
            client = Python("client.py\nhttpx async")
            rate = Python("Rate Limiter\nsliding window")

        api = Server("Гос. API\n(JSON)")

        # Request path
        user >> Edge(label="вопрос") >> mcp_client
        mcp_client >> Edge(label="tool call") >> bm25
        bm25 >> Edge(label="dispatch") >> tools
        tools >> client >> rate >> api

        # Response path (reverse labels)
        api >> Edge(label="JSON", style="dashed", color="darkgreen") >> client
        client >> Edge(label="Pydantic", style="dashed", color="darkgreen") >> tools
        tools >> Edge(label="Markdown", style="dashed", color="darkgreen") >> mcp_client
        mcp_client >> Edge(label="ответ", style="dashed", color="darkgreen") >> user

        # Retry annotation
        _ = Blank("")
        rate >> Edge(label="retry 429/5xx", style="dotted", color="red") >> rate


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # diagrams lib uses cwd for temp files, so switch to output dir
    original_cwd = os.getcwd()
    os.chdir(OUTPUT_DIR)
    try:
        system_overview()
        feature_anatomy()
        auto_registry_flow()
        data_flow()
    finally:
        os.chdir(original_cwd)

    generated = sorted(OUTPUT_DIR.glob("*.png"))
    print(f"Generated {len(generated)} diagrams in {OUTPUT_DIR}/")
    for p in generated:
        print(f"  {p.name}")


if __name__ == "__main__":
    main()
