import pandas as pd

from app                     import UPLOAD_FOLDER
from config                  import ESTADOS
from procesadorJuiciosHelper import getLimite_rap_para_normalizar

def get_df_filtrado(df: pd.DataFrame, filtro:str) -> pd.DataFrame:
    limite_rap_para_normalizar = getLimite_rap_para_normalizar(df)
    df_filtrado = df.iloc[0:0]
    if filtro == 'activo':
        df_filtrado = df[(df['activo'].notna())]
    elif filtro == 'en_tramite':
        df_filtrado = df[(df['enTramite'].notna())]
    elif filtro == 'no_aprobado':
        df_filtrado = df[(df['noAprobado'].notna())]
    elif filtro == 'para_productiva':
        df_filtrado = df[(df['porEvaluar'] == 1) & (df["PRO"] == 1)]
    elif filtro == 'error_productiva':
        df_filtrado = df[(df['porEvaluar'] == 1) & (df["PRO"] != 1)]
    elif filtro == 'para_normalizar':
        df_filtrado = df[(df['porEvaluar'] <= limite_rap_para_normalizar) & (~df['enTramite'].notna())]
    elif filtro == 'para_desertar':
        df_filtrado = df[(df['porEvaluar'] >  limite_rap_para_normalizar) & (~df['enTramite'].notna())]
    elif filtro in ESTADOS.keys():
        df_filtrado =  df[df['estado'] == ESTADOS[filtro][0]]
    return df_filtrado.reset_index(drop = True)


def get_listas_datos(df_datos: pd.DataFrame) -> dict:
    df_para_normalizar  = get_df_filtrado(df_datos, 'para_normalizar')
    df_para_desertar    = get_df_filtrado(df_datos, 'para_desertar')
    idx_tecnico         = df_datos.columns.get_loc("TEC")

    ls_instructores     = [df_datos.iloc[0, idx_tecnico]]
    ls_para_normalizar  = []
    ls_para_desertar    = []

    for index in df_para_normalizar.index:
        for col_competencia in range(10, 24):
            sufijo_competencia  = f"{df_datos.columns[col_competencia]}"
            if (df_para_normalizar.iloc[index, col_competencia] > 0) and (df_datos.columns[col_competencia] != "PRO"):
                instructor          = f"{df_datos.iloc[0, col_competencia]}"
                nombres             = f"{df_para_normalizar.iloc[index, 2]}"
                apellidos           = f"{df_para_normalizar.iloc[index, 3]}"                    
                rap_por_evaluar     = f"{df_para_normalizar.iloc[index, col_competencia]}"
                ls_para_normalizar.append([instructor, sufijo_competencia, rap_por_evaluar, nombres, apellidos])

                if instructor not in ls_instructores:
                    ls_instructores.append(instructor)

    for index in df_para_desertar.index:
        nombres             = f"{df_para_desertar.iloc[index, 2]}"
        apellidos           = f"{df_para_desertar.iloc[index, 3]}" 
        rap_por_evaluar     = f"{df_para_desertar.iloc[index, 6]}"
        ls_para_desertar.append([nombres, apellidos, rap_por_evaluar])

    return {
        'ls_instructores'       : ls_instructores,
        'ls_para_normalizar'    : ls_para_normalizar,
        'ls_para_desertar'      : ls_para_desertar,
    }

from config import EXTENSION_EXCEL_365, FILTROS
from entradaHelper import getDataFrame
if __name__ == "__main__":
    ficha = '3106275'
    try:
        df_datos = getDataFrame(UPLOAD_FOLDER, f"{ficha}.{EXTENSION_EXCEL_365}", 'datos')        
        for estado in ESTADOS.keys():
            print(f"\n\n ESTADO: {estado}")
            print(get_df_filtrado(df_datos, estado))
        for condicion in FILTROS:
            print(f"\n\n CONDICION: {condicion}")
            print(get_df_filtrado(df_datos, condicion))

    except Exception as e:
        raise ValueError(e)
