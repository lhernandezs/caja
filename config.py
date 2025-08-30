import os

class Config:
    SECRET_KEY          = "PorColombia2025"
    UPLOAD_FOLDER       = os.path.join("upload")
    UPLOAD_FOLDER_DATA  = os.path.join("data")
    ALLOWED_EXTENSIONS  = {"xls", "xlsx"}
    MAIL_SERVER         = 'mtp-mail.outlook.com'
    MAIL_PORT           = 587
    MAIL_USE_TLS        = True
    MAIL_USE_SSL        = False
    MAIL_USERNAME       = 'leo66@hotmail.com'
    MAIL_PASSWORD       = 'Codi2709.'
    MAIL_DEFAULT_SENDER = 'leo66@hotmail.com' 