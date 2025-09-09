import os

from entradaHelper    import getDataFrame
from config                import Config, ARCHIVO_DE_DATOS

class CargadorDatos:
    def getDatos(self) -> dict:
        df_novedades = None
        df_activos = None
        df_instructores = None
        if not os.path.isfile(os.path.join(Config.UPLOAD_FOLDER_DATA, ARCHIVO_DE_DATOS)):
            raise FileNotFoundError(f"Error: No se encontró el archivo {os.path.join(Config.UPLOAD_FOLDER_DATA, ARCHIVO_DE_DATOS)}")
        else:
            try:
                df_novedades    = getDataFrame(Config.UPLOAD_FOLDER_DATA, ARCHIVO_DE_DATOS, 'novedades').drop_duplicates()
                df_activos      = getDataFrame(Config.UPLOAD_FOLDER_DATA, ARCHIVO_DE_DATOS, 'activos').drop_duplicates()
                df_instructores = getDataFrame(Config.UPLOAD_FOLDER_DATA, ARCHIVO_DE_DATOS, 'instructores').drop_duplicates()
            except Exception as e:
                raise e
            try:
                df_novedades = df_novedades.astype({"documento": "int"})
            except ValueError as e:
                print("error nov")
                raise ValueError(f"Error: algunos documentos no se pueden convertir a número en la hoja 'novedades'.")

            try:
                df_activos = df_activos.astype({"documento": "int"})
            except ValueError as e:
                print("error act")
                raise ValueError(f"Error: algunos documentos no se pueden convertir a número en la hoja 'activos'.")

        return {'df_novedades': df_novedades, 'df_activos': df_activos, 'df_instructores': df_instructores}

from procesadorJuicios import ProcesadorJuicios
from config import Config
if __name__ == "__main__":
    fichas = {
        'agosto': [
            "2879546", "2879572", "2879609", "2879610", "2879689", "2879690", "2879691", "2879692", "2879693", "2879694",
            "2879695", "2879696", "2879697", "2879698", "2879699", "2879835", "2879836", "2879837", "2879838", "2879839",
            "2879840", "2879841", "2879842", "2879843", "2879844", "2879845", "2879846", "2879847", "2879848", "2879849",
        ],
        'junio': [
            "2758190", "2758230", "2758333", "2834649", "2834650", "2834651", "2834838", "2834839", "2834840", "2834841",
            "2834842", "2834843", "2834844", "2834845", "2834846", "2834847", "2834848", "2834849", "2834850", "2834851",
            "2834852", "2834853", "2834854", "2834855", "2834856", "2989236", "3013169", "3059562", "3059847", "3064539",
            "3069982", "3069983",
        ],
        'p_productivo': [
            "2675758", "2627061", "2627205", "2675759", "2758425", "2675911", "2675744", "2627062", "2626957",
        ],
        'kebin': [
            "3106275",
        ],
        'juan carlos': [
            "3041902",
        ],

    }
    
    cargadorDatos = CargadorDatos()
    datos = cargadorDatos.getDatos()
    # datos= pd.read_pickle('diccionario_dataframes.pkl')
    df_novedades = datos['df_novedades']
    df_activos = datos['df_activos']
    df_instructores = datos['df_instructores']
    for ficha in fichas['juan carlos']: 
        try:
            juiciosFicha = ProcesadorJuicios(Config.UPLOAD_FOLDER, f"Reporte de Juicios Evaluativos {ficha}.xls", df_novedades, df_activos, df_instructores)
            juiciosFicha.procesar()
            print(f"Archivo transformado a XLSX exitosamente para la ficha {ficha}.")
        except Exception as e:
            raise ValueError(e)
