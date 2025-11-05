import os.path
import smtplib

from email.message          import EmailMessage
from email.headerregistry   import Address
from email.mime.base        import MIMEBase
from email                  import encoders
from jinja2                 import Environment, select_autoescape, FileSystemLoader

from modelo                 import DatosCorreoJuicios
from config                 import Config, TEMPLATES_FOLDER, SMTP_SSL, SENDER_USERNAME, EMAIL_PASSWORD, SENDER_DOMAIN, SENDER_DISPLAY_NAME, SUBJECT, TEMPLATES, EXTENSION_EXCEL_365

class Correo:
    UPLOAD_FOLDER           = Config.UPLOAD_FOLDER
    ENV                     = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER), autoescape=select_autoescape())

    def __init__(self                                , 
                 destination_username           : str, 
                 destination_domain             : str, 
                 destination_display_name       : str, 
                 **kawargs):
                        
        self.destination_username               = destination_username
        self.destination_domain                 = destination_domain
        self.destination_display_name           = destination_display_name

        self.body                               = kawargs.get("body", "No se especificó el cuerpo del mensaje ni template")
        self.datos_correo : DatosCorreoJuicios  = kawargs.get("datos_correo", False) 

        indice_template                         = kawargs.get("template", -1)      
        if indice_template >= 0:
            if indice_template in range(len(TEMPLATES)):
                self.template                   = TEMPLATES[indice_template]
                if self.datos_correo:
                    self.subject                = SUBJECT
                    self.filename               = f"{self.datos_correo.ficha}.{EXTENSION_EXCEL_365}"
                else:
                    self.body                   = "No se enviaron los Datos del Correo"
            else:
                self.body                       = "El TEMPLATE indicado para el cuerpo del mensaje no existe"
        else:
            self.template                       = False
            self.subject                        = kawargs.get("subject","No se espeficó ASUNTO para el correo")
            self.ficha                          = kawargs.get("ficha", False)
            if self.ficha:
                self.filename                   = f"{self.ficha}.{EXTENSION_EXCEL_365}"
            else:
                self.filename                   = False

    def render_html(self):
        return Correo.ENV.get_template(self.template).render(datos_correo=self.datos_correo, asunto = self.subject)
    
    def create_email_message(self) -> EmailMessage:
        email_message            = EmailMessage()
        email_message["From"]    = Address(username=SENDER_USERNAME, domain=SENDER_DOMAIN, display_name=SENDER_DISPLAY_NAME)
        email_message["To"]      = Address(username=self.destination_username, domain=self.destination_domain, display_name=self.destination_display_name)
        email_message["Subject"] = self.subject

        if self.template:
            email_message.add_alternative(self.render_html(), subtype="html")
        else:
            email_message.add_alternative(self.body, subtype='html')

        if self.filename:
            try:
                part = MIMEBase('application', 'octet-stream')
                file = open(os.path.join(Correo.UPLOAD_FOLDER, self.filename ), 'rb')
                part.set_payload((file).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename = self.filename)
                email_message.attach(part)
                file.close()
            except:
                print(f"Error: no fue posible adjuntar al correo el archivo {self.filename}")
                # raise Exception(f"Error: no fue posible adjuntar al correo el archivo {self.filename}")
        return email_message.as_string()

    def send_email(self):
        remitente       = SENDER_USERNAME + "@" + SENDER_DOMAIN
        destinatario    = self.destination_username + "@" + self.destination_domain
        email_message   = self.create_email_message()
        smtp            = smtplib.SMTP_SSL(SMTP_SSL)
        smtp.login(remitente, EMAIL_PASSWORD)
        smtp.sendmail(remitente, destinatario, email_message)
        smtp.quit()

if __name__ == '__main__':
    destination_username        = 'lhernandezs'
    destination_domain          = 'sena.edu.co'
    destination_display_name    = 'LeonardoHS'

    ficha                       = "2977746"

    con_template = False
    if con_template:
        datos_correo =  DatosCorreoJuicios(
                    ficha           = ficha                             ,
                    instructores    = ['instructor1', 'instructor2']    , 
                    activos         = ['activo1', 'activo2']            , 
                    desertores      = ['desertor1', 'desertor2']
                    )
        correo = Correo(destination_username, destination_domain, destination_display_name, **{"datos_correo": datos_correo, "template": 0})
    else:
        body    = "este es el texto del correo"
        subject = "este es el asunto del correo"

        correo = Correo(destination_username, destination_domain, destination_display_name, **{"body": body, "subject": subject, "ficha": ficha})

    correo.send_email()
