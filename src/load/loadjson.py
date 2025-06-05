import json

def load_json_cantidad(path_json: str, column: str, n: int | None = None) -> list[int]:
    """
    Lee un JSON en formato lista de objetos y devuelve la columna `column` como lista de enteros,
    limitando a las primeras `n` entradas si n no es None.
    """
    with open(path_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Si n está definido, tomar solo los primeros n objetos
    if n is not None:
        data = data[:n]
    return [int(item[column]) for item in data]