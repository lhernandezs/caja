from correo                   import Correo
from modelo                   import DatosCorreoJuicios
from entradaHelper            import getDataFrame
from filtrosHelper            import get_listas_datos
from app                      import UPLOAD_FOLDER
from config                   import EXTENSION_EXCEL_365

class Robot:

    def sendCorreosJuicios(self, fichas):
        for ficha in fichas: 
            df_datos        = getDataFrame(UPLOAD_FOLDER, f"{ficha}.{EXTENSION_EXCEL_365}", "datos")
            listas_datos    = get_listas_datos(df_datos)
            instructores    = listas_datos['ls_instructores']
            datos_activos   = listas_datos['ls_para_normalizar']
            datos_a_desertar= listas_datos['ls_para_desertar']

            datos_correo_juicios = DatosCorreoJuicios(
                                        ficha                   = ficha,
                                        instructores            = instructores,
                                        activos                 = datos_activos,
                                        desertores              = datos_a_desertar
                                        )

            correo = Correo('lhernandezs', 'sena.edu.co', 'LeonardoSENA', **{"datos_correo": datos_correo_juicios, "template": 0})   # destino correo lhernandezs@sena.edu.co
            # correo = Correo('leo66'      , 'hotmail.com' , 'Leonardo HS' , **{"datos_correo": datos_correo_juicios, "template": 0})   # destino correo leo66@hotmail.com

            try:
                correo.send_email()
                print(f'Correo enviado exitosamente! {ficha}')
            except Exception as e:
                print(f'Error al enviar el correo {ficha}: {str(e)}')

if __name__ == '__main__':
    fichas = {
        'agosto'          : [
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
        'juan carlos':     [
                            "2977746",
                            ],
             }    
    
    robot = Robot()
    robot.sendCorreosJuicios(fichas['juan carlos'])