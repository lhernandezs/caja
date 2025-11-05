import os.path
import pandas as pd

def getDataFrame(folder: str, file: str, sheet: str) -> pd.DataFrame:
    try:
        df : pd.DataFrame = pd.read_excel(os.path.join(folder, file), sheet_name=sheet)
        df.columns = HOJAS[sheet]['columnas'][:df.shape[1]]
        return df
    except Exception as e:
        raise ValueError(f"Error: imposible leer el archivo {file}. {e}")

from config import ARCHIVO_DE_DATOS, HOJAS
from config import Config
if __name__ == "__main__":
    def _print_sheet_count(sheet: str):
        try:
            df = getDataFrame(Config.UPLOAD_FOLDER_DATA, ARCHIVO_DE_DATOS, sheet)
            print(f"El número de {sheet} en {ARCHIVO_DE_DATOS} es: {len(df)}")
        except Exception as e:
            print(f"Error leyendo la hoja '{sheet}': {e}")

    sheets = ['novedades', 'activos', 'instructores']
    for sheet in sheets:
        _print_sheet_count(sheet)      