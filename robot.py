import numpy as np
import pandas as pd

from correo                   import Correo
from modelo                   import DatosCorreoJuicios
from entrada                        import Entrada
from procesadorJuiciosHelper  import columnas_df_datos

class Robot:
    def __init__(self):
        pass

    def sendCorreosJuicios(self, fichas):
        for ficha in fichas: 
            df_datos : pd.DataFrame = Entrada().getDataFrame("upload", f"{ficha}.xlsx", "Datos", columnas_df_datos)

            # activos con juicios por evaluar
            df_activos   = df_datos[(df_datos['activo']            == "ACTIVO") & 
                                    (df_datos['porEvaluar'].values > 1)].reset_index()   
            # hay que desertarlos
            df_aDesertar = df_datos[(df_datos['estado']   == "EN FORMACION") &
                                    (df_datos['activo']   != "ACTIVO") & 
                                    (df_datos['enTramite'].isin([np.nan])) ].reset_index()

            instructores    = [df_datos.iloc[0, 23]]
            datosActivos    = []
            datosADesertar  = []

            for index, row in df_activos.iterrows():
                for col in range(11,24):
                    if (df_activos.iloc[index, col + 1] > 0) & (df_datos.columns[col] != "PRO"):
                        nombres =   f"{df_activos.iloc[index, 3]} {df_activos.iloc[index, 4]}"
                        competencia = df_datos.columns[col]
                        rapsPorEvaluar = int(df_activos.iloc[index, col + 1])
                        instructor = df_datos.iloc[0, col],
                        datosActivos.append([nombres, competencia, rapsPorEvaluar, instructor[0],])
                        if not instructor[0] in instructores:
                            instructores.append(instructor[0])

            for index,row in df_aDesertar.iterrows():
                nombres =   f"{df_aDesertar.iloc[index, 3]} {df_aDesertar.iloc[index, 4]}"                
                rapsPorEvaluar = int(df_aDesertar.iloc[index, 7])
                datosADesertar.append([ nombres, rapsPorEvaluar])

            datosCorreo = DatosCorreoJuicios(
                                        ficha                   = ficha,
                                        instructores            = instructores,
                                        activos                 = datosActivos,
                                        desertores              = datosADesertar
                                            )
            
            correo = Correo('JUICI','lhernandezs', 'sena.edu.co', 'LeonardoSENA', datosCorreo)   # destino correo Leonardo            
            correo.send_email(ficha = ficha) 

if __name__ == '__main__':
    fichas = {'agosto'          : [
                                    "2879546", "2879572", "2879609", "2879610", "2879689", "2879690", "2879691", "2879692", "2879693", "2879694",
                                    "2879695", "2879696", "2879697", "2879698", "2879699", "2879835", "2879836", "2879837", "2879838", "2879839",
                                    "2879840", "2879841", "2879842", "2879843", "2879844", "2879845", "2879846", "2879847", "2879848", "2879849", 
                                  ],
              'junio' :           [
                                    "2758190", "2758230", "2758333", "2834649", "2834650", "2834651", "2834838", "2834839", "2834840", "2834841",
                                    "2834842", "2834843", "2834844", "2834845", "2834846", "2834847", "2834848", "2834849", "2834850", "2834851",
                                    "2834852", "2834853", "2834854", "2834855", "2834856", "2989236", "3013169", "3059562", "3059847", "3064539",
                                    "3069982", "3069983",
                                  ],
              'p_productivo' :    [    
                                    "2675758", "2627061", "2627205", "2675759", "2758425", "2675911", "2675744", "2627062", "2626957",
                                  ],
               'kebin' :          [   
                                    "3106275", 
                                  ],
               'andres' :         [
                                    "3118505", "3118506", "3118507",           
                                  ],
               'prueba' :         [
                                    "2879847", "2879848", "2879849",           
                                  ],
             }    
    
    robot = Robot()
    robot.sendCorreosJuicios(fichas['agosto'])