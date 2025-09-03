
import os
import openpyxl
import pandas as pd

from openpyxl.styles                import Font
from openpyxl.styles                import Alignment
from openpyxl.worksheet.worksheet   import Worksheet

from config                         import ancho_columnas, ESTADOS
from procesadorJuiciosHelper        import getLimite_rap_para_normalizar



def color_rows(row, limite_rap_para_normalizar: int) -> list:
    if   row["estado"] == ESTADOS['induccion']:
        color = ['background-color: IndianRed']
    elif row["estado"] == ESTADOS['en_formacion']: 
        por_evaluar        = pd.to_numeric(row['porEvaluar'], errors='coerce')
        juicios_productiva = pd.to_numeric(row["PRO"], errors='coerce')
        se_tramita_novedad = isinstance(row['enTramite'], str) and row['enTramite'].strip() != ""
        if   por_evaluar == 1 and juicios_productiva == 1:
            color = ['background-color: PaleGreen']
        elif por_evaluar == 1 and juicios_productiva != 1:
            color = ['background-color: Yellow']
        elif por_evaluar in [n for n in range(2, limite_rap_para_normalizar + 1)]:
            color = ['background-color: PaleGoldenrod']
        elif se_tramita_novedad:
            color = ['background-color: DarkSalmon']                    
        elif por_evaluar >= limite_rap_para_normalizar and not se_tramita_novedad:
            color = ['background-color: Red']
        else:
            color = ['background-color: FireBrick']
    elif row["estado"] == ESTADOS['trasladado']:
        color = ['background-color: Violet']   
    elif row["estado"] == ESTADOS['aplazado']:
        color = ['background-color: Magenta']
    elif row["estado"] == ESTADOS['condicionado']:
        color = ['background-color: DarkViolet']
    elif row["estado"] == ESTADOS['por_certificar']:
        color = ['background-color: Lime']
    elif row["estado"] == ESTADOS['certificado']:
        color = ['background-color: ForestGreen']
    elif row["estado"] == ESTADOS['retiro_voluntario']:
        color = ['background-color: Aqua']
    elif row["estado"] == ESTADOS['cancelado']:
        color = ['background-color: SteelBlue']
    elif row["estado"] == ESTADOS['reintegrado']:
        color = ['background-color: DeepSkyBlue']
    else:
        color = ['background-color: Brown']
    print(color)        
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
            limite_rap_para_normalizar = getLimite_rap_para_normalizar(df_datos)
            df_datos.sort_values(by="orden").style.apply(lambda row: color_rows(row, limite_rap_para_normalizar), axis=1).to_excel(writer, sheet_name="Datos", index=False)  
            workbook = writer.book
            worksheet = workbook['Datos']
            worksheet.delete_cols(26)
            worksheet.delete_cols(25)
            ajustarFormatoCeldas(worksheet, ancho_columnas['datos'])
            # ajustar la fila de nombres de los instructores
            row_dimension_2 = worksheet.row_dimensions[2]
            row_dimension_2.height = 60
            row_dimension_3 = worksheet.row_dimensions[3]
            # Coloca la fila 3 en color beige claro
            for cell in worksheet[3]:
                cell.fill = openpyxl.styles.PatternFill(start_color="FFF5E1", end_color="FFF5E1", fill_type="solid")
            row_dimension_3.height = 45 
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
