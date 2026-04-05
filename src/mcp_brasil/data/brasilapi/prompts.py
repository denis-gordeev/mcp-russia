"""Переиспользуемые prompts для переходного слоя BrasilAPI."""

from __future__ import annotations


def analise_empresa(cnpj: str) -> str:
    """Анализ компании по CNPJ через текущий compatibility-layer.

    Собирает регистрационные сведения, адрес и статус компании.

    Args:
        cnpj: CNPJ da empresa (com ou sem formatação).
    """
    return (
        f"Подготовь структурированный профиль организации с CNPJ {cnpj}.\n\n"
        "Контекст:\n"
        "- Репозиторий `mcp-russia` еще находится в миграции.\n"
        "- Данные ниже приходят из исторического бразильского integration-layer BrasilAPI.\n\n"
        "Passos:\n"
        f"1. Use consultar_cnpj(cnpj='{cnpj}') para obter os dados cadastrais\n"
        "2. Com o CEP retornado, use consultar_cep para confirmar o endereço\n"
        "3. Com o DDD do telefone, use consultar_ddd para identificar a região\n\n"
        "Сформируй отчет со следующими блоками:\n"
        "- Профиль организации (razão social, nome fantasia, CNAE, porte)\n"
        "- Статус регистрации\n"
        "- Полный адрес\n"
        "- Контактные данные и капитал social\n"
        "- Короткая пометка, что это legacy-бразильский источник в переходном контуре `mcp-russia`"
    )


def panorama_economico() -> str:
    """Черновой макроэкономический обзор на базе исторических бразильских индикаторов."""
    return (
        "Собери краткий макроэкономический обзор по текущему compatibility-layer BrasilAPI.\n\n"
        "Контекст:\n"
        "- Это не финальная российская модель данных, а переходный бразильский набор индикаторов.\n"
        "- В выводе явно обозначь источник как legacy-layer внутри `mcp-russia`.\n\n"
        "Passos:\n"
        "1. Use consultar_taxa(sigla='SELIC') para a taxa básica de juros\n"
        "2. Use consultar_taxa(sigla='CDI') para o CDI\n"
        "3. Use consultar_taxa(sigla='IPCA') para a inflação\n"
        "4. Use consultar_cotacao(moeda='USD', data=<ontem>) para o dólar\n"
        "5. Use consultar_cotacao(moeda='EUR', data=<ontem>) para o euro\n\n"
        "В ответе дай сравнительную таблицу индикаторов, краткую интерпретацию и отдельную пометку о переходном статусе этих данных."
    )
