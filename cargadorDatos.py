import os
import pandas as pd

from entrada import Entrada

class CargadorDatos:
    def __init__(self, folder: str, file: str):
        self.file           = file
        self.folder         = folder
        
        self.df_novedades: pd.DataFrame     = None
        self.df_activos: pd.DataFrame       = None
        self.df_instructores: pd.DataFrame  = None

        self.novedades      = 0
        self.activos        = 0
        self.instructores   = 0

    def getDatos(self) -> dict:
        if not os.path.isfile(os.path.join(self.folder, self.file)):
            raise FileNotFoundError(f"Error: No se encontró el archivo {os.path.join(self.folder, self.file)}")
        else:
            try:
                self.df_novedades       = Entrada().getDataFrame(self.folder, self.file, "novedades",   ["DOCUMENTO", "NOMBRE", "FICHA", "NOVEDAD"])
                self.df_activos         = Entrada().getDataFrame(self.folder, self.file, "activos",     ["DOCUMENTO", "NOMBRE", "FICHA", "INSTRUCTOR"])
                self.df_instructores    = Entrada().getDataFrame(self.folder, self.file, "instructores",["INSTRUCTOR", "FICHA", "COMPETENCIA"])
            except Exception as e:
                raise e

            self.df_novedades.drop_duplicates(inplace=True)
            self.df_activos.drop_duplicates(inplace=True)
            self.df_instructores.drop_duplicates(inplace=True)

            self.novedades = len(self.df_novedades)
            self.activos = len(self.df_activos)
            self.instructores = len(self.df_instructores)

            try:
                self.df_novedades = self.df_novedades.astype({"DOCUMENTO": "int"}) 
            except ValueError as e:
                raise ValueError(f"Error: algunos documentos no se pueden convertir a número en la hoja 'novedades'.")

            try:
                self.df_activos = self.df_activos.astype({"DOCUMENTO": "int"})
            except ValueError as e:
                raise ValueError(f"Error: algunos documentos no se pueden convertir a número en la hoja 'activos'.")
            
            return {'df_novedades': self.df_novedades, 'df_activos': self.df_activos, 'df_instructores': self.df_instructores}

from procesadorJuicios import ProcesadorJuicios
if __name__ == "__main__":
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
    
    cargadorDatos = CargadorDatos("data", "datos.xlsx")
    try:
        cargadorDatos.getDatos()
    except:
        cargadorDatos.df_novedades = None
        cargadorDatos.df_activos = None
        cargadorDatos.df_instructores = None

    for ficha in fichas['agosto']: 
        try:
            juiciosFicha = ProcesadorJuicios("upload", f"Reporte de Juicios Evaluativos {ficha}.xls", cargadorDatos.df_novedades, cargadorDatos.df_activos, cargadorDatos.df_instructores)
            juiciosFicha.procesar()
            print(f"Archivo transformado a XLSX exitosamente para la ficha {ficha}.")
        except Exception as e:
            raise ValueError(e)
