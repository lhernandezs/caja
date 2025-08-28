from enum       import Enum
from pydantic   import BaseModel, EmailStr
from typing     import Optional

class Vinculacion(Enum):
    PLANTA      = 'Planta'
    CONTRATO    = 'Contrato'

class TipoCompetencia(Enum):
    TECNICA     = 'TEC'
    TRANSVERSAL = 'TRA'

class Instructor(BaseModel):
    cedula                      : str
    nombre                      : str
    vinculacion                 : str
    correo                      : EmailStr
    correo2                     : Optional[EmailStr] = None
    competencia                 : str | None

class Ficha(BaseModel):
    nivel                       : str
    programa                    : str
    nficha                      : int
    fecha_inicio                : str
    fecha_fin                   : Optional[str] = None
    aprendices                  : int
    ins_tecnico                 : Optional[str] = None
    competencias                : Optional[str] = None
    competencias_faltan         : Optional[str] = None
    nombre                      : Optional[str] = None

class Competencia(BaseModel):
    competencia                 : str
    descripcion_competencia     : str

class DatosCorreo(BaseModel):
    instructor                  : Instructor
    descripcion_competencia     : str
    fichas                      : list

class TopeAprendices(BaseModel):
    tipo_competencia            : TipoCompetencia
    vinculacion                 : Vinculacion
    tope                        : int

class Juicio(BaseModel):
    tipo                      : str
    documento	                : str
    nombre                    : str  	
    apellidos	                : str
    estado	                  : str
    competencia	              : str
    resultado	                : str
    juicio		                : str
    fecha	                    : str
    funcionario	              : str

class DatosCorreoJuicios(BaseModel):
    ficha                         : int
    instructores                  : list
    activos                       : list
    desertores                    : list