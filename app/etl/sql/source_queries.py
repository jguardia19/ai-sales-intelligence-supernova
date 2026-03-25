#consulta para tablas dimensiones
SQL_DIM_CLIENT_SOURCE = """
SELECT
    u.id AS client_id,
    TRIM(u.nombre) AS nombre,
    TRIM(u.apellido) AS apellido,
    TRIM(u.direccion) AS direccion,
    TRIM(u.colonia) AS colonia,
    TRIM(u.ciudad) AS ciudad,
    TRIM(u.estado) AS estado,
    TRIM(u.codigop) AS codigo_postal,
    TRIM(u.telefono) AS telefono,
    TRIM(u.correo) AS correo
FROM usuario u;
"""
#consulta para tablas dimensiones
SQL_DIM_SUBCATEGORY_SOURCE = """
SELECT
    s.id_subcategoria AS subcategoria_id,
    TRIM(s.nombre_subcategoria) AS nombre_subcategoria
FROM admin_subcategorias s;
"""

#consulta para tablas dimensiones
SQL_DIM_STOREHOUSE_SOURCE = """
SELECT
    a.id_almacen AS almacen_id,
    TRIM(a.nombre_almacen) AS nombre_almacen
FROM almacenes a WHERE a.status = 1;
"""

#consulta para tablas dimensiones
SQL_DIM_CHANNEL_SOURCE = """
SELECT DISTINCT
    TRIM(UPPER(f.vendedora)) AS channel_name
FROM folios f
WHERE f.vendedora IS NOT NULL
  AND TRIM(f.vendedora) <> ''
  AND f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR;
"""

#consulta para tablas dimensiones
SQL_DIM_DATE_SOURCE = """
SELECT DISTINCT
    DATE(t.full_date) AS full_date
FROM (
    SELECT f.fecha_procesado AS full_date
    FROM folios f
    WHERE f.fecha_procesado IS NOT NULL
      AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR

    UNION

    SELECT f.fecha_salida AS full_date
    FROM folios f
    WHERE f.fecha_salida IS NOT NULL
      AND DATE(f.fecha_salida) >= CURDATE() - INTERVAL 1 YEAR

    UNION

    SELECT f.fecha_entrega AS full_date
    FROM folios f
    WHERE f.fecha_entrega IS NOT NULL
      AND DATE(f.fecha_entrega) >= CURDATE() - INTERVAL 1 YEAR

    UNION

    SELECT ru.fecha AS full_date
    FROM registro_usuario ru
    WHERE ru.fecha IS NOT NULL
      AND DATE(ru.fecha) >= CURDATE() - INTERVAL 1 YEAR

    UNION

    SELECT ru.fecha_procesado AS full_date
    FROM registro_usuario ru
    WHERE ru.fecha_procesado IS NOT NULL
      AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
) t
WHERE t.full_date IS NOT NULL;
"""

