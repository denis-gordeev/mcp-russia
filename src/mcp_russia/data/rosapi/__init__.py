"""РосАПИ — мульти-API сервис для российских справочных данных.

Справочные данные для российских реалий:
- Адреса через ФИАС (Федеральная информационная адресная система)
- Организации по ИНН/ОГРН
- Справочник банков ЦБ РФ
- Праздники РФ
- Почтовые индексы
"""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="rosapi",
    opisanie=(
        "Справочные данные для России: адреса (ФИАС), организации (ИНН/ОГРН), "
        "банки, праздники, почтовые индексы"
    ),
    versiya="0.2.0",
    baza_api="https://dadata.ru/api",
    trebuet_autentifikatsii=True,
    peremennaya_avt_env="MCP_RUSSIA_DADATA_API_KEY",
    tegi=[
        "адрес",
        "фиас",
        "инн",
        "огрн",
        "банки",
        "праздники",
        "почтовый-индекс",
    ],
)
