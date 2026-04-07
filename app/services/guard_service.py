BAD_WORDS = {
    "idiota",
    "imbecil",
    "estupido",
    "pendejo",
    "mierda",
    "maldito",
    "puta",
    "pinche",
}


ALLOWED_DOMAIN_KEYWORDS = [
    "ventas",
    "clientes",
    "productos",
    "inventario",
    "stock",
    "dashboard",
    "documento",
    "proceso",
    "politica",
    "devolucion",
    "etl",
    "rag",
    "query",
    "orden",
    "pedido",
    "ingresos",
    "margen",
    "supernova",
    "analisis",
    "reporte",
    "categoria",
]


def contains_bad_words(text: str) -> dict:
    lowered = text.lower()
    found = [word for word in BAD_WORDS if word in lowered]

    return {
        "flagged": len(found) > 0,
        "words": found
    }


def is_domain_related(text: str) -> bool:
    lowered = text.lower()
    return any(k in lowered for k in ALLOWED_DOMAIN_KEYWORDS)


def sanitize_output(text: str) -> dict:
    blocked_patterns = [
        "system prompt",
        "developer instructions",
        "api key",
        "sk-",
        "drop table",
        "delete from",
        "insert into",
        "update ",
        "select * from",
    ]

    lowered = text.lower()
    found = [p for p in blocked_patterns if p in lowered]

    return {
        "blocked": len(found) > 0,
        "patterns": found
    }