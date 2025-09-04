import os.path
import pandas as pd

def getDataFrame(folder: str, file: str, sheet: str) -> pd.DataFrame:
    try:
        df : pd.DataFrame = pd.read_excel(os.path.join(folder, file), sheet_name=sheet)
        df.columns = HOJAS[sheet]['columnas']
        return df
    except Exception as e:
        raise ValueError(f"Error: imposible leer el archivo {file}. {e}")

from config import ARCHIVO_DE_DATOS, HOJAS
from config import Config

if __name__ == "__main__":
    datos = getDataFrame(Config.UPLOAD_FOLDER_DATA, ARCHIVO_DE_DATOS, 'novedades')
    print(f"El número de novedades en datos.xlsx es: {len(datos)}")