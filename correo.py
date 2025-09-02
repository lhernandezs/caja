import os.path
import json
import smtplib

from email.message          import EmailMessage
from email.headerregistry   import Address
from email.mime.base        import MIMEBase
from email                  import encoders
from jinja2                 import Environment, select_autoescape, FileSystemLoader

from modelo                 import DatosCorreoJuicios
from config                 import TEMPLATES_FOLDER, JSON_FOLDER, SMTP_SSL, SENDER_USERNAME, EMAIL_PASSWORD, SENDER_DOMAIN, SENDER_DISPLAY_NAME, SUBJECT, TEMPLATES
from config                 import Config

class Correo:
    UPLOAD_FOLDER = Config.UPLOAD_FOLDER
    ENV = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER), autoescape=select_autoescape()) # entorno para jinja2

    def __init__(self, destination_username: str        = 'lhernandezs', 
                       destination_domain: str          = 'sena.edu.co', 
                       destination_display_name: str    = 'LeonardoHS', 
                       datos_correo: DatosCorreoJuicios =  DatosCorreoJuicios(ficha = 9999999, 
                                                                              instructores = ['instructor1', 'instructor2'], 
                                                                              activos      = ['activo1', 'activo2'], 
                                                                              desertores   = ['desertor1', 'desertor2']),
                       template: int = 0,                         
                ):
        self.sender_username         = SENDER_USERNAME 
        self.sender_domain           = SENDER_DOMAIN
        self.sender_display_name     = SENDER_DISPLAY_NAME
        self.subject                 = SUBJECT
        self.template                = TEMPLATES[template]

        self.destination_username    = destination_username
        self.destination_domain      = destination_domain
        self.destination_display_name= destination_display_name
        self.datos_correo            = datos_correo
        
        self.email_message           = EmailMessage()    

    def render_html(self):
        return Correo.ENV.get_template(self.template).render(datos_correo=self.datos_correo, asunto = self.subject)

    # construye el email con los datos pasados en el parametro
    def build_email(self):
        self.email_message["Subject"] = f"{self.subject} {self.datos_correo.ficha}"
        self.email_message["From"]    = Address(username=self.sender_username, domain=self.sender_domain, display_name=self.sender_display_name)
        self.email_message["To"]      = Address(username=self.destination_username, domain=self.destination_domain, display_name=self.destination_display_name)
        self.email_message.add_alternative(self.render_html(), subtype="html")

        filename = f"{self.datos_correo.ficha}.xlsx"
        try:
            part = MIMEBase('application', 'octet-stream')
            file = open(os.path.join(Correo.UPLOAD_FOLDER, filename ), 'rb')
            part.set_payload((file).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename = filename)
            self.email_message.attach(part)
            file.close()
        except:
            print(f"Error: no fue posible adjuntar al correo el archivo {filename}")
            # raise Exception(f"Error: no fue posible adjuntar al correo el archivo {filename}")

    # metodo que envia el email
    def send_email(self):
        self.build_email()
        remitente       = self.sender_username + "@" + self.sender_domain
        destinatario    = self.destination_username + "@" + self.destination_domain

        smtp = smtplib.SMTP_SSL(SMTP_SSL)
        smtp.login(remitente, EMAIL_PASSWORD) # para enviar correo desde la cuenta formacionvirtualcsf@gmail.com

        smtp.sendmail(remitente, destinatario, self.email_message.as_string())
        smtp.quit()

if __name__ == '__main__':
    correo = Correo()
    correo.send_email()
