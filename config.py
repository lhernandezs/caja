import os

TEMPLATES_FOLDER        = os.path.join("templates")

SMTP_SSL                = "smtp.gmail.com"
SENDER_DOMAIN           = "gmail.com"
SUBJECT                 = "analizar estado ficha"
TEMPLATES               = ['correoJuicios.html','correoJuicios1.html']
# SENDER_USERNAME         = "formacionvirtualcsf"
# EMAIL_PASSWORD          = "ddycjigkgqrtsray"
# SENDER_DISPLAY_NAME     = "formacionvirtualcsf@sena.edu.co"
SENDER_USERNAME         = "creamos.porcolombia"
EMAIL_PASSWORD          = "qhjkzhhqeywqsasq"
SENDER_DISPLAY_NAME     = "porColombia"

PORCENTAJE_LIMITE_RAP   = 0.30

ARCHIVO_DE_DATOS        = "datos.xlsx"
EXTENSION_EXCEL_365     = "xlsx"
FONT_DATOS              = "Arial"
SIZE_FONT_DATOS         = 9
SIZE_FONT_TITULO        = 20

TITULO                  = "Reporte de Juicios"
TITULO_INSTRUCTORES     = "Instructor competencia"
TITULO_ULTIMA_FECHA     = "Fecha de registro del último RAP"
ALTO_FILA_INSTRUCTORES  = 60
ALTO_FILA_FEC_JUICIOS   = 45

ESTADOS                 = { 
                            "induccion"         : ("INDUCCION",         "IndianRed"     ),
                            "en_formacion"      : ("EN FORMACION",      "White"         ),
                            "trasladado"        : ("TRASLADADO",        "RosyBrown"     ),
                            "aplazado"          : ("APLAZADO",          "Magenta"       ),
                            "condicionado"      : ("CONDICIONADO",      "DarkViolet"    ),
                            "por_certificar"    : ("POR CERTIFICAR",    "Lime"          ),
                            "certificado"       : ("CERTIFICADO",       "ForestGreen"   ),
                            "retiro_voluntario" : ("RETIRO VOLUNTARIO", "Aqua"          ),
                            "cancelado"         : ("CANCELADO",         "SteelBlue"     ),
                            "reintegrado"       : ("REINTEGRADO",       "DeepSkyBlue"   ),
}

FILTROS                 = ['activo', 'en_tramite', 'no_aprobado', 'para_productiva', 'error_productiva', 'para_normalizar', 'para_desertar']

COLUMNAS_HOJA           = ["tipo", "documento", "nombres", "apellidos", "estado", "competencia", "resultado", "juicio", "vacio", "fecha", "funcionario"]
COLUMNAS_DATOS          = ['tipo', 'documento', 'nombres', 'apellidos', 'estado', 'aprobado', 'porEvaluar', 'noAprobado', 'enTramite', 'activo', 
                           'IND', 'BIL', 'CIE', 'COM', 'CUL', 'DER', 'EMP', 'ETI', 'INV', 'MAT', 'SST', 'TIC', 'TEC', 'PRO', 'color', 'orden']
COLUMNAS_NOVEDADES      = ["ficha", "documento", "novedad"]
COLUMNAS_ACTIVOS        = ["ficha", "documento"]
COLUMNAS_INSTRUCTORES   = ["ficha", "instructor", "competencia"]

COLUMNAS_INT_DATOS      = ['aprobado', 'porEvaluar', 'noAprobado', 'IND', 'BIL', 'CIE', 'COM', 'CUL', 'DER', 'EMP', 
                           'ETI', 'INV', 'MAT', 'SST', 'TIC', 'PRO', 'TEC',]

ANCHOS_HOJA             = [('A',  6), ('B', 15), ('C', 21), ('D', 21), ('E', 16), 
                           ('F', 40), ('G', 40), ('H', 12), ('I',  0), ('J', 16),
                           ('K', 30),]
