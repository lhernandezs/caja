import os.path
import smtplib

from email.message          import EmailMessage
from email.headerregistry   import Address
from email.mime.base        import MIMEBase
from email                  import encoders
from jinja2                 import Environment, select_autoescape, FileSystemLoader

from modelo                 import DatosCorreoJuicios
from config                 import TEMPLATES_FOLDER, SMTP_SSL, SENDER_USERNAME, EMAIL_PASSWORD, SENDER_DOMAIN, SENDER_DISPLAY_NAME, SUBJECT, TEMPLATES, EXTENSION_EXCEL_365
from config                 import Config

class Correo:

    UPLOAD_FOLDER = Config.UPLOAD_FOLDER
    ENV = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER), autoescape=select_autoescape())

    def __init__(self, 
                 destination_username           : str, 
                 destination_domain             : str, 
                 destination_display_name       : str, 
                 **kawargs):
                        
        self.destination_username       = destination_username
        self.destination_domain         = destination_domain
        self.destination_display_name   = destination_display_name

        self.attach                     = kawargs.get("attach", False)
        self.ficha                      = kawargs.get("ficha", "")

        self.body                       = kawargs.get("body", "")
        template                        = kawargs.get("template", -1)      

        self.subject                    = kawargs.get("subject", SUBJECT)

        if template == -1 and self.body == "":
            raise Exception("Debe especificar un template o un body para el correo")
        if template != -1 and self.body != "":
            raise Exception("No puede especificar un template y un body para el correo")
        if template != -1 and not template in TEMPLATES:
            raise Exception(f"El template {template} no existe")    
        
        if self.attach and self.ficha == "":
            raise Exception("Si attach es True, debe especificar la ficha para adjuntar el archivo")
        
        self.template                   = TEMPLATES.get(template, "")
        self.datos_correo               = kawargs.get("datos_correo", DatosCorreoJuicios()) 


    def render_html(self):
        return Correo.ENV.get_template(self.template).render(datos_correo=self.datos_correo, asunto = self.subject)
    
    def create_email_message(self) -> EmailMessage:
        email_message            = EmailMessage()
        email_message["From"]    = Address(username=SENDER_USERNAME, domain=SENDER_DOMAIN, display_name=SENDER_DISPLAY_NAME)
        email_message["To"]      = Address(username=self.destination_username, domain=self.destination_domain, display_name=self.destination_display_name)

        if not self.body == "":
            html_body = """
                    <html>
                    <body>
                        <h1>¡Hola desde Python!</h1>
                        <p>Este es un mensaje en formato <b>HTML</b>.</p>
                        <p>Puedes incluir texto en <i>cursiva</i>, <strong>negrita</strong>, y <a href="https://www.ejemplo.com">enlaces</a>.</p>
                    </body>
                    </html>
                    """
            email_message.set_content(html_body, subtype='html')
        else:
            email_message.add_alternative(self.render_html(), subtype="html")

       if self.attach:

        email_message["Subject"] = f"{self.subject} {self.datos_correo.ficha}"

        if not self.ficha == "":
            filename = f"{self.datos_correo.ficha}.{EXTENSION_EXCEL_365}"
            try:
                part = MIMEBase('application', 'octet-stream')
                file = open(os.path.join(Correo.UPLOAD_FOLDER, filename ), 'rb')
                part.set_payload((file).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename = filename)
                email_message.attach(part)
                file.close()
            except:
                print(f"Error: no fue posible adjuntar al correo el archivo {filename}")
                # raise Exception(f"Error: no fue posible adjuntar al correo el archivo {filename}")
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
    datos_correo =  DatosCorreoJuicios(
                ficha           = '2879836'                         , 
                instructores    = ['instructor1', 'instructor2']    , 
                activos         = ['activo1', 'activo2']            , 
                desertores      = ['desertor1', 'desertor2']
                )
    template        = 1
    correo = Correo(destination_username, destination_domain, destination_display_name, datos_correo, template)
    correo = Correo(destination_username, destination_domain, destination_display_name, body="Este es el cuerpo del correo")
    # print(correo.render_html())
    correo.send_email()
