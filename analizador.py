import numpy as np
import pandas as pd

from app import UPLOAD_FOLDER
from config import ESTADOS
from entrada import Entrada

class Analizador():
    def procesar(self, df_datos: pd.DataFrame) -> dict:
        df_induccion      = df_datos[(df_datos['estado'] == ESTADOS['induccion'])].reset_index() 
        df_en_formacion   = df_datos[(df_datos['estado'] == ESTADOS['en_formacion'])].reset_index()
        df_aplazados      = df_datos[(df_datos['estado'] == ESTADOS['aplazado'])].reset_index()
        df_trasladados    = df_datos[(df_datos['estado'] == ESTADOS['trasladado'])].reset_index()
        df_condicionados  = df_datos[(df_datos['estado'] == ESTADOS['condicionado'])].reset_index() 
        df_por_certificar = df_datos[(df_datos['estado'] == ESTADOS['por_certificar'])].reset_index()
        df_certificados   = df_datos[(df_datos['estado'] == ESTADOS['certificado'])].reset_index()
        df_retirados      = df_datos[(df_datos['estado'] == ESTADOS['retirado'])].reset_index()
        df_cancelados     = df_datos[(df_datos['estado'] == ESTADOS['cancelado'])].reset_index()

        df_activos      = df_datos[(df_datos['activo']    == "ACTIVO")                      & 
                                   (df_datos['porEvaluar'].values > 1)].reset_index()   
        df_a_desertar   = df_datos[(df_datos['estado']    == ESTADOS['en_formacion'])       &
                                   (df_datos['activo']    != "ACTIVO")                      & 
                                   (df_datos['enTramite'].isin([np.nan])) ].reset_index()

        instructores      = [df_datos.iloc[0, 23]]
        datos_activos     = []
        datos_a_desertar  = []

        for index in df_activos.index:
            for col in range(11, 24):
                if (df_activos.iloc[index, col + 1] > 0) and (df_datos.columns[col] != "PRO"):
                    nombres = f"{df_activos.iloc[index, 3]} {df_activos.iloc[index, 4]}"
                    competencia = df_datos.columns[col]
                    rapsPorEvaluar = int(df_activos.iloc[index, col + 1])
                    instructor = df_datos.iloc[0, col]
                    datos_activos.append([nombres, competencia, rapsPorEvaluar, instructor])
                    if instructor not in instructores:
                        instructores.append(instructor)

        for index in df_a_desertar.index:
            nombres = f"{df_a_desertar.iloc[index, 3]} {df_a_desertar.iloc[index, 4]}"
            rapsPorEvaluar = int(df_a_desertar.iloc[index, 7])
            datos_a_desertar.append([nombres, rapsPorEvaluar])

        return {
            'instructores': instructores,
            'datos_activos': datos_activos,
            'datos_a_desertar': datos_a_desertar,
            'df_induccion': df_induccion,
            'df_en_formacion': df_en_formacion,
            'df_aplazados': df_aplazados,
            'df_trasladados': df_trasladados,
            'df_condicionados': df_condicionados,
            'df_por_certificar': df_por_certificar,
            'df_certificados': df_certificados,
            'df_retirados': df_retirados,
            'df_cancelados': df_cancelados
        }

if __name__ == "__main__":
    ficha = '2879694'
    columnas = ["tipo", "documento", "nombres", "apellidos", "estado", "aprobado", "porEvaluar", "noAprobado", "enTramite", "activo", \
                          "IND", "BIL", "CIE", "COM", "CUL", "DER", "EMP", "ETI", "INV", "MAT", "SST", "TIC", "PRO", "TEC", "color" ]    
    try:
        df_datos: pd.DataFrame = Entrada().getDataFrame(UPLOAD_FOLDER, f"{ficha}.xlsx", "Datos", columnas)        
        analizador = Analizador()
        resultados = analizador.procesar(df_datos)
        for key, value in resultados.items():
            print(f"{key}: {value}")
    except Exception as e:
        raise ValueError(e)
