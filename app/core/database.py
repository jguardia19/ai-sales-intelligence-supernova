from sqlalchemy import create_engine
from app.core.config import settings


def build_mysql_url(
    host: str,
    port: int,
    user: str,
    password: str,
    db_name: str
) -> str:
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"


source_engine = create_engine(
    build_mysql_url(
        settings.source_db_host,
        settings.source_db_port,
        settings.source_db_user,
        settings.source_db_password,
        settings.source_db_name,
    ),
    pool_pre_ping=True,
)

warehouse_engine = create_engine(
    build_mysql_url(
        settings.warehouse_db_host,
        settings.warehouse_db_port,
        settings.warehouse_db_user,
        settings.warehouse_db_password,
        settings.warehouse_db_name,
    ),
    pool_pre_ping=True,
)