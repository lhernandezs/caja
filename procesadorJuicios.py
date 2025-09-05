import os.path
import numpy as np
import pandas as pd

from entradaHelper              import getDataFrame
from salidaHelper               import write_process_file, color_rows
from procesadorJuiciosHelper    import getCompetenciasNoTecnicas, numeroDeOrden, getInstructorEnReporte, getLimite_rap_para_normalizar
from config                     import HOJAS, COLUMNAS_INT_DATOS

class ProcesadorJuicios:
    def __init__(self, folder: str, archivo: str, novedades: pd.DataFrame = None, activos: pd.DataFrame = None, instructores: pd.DataFrame = None):
        self.folder                 = folder
        self.archivo                = archivo
        self.df_novedades           = novedades
        self.df_activos             = activos
        self.df_instructores        = instructores

        self.ficha                  : str = None
        self.codigo_programa        : str = None
        self.version_programa       : str = None
        self.fecha_inicio           : pd.Timestamp = None
        self.fecha_fin              : pd.Timestamp = None

        self.df_hoja                : pd.DataFrame = None
        self.df_datos               : pd.DataFrame = None
        self.df_novedades_ficha     : pd.DataFrame = None
        self.df_activos_ficha       : pd.DataFrame = None
        self.df_instructores_ficha  : pd.DataFrame = None

    def build_df_datos(self):
        # 1. creamos los dataframes novedades, acitvos, instructores de la ficha
        if self.df_novedades is not None:
            self.df_novedades_ficha     = self.df_novedades.query("ficha == @self.ficha")
        if self.df_activos is not None:
            self.df_activos_ficha       = self.df_activos.query("ficha == @self.ficha")
        if self.df_instructores is not None:
            self.df_instructores_ficha  = self.df_instructores.query("ficha == @self.ficha")

        # 2. creamos el dataframe self.df_datos a partir del dataframe hoja
        columnas_a_copiar = HOJAS['datos']['columnas'][:5]
        nuevas_columnas = {v: None for v in HOJAS['datos']['columnas'][5:25]}
        self.df_datos = self.df_hoja[columnas_a_copiar].copy() 
        self.df_datos = self.df_datos[12:]
        self.df_datos.drop_duplicates(inplace=True)
        self.df_datos = self.df_datos.assign( **nuevas_columnas ) 
        self.df_datos[COLUMNAS_INT_DATOS] = self.df_datos[COLUMNAS_INT_DATOS].astype('Int64')

        # 3. recorremos el dataframe df_datos y asignamos los valores de las nuevas columnas
        competencias_no_tecnicas = getCompetenciasNoTecnicas(self.codigo_programa, self.version_programa)
        for i in self.df_datos.index: 
            documento = self.df_datos["documento"][i]
            raps_aprobados      = self.df_hoja.query('documento == @documento and juicio == "APROBADO"').shape[0]
            raps_por_evaluar    = self.df_hoja.query('documento == @documento and juicio == "POR EVALUAR"').shape[0]
            raps_no_aprobados   = self.df_hoja.query('documento == @documento and juicio == "NO APROBADO"').shape[0]

            self.df_datos.loc[i, "aprobado"]    = raps_aprobados
            self.df_datos.loc[i, "porEvaluar"]  = raps_por_evaluar
            self.df_datos.loc[i, "noAprobado"]  = raps_no_aprobados

            df_por_evaluar = self.df_hoja.query('juicio == "POR EVALUAR" and documento == @documento')
            self.df_datos.loc[i, "orden"]       = numeroDeOrden(self.df_datos["estado"][i], len(df_por_evaluar))
           
            if self.df_activos_ficha is not None and documento in self.df_activos_ficha["documento"].values:
                self.df_datos.at[i, "activo"] = "ACTIVO"

            if self.df_novedades_ficha is not None and documento in self.df_novedades_ficha["documento"].values:
                df_filtrado  = self.df_novedades_ficha [self.df_novedades_ficha["documento"] == documento]
                self.df_datos.loc[i, "enTramite"] = df_filtrado["novedad"].iloc[-1]


            if self.df_datos["estado"][i] == "EN FORMACION":
                contador_todas = 0
                for competencia in competencias_no_tecnicas:
                    contador = df_por_evaluar["competencia"].str.startswith(competencia[1]).sum()
                    if contador > 0:
                        self.df_datos.at[i, competencia[0]] = contador
                        contador_todas += contador
                self.df_datos.loc[i, "TEC"] = len(df_por_evaluar) - contador_todas

        # Asignar el color a cada fila usando la función color_rows
        for index, row in self.df_datos.iterrows():
            list_color = color_rows(row, getLimite_rap_para_normalizar(self.df_datos))
            self.df_datos.at[index, "color"] = list_color[0].replace("background-color: ", "")

        # 4. creamos un dataframe con los nombres y fecha del ultimo juicio de los instructores de cada competencia sacados de datos o del reporte
        df_instructores         = pd.DataFrame([np.nan] * len(self.df_datos.columns)).transpose()
        df_fechas               = pd.DataFrame([np.nan] * len(self.df_datos.columns)).transpose()
        df_instructores.columns = self.df_datos.columns
        df_fechas.columns       = self.df_datos.columns        
        df_instructores['orden']= 1000
        df_fechas['orden']      = 2000
        for competencia in [c[0] for c in competencias_no_tecnicas] + ['TEC']:
            instructor = None
            if self.df_instructores_ficha is not None:
                df_instructor_ficha : pd.DataFrame = self.df_instructores_ficha[self.df_instructores_ficha['competencia'] == competencia]
                if not df_instructor_ficha.empty:
                    instructor = df_instructor_ficha.iloc[-1]['instructor']
            if instructor is None:
                instructor = getInstructorEnReporte(self.df_hoja, competencia, competencias_no_tecnicas)
            if instructor:
                df_jucios_instructor = self.df_hoja[self.df_hoja['funcionario'].str.upper().str.contains(instructor.upper(), na=False)]
                if not df_jucios_instructor.empty:
                    fecha_max = df_jucios_instructor['fecha'].max()
                    fecha_row = df_jucios_instructor[df_jucios_instructor['fecha'] == fecha_max].iloc[0]['fecha']
                    fecha_str = fecha_row.strftime("%d-%m\n%Y\n%H:%M")
                    df_fechas[competencia] = fecha_str
            df_instructores[competencia] = instructor

        empty_df = pd.DataFrame(columns=self.df_datos.columns).astype(self.df_datos.dtypes.to_dict())
        df_instructores = df_instructores.astype(self.df_datos.dtypes.to_dict(), errors='ignore')
        df_fechas = df_fechas.astype(self.df_datos.dtypes.to_dict(), errors='ignore')
        self.df_datos = pd.concat([empty_df, df_instructores, self.df_datos.iloc[0:]], ignore_index=True)
        self.df_datos = pd.concat([self.df_datos.iloc[:1], df_fechas, self.df_datos.iloc[1:]], ignore_index=True)


    def procesar(self) -> dict:
        try:
            self.df_hoja = getDataFrame(self.folder, self.archivo, "Hoja")
            try:
                file_path = os.path.join(self.folder, self.archivo)
                if os.path.isfile(file_path):
                    pass
                    # os.remove(file_path)
            except Exception as e:
                raise Exception(f"Error: no es posible borrar el archivo {e}")
        except Exception as e:
            raise e

        fecha_reporte           = self.df_hoja.iloc[0, 2]
        programa                = self.df_hoja.iloc[4, 2]
        self.ficha              = self.df_hoja.iloc[1, 2] 
        self.codigo_programa    = self.df_hoja.iloc[2, 2] 
        self.version_programa   = self.df_hoja.iloc[3, 2] 
        self.fecha_inicio       = self.df_hoja.iloc[6, 2] 
        self.fecha_fin          = self.df_hoja.iloc[7, 2] 

        print(f"Ficha: {self.ficha} - Programa: {programa}")

        try:
            self.df_hoja.loc[12:, "documento"] = self.df_hoja.loc[12:, "documento"].astype(int)
        except ValueError:
            raise ValueError(f"Error: Hay 'documentos' del reporte de Juicios {ficha} no convertibles a número")

        self.build_df_datos()
        write_process_file(self.folder, self.ficha, self.df_datos, self.df_novedades_ficha, self.df_activos_ficha, self.df_hoja)

        return {'fecha_reporte'         : fecha_reporte,
                'ficha'                 : self.ficha,
                'programa'              : programa,
                'codigo_programa'       : self.codigo_programa,
                'version_programa'      : self.version_programa,
                'fecha_inicio'          : self.fecha_inicio.strftime("%d-%m-%Y"),
                'fecha_fin'             : self.fecha_fin.strftime("%d-%m-%Y"),
                'df_hoja'               : self.df_hoja,
                'df_datos'              : self.df_datos,
                'df_activos_ficha'      : self.df_activos_ficha,
                'df_novedades_ficha'    : self.df_novedades_ficha,
                'df_instructores_ficha' : self.df_instructores_ficha
                }

if __name__ == "__main__":
    ficha = '2879698'        
    try:
        procesador_jucios = ProcesadorJuicios("upload", f"Reporte de Juicios Evaluativos {ficha}.xls", None, None, None)
        procesador_jucios.procesar()
        print(f"Archivo transformado a XLSX exitosamente para la ficha {ficha}.")
    except Exception as e:
        raise e