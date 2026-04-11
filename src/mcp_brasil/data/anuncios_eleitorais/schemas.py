"""Pydantic-схемы для модуля избирательной рекламы (Brazil, legacy)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FaixaValor(BaseModel):
    """Диапазон значений (мин/макс), используемый для показов и расходов (legacy -- Brazil)."""

    lower_bound: str | None = Field(
        default=None, description="Нижняя граница диапазона (legacy -- Brazil)"
    )
    upper_bound: str | None = Field(
        default=None, description="Верхняя граница диапазона (legacy -- Brazil)"
    )


class DistribuicaoDemografica(BaseModel):
    """Демографическое распределение по возрасту и полу (legacy -- Brazil)."""

    age: str | None = Field(
        default=None, description="Возрастная группа (напр.: 18-24, 25-34) (legacy -- Brazil)"
    )
    gender: str | None = Field(
        default=None, description="Пол (Male, Female, Unknown) (legacy -- Brazil)"
    )
    percentage: str | None = Field(default=None, description="Процент охвата (legacy -- Brazil)")


class DistribuicaoRegional(BaseModel):
    """Региональное распределение охвата рекламы (legacy -- Brazil)."""

    region: str | None = Field(
        default=None, description="Название региона/штата (legacy -- Brazil)"
    )
    percentage: str | None = Field(default=None, description="Процент охвата (legacy -- Brazil)")


class LocalizacaoAlvo(BaseModel):
    """Локация, включённая или исключённая из таргетинга (legacy -- Brazil)."""

    name: str | None = Field(default=None, description="Название локации (legacy -- Brazil)")
    num_obfuscated: int | None = Field(
        default=None, description="Количество скрытых локаций (legacy -- Brazil)"
    )
    excluded: bool | None = Field(
        default=None, description="Является ли исключением (legacy -- Brazil)"
    )


class AnuncioEleitoral(BaseModel):
    """Избирательная/политическая реклама из Библиотеки рекламы Meta (legacy -- Brazil)."""

    id: str = Field(description="ID из библиотеки рекламы (legacy -- Brazil)")
    ad_creation_time: str | None = Field(
        default=None, description="Дата/время создания рекламы (UTC) (legacy -- Brazil)"
    )
    ad_creative_bodies: list[str] | None = Field(
        default=None, description="Тексты креатива рекламы (legacy -- Brazil)"
    )
    ad_creative_link_captions: list[str] | None = Field(
        default=None, description="Подписи к ссылкам (legacy -- Brazil)"
    )
    ad_creative_link_descriptions: list[str] | None = Field(
        default=None, description="Описания ссылок (legacy -- Brazil)"
    )
    ad_creative_link_titles: list[str] | None = Field(
        default=None, description="Заголовки ссылок (legacy -- Brazil)"
    )
    ad_delivery_start_time: str | None = Field(
        default=None, description="Дата/время начала показа (legacy -- Brazil)"
    )
    ad_delivery_stop_time: str | None = Field(
        default=None, description="Дата/время окончания показа (legacy -- Brazil)"
    )
    ad_snapshot_url: str | None = Field(
        default=None, description="URL для просмотра архивной рекламы (legacy -- Brazil)"
    )
    bylines: str | None = Field(
        default=None, description="Имя спонсора рекламы (legacy -- Brazil)"
    )
    currency: str | None = Field(default=None, description="Валюта (ISO) (legacy -- Brazil)")
    spend: FaixaValor | None = Field(
        default=None, description="Общие расходы (диапазон) (legacy -- Brazil)"
    )
    impressions: FaixaValor | None = Field(
        default=None, description="Показы (диапазон) (legacy -- Brazil)"
    )
    demographic_distribution: list[DistribuicaoDemografica] | None = Field(
        default=None, description="Демографическое распределение (возраст/пол) (legacy -- Brazil)"
    )
    delivery_by_region: list[DistribuicaoRegional] | None = Field(
        default=None, description="Региональное распределение охвата (legacy -- Brazil)"
    )
    estimated_audience_size: FaixaValor | None = Field(
        default=None, description="Оценочный размер аудитории (legacy -- Brazil)"
    )
    br_total_reach: int | None = Field(
        default=None, description="Оценочный охват в Бразилии (legacy -- Brazil)"
    )
    languages: list[str] | None = Field(
        default=None, description="Языки рекламы (legacy -- Brazil)"
    )
    page_id: str | None = Field(
        default=None, description="ID страницы Facebook (legacy -- Brazil)"
    )
    page_name: str | None = Field(
        default=None, description="Название страницы Facebook (legacy -- Brazil)"
    )
    publisher_platforms: list[str] | None = Field(
        default=None, description="Платформы, на которых показывалась реклама (legacy -- Brazil)"
    )
    target_ages: list[str] | None = Field(
        default=None, description="Возрастные группы таргетинга (legacy -- Brazil)"
    )
    target_gender: str | None = Field(
        default=None, description="Пол таргетинга (Women, Men, All) (legacy -- Brazil)"
    )
    target_locations: list[LocalizacaoAlvo] | None = Field(
        default=None, description="Локации таргетинга (legacy -- Brazil)"
    )
    age_country_gender_reach_breakdown: list[dict[str, object]] | None = Field(
        default=None, description="Разбивка охвата по возрасту/стране/полу (legacy -- Brazil)"
    )


class CursorPaginacao(BaseModel):
    """Курсоры для постраничной навигации API (legacy -- Brazil)."""

    before: str | None = None
    after: str | None = None


class Paginacao(BaseModel):
    """Данные постраничной навигации ответа (legacy -- Brazil)."""

    cursors: CursorPaginacao | None = None
    next: str | None = Field(default=None, description="URL следующей страницы (legacy -- Brazil)")


class RespostaAnuncios(BaseModel):
    """Страничный ответ API рекламы (legacy -- Brazil)."""

    data: list[AnuncioEleitoral] = Field(default_factory=list)
    paging: Paginacao | None = None
