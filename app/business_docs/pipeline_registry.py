from app.etl.sql.source_queries import (
    DOCUMENT_QUERIES,
    QUERY_CLIENT,
    QUERY_STOREHOUSE,
    QUERY_PRODUCT,
    QUERY_CATEGORY,
    QUERY_MONTH,
    QUERY_ZONE,
)

#import tranformers de datas
from app.business_docs.services.products_top_dataset_transformer import transform_product_dataset
from app.business_docs.services.client_dataset_transformer import transform_client_dataset
from app.business_docs.services.warehouse_dataset_transformer import transform_warehouse_dataset
from app.business_docs.services.dead_stock_dataset_transformer import transform_dead_stock_dataset
from app.business_docs.services.category_products_dataset_transformer import transform_category_dataset
from app.business_docs.services.monthly_trend_transformer import transform_monthly_trends
from app.business_docs.services.zone_dataset_transformer import transform_zone_dataset

# import generacion de documentos
from app.business_docs.generators.products_top_documents import generate_product_documents
from app.business_docs.generators.clients_documents import generate_client_documents
from app.business_docs.generators.warehouse_documents import generate_warehouse_documents
from app.business_docs.generators.dead_stock_documents import generate_dead_stock_documents
from app.business_docs.generators.category_products_documents import generate_category_documents
from app.business_docs.generators.monthly_trend_documents import generate_monthly_documents
from app.business_docs.generators.zone_documents import generate_zone_documents

# import cleaners
from app.business_docs.cleaners.product_cleaner import clean_product_dataset
from app.business_docs.cleaners.client_cleaner import clean_client_dataset
from app.business_docs.cleaners.warehouse_cleaner import clean_warehouse_dataset
from app.business_docs.cleaners.dead_stock_cleaner import clean_dead_stock_dataset
from app.business_docs.cleaners.category_cleaner import clean_category_dataset
from app.business_docs.cleaners.monthly_cleaner import clean_monthly_dataset
from app.business_docs.cleaners.zone_cleaner import clean_zone_dataset
#from app.business_docs.cleaners.channel_cleaner import clean_channel_dataset




PIPELINE_REGISTRY = [
    {
        "dataset_name": "top_products",
        "query_dict": DOCUMENT_QUERIES,
        "query_key": "top_products",
        "transformer": transform_product_dataset,
        "cleaner": clean_product_dataset,
        "generator": generate_product_documents,
    },
    {
        "dataset_name": "top_clients",
        "query_dict": QUERY_CLIENT,
        "query_key": "top_clients",
        "transformer": transform_client_dataset,
        "cleaner": clean_client_dataset,
        "generator": generate_client_documents,
    },
    {
        "dataset_name": "inventory_by_storehouse",
        "query_dict": QUERY_STOREHOUSE,
        "query_key": "inventory_by_storehouse",
        "transformer": transform_warehouse_dataset,
        "cleaner": clean_warehouse_dataset,
        "generator": generate_warehouse_documents,
    },
    {
        "dataset_name": "products_without_sales_last_year",
        "query_dict": QUERY_PRODUCT,
        "query_key": "products_without_sales_last_year",
        "transformer": transform_dead_stock_dataset,
        "cleaner": clean_dead_stock_dataset,
        "generator": generate_dead_stock_documents,
    },
    {
        "dataset_name": "top_categories",
        "query_dict": QUERY_CATEGORY,
        "query_key": "top_categories",
        "transformer": transform_category_dataset,
        "cleaner": clean_category_dataset,
        "generator": generate_category_documents,
    },
    {
        "dataset_name": "sales_by_month",
        "query_dict": QUERY_MONTH,
        "query_key": "sales_by_month",
        "transformer": transform_monthly_trends,
        "cleaner": clean_monthly_dataset,
        "generator": generate_monthly_documents,
    },
    {
        "dataset_name": "sales_by_state",
        "query_dict": QUERY_ZONE,
        "query_key": "sales_by_state",
        "transformer": transform_zone_dataset,
        "cleaner": clean_zone_dataset,
        "generator": generate_zone_documents,
    },
]