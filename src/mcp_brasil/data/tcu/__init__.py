"""⚠️ DEPRECATED — Legacy-слой TCU внутри mcp-russia — Tribunal de Contas da Uniao (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_brasil.data.rosstat`` (Росстат) и будущий модуль Счётной палаты РФ
    для российских аудиторских данных.
    Данный модуль сохраняет обратную совместимость для бразильских данных TCU.
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tcu",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TCU внутри mcp-russia: "
        "Tribunal de Contas da Uniao: решения, недопущенные поставщики, "
        "лишённые права занимать публичные должности, консолидированные сертификаты (APF), "
        "расчёт задолженности, запросы Конгресса, контракты TCU и CADIRREG. "
        "Для российских аудиторских данных используйте модуль rosstat."
    ),
    version="0.1.0-deprecated",
    api_base="https://dados-abertos.apps.tcu.gov.br",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "tcu", "решения", "недопущенные", "лишённые-прав", "сертификаты", "контракты", "бразилия-legacy"],
)