#consulta para tablas dimensiones
SQL_DIM_PRODUCT_SOURCE = """
SELECT DISTINCT
    p.id AS product_id,
    TRIM(p.nombre) AS nombre,
    TRIM(p.codigo) AS codigo,
    p.preciou,
    p.preciom,
    p.precioc,
    p.topem,
    p.topec,
    p.visitas,
    TRIM(p.estatus) AS estatus,
    p.precio_costo,
    p.precio_yuan,
    TRIM(p.almacen) AS almacen,
    p.sub_categoria AS subcategoria_id,
    TRIM(s.nombre_subcategoria) AS nombre_subcategoria
FROM productos p
LEFT JOIN admin_subcategorias s
    ON s.id_subcategoria = p.sub_categoria;
"""
#consulta para tablas hechos
SQL_FACT_ORDER_SOURCE = """
SELECT
    f.id AS folio_id,
    TRIM(f.orden) AS orden,
    f.id_usuario AS client_id,
    TRIM(f.nombres) AS nombres_cliente_snapshot,
    TRIM(UPPER(f.vendedora)) AS channel_name,
    TRIM(f.paqueteria) AS paqueteria,
    f.cantidad AS cantidad_productos,
    f.total,
    TRIM(f.estatus) AS estatus,
    f.cajas,
    TRIM(UPPER(f.envio)) AS envio,
    CASE
        WHEN TRIM(UPPER(f.envio)) = 'SI' THEN 1
        ELSE 0
    END AS is_delivery,
    DATE(f.fecha_procesado) AS fecha_procesado,
    DATE(f.fecha_salida) AS fecha_salida,
    DATE(f.fecha_entrega) AS fecha_entrega
FROM folios f
WHERE f.orden IS NOT NULL
  AND TRIM(f.orden) <> '';
"""
# tabla hechos
SQL_FACT_ORDER_SOURCE = """
SELECT
    f.id AS folio_id,
    TRIM(f.orden) AS orden,
    f.id_usuario AS client_id,
    TRIM(f.nombres) AS nombres_cliente_snapshot,
    TRIM(UPPER(f.vendedora)) AS channel_name,
    TRIM(f.paqueteria) AS paqueteria,
    f.cantidad AS cantidad_productos,
    f.total,
    TRIM(f.estatus) AS estatus,
    f.cajas,
    TRIM(UPPER(f.envio)) AS envio,
    CASE
        WHEN TRIM(UPPER(f.envio)) = 'SI' THEN 1
        ELSE 0
    END AS is_delivery,
    DATE(f.fecha_procesado) AS fecha_procesado,
    DATE(f.fecha_salida) AS fecha_salida,
    DATE(f.fecha_entrega) AS fecha_entrega
FROM folios f
WHERE f.orden IS NOT NULL
  AND TRIM(f.orden) <> ''
  AND f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR;
"""
#tabla hechos
SQL_FACT_ORDER_DETAIL_SOURCE = """
SELECT
    ru.id AS detail_id,
    TRIM(ru.orden) AS orden,
    ru.id_usuario AS client_id,
    ru.id_producto AS product_id,
    TRIM(ru.nombre) AS product_name_snapshot,
    TRIM(ru.codigo) AS product_code_snapshot,
    ru.precio AS precio_unitario,
    ru.cantidad,
    (ru.precio * ru.cantidad) AS subtotal,
    DATE(ru.fecha) AS fecha,
    DATE(ru.fecha_procesado) AS fecha_procesado
FROM registro_usuario ru
WHERE ru.orden IS NOT NULL
  AND TRIM(ru.orden) <> ''
  AND ru.fecha_procesado IS NOT NULL
  AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR;
"""
# tabla hechos
SQL_FACT_INVENTORY_SNAPSHOT_SOURCE = """
SELECT
    ap.id AS inventory_row_id,
    ap.id_almacen AS almacen_id,
    ap.id_producto AS product_id,
    ap.cantidad
FROM almacen_producto ap;
"""

SQL_FACT_ORDER_ENRICHED_SOURCE = """
SELECT
    f.id AS folio_id,
    TRIM(f.orden) AS orden,
    f.id_usuario AS client_id,
    TRIM(u.nombre) AS client_nombre,
    TRIM(u.apellido) AS client_apellido,
    TRIM(CONCAT(COALESCE(u.nombre, ''), ' ', COALESCE(u.apellido, ''))) AS client_full_name,
    TRIM(UPPER(f.vendedora)) AS channel_name,
    TRIM(f.paqueteria) AS paqueteria,
    f.cantidad AS cantidad_productos,
    f.total,
    TRIM(f.estatus) AS estatus,
    f.cajas,
    TRIM(UPPER(f.envio)) AS envio,
    CASE
        WHEN TRIM(UPPER(f.envio)) = 'SI' THEN 1
        ELSE 0
    END AS is_delivery,
    DATE(f.fecha_procesado) AS fecha_procesado,
    DATE(f.fecha_salida) AS fecha_salida,
    DATE(f.fecha_entrega) AS fecha_entrega
FROM folios f
LEFT JOIN usuario u
    ON u.id = f.id_usuario
WHERE f.orden IS NOT NULL
  AND TRIM(f.orden) <> ''
  AND f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR;
"""

