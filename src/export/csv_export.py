import pandas as pd           # Para manejar datos en formato de tablas (DataFrame)
import time                   # Para medir el tiempo de ejecución
import os                     # Para interactuar con el sistema de archivos (tamaño de archivo)
from database.sql_connection import get_connection, get_data
# get_connection(): devuelve una conexión a la base de datos MySQL a partir de las credenciales
# get_data(conn, query): ejecuta una consulta SQL y devuelve los resultados como lista de tuplas

def export_csv():
    """
    Extrae todos los registros de la tabla UN.VENTAS desde MySQL,
    los convierte en DataFrame de pandas y los exporta a un archivo CSV.
    Retorna un diccionario con:
      - formato: "CSV"
      - tiempo: tiempo total de exportación (en segundos, con 4 decimales)
      - tamano_kb: tamaño del archivo CSV resultante (en KB, con 2 decimales)
    """

    # 1. Marcamos inicio para medir tiempo total
    start = time.time()

    # 2. Nos conectamos  a la base de datos y obtenemos todos los registros de UN.VENTAS
    conn = get_connection()  # Crea/levanta la conexión MySQL
    data = get_data(conn, "SELECT * FROM UN.VENTAS")  # Ejecuta la consulta SQL
    conn.close()  # Cierra la conexión para liberar recursos

    # 3. Definir los nombres de las columnas que devolverá la consulta
    columnas = [
        'ID_VENTA',        # Identificador único de la venta
        'FECHA_VENTA',     # Fecha en que se realizó la venta
        'ID_CLIENTE',      # Identificador del cliente
        'ID_EMPLEADO',     # Identificador del empleado que procesó la venta
        'ID_PRODUCTO',     # Identificador del producto vendido
        'CANTIDAD',        # Cantidad de unidades vendidas
        'PRECIO_UNITARIO', # Precio por unidad al momento de la venta
        'DESCUENTO',       # Descuento aplicado (porcentaje o valor)
        'FORMA_PAGO'       # Método de pago utilizado (p.ej., 'Efectivo', 'Tarjeta')
    ]

    # 4. Convertimos los datos (lista de tuplas) en un DataFrame de pandas
    df = pd.DataFrame(data, columns=columnas)

    # 5. Definimos la ruta y nombre del archivo CSV de destino
    csv_path = "ventas.csv"
    # Guardamos el DataFrame en formato CSV, sin incluir índice de pandas
    df.to_csv(csv_path, index=False)

    # 6. Se mide tiempo final y se calcula el tamaño del archivo en kilobytes
    end = time.time()  # Marca el momento después de guardar el CSV
    size_kb = os.path.getsize(csv_path) / 1024  # Tamaño en bytes, dividido por 1024 → KB

    # 7. Construir y retornar el diccionario con la información solicitada
    return {
        "formato": "CSV",
        "tiempo": round(end - start, 4),    # Tiempo total de exportación (s)
        "tamano_kb": round(size_kb, 2)      # Tamaño del CSV en KB
    }
