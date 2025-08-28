import os.path
import json
import smtplib

from email.message          import EmailMessage
from email.headerregistry   import Address
from email.mime.base        import MIMEBase
from email                  import encoders
from jinja2                 import Environment, select_autoescape, FileSystemLoader

from modelo                 import DatosCorreo

class Correo:
    # variable de entorno para la API de jinja2
    ENV = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
    # constructor de la clase - cada correo tiene un email que recibe, un servidor que recibe, un nombre del que recibe y el modelo con los datos
    def __init__(self, tipo, emaRec, serRec, namRec, datosCorreo: DatosCorreo):
        with open(os.path.join('json', 'sercorreo.json'), 'r') as conex:
            arc = json.load(conex)
        
        self._emaEnv        = arc[tipo]["emailRemitente"] 
        self._serEnv        = arc[tipo]["servidorRemitente"] 
        self._namEnv        = arc[tipo]["nombreRemitente"] 
        self._asunto        = arc[tipo]["asunto"] 
        self._templa        = arc[tipo]["template"]

        self._emaRec        = emaRec            # email destino
        self._serRec        = serRec            # servidor destino
        self._namRec        = namRec            # nombre destino
        self._datosCorreo   = datosCorreo       # datos del correo
        
        self._email_message = EmailMessage()    # contiene el empaquetado que se va a enviar 

    # renderiza la plantilla -template- con los datos -modelo-
    def render_html(self):
        return Correo.ENV.get_template(self._templa).render(datosCorreo=self._datosCorreo, asunto = self._asunto)

    # construye el cuerpo del email con los datos pasados en el parametro
    def build_email(self, ficha: int = None):
        self._email_message["Subject"]    = f"{self._asunto} {ficha}"
        self._email_message["From"]       = Address(username=self._emaEnv, domain=self._serEnv, display_name=self._namEnv)
        self._email_message["To"]         = Address(username=self._emaRec, domain=self._serRec, display_name=self._namRec)
        html_data: str                    = self.render_html()
        self._email_message.add_alternative(html_data, subtype="html")

        if ficha:
            part = MIMEBase('application', 'octet-stream')
            archivo = open(os.path.join('upload', f"{ficha}.xlsx" ), 'rb')
            part.set_payload((archivo).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename = f"{ficha}.xlsx")
            self._email_message.attach(part)
            archivo.close()

    # metodo que envia el email
    def send_email(self, ficha: int = None):
        self.build_email(ficha)
        remitente       = self._emaEnv + "@" + self._serEnv
        destinatario    = self._emaRec + "@" + self._serRec

        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(remitente, "ddycjigkgqrtsray") # para enviar correo desde la cuenta formacionvirtualcsf@gmail.com
        smtp.sendmail(remitente, destinatario, self._email_message.as_string())
        smtp.quit()


if __name__ == '__main__':
    pass
