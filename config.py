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
            "induccion"      : "INDUCCION",
            "en_formacion"   : "EN FORMACION",
            "trasladado"     : "TRASLADADO",
            "aplazado"       : "APLAZADO",
            "condicionado"   : "CONDICIONADO",
            "por_certificar" : "POR CERTIFICAR",
            "certificado"    : "CERTIFICADO",
            "retirado"       : "RETIRO VOLUNTARIO",
            "cancelado"      : "CANCELADO",
           }


class Config:
    SECRET_KEY          = "PorColombia2025"
    UPLOAD_FOLDER       = os.path.join("upload")
    UPLOAD_FOLDER_DATA  = os.path.join("data")
    ALLOWED_EXTENSIONS  = {"xls", "xlsx"}
    