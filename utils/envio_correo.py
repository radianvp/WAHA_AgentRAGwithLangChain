#gmail
from email.message import EmailMessage
import smtplib

##Obtener el api key
from dotenv import load_dotenv
import os


class EnvioCorreo:
    load_dotenv()
    ##credenciales
    APP_PASSWORD_GMAIL=os.getenv("APP_PASSWORD_GMAIL")
    CORREO_REMITENTE=os.getenv("EMAIL_REMITENTE")

    def enviar_correo(self, nombre_lead,correo_lead,mensaje_para_lead):
        try:
            remitente = self.CORREO_REMITENTE #host
            destinatario = correo_lead
            mensaje = mensaje_para_lead

            email = EmailMessage()
            email["From"] = remitente
            email["To"] = destinatario
            email["Subject"] = "Mensaje Importante de Datapath para ti " + nombre_lead
            email.set_content(mensaje)
            smtp = smtplib.SMTP_SSL("smtp.gmail.com")
            smtp.login(remitente, self.APP_PASSWORD_GMAIL)
            smtp.sendmail(remitente, destinatario, email.as_string())
            smtp.quit()
            return True
        except Exception as e:
            print(e)
            return False

#if __name__ == '__main__':
#    enviador = EnvioCorreo()
#    enviador.enviar_correo(nombre_lead = "Jeanpier Ancori",correo_lead = "radianstk@gmail.com",mensaje_para_lead="Hola en breve nuestro asesor se va a comunicar contigo")