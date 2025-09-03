import numpy as np
import pandas as pd

from app        import UPLOAD_FOLDER
from entradaHelper    import Entrada
from config     import ESTADOS, COLUMNAS_DATOS, PORCENTAJE_LIMITE_RAP

class FiltrosHelper():
    def procesar(self, df_datos: pd.DataFrame) -> dict:

        limite_rap_para_normalizar = int(np.ceil((df_datos.at[2, "aprobado"] + df_datos.at[2,"porEvaluar"] + df_datos.at[2,"noAprobado"]) * PORCENTAJE_LIMITE_RAP ))
        columna_tecnico            = next((k for k, v in COLUMNAS_DATOS.items() if v == "TEC"), None)
        columna_productiva         = next((k for k, v in COLUMNAS_DATOS.items() if v == "PRO"), None) -1

        df_estados = {f"df_{key}": df_datos[df_datos['estado'] == ESTADOS[key]].reset_index(drop=True) for key in ESTADOS.keys()}

        df_induccion        = df_estados['df_induccion']
        df_en_formacion     = df_estados['df_en_formacion']
        df_aplazado         = df_estados['df_aplazado']
        df_trasladado       = df_estados['df_trasladado']
        df_condicionado     = df_estados['df_condicionado']
        df_por_certificar   = df_estados['df_por_certificar']
        df_certificado      = df_estados['df_certificado']
        df_retiro_voluntario= df_estados['df_retiro_voluntario']
        df_cancelado        = df_estados['df_cancelado']
        df_reintegrado      = df_estados['df_reintegrado']

        df_activo           = df_en_formacion[(df_en_formacion['activo'] == "ACTIVO")].reset_index(drop = True)
        df_por_evaluar      = df_en_formacion[(pd.to_numeric(df_en_formacion['porEvaluar'], errors='coerce') > 1)].reset_index(drop = True)
        df_en_tramite       = df_en_formacion[(df_en_formacion['enTramite'].notna())].reset_index(drop = True)
        df_para_productiva  = df_en_formacion[(pd.to_numeric(df_en_formacion['porEvaluar'], errors='coerce') == 1) &
                                              (df_en_formacion.iloc[:, columna_productiva] == 1)].reset_index(drop=True) 
        df_error_productiva = df_en_formacion[(pd.to_numeric(df_en_formacion['porEvaluar'], errors='coerce') == 1) &
                                              (df_en_formacion.iloc[:, columna_productiva] != 1)].reset_index(drop=True) 
        df_para_normalizar  = df_en_formacion[(pd.to_numeric(df_en_formacion['porEvaluar'], errors='coerce').between(2, limite_rap_para_normalizar - 1))].reset_index(drop=True)
        df_para_desertar    = df_en_formacion[(pd.to_numeric(df_en_formacion['porEvaluar'], errors='coerce') > limite_rap_para_normalizar) &
                                              (df_en_formacion['enTramite'].isin([np.nan])) ].reset_index(drop = True)

        instructores       = [df_datos.iloc[0, columna_tecnico]]
        para_normalizar = []
        para_desertar   = []

        for index in df_para_normalizar.index:
            for col_competencia in range(10, 24):
                sufijo_competencia  = f"{df_datos.columns[col_competencia]}"
                if (df_para_normalizar.iloc[index, col_competencia] > 0) and (df_datos.columns[col_competencia] != "PRO"):
                    instructor          = f"{df_datos.iloc[0, col_competencia]}"
                    nombres             = f"{df_para_normalizar.iloc[index, 2]}"
                    apellidos           = f"{df_para_normalizar.iloc[index, 3]}"                    
                    rap_por_evaluar     = f"{df_para_normalizar.iloc[index, col_competencia]}"
                    para_normalizar.append([instructor, sufijo_competencia, rap_por_evaluar, nombres, apellidos])

                    if instructor not in instructores:
                        instructores.append(instructor)

        for index in df_para_desertar.index:
            nombres             = f"{df_para_desertar.iloc[index, 2]}"
            apellidos           = f"{df_para_desertar.iloc[index, 3]}" 
            rap_por_evaluar     = f"{df_para_desertar.iloc[index, 6]}"
            para_desertar.append([nombres, apellidos, rap_por_evaluar])

        return {
            'df_induccion'          : df_induccion,
            'df_en_formacion'       : df_en_formacion,
            'df_aplazado'           : df_aplazado,
            'df_trasladado'         : df_trasladado,
            'df_condicionado'       : df_condicionado,
            'df_por_certificar'     : df_por_certificar,
            'df_certificado'        : df_certificado,
            'df_retiro_voluntario'  : df_retiro_voluntario,
            'df_cancelado'          : df_cancelado,
            'df_reintegrado'        : df_reintegrado,
            'df_activo'             : df_activo,
            'df_por_evaluar'        : df_por_evaluar,            
            'df_en_tramite'         : df_en_tramite,            
            'df_para_productiva'    : df_para_productiva,
            'df_error_productiva'   : df_error_productiva,
            'df_para_normalizar'     : df_para_normalizar,            
            'df_para_desertar'      : df_para_desertar,
            'instructores'          : instructores,
            'para_normalizar'       : para_normalizar,
            'para_desertar'         : para_desertar,
        }
    
if __name__ == "__main__":
    ficha = '3106275'
    try:
        df_datos: pd.DataFrame = Entrada().getDataFrame(UPLOAD_FOLDER, f"{ficha}.xlsx", "Datos", list(COLUMNAS_DATOS.values()))        
        FiltrosHelper = FiltrosHelper()
        resultados = FiltrosHelper.procesar(df_datos)
        # var = ESTADOS['activo']
        var = 'para_desertar'
        df_name = f"df_{var.lower().replace(' ', '_')}"
        print(f"df: {var}  {df_name}  {len(resultados[df_name])}")
        print(resultados[df_name])
            # for item in value:
            #     linea += f"{item:30} "
            # print(linea)
    except Exception as e:
        raise ValueError(e)