SQL_FACT_ORDER_DETAIL_ENRICHED_SOURCE = """
SELECT
    ru.id AS detail_id,
    TRIM(ru.orden) AS orden,
    ru.id_usuario AS client_id,
    ru.id_producto AS product_id,
    TRIM(ru.nombre) AS product_name_snapshot,
    TRIM(ru.codigo) AS product_code_snapshot,
    ru.precio AS precio_unitario,
    ru.cantidad,
    (ru.precio * ru.cantidad) AS subtotal,
    DATE(ru.fecha) AS fecha,
    DATE(ru.fecha_procesado) AS fecha_procesado,
    TRIM(p.nombre) AS product_nombre_master,
    TRIM(p.codigo) AS product_codigo_master,
    p.precio_costo,
    p.sub_categoria AS subcategoria_id,
    TRIM(s.nombre_subcategoria) AS nombre_subcategoria
FROM registro_usuario ru
LEFT JOIN productos p
    ON p.id = ru.id_producto
LEFT JOIN admin_subcategorias s
    ON s.id_subcategoria = p.sub_categoria
WHERE ru.orden IS NOT NULL
  AND TRIM(ru.orden) <> ''
  AND ru.fecha_procesado IS NOT NULL
  AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR;
"""

SQL_FACT_INVENTORY_ENRICHED_SOURCE = """
SELECT
    ap.id AS inventory_row_id,
    ap.id_almacen AS almacen_id,
    TRIM(a.nombre_almacen) AS nombre_almacen,
    ap.id_producto AS product_id,
    TRIM(p.nombre) AS product_nombre,
    TRIM(p.codigo) AS product_codigo,
    ap.cantidad,
    p.sub_categoria AS subcategoria_id,
    TRIM(s.nombre_subcategoria) AS nombre_subcategoria
FROM almacen_producto ap
LEFT JOIN almacenes a
    ON a.id_almacen = ap.id_almacen
LEFT JOIN productos p
    ON p.id = ap.id_producto
LEFT JOIN admin_subcategorias s
    ON s.id_subcategoria = p.sub_categoria;
"""


# =========================================================
# DATA QUALITY - ULTIMO AÑO EN VENTAS
# =========================================================

SQL_DQ_DUPLICATE_ORDERS = """
SELECT
    TRIM(f.orden) AS orden,
    COUNT(*) AS total_registros
FROM folios f
WHERE f.orden IS NOT NULL
  AND TRIM(f.orden) <> ''
  AND f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY TRIM(f.orden)
HAVING COUNT(*) > 1;
"""

SQL_DQ_DUPLICATE_ORDER_DETAIL_IDS = """
SELECT
    ru.id,
    COUNT(*) AS total_registros
FROM registro_usuario ru
WHERE ru.fecha_procesado IS NOT NULL
  AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY ru.id
HAVING COUNT(*) > 1;
"""

SQL_DQ_ORDERS_WITHOUT_DETAIL = """
SELECT
    f.id AS folio_id,
    TRIM(f.orden) AS orden,
    f.id_usuario,
    f.total,
    f.cantidad,
    DATE(f.fecha_procesado) AS fecha_procesado
FROM folios f
LEFT JOIN registro_usuario ru
    ON TRIM(ru.orden) = TRIM(f.orden)
   AND ru.fecha_procesado IS NOT NULL
   AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
WHERE f.orden IS NOT NULL
  AND TRIM(f.orden) <> ''
  AND f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
  AND ru.id IS NULL;
"""

SQL_DQ_DETAIL_WITHOUT_ORDER_HEADER = """
SELECT
    TRIM(ru.orden) AS orden,
    ru.id_usuario,
    COUNT(*) AS total_lineas
FROM registro_usuario ru
LEFT JOIN folios f
    ON TRIM(f.orden) = TRIM(ru.orden)
   AND f.fecha_procesado IS NOT NULL
   AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
WHERE ru.orden IS NOT NULL
  AND TRIM(ru.orden) <> ''
  AND ru.fecha_procesado IS NOT NULL
  AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
  AND f.id IS NULL
GROUP BY TRIM(ru.orden), ru.id_usuario;
"""

