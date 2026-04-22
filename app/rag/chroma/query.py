import re

from app.rag.chroma.chroma_client import get_or_create_collection
from app.rag.embeddings.openai_embedder import generate_embedding


def extract_top_k(user_query: str, default: int = 5) -> int:
    q = user_query.lower()

    match = re.search(r"top\s*(\d+)", q)
    if match:
        return int(match.group(1))

    return default


def detect_query_intent(user_query: str) -> str:
    q = user_query.lower()

    has_top = "top" in q or "ranking" in q
    has_product = "producto" in q or "productos" in q
    has_client = "cliente" in q or "clientes" in q
    has_category = (
        "categoría" in q or "categorias" in q or
        "categorías" in q or "categoria" in q
    )
    has_warehouse = "almacen" in q or "almacén" in q or "almacenes" in q
    has_dead_stock = (
        "stock muerto" in q or
        "sin movimiento" in q or
        "productos sin ventas" in q or
        "dead stock" in q or
        "inventario inmovilizado" in q
    )
    has_month = (
        "mes" in q or "mensual" in q or
        "periodo" in q or "período" in q or
        "meses" in q
    )

    has_sales_words = (
        "más vendido" in q or "mas vendido" in q or
        "más vendidos" in q or "mas vendidos" in q or
        "ventas" in q or "ingresos" in q or
        "mejor" in q or "peor" in q
    )

    if (has_top and has_product) or (has_product and has_sales_words):
        return "product_ranking"

    if (has_top and has_client) or (has_client and has_sales_words):
        return "client_ranking"

    if (has_top and has_category) or (has_category and has_sales_words):
        return "category_ranking"

    if has_warehouse and (has_top or "inventario" in q or "stock" in q):
        return "warehouse_ranking"

    if has_dead_stock:
        return "dead_stock"

    if has_month and (has_top or has_sales_words or "tendencia" in q):
        return "monthly_trend"

    return "semantic"


def search_similar_chunks(
    query: str,
    top_k: int = 8,
    collection_name: str = "ai_sales_supernova",
    where: dict | None = None,
    where_document: dict | None = None,
):
    collection = get_or_create_collection(collection_name)
    query_embedding = generate_embedding(query)

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
        where_document=where_document,
        include=["documents", "metadatas", "distances"],
    )

    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    ids = result.get("ids", [[]])[0]
    distances = result.get("distances", [[]])[0]

    rows = []
    for i, doc in enumerate(docs):
        rows.append({
            "chunk_id": ids[i],
            "text": doc,
            "metadata": metas[i] if i < len(metas) else {},
            "distance": distances[i] if i < len(distances) else None,
        })

    return rows


def get_documents_by_group(
    collection_name: str,
    document_group: str,
    top_k: int = 5,
    extra_where: dict | None = None,
    sort_field: str = "ranking",
    reverse: bool = False,
):
    collection = get_or_create_collection(collection_name)

    filters = [{"document_group": document_group}]

    if extra_where:
        for key, value in extra_where.items():
            filters.append({key: value})

    if len(filters) == 1:
        where = filters[0]
    else:
        where = {"$and": filters}

    result = collection.get(
        where=where,
        include=["documents", "metadatas"],
    )

    docs = result.get("documents") or []
    metas = result.get("metadatas") or []
    ids = result.get("ids") or []

    rows = []
    total = min(len(ids), len(docs), len(metas))

    for i in range(total):
        rows.append({
            "chunk_id": ids[i],
            "text": docs[i] if docs[i] else "",
            "metadata": metas[i] if metas[i] else {},
            "distance": None,
        })

    rows = [r for r in rows if r["metadata"].get(sort_field) is not None]
    rows.sort(key=lambda x: x["metadata"][sort_field], reverse=reverse)

    return rows[:top_k]

def rerank_results(user_query: str, rows: list[dict]) -> list[dict]:
    q = user_query.lower()

    for row in rows:
        text = (row.get("text") or "").lower()
        meta = row.get("metadata") or {}
        distance = row.get("distance")

        score = 0

        if distance is not None:
            score += -distance

        if meta.get("ranking") is not None:
            score += 3

        if meta.get("ranking_revenue") is not None:
            score += 2

        if meta.get("ranking_stock") is not None:
            score += 2

        if meta.get("ranking_month") is not None:
            score += 2

        if meta.get("document_group") in [
            "product_performance",
            "client_profile",
            "category_performance",
            "monthly_trend",
            "warehouse_inventory",
            "dead_stock_alert",
            "zone_performance",
        ]:
            score += 2

        if "ranking" in q or "top" in q:
            if "ranking" in text or "top" in text:
                score += 2

        if "más vendido" in q or "mas vendido" in q:
            if "más vendido" in text or "mas vendido" in text:
                score += 2

        if "cliente" in q and meta.get("client_name"):
            score += 2

        if "categor" in q and (meta.get("category_name") or meta.get("category")):
            score += 2

        if "almacen" in q or "almacén" in q:
            if meta.get("warehouse_name"):
                score += 2

        if "stock muerto" in q or "sin movimiento" in q:
            if meta.get("document_group") == "dead_stock_alert":
                score += 4

        row["final_score"] = score

    return sorted(rows, key=lambda x: x["final_score"], reverse=True)


