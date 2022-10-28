from email.message import EmailMessage
import smtplib

def enviar_email(email_destino,codigo):
    remitente = "julcastel@hotmail.com"
    destinatario = email_destino
    mensaje = "Ingrese el Siguiente Codigo: "+codigo+" Para Activar Su Cuenta http://localhost:5000/validar"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Codigo de Activacion"
    email.set_content(mensaje)
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "130710384julio")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()

def recuperar_email(email_destino):
    remitente = "julcastel@hotmail.com"
    destinatario = email_destino
    mensaje = "<h2>Correo de Restablecimiento de Contraseña</h2>"
    mensaje=mensaje+"<br>"
    mensaje=mensaje+ "<a href='http://localhost:5000/restablecer/"+email_destino+"'>Clic para el Restablecimiento de Contraseña</a>"
    mensaje=mensaje+"<hr>"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Link restablecimiento de contraseña"
    email.set_content(mensaje, subtype="html")
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "130710384julio")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()