SQL_DQ_ORDER_QUANTITY_MISMATCH = """
SELECT
    TRIM(f.orden) AS orden,
    f.cantidad AS cantidad_folio,
    COALESCE(SUM(ru.cantidad), 0) AS cantidad_detalle,
    (f.cantidad - COALESCE(SUM(ru.cantidad), 0)) AS diferencia
FROM folios f
LEFT JOIN registro_usuario ru
    ON TRIM(ru.orden) = TRIM(f.orden)
   AND ru.fecha_procesado IS NOT NULL
   AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
WHERE f.orden IS NOT NULL
  AND TRIM(f.orden) <> ''
  AND f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY TRIM(f.orden), f.cantidad
HAVING f.cantidad <> COALESCE(SUM(ru.cantidad), 0);
"""

#revisar consulta muy pesada
SQL_DQ_ORDER_TOTAL_MISMATCH = """
SELECT
    TRIM(f.orden) AS orden,
    f.total AS total_folio,
    COALESCE(SUM(ru.precio * ru.cantidad), 0) AS total_detalle,
    ROUND(f.total - COALESCE(SUM(ru.precio * ru.cantidad), 0), 2) AS diferencia
FROM folios f
LEFT JOIN registro_usuario ru
    ON TRIM(ru.orden) = TRIM(f.orden)
   AND ru.fecha_procesado IS NOT NULL
   AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
WHERE f.orden IS NOT NULL
  AND TRIM(f.orden) <> ''
  AND f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY TRIM(f.orden), f.total
HAVING ABS(f.total - COALESCE(SUM(ru.precio * ru.cantidad), 0)) > 0.01;
"""


# =========================================================
# ANALITICAS BASE - ULTIMO AÑO
# =========================================================

SQL_ANALYTICS_SALES_BY_DAY = """
SELECT
    DATE(f.fecha_procesado) AS fecha,
    COUNT(DISTINCT TRIM(f.orden)) AS pedidos,
    SUM(f.total) AS ventas_totales
FROM folios f
WHERE f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY DATE(f.fecha_procesado)
ORDER BY fecha;
"""

#GENERAR DOCUMENTOS DE NEGOCIO
SQL_ANALYTICS_SALES_BY_MONTH = """
SELECT
    DATE_FORMAT(f.fecha_procesado, '%Y-%m') AS periodo,
    COUNT(DISTINCT TRIM(f.orden)) AS pedidos,
    SUM(f.total) AS ventas_totales
FROM folios f
WHERE f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY DATE_FORMAT(f.fecha_procesado, '%Y-%m')
ORDER BY periodo;
"""

#GENERAR DOCUMENTOS DE NEGOCIO
SQL_ANALYTICS_SALES_BY_CHANNEL = """
SELECT
    TRIM(UPPER(f.vendedora)) AS canal,
    COUNT(DISTINCT TRIM(f.orden)) AS pedidos,
    SUM(f.total) AS ventas_totales
FROM folios f
WHERE f.vendedora IS NOT NULL
  AND TRIM(f.vendedora) <> ''
  AND f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY TRIM(UPPER(f.vendedora))
ORDER BY ventas_totales DESC;
"""

#GENERAR DOCUMENTOS SOLO SI SE LIMITA A TOP 20 O TOP 50
SQL_ANALYTICS_TOP_PRODUCTS = """
SELECT
    ru.id_producto AS product_id,
    TRIM(ru.codigo) AS codigo,
    TRIM(ru.nombre) AS nombre,
    SUM(ru.cantidad) AS unidades_vendidas,
    SUM(ru.precio * ru.cantidad) AS monto_vendido
FROM registro_usuario ru
WHERE ru.fecha_procesado IS NOT NULL
  AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY ru.id_producto, TRIM(ru.codigo), TRIM(ru.nombre)
ORDER BY unidades_vendidas DESC;
"""