def extract_product_category_filter(user_query: str) -> str | None:
    q = user_query.lower()

    category_map = {
        "pestañas": "Pestañas",
        "pestanas": "Pestañas",
        "lamparas para uñas": "Lamparas para uñas",
        "lámparas para uñas": "Lamparas para uñas",
        "utensilios y herramientas": "Utensilios y Herramientas",
        "gamas le'mussa": "Gamas Le'Mussa",
        "gamas le mussa": "Gamas Le'Mussa",
        "eléctricos": "Eléctricos",
        "electricos": "Eléctricos",
        "organizadores": "Organizadores",
        "productos para el hogar": "Productos para el hogar",
    }

    for key, value in category_map.items():
        if key in q:
            return value

    return None


def retrieve_context_smart(
    user_query: str,
    top_k: int = 8,
    collection_name: str = "ai_sales_supernova",
):
    intent = detect_query_intent(user_query)
    top_n = extract_top_k(user_query, default=5)
    q = user_query.lower()

    print("USER QUERY:", user_query)
    print("INTENT DETECTADO:", intent)
    print("TOP N DETECTADO:", top_n)

    if intent == "product_ranking":
        extra_where = {"metric_scope": "annual"}

        category_filter = extract_product_category_filter(user_query)
        if category_filter:
            extra_where["category"] = category_filter

        results = get_documents_by_group(
            collection_name=collection_name,
            document_group="product_performance",
            top_k=top_n,
            extra_where=extra_where,
            sort_field="ranking",
            reverse=False,
        )

        print("TOTAL DOCUMENTOS RECUPERADOS:", len(results))
        for r in results:
            print(
                r["metadata"].get("ranking"),
                r["metadata"].get("product_name")
            )

        return {
            "intent": intent,
            "results": results,
        }

    if intent == "client_ranking":
        results = get_documents_by_group(
            collection_name=collection_name,
            document_group="client_profile",
            top_k=top_n,
            extra_where={"metric_scope": "annual"},
            sort_field="ranking_revenue",
            reverse=False,
        )

        print("TOTAL DOCUMENTOS RECUPERADOS:", len(results))
        for r in results:
            print(
                r["metadata"].get("ranking_revenue"),
                r["metadata"].get("client_name")
            )

        return {
            "intent": intent,
            "results": results,
        }

    if intent == "category_ranking":
        results = get_documents_by_group(
            collection_name=collection_name,
            document_group="category_performance",
            top_k=top_n,
            extra_where={"metric_scope": "annual"},
            sort_field="ranking_revenue",
            reverse=False,
        )

        print("TOTAL DOCUMENTOS RECUPERADOS:", len(results))
        for r in results:
            print(
                r["metadata"].get("ranking_revenue"),
                r["metadata"].get("category_name")
            )

        return {
            "intent": intent,
            "results": results,
        }

    if intent == "warehouse_ranking":
        results = get_documents_by_group(
            collection_name=collection_name,
            document_group="warehouse_inventory",
            top_k=top_n,
            extra_where={"metric_scope": "annual"},
            sort_field="ranking_stock",
            reverse=False,
        )

        print("TOTAL DOCUMENTOS RECUPERADOS:", len(results))
        for r in results:
            print(
                r["metadata"].get("ranking_stock"),
                r["metadata"].get("warehouse_name")
            )

        return {
            "intent": intent,
            "results": results,
        }

    if intent == "dead_stock":
        results = get_documents_by_group(
            collection_name=collection_name,
            document_group="dead_stock_alert",
            top_k=top_n,
            extra_where={"metric_scope": "annual"},
            sort_field="ranking_stock",
            reverse=False,
        )

        print("TOTAL DOCUMENTOS RECUPERADOS:", len(results))
        for r in results:
            print(
                r["metadata"].get("ranking_stock"),
                r["metadata"].get("product_name")
            )

        return {
            "intent": intent,
            "results": results,
        }

    if intent == "monthly_trend":
        sort_field = "ranking_month"
        reverse = False

        if "peor mes" in q or "caída" in q or "caida" in q:
            sort_field = "sales_variation_pct"
            reverse = False

        results = get_documents_by_group(
            collection_name=collection_name,
            document_group="monthly_trend",
            top_k=top_n,
            extra_where={"metric_scope": "monthly"},
            sort_field=sort_field,
            reverse=reverse,
        )

        print("TOTAL DOCUMENTOS RECUPERADOS:", len(results))
        for r in results:
            print(
                r["metadata"].get(sort_field),
                r["metadata"].get("period")
            )

        return {
            "intent": intent,
            "results": results,
        }

    results = search_similar_chunks(
        query=user_query,
        top_k=top_k,
        collection_name=collection_name,
        where=None,
        where_document=None,
    )

    results = rerank_results(user_query, results)

    print("TOTAL DOCUMENTOS RECUPERADOS:", len(results))
    for r in results[:10]:
        print(
            r["metadata"].get("document_group"),
            r["metadata"].get("ranking"),
            r["metadata"].get("product_name")
            or r["metadata"].get("client_name")
            or r["metadata"].get("category_name")
            or r["metadata"].get("warehouse_name")
            or r["metadata"].get("period")
        )

    return {
        "intent": "semantic",
        "results": results,
    }