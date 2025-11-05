from pydantic   import BaseModel

class DatosCorreoJuicios(BaseModel):
    ficha                       : int
    instructores                : list
    activos                     : list
    desertores                  : list