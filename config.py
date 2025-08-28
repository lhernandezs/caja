import os

class Config:
    SECRET_KEY = "PorColombia2025"
    # UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "upload")
    UPLOAD_FOLDER = os.path.join("upload")

    UPLOAD_FOLDER_DATA = os.path.join("data")
    # UPLOAD_FOLDER_DATA = os.path.join(os.path.dirname(__file__), "data")
    DATA_FILE = "datos.xlsx"
    ALLOWED_EXTENSIONS = {"xls", "xlsx"}