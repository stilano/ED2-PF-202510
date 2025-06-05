import pandas as pd
import time
import os
from database.sql_connection import get_connection, get_data

def export_csv():
    start = time.time()

    conn = get_connection()
    data = get_data(conn, "SELECT * FROM UN.VENTAS")
    conn.close()

    columnas = ['ID_VENTA', 'FECHA_VENTA', 'ID_CLIENTE', 'ID_EMPLEADO',
                'ID_PRODUCTO', 'CANTIDAD', 'PRECIO_UNITARIO',
                'DESCUENTO', 'FORMA_PAGO']
    
    df = pd.DataFrame(data, columns=columnas) 
    csv_path = "ventas.csv"
    df.to_csv(csv_path, index=False)

    end = time.time()
    size_kb = os.path.getsize(csv_path) / 1024

    return {
        "formato": "CSV",
        "tiempo": round(end - start, 4),
        "tamano_kb": round(size_kb, 2)
    }
