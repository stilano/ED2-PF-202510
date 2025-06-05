import json  # Para manejar carga de archivos JSON

def load_json_cantidad(path_json: str, column: str, n: int | None = None) -> list[int]:
    """
    Lee un JSON en formato lista de objetos y devuelve la columna `column` como lista de enteros,
    limitando a las primeras `n` entradas si n no es None.

    Parámetros:
    - path_json: Ruta al archivo JSON (p.ej., "ventas.json").
    - column: Nombre de la clave cuyo valor se extraerá (p.ej., "CANTIDAD").
    - n: Número de registros a leer. Si es None, lee todos los objetos del JSON.

    Retorno:
    - Lista de enteros con los valores de la clave especificada.
    """

    # 1. Abrimos el archivo JSON en modo lectura con codificación UTF-8
    with open(path_json, "r", encoding="utf-8") as f:
        # json.load() convierte el contenido JSON en un objeto de Python (lista de diccionarios)
        data = json.load(f)

    # 2. Si se proporcionó un límite 'n', truncamos la lista a los primeros n objetos
    if n is not None:
        data = data[:n]  # Se toman solo las primeras n entradas

    # 3. Iteramos sobre cada objeto (diccionario) en la lista y extraer el valor de la clave 'column'
    #    Se convierte dicho valor a entero con int(), y devolver la lista de esos enteros.
    return [int(item[column]) for item in data]
