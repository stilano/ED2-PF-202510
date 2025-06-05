import pandas as pd  # Para manejar operaciones con DataFrame

def load_csv_cantidad(path_csv: str, column: str, n: int | None = None) -> list[int]:
    """
    Lee las primeras `n` filas del CSV (o todas si n=None) y devuelve la columna `column`
    como lista de enteros.

    Parámetros:
    - path_csv: Ruta al archivo CSV.
    - column: Nombre de la columna a extraer (p.ej., "CANTIDAD").
    - n: Número de filas a leer. Si es None, lee todas las filas.

    Retorno:
    - Lista de enteros con los valores de la columna especificada.
    """

    # 1. Cargar solo la columna deseada del CSV.
    #    Si 'n' no es None, usamos 'nrows=n' para limitar la lectura a las primeras n filas.
    if n is not None:
        df = pd.read_csv(path_csv, usecols=[column], nrows=n)
    else:
        # Si no se especifica 'n', leemos todas las filas de la columna indicada
        df = pd.read_csv(path_csv, usecols=[column])

    # 2. Convertir la serie de pandas a entero y luego a lista de Python
    #   df[column] accede a la columna solicitada
    #   .astype(int) asegura que todos los valores sean enteros (evita decimales o cadenas)
    #   .tolist() convierte la Serie de pandas en una lista de Python
    return df[column].astype(int).tolist()
