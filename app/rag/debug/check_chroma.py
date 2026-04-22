from app.rag.chroma.chroma_client import get_or_create_collection

def debug_chroma():
    collection = get_or_create_collection("ai_sales_supernova")

    print("TOTAL EN COLECCION:", collection.count())

    res = collection.get(include=["metadatas"])

    print("TOTAL METADATAS:", len(res["metadatas"]))

    # agrupar por document_group
    groups = {}
    for meta in res["metadatas"]:
        group = meta.get("document_group", "SIN_GROUP")
        groups[group] = groups.get(group, 0) + 1

    print("\nGRUPOS EN CHROMA:")
    for g, count in groups.items():
        print(f"{g}: {count}")

    print("\nPRODUCT_PERFORMANCE:")
    for meta in res["metadatas"]:
        if meta.get("document_group") == "product_performance":
            print(meta.get("ranking"), meta.get("product_name"))

if __name__ == "__main__":
    debug_chroma()