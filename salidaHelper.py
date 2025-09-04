
import os
import openpyxl
import pandas as pd

from openpyxl.styles                import Font
from openpyxl.styles                import Alignment
from openpyxl.worksheet.worksheet   import Worksheet

from config                         import ancho_columnas, ESTADOS, FONT_DATOS, SIZE_FONT_DATOS, SIZE_FONT_TITULO, TITULO, EXTENSION_EXCEL_365
from config                         import HOJA_DATOS, HOJA_NOVEDADES, HOJA_ACTIVOS, HOJA_HOJA, TITULO_INSTRUCTORES, TITULO_ULTIMA_FECHA, COLUMNAS_DATOS
from procesadorJuiciosHelper        import getLimite_rap_para_normalizar

def color_rows(row, limite_rap_para_normalizar: int):
    if pd.notnull(row['estado']) and str(row['estado']).strip() != "":
        if row['estado'] != ESTADOS['en_formacion'][0]:
            for value in ESTADOS.values():
                if value[0] == row["estado"]:
                    color = value[1]
                    break
        else:
            col_aprobado       = next(key for key, value in COLUMNAS_DATOS.items() if value == "aprobado")
            col_productiva     = next(key for key, value in COLUMNAS_DATOS.items() if value == "PRO")
            col_en_tramite     = next(key for key, value in COLUMNAS_DATOS.items() if value == "enTramite")  
            # print(f"col_aprobado: {col_aprobado}  col_productiva {col_productiva} col en tramite {col_en_tramite}")      
            por_evaluar        = int(pd.to_numeric(row[col_aprobado], errors='coerce'))
            juicios_productiva = int(pd.to_numeric(row[col_productiva], errors='coerce'))
            por_evaluar        = por_evaluar if pd.notnull(por_evaluar) else 0
            juicios_productiva = juicios_productiva if pd.notnull(juicios_productiva) else 0
            se_tramita_novedad = isinstance(row[col_en_tramite], str) and row[col_en_tramite].strip() != ""
            if   por_evaluar == 1 and juicios_productiva == 1:
                color = "PaleGreen"
            elif por_evaluar == 1 and juicios_productiva != 1:
                color = "Yellow"
            elif por_evaluar in [n for n in range(2, limite_rap_para_normalizar + 1)]:
                color = "PaleGoldenrod"
            elif se_tramita_novedad:
                color = "DarkSalmon']                  "
            elif por_evaluar >= limite_rap_para_normalizar and not se_tramita_novedad:
                color = "Red"
            else:
                color = "FireBrick"
            print(f"color : {color} por evaluar: {por_evaluar} juicios productiva: {juicios_productiva} novedad: {se_tramita_novedad}")
        color_final = [f'background-color: {color}']
    else:
        color_final = [f'background-color: White']
    return color_final * len(row) 

def ajustarFormatoCeldas(hoja: Worksheet, ancho_columnas: list):
    font = Font(name=FONT_DATOS, size=SIZE_FONT_DATOS)
    for row in hoja.iter_rows():
        for cell in row:
            cell.font = font
        for i in range(len(ancho_columnas)):
            row[i].alignment = Alignment(horizontal='center')      
    for col, width in ancho_columnas:
        hoja.column_dimensions[col].width = width

def write_process_file(folder: str, ficha: str, df_datos: pd.DataFrame, df_novedades_ficha: pd.DataFrame, df_activos_ficha: pd.DataFrame, df_hoja: pd.DataFrame):
    file_name = f"{ficha}.{EXTENSION_EXCEL_365}"
    try:
        with pd.ExcelWriter(os.path.join(folder, file_name), engine="openpyxl") as writer:
            limite_rap_para_normalizar = getLimite_rap_para_normalizar(df_datos)
            print(limite_rap_para_normalizar)
            # df_datos.sort_values(by="orden").to_excel(writer, sheet_name=HOJA_DATOS, index=False) 
            df_datos.sort_values(by="orden").style.apply(lambda row: color_rows(row, limite_rap_para_normalizar), axis=1).to_excel(writer, sheet_name=HOJA_DATOS, index=False)  
            workbook = writer.book
            worksheet = workbook[HOJA_DATOS]
            worksheet.delete_cols(25, 2)
            ajustarFormatoCeldas(worksheet, ancho_columnas['datos'])
            worksheet.cell(2, 1).value = TITULO_INSTRUCTORES
            worksheet.cell(3, 1).value = TITULO_ULTIMA_FECHA            
            worksheet.row_dimensions[2].height = 60
            worksheet.row_dimensions[3].height = 45
            for cell in worksheet[2]:
                cell.fill = openpyxl.styles.PatternFill(start_color="BFEFFF", end_color="BFEFFF", fill_type="solid")  
            for cell in worksheet[3]:
                cell.fill = openpyxl.styles.PatternFill(start_color="FFF5E1", end_color="FFF5E1", fill_type="solid")
            for cell in worksheet[2]:
                cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')  
            for cell in worksheet[3]:
                cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')  


            if not df_novedades_ficha is None:
                df_novedades_ficha.to_excel( writer, sheet_name=HOJA_NOVEDADES, index=False)
                ajustarFormatoCeldas(workbook[HOJA_NOVEDADES], ancho_columnas['novedades'])

            if not df_activos_ficha is None:
                df_activos_ficha.to_excel(writer, sheet_name=HOJA_ACTIVOS, index=False)
                ajustarFormatoCeldas(workbook[HOJA_ACTIVOS], ancho_columnas['novedades'])

            df_hoja.to_excel( writer, sheet_name=HOJA_HOJA, index=False)
            worksheet = workbook[HOJA_HOJA]
            ajustarFormatoCeldas(worksheet, ancho_columnas['hoja'])
            for fila in range(2, 13):
                worksheet.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=2)
                worksheet.cell(row=fila, column=1).alignment = Alignment(horizontal='left', vertical='center')
                worksheet.cell(row=fila, column=3).alignment = Alignment(horizontal='left', vertical='center')
            for row in worksheet.iter_rows():
                row[5].alignment = Alignment(horizontal='left')  
                row[6].alignment = Alignment(horizontal='left')
            for col in range(1, 12):
                worksheet.cell(1, col).value = None
            worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=11)
            worksheet.cell(1, 1).value = TITULO
            worksheet.cell(1, 1).font = Font(name=FONT_DATOS, size=SIZE_FONT_TITULO)
    except Exception as e:
        raise Exception(f"Error: no es posible guardar el archivo: {e}")
