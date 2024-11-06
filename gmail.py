import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email_with_attachment(sender_email, receiver_email, subject, body, attachment_file_path, sender_password):
    # Crear el objeto MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el archivo
    try:
        # Abrir el archivo en modo binario
        with open(attachment_file_path, 'rb') as attachment:
            # Crear el objeto MIME para el archivo adjunto
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)  # Codificar el archivo adjunto
            part.add_header('Content-Disposition', f'attachment; filename={attachment_file_path.split("/")[-1]}')

            # Adjuntar el archivo al mensaje
            msg.attach(part)
            print ("Mensaje preparado con éxito")
    except Exception as e:
        print(f"Error al adjuntar el archivo: {e}")
        return False

    # Conectar con el servidor SMTP de Gmail
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Iniciar conexión segura
            server.login(sender_email, sender_password)  # Iniciar sesión en Gmail
            text = msg.as_string()  # Convertir el mensaje a una cadena
            server.sendmail(sender_email, receiver_email, text)  # Enviar el correo
            print("Correo enviado con éxito.")
            return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False
   