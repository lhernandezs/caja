import os

TEMPLATES_FOLDER    = os.path.join("templates")
JSON_FOLDER         = os.path.join("json")
EMAIL_PASSWORD      = "ddycjigkgqrtsray"
SMTP_SSL            = "smtp.gmail.com"

class Config:
    SECRET_KEY          = "PorColombia2025"
    UPLOAD_FOLDER       = os.path.join("upload")
    UPLOAD_FOLDER_DATA  = os.path.join("data")
    ALLOWED_EXTENSIONS  = {"xls", "xlsx"}
    