#GENERAR DOCUMENTOS SOLO SI SE LIMITA A TOP 20 O TOP 50
SQL_ANALYTICS_TOP_CLIENTS = """
SELECT
    u.id AS client_id,
    TRIM(CONCAT(COALESCE(u.nombre, ''), ' ', COALESCE(u.apellido, ''))) AS cliente,
    COUNT(DISTINCT TRIM(f.orden)) AS total_pedidos,
    SUM(f.total) AS total_comprado
FROM folios f
JOIN usuario u
    ON u.id = f.id_usuario
WHERE f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY u.id, TRIM(CONCAT(COALESCE(u.nombre, ''), ' ', COALESCE(u.apellido, '')))
ORDER BY total_comprado DESC LIMIT 50;
"""

#GENERAR DOCUMENTOS DE NEGOCIO
SQL_ANALYTICS_INVENTORY_BY_STOREHOUSE = """
SELECT
    a.id_almacen,
    TRIM(a.nombre_almacen) AS nombre_almacen,
    COUNT(DISTINCT ap.id_producto) AS productos_distintos,
    SUM(ap.cantidad) AS stock_total
FROM almacenes a
LEFT JOIN almacen_producto ap
    ON ap.id_almacen = a.id_almacen
GROUP BY a.id_almacen, TRIM(a.nombre_almacen)
ORDER BY stock_total DESC;
"""


SQL_ANALYTICS_PRODUCTS_WITHOUT_SALES_LAST_YEAR = """
SELECT
    p.id AS product_id,
    TRIM(p.codigo) AS codigo,
    TRIM(p.nombre) AS nombre
FROM productos p
LEFT JOIN registro_usuario ru
    ON ru.id_producto = p.id
   AND ru.fecha_procesado IS NOT NULL
   AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
WHERE ru.id_producto IS NULL;
"""

#=========================================================
# categorias mas vendidas , data para RAG
#=========================================================
SQL_ANALYTICS_TOP_CATEGORIES = """
SELECT
    s.id_subcategoria AS subcategoria_id,
    TRIM(s.nombre_subcategoria) AS categoria,
    SUM(ru.cantidad) AS unidades_vendidas,
    ROUND(SUM(ru.precio * ru.cantidad), 2) AS monto_vendido
FROM registro_usuario ru
INNER JOIN productos p
    ON p.id = ru.id_producto
LEFT JOIN admin_subcategorias s
    ON s.id_subcategoria = p.sub_categoria
WHERE ru.fecha_procesado IS NOT NULL
  AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY
    s.id_subcategoria,
    TRIM(s.nombre_subcategoria)
ORDER BY monto_vendido DESC;
"""

# =========================================================
# TOP PRPODUCTOS MAS VENDIOS 
# =========================================================
SQL_ANALYTICS_TOP_PRODUCTS = """
SELECT
    p.id AS product_id,
    TRIM(p.codigo) AS codigo,
    TRIM(p.nombre) AS nombre,
    TRIM(s.nombre_subcategoria) AS categoria,
    SUM(ru.cantidad) AS unidades_vendidas,
    ROUND(SUM(ru.precio * ru.cantidad), 2) AS monto_vendido
FROM registro_usuario ru
INNER JOIN productos p
    ON p.id = ru.id_producto
LEFT JOIN admin_subcategorias s
    ON s.id_subcategoria = p.sub_categoria
WHERE ru.fecha_procesado IS NOT NULL
  AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY
    p.id,
    TRIM(p.codigo),
    TRIM(p.nombre),
    TRIM(s.nombre_subcategoria)
ORDER BY monto_vendido DESC LIMIT 20;
"""

# =========================================================
# TENDENCIA MENSUAL DE VENTAS
# =========================================================
SQL_ANALYTICS_MONTHLY_SALES_TREND = """
SELECT
    DATE_FORMAT(f.fecha_procesado, '%Y-%m') AS periodo,
    COUNT(DISTINCT f.orden) AS pedidos,
    ROUND(SUM(f.total), 2) AS ventas_totales,
    ROUND(AVG(f.total), 2) AS ticket_promedio
FROM folios f
WHERE f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY DATE_FORMAT(f.fecha_procesado, '%Y-%m')
ORDER BY periodo;
"""

