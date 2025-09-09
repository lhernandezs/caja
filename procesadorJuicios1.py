import os.path
import numpy as np
import pandas as pd

from entradaHelper              import getDataFrame
from salidaHelper               import write_process_file, color_rows
from procesadorJuiciosHelper    import getCompetenciasNoTecnicas, getInstructorEnReporte, getLimite_rap_para_normalizar
from config                     import ESTADOS, HOJAS, COLUMNAS_INT_DATOS, COLUMNAS_NOVEDADES, COLUMNAS_ACTIVOS, COLUMNAS_INSTRUCTORES

class ProcesadorJuicios1:
    def __init__(self, folder: str, archivo: str, datos: dict = None):
        self.folder                 = folder
        self.archivo                = archivo
        if datos:
            import io
            self.df_novedades           = pd.read_json(io.StringIO(datos['df_novedades']))
            self.df_activos             = pd.read_json(io.StringIO(datos['df_activos']))
            self.df_instructores        = pd.read_json(io.StringIO(datos['df_instructores']))
        else:
            self.df_novedades           = None
            self.df_activos             = None
            self.df_instructores        = None

    def build_df_datos(self, codigo_programa, version_programa, ficha, df_hoja):
        # 1. creamos los dataframes novedades, activos, instructores de la ficha
        df_novedades_ficha      = None
        df_activos_ficha        = None
        df_instructores_ficha   = None
        if self.df_novedades is not None:
            d = {col: [] for col in COLUMNAS_NOVEDADES}
            for _, serie in self.df_novedades.iterrows():
                if serie.iloc[2] == ficha:
                    for idx, col in enumerate(COLUMNAS_NOVEDADES):
                        d[col].append(serie.iloc[idx])
            df_novedades_ficha      = pd.DataFrame(d)

        if self.df_activos is not None:
            d = {col: [] for col in COLUMNAS_ACTIVOS}
            for _, serie in self.df_activos.iterrows():
                if serie.iloc[2] == ficha:
                    for idx, col in enumerate(COLUMNAS_ACTIVOS):
                        d[col].append(serie.iloc[idx])
            df_activos_ficha      = pd.DataFrame(d)

        if self.df_instructores is not None:
            d = {col: [] for col in COLUMNAS_INSTRUCTORES}
            for _, serie in self.df_instructores.iterrows():
                if serie.iloc[1] == ficha:
                    for idx, col in enumerate(COLUMNAS_INSTRUCTORES):
                        d[col].append(serie.iloc[idx])
            df_instructores_ficha      = pd.DataFrame(d)

        # 2. creamos el dataframe df_datos a partir del dataframe hoja
        columnas_a_copiar = HOJAS['datos']['columnas'][:5]
        nuevas_columnas   = {v: None for v in HOJAS['datos']['columnas'][5:25]}
        df_datos          = df_hoja[columnas_a_copiar].copy() 
        df_datos          = df_datos[12:]
        df_datos.drop_duplicates(inplace=True)
        df_datos          = df_datos.assign( **nuevas_columnas ) 
        df_datos[COLUMNAS_INT_DATOS] = df_datos[COLUMNAS_INT_DATOS].astype('Int64')

        # 3. recorremos el dataframe df_datos y asignamos los valores de las nuevas columnas
        competencias_no_tecnicas = getCompetenciasNoTecnicas(codigo_programa, version_programa)
        for i in df_datos.index: 
            documento = df_datos["documento"][i]
            raps_aprobados      = df_hoja.query('documento == @documento and juicio == "APROBADO"').shape[0]
            raps_por_evaluar    = df_hoja.query('documento == @documento and juicio == "POR EVALUAR"').shape[0]
            raps_no_aprobados   = df_hoja.query('documento == @documento and juicio == "NO APROBADO"').shape[0]
            if raps_aprobados > 0:
                df_datos.loc[i, "aprobado"]    = raps_aprobados
            if raps_por_evaluar > 0:
                df_datos.loc[i, "porEvaluar"]  = raps_por_evaluar
            if raps_no_aprobados > 0:
                df_datos.loc[i, "noAprobado"]  = raps_no_aprobados

            df_por_evaluar = df_hoja.query('juicio == "POR EVALUAR" and documento == @documento')
            estado = df_datos["estado"][i]
            indice_estado = next((i for i, value in enumerate(ESTADOS.values()) if value[0] == estado), None)
            df_datos.loc[i, "orden"]     = (indice_estado + 2) * 1000 +  len(df_por_evaluar)
           
            if df_activos_ficha is not None and documento in df_activos_ficha["documento"].values:
                df_datos.at[i, "activo"] = "ACTIVO"

            if df_novedades_ficha is not None and documento in df_novedades_ficha["documento"].values:
                df_filtrado  = df_novedades_ficha [df_novedades_ficha["documento"] == documento]
                df_datos.loc[i, "enTramite"] = df_filtrado["novedad"].iloc[-1]

            if df_datos["estado"][i] == "EN FORMACION":
                contador_todas = 0
                for competencia in competencias_no_tecnicas:
                    contador = df_por_evaluar["competencia"].str.startswith(competencia[1]).sum()
                    if contador > 0:
                        df_datos.at[i, competencia[0]] = contador
                        contador_todas += contador
                raps_tecnicos = len(df_por_evaluar) - contador_todas
                if raps_tecnicos > 0:
                    df_datos.loc[i, "TEC"] = len(df_por_evaluar) - contador_todas

        # Asignar el color a cada fila usando la función color_rows
        for index, row in df_datos.iterrows():
            list_color = color_rows(row, getLimite_rap_para_normalizar(df_datos))
            df_datos.at[index, "color"] = list_color[0].replace("background-color: ", "")

        # 4. creamos un dataframe con los nombres y fecha del ultimo juicio de los instructores de cada competencia sacados de datos o del reporte
        df_instructores         = pd.DataFrame([np.nan] * len(df_datos.columns)).transpose()
        df_fechas               = pd.DataFrame([np.nan] * len(df_datos.columns)).transpose()
        df_instructores.columns = df_datos.columns
        df_fechas.columns       = df_datos.columns        
        df_instructores['orden']= 1000
        df_fechas['orden']      = 2000
        for competencia in [c[0] for c in competencias_no_tecnicas] + ['TEC']:
            instructor = None
            if df_instructores_ficha is not None:
                df_instructor_ficha : pd.DataFrame = df_instructores_ficha[df_instructores_ficha['competencia'] == competencia]
                if not df_instructor_ficha.empty:
                    instructor = df_instructor_ficha.iloc[-1]['instructor']
            if instructor is None:
                instructor = getInstructorEnReporte(df_hoja, competencia, competencias_no_tecnicas)
            if instructor:
                df_jucios_instructor = df_hoja[df_hoja['funcionario'].str.upper().str.contains(instructor.upper(), na=False)]
                if not df_jucios_instructor.empty:
                    fecha_max = df_jucios_instructor['fecha'].max()
                    fecha_row = df_jucios_instructor[df_jucios_instructor['fecha'] == fecha_max].iloc[0]['fecha']
                    fecha_str = fecha_row.strftime("%d-%m\n%Y\n%H:%M")
                    df_fechas[competencia] = fecha_str
            df_instructores[competencia] = instructor

        empty_df = pd.DataFrame(columns=df_datos.columns).astype(df_datos.dtypes.to_dict())
        df_instructores = df_instructores.astype(df_datos.dtypes.to_dict(), errors='ignore')
        df_fechas = df_fechas.astype(df_datos.dtypes.to_dict(), errors='ignore')
        df_datos = pd.concat([empty_df, df_instructores, df_datos.iloc[0:]], ignore_index=True)
        df_datos = pd.concat([df_datos.iloc[:1], df_fechas, df_datos.iloc[1:]], ignore_index=True)

        return {
                'df_datos'              : df_datos             , 
                'df_novedades_ficha'    : df_novedades_ficha   , 
                'df_activos_ficha'      : df_activos_ficha     , 
                'df_hoja'               : df_hoja              ,
                'df_instructores_ficha' : df_instructores_ficha    ,
                }

    def procesar(self) -> dict:
        try:
            df_hoja = getDataFrame(self.folder, self.archivo, "Hoja")
            try:
                file_path = os.path.join(self.folder, self.archivo)
                if os.path.isfile(file_path):
                    pass
                    # os.remove(file_path)
            except Exception as e:
                raise Exception(f"Error: no es posible borrar el archivo {e}")
        except Exception as e:
            raise e

        fecha_reporte      = df_hoja.iloc[0, 2]
        programa           = df_hoja.iloc[4, 2]
        ficha              = df_hoja.iloc[1, 2] 
        codigo_programa    = df_hoja.iloc[2, 2] 
        version_programa   = df_hoja.iloc[3, 2] 
        fecha_inicio       = df_hoja.iloc[6, 2] 
        fecha_fin          = df_hoja.iloc[7, 2] 

        print(f"Ficha: {ficha} - Programa: {programa}")

        try:
            df_hoja.loc[12:, "documento"] = df_hoja.loc[12:, "documento"].astype(int)
        except ValueError:
            raise ValueError(f"Error: Hay 'documentos' del reporte de Juicios {ficha} no convertibles a número")


        result = self.build_df_datos(codigo_programa, version_programa, ficha, df_hoja)
        write_process_file(self.folder, ficha,  result['df_datos'], result['df_novedades_ficha'], result['df_activos_ficha'], result['df_hoja'])

        return {'fecha_reporte'         : fecha_reporte,
                'ficha'                 : ficha,
                'programa'              : programa,
                'codigo_programa'       : codigo_programa,
                'version_programa'      : version_programa,
                'fecha_inicio'          : fecha_inicio.strftime("%d-%m-%Y"),
                'fecha_fin'             : fecha_fin.strftime("%d-%m-%Y"),
                'df_hoja'               : result['df_hoja']                         ,
                'df_datos'              : result['df_datos']                        ,
                'df_novedades_ficha'    : result['df_novedades_ficha']              ,
                'df_activos_ficha'      : result['df_activos_ficha']                ,
                'df_instructores_ficha' : result['df_instructores_ficha']           ,
                }

if __name__ == "__main__":
    ficha = '3106275'        
    try:
        procesador_jucios = ProcesadorJuicios("upload", f"Reporte de Juicios Evaluativos {ficha}.xls", None, None, None)
        procesador_jucios.procesar()
        print(f"Archivo transformado a XLSX exitosamente para la ficha {ficha}.")
    except Exception as e:
        raise e