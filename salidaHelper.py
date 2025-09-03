
import os
import numpy as np
import pandas as pd

from openpyxl.styles                import Font
from openpyxl.styles                import Alignment
from openpyxl.worksheet.worksheet   import Worksheet

from config                         import ancho_columnas

def color_rows(row) -> list:
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

def ajustarFormatoCeldas(hoja: Worksheet, ancho_columnas: list):
    font = Font(name='Arial', size=8)
    for row in hoja.iter_rows():
        for cell in row:
            cell.font = font
        for i in range(len(ancho_columnas)):
            row[i].alignment = Alignment(horizontal='center')      
    for col, width in ancho_columnas:
        hoja.column_dimensions[col].width = width

def write_process_file(folder: str, ficha: str, df_datos: pd.DataFrame, df_novedades_ficha: pd.DataFrame, df_activos_ficha: pd.DataFrame, df_hoja: pd.DataFrame):
    nuevo_nombre = f"{ficha}.xlsx"
    try:
        with pd.ExcelWriter(os.path.join(folder, nuevo_nombre), engine="openpyxl") as writer:
            df_datos.sort_values(by="orden").style.apply(color_rows, axis=1).to_excel(writer, sheet_name="Datos", index=False)  
            workbook = writer.book
            worksheet = workbook['Datos']
            worksheet.delete_cols(26)
            worksheet.delete_cols(25)
            ajustarFormatoCeldas(worksheet, ancho_columnas['datos'])
            # ajustar la fila de nombres de los instructores
            row_dimension_2 = worksheet.row_dimensions[2]
            row_dimension_2.height = 60
            row_dimension_3 = worksheet.row_dimensions[3]
            row_dimension_3.height = 60 
            for cell in worksheet[2]:
                cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')                   
            for cell in worksheet[3]:
                cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')                   

            if not df_novedades_ficha is None:
                df_novedades_ficha.to_excel( writer, sheet_name="Novedades", index=False)
                ajustarFormatoCeldas(workbook['Novedades'], ancho_columnas['novedades'])

            if not df_activos_ficha is None:
                df_activos_ficha.to_excel(writer, sheet_name="Activos", index=False)
                ajustarFormatoCeldas(workbook['Activos'], ancho_columnas['novedades'])

            df_hoja.to_excel( writer, sheet_name="Hoja", index=False)
            ajustarFormatoCeldas(workbook['Hoja'], ancho_columnas['hoja'])
            worksheet = workbook['Hoja']
            for fila in range(2,13):
                worksheet.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=2)
                worksheet.cell(row=fila, column=1).alignment
            for fila in range(2,13):
                worksheet.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=2)
                worksheet.cell(row=fila, column=1).alignment = Alignment(horizontal='left', vertical='center')
                worksheet.cell(row=fila, column=3).alignment = Alignment(horizontal='left', vertical='center')
            for row in worksheet.iter_rows():
                row[5].alignment = Alignment(horizontal='left')  
                row[6].alignment = Alignment(horizontal='left')
            for col in range(1,12):
                worksheet.cell(1, col).value = None
            worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=11)
            worksheet.cell(1,1).value = "Reporte de Juicios"
            worksheet.cell(1,1).font = Font(name='Arial', size=20)  

    except Exception as e:
        raise Exception(f"Error: no es posible guardar el archivo: {e}")