# =========================================================
# PRODUCTOS CON BAJA ROTACION ELEGIR UN LIMIT PARA TOP 20 O TOP 50
# =========================================================
SQL_ANALYTICS_LOW_STOCK_PRODUCTS = """
SELECT
    p.id AS product_id,
    TRIM(p.codigo) AS codigo,
    TRIM(p.nombre) AS nombre,
    TRIM(s.nombre_subcategoria) AS categoria,
    COALESCE(v.unidades_vendidas_90d, 0) AS unidades_vendidas_90d,
    ROUND(COALESCE(v.monto_vendido_90d, 0), 2) AS monto_vendido_90d,
    COALESCE(i.stock_actual, 0) AS stock_actual,
    CASE
        WHEN COALESCE(v.unidades_vendidas_90d, 0) = 0 THEN 'SIN MOVIMIENTO'
        WHEN COALESCE(v.unidades_vendidas_90d, 0) BETWEEN 1 AND 10 THEN 'ROTACION MUY BAJA'
        WHEN COALESCE(v.unidades_vendidas_90d, 0) BETWEEN 11 AND 50 THEN 'ROTACION BAJA'
        ELSE 'ROTACION NORMAL/ALTA'
    END AS nivel_rotacion
FROM productos p
LEFT JOIN admin_subcategorias s
    ON s.id_subcategoria = p.sub_categoria
LEFT JOIN (
    SELECT
        ru.id_producto,
        SUM(ru.cantidad) AS unidades_vendidas_90d,
        SUM(ru.precio * ru.cantidad) AS monto_vendido_90d
    FROM registro_usuario ru
    WHERE ru.fecha_procesado IS NOT NULL
      AND DATE(ru.fecha_procesado) >= CURDATE() - INTERVAL 90 DAY
    GROUP BY ru.id_producto
) v
    ON v.id_producto = p.id
LEFT JOIN (
    SELECT
        ap.id_producto,
        SUM(ap.cantidad) AS stock_actual
    FROM almacen_producto ap
    GROUP BY ap.id_producto
) i
    ON i.id_producto = p.id
WHERE COALESCE(i.stock_actual, 0) > 0
ORDER BY unidades_vendidas_90d ASC, stock_actual DESC;
"""

# =========================================================
# PERFIL COMERCIAL DEL CLIENTE
# =========================================================
SQL_ANALYTICS_CLIENT_PROFILE = """
SELECT
    u.id AS client_id,
    TRIM(CONCAT(COALESCE(u.nombre, ''), ' ', COALESCE(u.apellido, ''))) AS cliente,
    TRIM(u.ciudad) AS ciudad,
    TRIM(u.estado) AS estado,
    COUNT(DISTINCT f.orden) AS total_pedidos_12m,
    ROUND(SUM(f.total), 2) AS total_comprado_12m,
    ROUND(AVG(f.total), 2) AS ticket_promedio,
    MAX(DATE(f.fecha_procesado)) AS ultima_compra,
    DATEDIFF(CURDATE(), MAX(DATE(f.fecha_procesado))) AS dias_desde_ultima_compra
FROM folios f
INNER JOIN usuario u
    ON u.id = f.id_usuario
WHERE f.fecha_procesado IS NOT NULL
  AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
GROUP BY
    u.id,
    TRIM(CONCAT(COALESCE(u.nombre, ''), ' ', COALESCE(u.apellido, ''))),
    TRIM(u.ciudad),
    TRIM(u.estado)
ORDER BY total_comprado_12m DESC;
"""

