import pandas as pd
import time
import os
from database.sql_connection import get_connection, get_data

def export_json():
    start = time.time()

    conn = get_connection()
    data = get_data(conn, "SELECT * FROM UN.VENTAS")
    conn.close()

    columnas = ['ID_VENTA', 'FECHA_VENTA', 'ID_CLIENTE', 'ID_EMPLEADO',
                'ID_PRODUCTO', 'CANTIDAD', 'PRECIO_UNITARIO',
                'DESCUENTO', 'FORMA_PAGO']
    
    df = pd.DataFrame(data, columns=columnas)
    json_path = "ventas.json"
    df.to_json(json_path, orient="records", indent=4, force_ascii=False)

    end = time.time()
    size_kb = os.path.getsize(json_path) / 1024

    return {
        "formato": "JSON",
        "tiempo": round(end - start, 4),
        "tamano_kb": round(size_kb, 2)
    }