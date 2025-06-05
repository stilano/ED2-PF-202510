import pandas as pd

def load_csv_cantidad(path_csv: str, column: str, n: int | None = None) -> list[int]:
    """
    Lee las primeras `n` filas del CSV (o todas si n=None) y devuelve la columna `column` como lista de enteros.
    """
    if n is not None:
        df = pd.read_csv(path_csv, usecols=[column], nrows=n)
    else:
        df = pd.read_csv(path_csv, usecols=[column])
    return df[column].astype(int).tolist()