ANCHOS_DATOS            = [('A',  6), ('B', 15), ('C', 21), ('D', 21), ('E', 16), 
                           ('F', 12), ('G', 12), ('H', 12), ('I', 15), ('J', 12),
                           ('K',  6), ('L',  6), ('M',  6), ('N',  6), ('O',  6), 
                           ('P',  6), ('Q',  6), ('R',  6), ('S',  6), ('T',  6), 
                           ('U',  6), ('V',  6), ('W',  6), ('X',  6),]
ANCHOS_NOVEDADES        = [('A', 16), ('B', 12), ('C', 12),]
ANCHOS_ACTIVOS          = [('A', 16), ('B', 12),]
ANCHOS_INSTRUCTORES     = [('A', 16), ('B', 42), ('C', 12),]

HOJAS                   = {
                            'Hoja'          : {'columnas': COLUMNAS_HOJA          , 'ancho_columnas' : ANCHOS_HOJA},
                            'datos'         : {'columnas': COLUMNAS_DATOS         , 'ancho_columnas' : ANCHOS_DATOS},
                            'novedades'     : {'columnas': COLUMNAS_NOVEDADES     , 'ancho_columnas' : ANCHOS_NOVEDADES},
                            'activos'       : {'columnas': COLUMNAS_ACTIVOS       , 'ancho_columnas' : ANCHOS_ACTIVOS},
                            'instructores'  : {'columnas': COLUMNAS_INSTRUCTORES  , 'ancho_columnas' : ANCHOS_INSTRUCTORES}, }

REGLAMENTOS             = [
                            'Acuerdo 7 de 2012',
                            'Acuerdo 9 de 2024']

COMPETENCIAS_NO_TECNICAS = {
                            "IND": "36182",
                            "BIL": "37714",
                            "CIE": "37801",
                            "COM": "37802",
                            "CUL": "37800",
                            "DER": "38558",
                            "EMP": "38561",
                            "ETI": "36180",
                            "INV": "38199",
                            "MAT": "38560",
                            "SST": "37799",
                            "TIC": "37371",
                            "PRO": "2 - R",}

#la clave es codigo del programa ", " version
COMPETENCIAS_PROGRAMAS_ESPECIALES = {
                            '621201, 102'   :[('ETI', '1 - P'),],
                            '121202, 101'   :[('ETI', '1 - P'),],
                            '123111, 100'   :[('ETI', '1 - P'),],
                            '135319, 1'     :[('ETI', '1 - P'),],
                            '123303, 101'   :[('ETI', '1 - P'),],
                            '621201, 102'   :[('BIL', '3226 '),],
                            '121202, 101'   :[('BIL', '3226 '),],
                            '123111, 100'   :[('BIL', '3226 '),],
                            '135319, 1'     :[('BIL', '3226 '),],
                            '123303, 101'   :[('BIL', '3226 '),],
                            '621201, 102'   :[('COM', '3227 '),],
                            '121202, 101'   :[('COM', '3227 '),],
                            '123111, 100'   :[('COM', '3227 '),],
                            '123303, 101'   :[('COM', '3227 '),],
                            '632223, 2'     :[('EMP', '39811'),],
                            '631101, 2'     :[('EMP', '39811'),],
                            '134101, 2'     :[('EMP', '39811'),],
                            '133303, 1'     :[('EMP', '39811'),],
                            '233104, 2'     :[('EMP', '39811'),],
                            '134200, 2'     :[('EMP', '39811'),],
                            '233108, 1'     :[('EMP', '39811'),],
                            '233105, 2'     :[('EMP', '39811'),],
                            '133305, 1'     :[('EMP', '39811'),],
                            '134104, 1'     :[('EMP', '39811'),],
                            '134600, 1'     :[('EMP', '39811'),],
                        }

MESES_ESPANOL           = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

TOLERANCIA_MESES        = 0.1

DURACION_PROGRAMAS      = {
                            'tecnologo'         : 27,
                            'tecnico'           : 15,
                            'tecnico_corto'     : 12,
                            'tecnico_express'   : 9,}

class Config:
    SECRET_KEY              = "PorColombia2025"
    UPLOAD_FOLDER           = os.path.join("upload")
    UPLOAD_FOLDER_DATA      = os.path.join("data")
    ALLOWED_EXTENSIONS      = {"xls", "xlsx"}

