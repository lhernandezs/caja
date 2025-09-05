import pandas as pd

from dateutil.relativedelta         import relativedelta
from datetime                       import datetime

from config                         import competencias_no_tecnicas, competencias_programas_especiales, PORCENTAJE_LIMITE_RAP, HOJAS, ESTADOS

def getLimite_rap_para_normalizar(df_datos: pd.DataFrame) -> int:
    columnas_datos      = HOJAS['datos']['columnas']
    col_aprobado        = columnas_datos.index("aprobado")
    col_por_evaluar     = columnas_datos.index("porEvaluar")
    col_no_aprobado     = columnas_datos.index("noAprobado")    
    fila = 4
    raps_aprobados      = pd.to_numeric(df_datos.iloc[fila, col_aprobado], errors='coerce')
    raps_por_evaluar    = pd.to_numeric(df_datos.iloc[fila, col_por_evaluar], errors='coerce')
    raps_no_aprobados   = pd.to_numeric(df_datos.iloc[fila, col_no_aprobado], errors='coerce')
    raps_aprobados      = raps_aprobados if pd.notnull(raps_aprobados) else 0
    raps_por_evaluar    = raps_por_evaluar if pd.notnull(raps_por_evaluar) else 0
    raps_no_aprobados   = raps_no_aprobados if pd.notnull(raps_no_aprobados) else 0
    total_raps          = raps_aprobados + raps_por_evaluar + raps_no_aprobados
    return int(total_raps * PORCENTAJE_LIMITE_RAP)

def numeroDeOrden(estado: str, porEvaluar: int) -> int:
    indice_estado = next((i for i, value in enumerate(ESTADOS.values()) if value[0] == estado), None)
    return (indice_estado + 2) * 1000 + porEvaluar

def getInstructorEnReporte(df_hoja: pd.DataFrame, competencia, competencias_no_tecnicas_ajustadas) -> str:
    if competencia == 'TEC':
        codigos_competencias_trasversales = [x[1] for x in competencias_no_tecnicas_ajustadas]
        df_instructores_competencia_tecnica = df_hoja[(~df_hoja["competencia"].str.slice(0,5).isin(codigos_competencias_trasversales))]
        df_instructores_competencia = df_instructores_competencia_tecnica[df_instructores_competencia_tecnica['juicio'].isin(['APROBADO'])]
    else:
        codigo_competencia = dict(competencias_no_tecnicas_ajustadas)[competencia]
        df_instructores_competencia = df_hoja[(df_hoja["competencia"].str.slice(0,5) == codigo_competencia) & (df_hoja['juicio'].isin(['APROBADO']))]

    if df_instructores_competencia.empty:
        nombre = "SIN JUICIOS APROBADOS"
    else: 
        indice_fecha_maxima = df_instructores_competencia['fecha'].idxmax()
        nombre = df_instructores_competencia.loc[indice_fecha_maxima]['funcionario'].split('-')[1]
    return f"{' '.join([w.capitalize() for w in nombre.strip().split()])}"


def calcular_raps_tecnicos(fecha_inicio: datetime, fecha_fin: datetime, df_hoja: pd.DataFrame, competencias_no_tecnicas_ajustadas) -> int:
    if fecha_fin is None or fecha_inicio is None:
        return 0
    meses_etapa_lectiva = 21 if ((fecha_fin.year - fecha_inicio.year) * 12 + (fecha_fin.month - fecha_inicio.month)) > 21 else 9
    diferencia = relativedelta(datetime.now(), fecha_inicio)
    meses_desde_inicio = diferencia.years * 12 + diferencia.months
    porcentaje_avance = min(meses_desde_inicio / meses_etapa_lectiva, 1)
    columnas_copiar = ['competencia', 'resultado']
    df_competencias_raps = df_hoja[columnas_copiar].copy()
    df_competencias_raps = df_competencias_raps[12:]
    df_competencias_raps.drop_duplicates(inplace=True)
    lista_no_tecnicas = [x[1] for x in competencias_no_tecnicas_ajustadas]
    total_raps_no_tecnicos = df_competencias_raps[df_competencias_raps['competencia'].str.slice(0, 5).isin(lista_no_tecnicas)].shape[0]
    total_raps_tecnicos = df_competencias_raps.shape[0] - total_raps_no_tecnicos
    print(f"M Lectiva {meses_etapa_lectiva}, M desde inicio {meses_desde_inicio}, % avance {porcentaje_avance}, Raps NoT {total_raps_no_tecnicos}, Raps T {total_raps_tecnicos}")
    return int(total_raps_tecnicos * porcentaje_avance)

def getCompetenciasNoTecnicas(programa: str, version: str) -> list:
    competencias = competencias_no_tecnicas
    clave = f"{programa}, {version}"
    if clave in competencias_programas_especiales:
        for competencia, codigo in competencias_programas_especiales[clave]:
            competencias[competencia] = codigo
    return list(competencias.items())

if __name__ == "__main__":
    print(getCompetenciasNoTecnicas('631101', '2'))