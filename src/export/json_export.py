import pandas as pd           # Para manejar datos en formato de tablas (DataFrame)
import time                   # Para medir el tiempo de ejecución
import os                     # Para interactuar con el sistema de archivos (tamaño de archivo)
import json                   # Para manejo de datos JSON (aunque pandas se encarga de la escritura)
from database.sql_connection import get_connection, get_data
# get_connection(): devuelve una conexión a la base de datos MySQL
# get_data(conn, query): ejecuta una consulta SQL y devuelve resultados como lista de tuplas

def export_json():
    """
    Extrae todos los registros de la tabla UN.VENTAS desde MySQL,
    los convierte a un DataFrame de pandas y los exporta a un archivo JSON.
    Retorna un diccionario con:
      - formato: "JSON"
      - tiempo: tiempo total de exportación (en segundos, con 4 decimales)
      - tamano_kb: tamaño del archivo JSON resultante (en KB, con 2 decimales)
    """

    # 1) Marcar el inicio para medir el tiempo total de la operación
    start = time.time()

    # 2) Conectarse a la base de datos y recuperar todos los registros de UN.VENTAS
    conn = get_connection()  # Crea/levanta la conexión MySQL
    data = get_data(conn, "SELECT * FROM UN.VENTAS")  # Ejecuta la consulta SQL
    conn.close()  # Cierra la conexión para liberar recursos

    # 3) Definir nombres de columna para el DataFrame
    columnas = [
        'ID_VENTA',        # Identificador único de la venta
        'FECHA_VENTA',     # Fecha en que se realizó la venta
        'ID_CLIENTE',      # Identificador del cliente
        'ID_EMPLEADO',     # Identificador del empleado que registró la venta
        'ID_PRODUCTO',     # Identificador del producto vendido
        'CANTIDAD',        # Cantidad de unidades vendidas
        'PRECIO_UNITARIO', # Precio por unidad en el momento de la venta
        'DESCUENTO',       # Descuento aplicado (porcentaje o valor)
        'FORMA_PAGO'       # Método de pago utilizado (p.ej. 'Efectivo', 'Tarjeta')
    ]

    # 4) Convertir la lista de tuplas 'data' en un DataFrame de pandas
    df = pd.DataFrame(data, columns=columnas)

    # 5) Definir la ruta y nombre del archivo JSON de destino
    json_path = "ventas.json"
    # Guardar el DataFrame en formato JSON:
    #  - orient="records": cada fila se convierte en un objeto JSON dentro de una lista
    #  - indent=4: agrega sangría para legibilidad
    #  - force_ascii=False: permite caracteres no ASCII en el JSON (acentos, eñes, etc.)
    df.to_json(json_path, orient="records", indent=4, force_ascii=False)

    # 6) Medir el tiempo final y calcular el tamaño del archivo en kilobytes
    end = time.time()  # Momento después de escribir el JSON
    size_kb = os.path.getsize(json_path) / 1024  # Tamaño en bytes, dividido por 1024 → KB

    # 7) Construir y retornar el diccionario con la información solicitada
    return {
        "formato": "JSON",
        "tiempo": round(end - start, 4),   # Tiempo total de exportación (s)
        "tamano_kb": round(size_kb, 2)     # Tamaño del JSON en KB
    }

