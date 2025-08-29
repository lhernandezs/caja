import os

class Config:
    SECRET_KEY          = "PorColombia2025"
    UPLOAD_FOLDER       = os.path.join("upload")
    UPLOAD_FOLDER_DATA  = os.path.join("data")
    ALLOWED_EXTENSIONS  = {"xls", "xlsx"}