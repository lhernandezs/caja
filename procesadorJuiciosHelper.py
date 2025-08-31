import numpy as np
import pandas as pd
from openpyxl.styles import Font
from openpyxl.styles import Alignment
from openpyxl.worksheet.worksheet import Worksheet
from dateutil.relativedelta import relativedelta
from datetime import datetime

competencias_no_tecnicas = [
    ("IND", "36182"), 
    ("BIL", "37714"), 
    ("CIE", "37801"), 
    ("COM", "37802"), 
    ("CUL", "37800"), 
    ("DER", "38558"),
    ("EMP", "38561"), 
    ("ETI", "36180"), 
    ("INV", "38199"), 
    ("MAT", "38560"), 
    ("SST", "37799"), 
    ("TIC", "37371"), 
    ("PRO", "2 - R"),
]

ancho_columnas = {'datos' :     [('A',  6), ('B', 15), ('C', 21), ('D', 21), ('E', 16), 
                                 ('F', 12), ('G', 12), ('H', 12), ('I', 15), ('J', 12),
                                 ('K',  6), ('L',  6), ('M',  6), ('N',  6), ('O',  6), 
                                 ('P',  6), ('Q',  6), ('R',  6), ('S',  6), ('T',  6), 
                                 ('U',  6), ('V',  6), ('W',  6), ('X',  6),],
                  'novedades':  [('A', 16), ('B', 42), ('C', 12), ('D', 30),],
                  'hoja':       [('A',  6), ('B', 15), ('C', 21), ('D', 21), ('E', 16), 
                                 ('F', 40), ('G', 40), ('H', 12), ('I',  0), ('J', 16),
                                 ('K', 30),]}

columnas_df_datos = ["tipo", "documento", "nombres", "apellidos", "estado", "aprobado", "porEvaluar", "noAprobado",	"enTramite", "activo",	\
                     "IND",	"BIL",	"CIE",	"COM",	"CUL",	"DER",	"EMP",	"ETI",	"INV",	"MAT",	"SST",	"TIC",	"PRO",	"TEC", "color"]

def numeroDeOrden(estado: str, porEvaluar: int) -> int:
    """
    Metodo para definir la columna de ordenación
    :return: Número de Orden.
    """
    if estado == 'EN FORMACION':
        return 1000 + porEvaluar
    elif estado == 'CANCELADO':
        return 2000 + porEvaluar
    elif estado == 'RETIRO VOLUNTARIO':
        return 3000 + porEvaluar
    else:
        return 4000 + porEvaluar

def color_rows(row):
    """
    Metodo para colorear las filas en el DataFrame.
    return: color elegido por la cantidad de celdas del row
    """
    if row["estado"] == "EN FORMACION": 
        if row["porEvaluar"] in [0, 1]:
            color = ['background-color: PaleGreen']
        elif row["porEvaluar"] in range(2, 16):
            if row["enTramite"] == None:
                color = ['background-color: LightYellow']
            else:
                color = ['background-color: Yellow']                    
        else:
            if row["enTramite"] == None:
                color = ['background-color: Red']
            else:
                color = ['background-color: DarkSalmon']
    elif row["estado"] is np.nan:
        color = ['background-color: Lavender']
    else:
        color = ['background-color: LightGray']
    return color * len(row) 



def ajustarFormatoCeldas(hoja: Worksheet, rango: int, ancho_columnas: list):
    """
    Metodo para ajustar el formato de las celdas.
    """
    font = Font(name='Arial', size=8)
    for row in hoja.iter_rows():
        for cell in row:
            cell.font = font
        for i in range(rango):
            row[i].alignment = Alignment(horizontal='center')      
    for col, width in ancho_columnas:
        hoja.column_dimensions[col].width = width

def getInstructorEnReporte(df_hoja: pd.DataFrame, competencia, competencias_no_tecnicas_ajustadas):
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
    return f"R:{' '.join([w.capitalize() for w in nombre.strip().split()])}"


def calcular_raps_tecnicos(fecha_inicio: datetime, fecha_fin: datetime, df_hoja: pd.DataFrame, competencias_no_tecnicas_ajustadas) -> int:
    """
    Calcula la cantidad de RAPs técnicos que debería llevar la ficha.
    :return: Número de RAPs técnicos esperados.
    """
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