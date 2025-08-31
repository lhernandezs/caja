import os.path
import json
import smtplib

from email.message          import EmailMessage
from email.headerregistry   import Address
from email.mime.base        import MIMEBase
from email                  import encoders
from jinja2                 import Environment, select_autoescape, FileSystemLoader

from modelo                 import DatosCorreoJuicios
from config                 import TEMPLATES_FOLDER, JSON_FOLDER, SMTP_SSL, EMAIL_PASSWORD
from config                 import Config

class Correo:

    UPLOAD_FOLDER = Config.UPLOAD_FOLDER
    ENV = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER), autoescape=select_autoescape()) # entorno para jinja2

    def __init__(self, tipo: str = 'JUICI', 
                       destination_username: str = 'lhernandezs', 
                       destination_domain: str = 'sena.edu.co', 
                       destination_display_name: str = 'LeonardoHS', 
                       datosCorreo: DatosCorreoJuicios =  DatosCorreoJuicios(ficha = 9999999, 
                                                                            instructores = ['instructor1', 'instructor2'], 
                                                                            activos = ['activo1', 'activo2'], 
                                                                            desertores = ['desertor1', 'desertor2'])):
        
        with open(os.path.join(JSON_FOLDER, 'sercorreo.json'), 'r') as conex:
            arc = json.load(conex)
        self._sender_username           = arc[tipo]["emailRemitente"] 
        self._sender_domain             = arc[tipo]["servidorRemitente"] 
        self._sender_display_name       = arc[tipo]["nombreRemitente"] 
        self._subject                   = arc[tipo]["asunto"] 
        self._template                  = arc[tipo]["template"]

        self._destination_username      = destination_username
        self._destination_domain        = destination_domain
        self._destination_display_name  = destination_display_name
        self._datosCorreo               = datosCorreo
        
        self._email_message = EmailMessage()    

    # renderiza la plantilla -template- con los datos -modelo-
    def render_html(self):
        return Correo.ENV.get_template(self._template).render(datosCorreo=self._datosCorreo, asunto = self._subject)

    # construye el cuerpo del email con los datos pasados en el parametro
    def build_email(self):
        self._email_message["Subject"] = f"{self._subject} {self._datosCorreo.ficha}"
        self._email_message["From"]    = Address(username=self._sender_username, domain=self._sender_domain, display_name=self._sender_display_name)
        self._email_message["To"]      = Address(username=self._destination_username, domain=self._destination_domain, display_name=self._destination_display_name)
        html_data: str                 = self.render_html()
        self._email_message.add_alternative(html_data, subtype="html")
        filename = f"{self._datosCorreo.ficha}.xlsx"

        try:
            part = MIMEBase('application', 'octet-stream')
            file = open(os.path.join(Correo.UPLOAD_FOLDER, filename ), 'rb')
            part.set_payload((file).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename = filename)
            self._email_message.attach(part)
            file.close()
        except:
            print(f"Error: no fue posible adjuntar al correo el archivo {filename}")
            # raise Exception(f"Error: no fue posible adjuntar al correo el archivo {filename}")

    # metodo que envia el email
    def send_email(self):
        self.build_email()
        remitente       = self._sender_username + "@" + self._sender_domain
        destinatario    = self._destination_username + "@" + self._destination_domain

        smtp = smtplib.SMTP_SSL(SMTP_SSL)
        smtp.login(remitente, EMAIL_PASSWORD) # para enviar correo desde la cuenta formacionvirtualcsf@gmail.com

        smtp.sendmail(remitente, destinatario, self._email_message.as_string())
        smtp.quit()

if __name__ == '__main__':
    correo = Correo()
    correo.send_email()
