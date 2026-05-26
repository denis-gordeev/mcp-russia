"""Pydantic schemas for the Роскомнадзор feature."""

from __future__ import annotations

from pydantic import BaseModel


class LicenziyaSvyazi(BaseModel):
    """Лицензия на оказание услуг связи."""

    nomer: str
    tip_licenzii: str = ""
    organizaciya: str = ""
    data_vydachi: str = ""
    data_okonchaniya: str = ""
    status: str = ""  # "действует", "приостановлена", "аннулирована"
    territoriya: str = ""


class SMI(BaseModel):
    """Средство массовой информации."""

    nazvanie: str = ""
    tip_smi: str = ""
    registracionnyy_nomer: str = ""
    data_registracii: str = ""
    uchreditel: str = ""
    yazyk: str = ""
    territoriye_rasprostraneniya: str = ""


class OperatorPD(BaseModel):
    """Оператор персональных данных."""

    nazvanie: str = ""
    inn: str = ""
    tip_operatora: str = ""
    data_vneseniya_v_reestr: str = ""
    cel_obrabotki: str = ""
    status: str = ""


class NarushenieRKN(BaseModel):
    """Нарушение в сфере связи/информационных технологий."""

    opisanie: str
    tip_narusheniya: str = ""
    organizaciya: str = ""
    norma_prava: str = ""  # ссылка на закон (152-ФЗ, 149-ФЗ и т.д.)
    data_vyyavleniya: str = ""
    status_rassmotreniya: str = ""
    shtraf: float | None = None
    valyuta: str = "руб."


class ZapisReestra(BaseModel):
    """Запись из реестра Роскомнадзора."""

    registry_code: str  # код реестра
    zapisi_id: str
    osnovanie: str = ""
    data_vneseniya: str = ""
    status: str = ""
    opisanie: str = ""
