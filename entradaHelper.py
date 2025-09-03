import os.path
import pandas as pd

def getDataFrame(folder: str, file: str, sheet: str, columns: list) -> pd.DataFrame:
    try:
        df : pd.DataFrame = pd.read_excel(os.path.join(folder, file), sheet_name=sheet)
        df.columns = columns
        return df
    except Exception as e:
        raise ValueError(f"Error: imposible leer el archivo {file}. {e}")

if __name__ == "__main__":
    datos = getDataFrame("data", "datos.xlsx", "novedades", ["documento","nombre","ficha", "novedad"])
    print(f"El número de novedades en datos.xlsx es: {len(datos)}")
