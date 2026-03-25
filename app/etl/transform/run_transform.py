from datetime import datetime

from app.etl.transform.clients_transform import transform_dim_client
from app.etl.transform.products_transform import transform_dim_product
from app.etl.transform.orders_transform import transform_fact_order
from app.etl.transform.order_detail_transform import transform_fact_order_detail
from app.etl.transform.inventory_transform import transform_fact_inventory_snapshot


def get_today_date_key() -> int:
    return int(datetime.now().strftime("%Y%m%d"))


def transform_all_sources(raw_data: dict) -> dict:
    transformed = {}

    if "dim_client" in raw_data:
        transformed["dim_client"] = transform_dim_client(raw_data["dim_client"])

    if "dim_product" in raw_data:
        transformed["dim_product"] = transform_dim_product(raw_data["dim_product"])

    if "fact_order" in raw_data:
        transformed["fact_order"] = transform_fact_order(raw_data["fact_order"])

    if "fact_order_detail" in raw_data:
        transformed["fact_order_detail"] = transform_fact_order_detail(raw_data["fact_order_detail"])

    if "fact_inventory_snapshot" in raw_data:
        transformed["fact_inventory_snapshot"] = transform_fact_inventory_snapshot(
            raw_data["fact_inventory_snapshot"],
            snapshot_date_key=get_today_date_key()
        )

    return transformed