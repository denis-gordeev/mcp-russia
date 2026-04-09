"""Constants for Russian official document generation.

Based on GOST R 7.0.97-2016 and Russian deloproizvodstvo standards.

The historical Brazilian constants are preserved in a legacy section
for backward compatibility during migration.
"""

# Russian months for official documents
МЕСЯЦЫ = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}

# Document types according to Russian standards
ТИПЫ_ДОКУМЕНТОВ = [
    "письмо",
    "распоряжение",
    "приказ",
    "акт",
    "справка",
    "протокол",
    "докладная_записка",
]

# Document prefixes
ПРЕФИКСЫ_ДОКУМЕНТОВ: dict[str, str] = {
    "письмо": "ПИСЬМО",
    "распоряжение": "РАСПОРЯЖЕНИЕ",
    "приказ": "ПРИКАЗ",
    "акт": "АКТ",  # noqa: RUF001
    "справка": "СПРАВКА",
    "протокол": "ПРОТОКОЛ",
    "докладная_записка": "ДОКЛАДНАЯ ЗАПИСКА",
}

# Russian official treatment forms (Обращения в официальных документах)
ОБРАЩЕНИЯ: dict[str, dict[str, str]] = {
    # Heads of state and government
    "президент российской федерации": {
        "обращение": "Уважаемый господин Президент",
        "титулование": "Президент Российской Федерации",
        "адресация": "Президенту Российской Федерации",
    },
    "председатель правительства": {
        "обращение": "Уважаемый господин Председатель",
        "титулование": "Председатель Правительства Российской Федерации",
        "адресация": "Председателю Правительства Российской Федерации",
    },
    "председатель совета федерации": {
        "обращение": "Уважаемый господин Председатель",
        "титулование": "Председатель Совета Федерации",
        "адресация": "Председателю Совета Федерации",
    },
    "председатель государственной думы": {
        "обращение": "Уважаемый господин Председатель",
        "титулование": "Председатель Государственной Думы",
        "адресация": "Председателю Государственной Думы",
    },
    # Ministers and heads of agencies
    "министр": {
        "обращение": "Уважаемый господин Министр",
        "титулование": "Министр [название министерства]",
        "адресация": "Министру [название министерства]",
    },
    "руководитель федеральной службы": {
        "обращение": "Уважаемый господин Руководитель",
        "титулование": "Руководитель [название службы]",
        "адресация": "Руководителю [название службы]",
    },
    "губернатор": {
        "обращение": "Уважаемый господин Губернатор",
        "титулование": "Губернатор [название субъекта]",
        "адресация": "Губернатору [название субъекта]",
    },
    "мэр": {
        "обращение": "Уважаемый господин Мэр",
        "титулование": "Мэр города [название]",
        "адресация": "Мэру города [название]",
    },
    # Judicial officials
    "председатель конституционного суда": {
        "обращение": "Уважаемый господин Председатель",
        "титулование": "Председатель Конституционного Суда",
        "адресация": "Председателю Конституционного Суда",
    },
    "председатель верховного суда": {
        "обращение": "Уважаемый господин Председатель",
        "титулование": "Председатель Верховного Суда",
        "адресация": "Председателю Верховного Суда",
    },
    "судья": {
        "обращение": "Уважаемый суд",
        "титулование": "Судья [название суда]",
        "адресация": "В [название суда]",  # noqa: RUF001
    },
    # Local government
    "глава муниципального образования": {
        "обращение": "Уважаемый господин Глава",
        "титулование": "Глава [название муниципального образования]",
        "адресация": "Главе [название муниципального образования]",
    },
    "депутат": {
        "обращение": "Уважаемый господин Депутат",
        "титулование": "Депутат [название органа]",
        "адресация": "Депутату [название органа]",
    },
    # Corporate/organizational
    "генеральный директор": {
        "обращение": "Уважаемый господин Генеральный директор",
        "титулование": "Генеральный директор [название организации]",
        "адресация": "Генеральному директору [название организации]",
    },
    "директор": {
        "обращение": "Уважаемый господин Директор",
        "титулование": "Директор [название организации]",
        "адресация": "Директору [название организации]",
    },
    "начальник": {
        "обращение": "Уважаемый господин Начальник",
        "титулование": "Начальник [название подразделения]",
        "адресация": "Начальнику [название подразделения]",
    },
    "ректор": {
        "обращение": "Уважаемый господин Ректор",
        "титулование": "Ректор [название вуза]",
        "адресация": "Ректору [название вуза]",
    },
}

# ============================================================================
# LEGACY Brazilian constants (preserved for backward compatibility)
# Based on Manual de Redação da Presidência da República, 3ª edição (2018)
# ============================================================================

MESES = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro",
}

TIPOS_DOCUMENTO = [
    "oficio",
    "despacho",
    "portaria",
    "parecer",
    "nota_tecnica",
    "ata",
    "exposicao_motivos",
]

PREFIXOS_DOCUMENTO: dict[str, str] = {
    "oficio": "OFÍCIO",
    "despacho": "Despacho",
    "portaria": "PORTARIA",
    "parecer": "Parecer",
    "nota_tecnica": "Nota Técnica",
    "ata": "Ata",
    "exposicao_motivos": "EM",
    # Legados (abolidos na 3ª edição, mas aceitos para retrocompatibilidade)
    "memorando": "OFÍCIO",
    "aviso": "OFÍCIO",
}

PRONOMES_TRATAMENTO: dict[str, dict[str, str]] = {
    "presidente da república": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Excelentíssimo Senhor Presidente da República,",
        "abreviatura": "Não se usa",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "presidente do congresso nacional": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Excelentíssimo Senhor Presidente do Congresso Nacional,",
        "abreviatura": "Não se usa",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "presidente do supremo tribunal federal": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Excelentíssimo Senhor Presidente do Supremo Tribunal Federal,",
        "abreviatura": "Não se usa",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "vice-presidente da república": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Senhor Vice-Presidente da República,",
        "abreviatura": "V. Exa.",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "ministro": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Senhor Ministro,",
        "abreviatura": "V. Exa.",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "governador": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Senhor Governador,",
        "abreviatura": "V. Exa.",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "prefeito": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Senhor Prefeito,",
        "abreviatura": "V. Exa.",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "senador": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Senhor Senador,",
        "abreviatura": "V. Exa.",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "deputado": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Senhor Deputado,",
        "abreviatura": "V. Exa.",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "juiz": {
        "tratamento": "Vossa Excelência",
        "vocativo": "Senhor Juiz,",
        "abreviatura": "V. Exa.",
        "enderecamento": "A Sua Excelência o Senhor",
    },
    "diretor": {
        "tratamento": "Vossa Senhoria",
        "vocativo": "Senhor Diretor,",
        "abreviatura": "V. Sa.",
        "enderecamento": "Ao Senhor",
    },
    "reitor": {
        "tratamento": "Vossa Magnificência",
        "vocativo": "Magnífico Reitor,",
        "abreviatura": "V. Maga.",
        "enderecamento": "Ao Magnífico Senhor Reitor",
    },
}