# =========================================================
# CLASIFICACION POR ESTADOS DE MEXICO COMPRAS 12 MESES
# =========================================================
SQL_ANALYTICS_SALES_BY_STATE = """
WITH zone_sales AS (
    SELECT
        TRIM(u.estado) AS estado,
        COUNT(DISTINCT u.id) AS clientes_activos,
        COUNT(DISTINCT f.orden) AS total_pedidos,
        SUM(f.total) AS ventas_totales,
        AVG(f.total) AS ticket_promedio,
        MAX(DATE(f.fecha_procesado)) AS ultima_compra_zona
    FROM usuario u
    INNER JOIN folios f
        ON f.id_usuario = u.id
    WHERE f.fecha_procesado IS NOT NULL
      AND DATE(f.fecha_procesado) >= CURDATE() - INTERVAL 1 YEAR
      AND u.estado IS NOT NULL
      AND TRIM(u.estado) <> ''
    GROUP BY TRIM(u.estado)
),
totals AS (
    SELECT SUM(ventas_totales) AS total_general_ventas
    FROM zone_sales
)
SELECT
    zs.estado,
    zs.clientes_activos,
    zs.total_pedidos,
    ROUND(zs.ventas_totales, 2) AS ventas_totales,
    ROUND(zs.ticket_promedio, 2) AS ticket_promedio,
    zs.ultima_compra_zona,
    ROUND((zs.ventas_totales / t.total_general_ventas) * 100, 2) AS participacion_ventas_pct,
    CASE
        WHEN zs.clientes_activos >= 300 THEN 'ALTA CONCENTRACION'
        WHEN zs.clientes_activos BETWEEN 100 AND 299 THEN 'CONCENTRACION MEDIA'
        ELSE 'BAJA CONCENTRACION'
    END AS nivel_concentracion
FROM zone_sales zs
CROSS JOIN totals t
ORDER BY zs.clientes_activos DESC, zs.ventas_totales DESC;
"""


# =========================================================
# DICCIONARIOS
# =========================================================

SOURCE_QUERIES = {
    "dim_client": SQL_DIM_CLIENT_SOURCE,
    "dim_subcategory": SQL_DIM_SUBCATEGORY_SOURCE,
    "dim_storehouse": SQL_DIM_STOREHOUSE_SOURCE,
    "dim_channel": SQL_DIM_CHANNEL_SOURCE,
    "dim_date": SQL_DIM_DATE_SOURCE,
    "dim_product": SQL_DIM_PRODUCT_SOURCE,
    "fact_order": SQL_FACT_ORDER_SOURCE,
    "fact_order_detail": SQL_FACT_ORDER_DETAIL_SOURCE,
    "fact_inventory_snapshot": SQL_FACT_INVENTORY_SNAPSHOT_SOURCE,
}

ENRICHED_SOURCE_QUERIES = {
    "fact_order_enriched": SQL_FACT_ORDER_ENRICHED_SOURCE,
    "fact_order_detail_enriched": SQL_FACT_ORDER_DETAIL_ENRICHED_SOURCE,
    "fact_inventory_enriched": SQL_FACT_INVENTORY_ENRICHED_SOURCE,
}

QUALITY_QUERIES = {
    "duplicate_orders": SQL_DQ_DUPLICATE_ORDERS,
    "duplicate_order_detail_ids": SQL_DQ_DUPLICATE_ORDER_DETAIL_IDS,
    "orders_without_detail": SQL_DQ_ORDERS_WITHOUT_DETAIL,
    "detail_without_order_header": SQL_DQ_DETAIL_WITHOUT_ORDER_HEADER,
    "order_quantity_mismatch": SQL_DQ_ORDER_QUANTITY_MISMATCH,
    "order_total_mismatch": SQL_DQ_ORDER_TOTAL_MISMATCH,
}

ANALYTICS_QUERIES = {
    "sales_by_day": SQL_ANALYTICS_SALES_BY_DAY,
    "sales_by_month": SQL_ANALYTICS_SALES_BY_MONTH,
    "sales_by_channel": SQL_ANALYTICS_SALES_BY_CHANNEL,
    "top_products": SQL_ANALYTICS_TOP_PRODUCTS,
    "top_clients": SQL_ANALYTICS_TOP_CLIENTS,
    "inventory_by_storehouse": SQL_ANALYTICS_INVENTORY_BY_STOREHOUSE,
    "products_without_sales_last_year": SQL_ANALYTICS_PRODUCTS_WITHOUT_SALES_LAST_YEAR,
}