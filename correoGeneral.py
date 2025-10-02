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

    def __init__(self, destination_username: str, destination_domain: str, destination_display_name: str, subject: str, mensaje: str):
        self.sender_username            = SENDER_USERNAME 
        self.sender_domain              = SENDER_DOMAIN
        self.sender_display_name        = SENDER_DISPLAY_NAME
        self.subject                    = SUBJECT
  
        self.destination_username       = destination_username
        self.destination_domain         = destination_domain
        self.destination_display_name   = destination_display_name
        self.subject                    = subject
        self.mensaje                    = mensaje   
    
    def create_email_message(self, file_adjunto) -> EmailMessage:

        # Creación del cuerpo del mensaje en HTML
        html_body = """
        <html>
        <body>
            <h1>¡Hola desde Python!</h1>
            <p>Este es un mensaje en formato <b>HTML</b>.</p>
            <p>Puedes incluir texto en <i>cursiva</i>, <strong>negrita</strong>, y <a href="https://www.ejemplo.com">enlaces</a>.</p>
        </body>
        </html>
        """

        email_message            = EmailMessage()         
        email_message["From"]    = Address(username=self.sender_username, domain=self.sender_domain, display_name=self.sender_display_name)
        email_message["To"]      = Address(username=self.destination_username, domain=self.destination_domain, display_name=self.destination_display_name)
        email_message["Subject"] = self.subject
        email_message.set_content(html_body, subtype='html')

        filename = f"2879836.{EXTENSION_EXCEL_365}"
        if file_adjunto:
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

    def send_email(self, file_adjunto: bool = True):
        remitente       = self.sender_username + "@" + self.sender_domain
        destinatario    = self.destination_username + "@" + self.destination_domain
        email_message   = self.create_email_message(file_adjunto)
        smtp            = smtplib.SMTP_SSL(SMTP_SSL)
        smtp.login(remitente, EMAIL_PASSWORD)
        smtp.sendmail(remitente, destinatario, email_message)
        smtp.quit()

if __name__ == '__main__':
    destination_username        = 'lhernandezs'
    destination_domain          = 'sena.edu.co'
    destination_display_name    = 'LeonardoHS'
    correo = Correo(destination_username, destination_domain, destination_display_name, "Asunto del correo", "Cuerpo del correo")
    correo.send_email(False)
