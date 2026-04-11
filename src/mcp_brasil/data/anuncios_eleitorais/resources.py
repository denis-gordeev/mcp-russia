"""Справочные resources для compatibility-layer Meta Ad Library.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские данные о политической рекламе сохраняются для обратной совместимости
с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json

from .constants import (
    ESTADOS_BRASILEIROS,
    FAIXAS_AUDIENCIA,
    PLATAFORMAS,
)


def estados_brasileiros() -> str:
    """Список 27 бразильских штатов (аббревиатура и название) для региональных фильтров (legacy)."""
    estados = [
        {"sigla": sigla, "nome": nome} for sigla, nome in sorted(ESTADOS_BRASILEIROS.items())
    ]
    return json.dumps(estados, ensure_ascii=False, indent=2)


def parametros_busca() -> str:
    """Справка по параметрам поиска в текущем legacy API политической рекламы Бразилии."""
    params = {
        "search_terms": {
            "descricao": "Поисковые термины (макс. 100 символов). Пробел = AND.",
            "exemplo": "educação saúde",
        },
        "search_page_ids": {
            "descricao": "ID страниц Facebook (до 10).",
            "exemplo": ["123456789"],
        },
        "ad_active_status": {
            "descricao": "Статус объявления.",
            "valores": ["ACTIVE", "INACTIVE", "ALL"],
        },
        "ad_delivery_date_min": {
            "descricao": "Минимальная дата показа.",
            "formato": "YYYY-mm-dd",
        },
        "ad_delivery_date_max": {
            "descricao": "Максимальная дата показа.",
            "formato": "YYYY-mm-dd",
        },
        "bylines": {
            "descricao": "Спонсоры (поле 'Оплачено'; точный текст).",
            "exemplo": ["Partido X"],
        },
        "delivery_by_region": {
            "descricao": "Регионы/штаты доставки. Используйте полное название.",
            "exemplo": ["São Paulo", "Rio de Janeiro"],
        },
        "estimated_audience_size_min": {
            "descricao": "Минимальный размер целевой аудитории.",
            "valores_permitidos": FAIXAS_AUDIENCIA,
        },
        "estimated_audience_size_max": {
            "descricao": "Максимальный размер целевой аудитории.",
            "valores_permitidos": FAIXAS_AUDIENCIA,
        },
        "media_type": {
            "descricao": "Тип медиа объявления.",
            "valores": ["ALL", "IMAGE", "MEME", "VIDEO", "NONE"],
        },
        "publisher_platforms": {
            "descricao": "Платформы, на которых появилось объявление.",
            "valores": PLATAFORMAS,
        },
        "search_type": {
            "descricao": "Тип текстового поиска.",
            "valores": ["KEYWORD_UNORDERED", "KEYWORD_EXACT_PHRASE"],
        },
    }
    return json.dumps(params, ensure_ascii=False, indent=2)


def campos_disponiveis() -> str:
    """Справка по полям, которые возвращает текущий compatibility-layer объявлений (legacy, Бразилия)."""
    campos = {
        "basicos": {
            "id": "ID в библиотеке объявлений",
            "page_id": "ID страницы Facebook",
            "page_name": "Название страницы Facebook",
            "ad_creation_time": "Дата/время создания (UTC)",
            "ad_delivery_start_time": "Начало показа",
            "ad_delivery_stop_time": "Окончание показа",
            "ad_snapshot_url": "URL для просмотра объявления",
            "ad_creative_bodies": "Тексты креатива",
            "ad_creative_link_titles": "Заголовки ссылок",
            "ad_creative_link_descriptions": "Описания ссылок",
            "ad_creative_link_captions": "Подписи ссылок",
            "languages": "Языки объявления",
            "publisher_platforms": "Платформы (Facebook, Instagram и т.д.)",
        },
        "politicos_brasil": {
            "bylines": "Спонсор (поле 'Оплачено'; legacy coverage в Бразилии)",
            "currency": "Валюта расходов (BRL; legacy coverage в Бразилии)",
            "spend": "Общие расходы (диапазон: <100, 100-499, 500-999, ...)",
            "impressions": "Показы (диапазон: <1000, 1K-5K, ...)",
            "demographic_distribution": "Распределение по возрасту и полу (%)",
            "delivery_by_region": "Распределение по штатам (%)",
            "estimated_audience_size": "Оценочный размер аудитории",
            "br_total_reach": "Оценочный охват в Бразилии",
            "target_ages": "Целевые возрастные группы",
            "target_gender": "Целевой пол",
            "target_locations": "Целевые локации",
            "age_country_gender_reach_breakdown": "Детализация охвата по возрасту/полу",
        },
    }
    return json.dumps(campos, ensure_ascii=False, indent=2)
