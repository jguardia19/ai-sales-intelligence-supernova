import json
from pathlib import Path

from app.core.database import source_engine
from app.etl.extract.extractors import extract_named_dataframe
from app.business_docs.pipeline_registry import PIPELINE_REGISTRY
from app.business_docs.utils.json_utils import clean_document_for_json



def save_documents_to_json(documents: list[dict], output_path: str) -> None:
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

    print(f"[DOCS] Archivo generado en: {output_file}")
    print(f"[DOCS] Total documentos: {len(documents)}")


def run():
    all_documents = []

    for item in PIPELINE_REGISTRY:
        dataset_name = item["dataset_name"]
        query_dict = item["query_dict"]
        query_key = item["query_key"]
        cleaner = item["cleaner"]
        transformer = item["transformer"]
        generator = item["generator"]

        print("=" * 100)
        print(f"[PIPELINE] Procesando dataset: {dataset_name}")

        query_sql = query_dict[query_key]

        df_raw = extract_named_dataframe(
            source_engine,
            query_key,
            query_sql
        )

        df_clean = cleaner(df_raw)
        print(f"[PIPELINE] Filas limpias: {len(df_clean)}")

        print(f"[PIPELINE] Transformando dataset: {dataset_name}")
        df_transformed = transformer(df_clean)

        print(f"[PIPELINE] Generando documentos: {dataset_name}")
        documents = generator(df_transformed)
        documents = [clean_document_for_json(doc) for doc in documents]

        print(f"[PIPELINE] Documentos generados para {dataset_name}: {len(documents)}")

        all_documents.extend(documents)

    print("=" * 100)
    print(f"[PIPELINE] Total documentos acumulados: {len(all_documents)}")

    save_documents_to_json(
        all_documents,
        output_path="data/business_docs/business_documents.json"
    )

    return all_documents


if __name__ == "__main__":
    run()