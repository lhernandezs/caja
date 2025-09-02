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

ESTADOS = { 
            "induccion"         : "INDUCCION",
            "en_formacion"      : "EN FORMACION",
            "trasladado"        : "TRASLADADO",
            "aplazado"          : "APLAZADO",
            "condicionado"      : "CONDICIONADO",
            "por_certificar"    : "POR CERTIFICAR",
            "certificado"       : "CERTIFICADO",
            "retiro_voluntario" : "RETIRO VOLUNTARIO",
            "cancelado"         : "CANCELADO",
            "reintegrado"       : "REINTEGRADO",
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

PORCENTAJE_RAPS_POR_NORMALIZAR = 25

class Config:
    SECRET_KEY          = "PorColombia2025"
    UPLOAD_FOLDER       = os.path.join("upload")
    UPLOAD_FOLDER_DATA  = os.path.join("data")
    ALLOWED_EXTENSIONS  = {"xls", "xlsx"}
    