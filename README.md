# AI Sales Intelligence Supernova

Sistema de inteligencia de ventas con ETL, Data Warehouse y análisis avanzado.

## 📋 Descripción

Plataforma de análisis de ventas que extrae datos de una base de datos transaccional (MySQL), los transforma y carga en un Data Warehouse dimensional para análisis avanzado y generación de insights de negocio.

## 🏗️ Arquitectura

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────────┐
│  Base de Datos  │ ───> │  ETL Process │ ───> │ Data Warehouse  │
│   Transaccional │      │   (Python)   │      │  (Dimensional)  │
└─────────────────┘      └──────────────┘      └─────────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  Analytics   │
                         │   & Reports  │
                         └──────────────┘
```

### Componentes Principales

- **Source DB**: Base de datos MySQL transaccional (OLTP)
- **ETL Pipeline**: Procesos de extracción, transformación y carga
- **Data Warehouse**: Base de datos dimensional (OLAP) con modelo estrella
- **Analytics**: Consultas y reportes de negocio

## 📁 Estructura del Proyecto

```
ai_sales_intelligence_supernova/
├── app/
│   ├── core/
│   │   ├── config.py           # Configuración y variables de entorno
│   │   └── database.py         # Conexiones a bases de datos
│   ├── etl/
│   │   ├── jobs/               # Scripts de ejecución ETL
│   │   │   ├── test_extract.py
│   │   │   └── run_etl.py
│   │   ├── sql/
│   │   │   └── source_queries.py  # Queries SQL para extracción
│   │   ├── extract.py          # Lógica de extracción
│   │   ├── transform.py        # Lógica de transformación
│   │   └── load.py             # Lógica de carga
│   └── main.py                 # Punto de entrada FastAPI
├── .env                        # Variables de entorno (NO subir a Git)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.8+
- MySQL 5.7+ o MariaDB
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el repositorio

```bash
git clone <repository-url>
cd ai_sales_intelligence_supernova
```

### Paso 2: Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Base de datos origen (transaccional)
SOURCE_DB_HOST=localhost
SOURCE_DB_PORT=3306
SOURCE_DB_USER=tu_usuario
SOURCE_DB_PASSWORD=tu_password
SOURCE_DB_NAME=nombre_db_origen

# Data Warehouse (dimensional)
WAREHOUSE_DB_HOST=localhost
WAREHOUSE_DB_PORT=3306
WAREHOUSE_DB_USER=tu_usuario
WAREHOUSE_DB_PASSWORD=tu_password
WAREHOUSE_DB_NAME=nombre_db_warehouse
```

### Paso 5: Verificar conexión

```bash
python -c "from app.core.config import settings; print(f'DB Host: {settings.source_db_host}'); print(f'DB Name: {settings.source_db_name}')"
```

## 🔧 Uso

### Ejecutar ETL completo

```bash
python -m app.etl.jobs.run_etl
```

### Probar extracción de datos

```bash
python -m app.etl.jobs.test_extract
```

### Ejecutar servidor FastAPI

```bash
uvicorn app.main:app --reload
```

Accede a:
- API: http://127.0.0.1:8000
- Documentación interactiva: http://127.0.0.1:8000/docs
- Documentación alternativa: http://127.0.0.1:8000/redoc

## 📊 Modelo de Datos

### Tablas Dimensionales

- `dim_client`: Dimensión de clientes
- `dim_product`: Dimensión de productos
- `dim_subcategory`: Dimensión de subcategorías
- `dim_storehouse`: Dimensión de almacenes
- `dim_channel`: Dimensión de canales de venta
- `dim_date`: Dimensión de fechas

### Tablas de Hechos

- `fact_order`: Hechos de órdenes/pedidos
- `fact_order_detail`: Detalle de líneas de pedido
- `fact_inventory_snapshot`: Snapshots de inventario

### Vistas Enriquecidas

- `fact_order_enriched`: Órdenes con información dimensional
- `fact_order_detail_enriched`: Detalle enriquecido con dimensiones
- `fact_inventory_enriched`: Inventario con información de productos

## 📈 Análisis Disponibles

El sistema incluye consultas analíticas predefinidas:

- **Ventas por día/mes**: Tendencias temporales
- **Ventas por canal**: Análisis de canales de distribución
- **Top productos**: Productos más vendidos
- **Top clientes**: Clientes con mayor facturación
- **Inventario por almacén**: Stock disponible por ubicación
- **Productos sin ventas**: Identificación de productos sin rotación
- **Tendencia mensual**: Evolución de ventas en el tiempo
- **Productos de baja rotación**: Análisis de inventario lento
- **Perfil comercial de clientes**: Segmentación de clientes
- **Ventas por estado**: Análisis geográfico de ventas

## 🔍 Calidad de Datos

El sistema incluye validaciones de calidad:

- Detección de órdenes duplicadas
- Validación de integridad referencial
- Verificación de cantidades y totales
- Identificación de inconsistencias

## 🛠️ Tecnologías

- **Python 3.8+**: Lenguaje principal
- **FastAPI**: Framework web
- **SQLAlchemy**: ORM y gestión de bases de datos
- **Pydantic**: Validación de datos y configuración
- **PyMySQL**: Driver de MySQL
- **Pandas**: Manipulación de datos (opcional)
- **NumPy**: Operaciones numéricas (opcional)

## 📝 Notas Importantes

1. **Seguridad**: Nunca subas el archivo `.env` a Git. Ya está incluido en `.gitignore`.
2. **Backups**: Realiza backups regulares antes de ejecutar procesos ETL.
3. **Rendimiento**: Los procesos ETL pueden tardar según el volumen de datos.
4. **Logs**: Revisa los logs para identificar errores en el proceso.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es privado y confidencial.

## 👥 Contacto

Para preguntas o soporte, contacta al equipo de desarrollo.
