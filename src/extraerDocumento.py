import pandas as pd
import os

from entradaSalida import EntradaSalida

dfNombresAVerificar: pd.DataFrame = EntradaSalida().leerArchivo("novedades.xlsx", "nombresAprendices", ["NOMBRE", "FICHA",])

columnas = [ "tipo", "documento", "nombres", "apellidos", "estado", "competencia", "resultado", "juicio", "vacio", "fecha", "funcionario", ]
columnasACopiar = ["documento", "nombres", "apellidos"]

dfEncontrados = pd.DataFrame(columns=['documento', 'nombre', 'ficha'])
dfNoEncontrados = pd.DataFrame(columns=['nombre', 'ficha'])

fichas = [
        '2758190',
        '2758230',
        '2758333',
        # '2834649',
        # '2834650',
        # '2834651',
        # '2834838',
        # '2834839',
        # '2834840',
        # '2834841',
        # '2834842',
        # '2834843',
        # '2834844',
        # '2834845',
        # '2834846',
        # '2834847',
        # '2834848',
        # '2834849',
        # '2834850',
        # '2834851',
        # '2834852',
        # '2834853',
        # '2834854',
        # '2834855',
        # '2834856',
        # '2989236',
        # '3013169',
        # '3059562',
        # '3059847',
        # '3064539',
        # '3069982',
        # '3069983',
    ]

for ficha in fichas:
    # leemos el reporte de la ficha y creamos la nueva columna con nombres y apellidos
    dfHoja = EntradaSalida().leerArchivo(f"Reporte de Juicios Evaluativos {ficha}.xls", "Hoja", columnas)
    dfNombresFicha = dfHoja[columnasACopiar].copy()
    dfNombresFicha = dfNombresFicha[12:]
    dfNombresFicha.drop_duplicates(inplace=True)
    dfNombresFicha['nombre'] = dfNombresFicha['nombres'].astype(str) + " " + dfNombresFicha['apellidos'].astype(str)

    # encontramos el documento que conincida con el nombre
    dfAVerficarFicha = dfNombresAVerificar[dfNombresAVerificar['FICHA'] == int(ficha)]
    for nombre in dfAVerficarFicha['NOMBRE']:
        try:
            documento = dfNombresFicha[dfNombresFicha['nombre'].str.contains(nombre.strip())]['documento'].values[0]
            nueva_fila = {'documento': documento, 'nombre': nombre, 'ficha': ficha}
            dfEncontrados = dfEncontrados._append(nueva_fila, ignore_index=True)
            print(f"{documento}, {nombre}, {ficha}")
        except:
            nueva_fila = {'nombre': nombre, 'ficha': ficha}
            dfNoEncontrados = dfNoEncontrados._append(nueva_fila, ignore_index=True)

try:
    with pd.ExcelWriter(os.path.join("datos", 'documentosEncontrados.xlsx'), engine="openpyxl") as writer:
        dfEncontrados.to_excel( writer, sheet_name="encontrados", index=False)
        dfNoEncontrados.to_excel( writer, sheet_name="no encontrados", index=False)        
except Exception as e:
    print(f"Error al guardar el archivo Excel: {e}")
    exit()                                     
