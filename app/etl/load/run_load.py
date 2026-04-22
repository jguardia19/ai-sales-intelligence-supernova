from app.etl.load.dim_load import load_dimensions
from app.etl.load.fact_load import load_facts


def run_load(transformed_data: dict) -> None:
    print(" Iniciando carga de dimensiones...")
    load_dimensions(transformed_data)

    print("Iniciando carga de hechos...")
    load_facts(transformed_data)

    print(" Carga finalizada correctamente.")