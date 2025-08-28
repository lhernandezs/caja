from entradaSalida import EntradaSalida

# Utilidad para conocer todas las competencias difentes de las fichas
fichas = [
    '2834841',
    '2834842',
    '2834843',
]

competencias = []
for ficha in fichas:
    columnas = [ "tipo", "documento", "nombres", "apellidos", "estado", "competencia", "resultado", "juicio", "vacio", "fecha", "funcionario", ]
    dfHoja = EntradaSalida().leerArchivo(f"Reporte de Juicios Evaluativos {ficha}.xls", "Hoja", columnas)
    for competencia in dfHoja[12:]["competencia"]:
        if competencia not in competencias:
            print(competencia)
            competencias.append(competencia)