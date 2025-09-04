import os

TEMPLATES_FOLDER        = os.path.join("templates")
JSON_FOLDER             = os.path.join("json")

SMTP_SSL                = "smtp.gmail.com"
SENDER_USERNAME         = "formacionvirtualcsf"
SENDER_DOMAIN           = "gmail.com"
EMAIL_PASSWORD          = "ddycjigkgqrtsray"
SENDER_DISPLAY_NAME     = "formacionvirtualcsf@sena.edu.co"
SUBJECT                 = "normalizar ficha  "
TEMPLATES               = ['correoJuicios.html']

PORCENTAJE_LIMITE_RAP = 0.25

ARCHIVO_DE_DATOS    = "datos.xlsx"
HOJA_DATOS          = "datos"
HOJA_NOVEDADES      = "novedades"
HOJA_ACTIVOS        = "activos"
HOJA_INSTRUCTORES   = "instructor"
HOJA_HOJA           = "hoja"
EXTENSION_EXCEL_365 = "xlsx"
FONT_DATOS          = "Arial"
SIZE_FONT_DATOS     = 9
SIZE_FONT_TITULO    = 20
TITULO              = "Reporte de Juicios"
TITULO_INSTRUCTORES = "Instructor por compentencia"
TITULO_ULTIMA_FECHA = "Fecha de registro del último RAP"

ESTADOS = { 
            "induccion"         : ("INDUCCION",         "IndianRed"),
            "en_formacion"      : ("EN FORMACION",      "White"),
            "trasladado"        : ("TRASLADADO",        "Violet"),
            "aplazado"          : ("APLAZADO",          "Magenta"),
            "condicionado"      : ("CONDICIONADO",      "DarkViolet"),
            "por_certificar"    : ("POR CERTIFICAR",    "Lime"),
            "certificado"       : ("CERTIFICADO",       "ForestGreen"),
            "retiro_voluntario" : ("RETIRO VOLUNTARIO", "Aqua"),
            "cancelado"         : ("CANCELADO",         "SteelBlue"),
            "reintegrado"       : ("REINTEGRADO",       "DeepSkyBlue"),
}

COLUMNAS_HOJA = {
            1: "tipo",
            2: "documento",
            3: "nombres",
            4: "apellidos",
            5: "estado",
            6: "competencia",
            7: "resultado",
            8: "juicio",
            9: "vacio",
            10: "fecha",
            11: "funcionario",
}

COLUMNAS_DATOS = {
            1: "tipo",
            2: "documento",
            3: "nombres",
            4: "apellidos",
            5: "estado",
            6: "aprobado",
            7: "porEvaluar",
            8: "noAprobado",
            9: "enTramite",
            10: "activo",
            11: "IND",
            12: "BIL",
            13: "CIE",
            14: "COM",
            15: "CUL",
            16: "DER",
            17: "EMP",
            18: "ETI",
            19: "INV",
            20: "MAT",
            21: "SST",
            22: "TIC",
            23: "PRO",
            24: "TEC",
            25: "color",
        }

COLUMNAS_NOVEDADES = {
    1: "documento",
    2: "nombre",
    3: "ficha",
    4: "novedad",
}

COLUMNAS_ACTIVOS = {
    1: "documento",
    2: "nombre",
    3: "ficha",
    4: "instructor",
}

COLUMNAS_INSTRUCTOR = {
    1: "INSTRUCTOR",
    2: "FICHA",
    3: "COMPETENCIA",
}

competencias_no_tecnicas = {
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
            "PRO": "2 - R",
        }

#la clave es codigo del programa ", " version
competencias_programas_especiales = {
            '631101, 2' : [('EMP', '39811'), ],
        }

ancho_columnas = {'datos' :     [('A',  6), ('B', 15), ('C', 21), ('D', 21), ('E', 16), 
                                 ('F', 12), ('G', 12), ('H', 12), ('I', 15), ('J', 12),
                                 ('K',  6), ('L',  6), ('M',  6), ('N',  6), ('O',  6), 
                                 ('P',  6), ('Q',  6), ('R',  6), ('S',  6), ('T',  6), 
                                 ('U',  6), ('V',  6), ('W',  6), ('X',  6),],
                  'novedades':  [('A', 16), ('B', 42), ('C', 12), ('D', 30),],
                  'hoja':       [('A',  6), ('B', 15), ('C', 21), ('D', 21), ('E', 16), 
                                 ('F', 40), ('G', 40), ('H', 12), ('I',  0), ('J', 16),
                                 ('K', 30),]}



class Config:
    SECRET_KEY          = "PorColombia2025"
    UPLOAD_FOLDER       = os.path.join("upload")
    UPLOAD_FOLDER_DATA  = os.path.join("data")
    ALLOWED_EXTENSIONS  = {"xls", "xlsx"}

