import configparser
import os
import argparse
import logging
from utils.qrzapi import consulta_email, get_api_key
from utils.transform import extraer_campos, create_pdf
from utils.gmail import send_email_with_attachment

# Cargar la configuración desde config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Obtener el nivel de logging desde el archivo de configuración
loglevel_str = config.get('logging', 'loglevel', fallback='INFO').upper()
loglevel = getattr(logging, loglevel_str, logging.INFO)  # Convertir a nivel de logging válido

# Configurar el logging para guardar en execution.log y mostrar en la terminal
logging.basicConfig(
    level=loglevel,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execution.log"),
        logging.StreamHandler()  # Agrega salida de logging en la terminal
    ]
)

# Configuración de argparse para recibir los archivos .qsl y .adi como parámetros
parser = argparse.ArgumentParser(description="Procesa un archivo .adi para generar y enviar QSLs.")
parser.add_argument("qsl_file", type=str, help="Ruta del archivo de imagen de fondo QSL")
parser.add_argument("adi_file", type=str, help="Ruta del archivo .adi a procesar")
args = parser.parse_args()

apikey = get_api_key(config['qrz']['username'], config['qrz']['password'])

# Inicializar contadores y lista de fallos
emails_enviados = 0
emails_fallidos = 0
callsign_fallidos = []

if __name__ == "__main__":
    # Usar el archivo QSL especificado por el usuario
    image_path = args.qsl_file

    # Crear carpeta de salida si no existe
    output_folder = config['qsl']['outputfolder']
    os.makedirs(output_folder, exist_ok=True)

    # Extraer los datos de los registros usando el archivo .adi pasado como parámetro
    registros = extraer_campos(args.adi_file)

    # Crear un PDF individual por cada registro extraído
    for registro in registros:
        call_sign = registro[0]  # Suponemos que CALL es el primer elemento del registro
        # Nombre del archivo usando CALL, asegurando que no tenga caracteres inválidos
        safe_call_sign = "".join(c for c in call_sign if c.isalnum() or c in ("_", "-"))  # Filtrar caracteres inválidos
        email = consulta_email(apikey, safe_call_sign)  # Obtener el email usando la función que ahora llama a get_api_key internamente
        if email:
            logging.info(f"El email del callsign {safe_call_sign} es: {email}")
            output_filename = os.path.join(output_folder, f"{safe_call_sign}.pdf")  # Ruta completa del archivo
            create_pdf(output_filename, image_path, registro)
            qlsfile = output_folder + '/' + safe_call_sign + '.pdf'
            subject = 'New QSL card from ' + config['qrz']['username'] + ' to ' + safe_call_sign
            
            try:
                # Intentar enviar el email con adjunto
                send_email_with_attachment(
                    config['gmail']['sender_email'],
                    email,
                    subject,
                    config['gmail']['mail_body'],
                    qlsfile,
                    config['gmail']['sender_password'],
                    config['gmail']['smtp_server']
                )
                emails_enviados += 1  # Incrementar el contador de emails enviados exitosamente
                logging.info(f"Email enviado exitosamente a {safe_call_sign}.")
            except Exception as e:
                # En caso de fallo al enviar, actualizar el contador y la lista de fallos
                emails_fallidos += 1
                callsign_fallidos.append(safe_call_sign)
                logging.error(f"Error al enviar email a {safe_call_sign}: {e}")
            
            # Eliminar el archivo PDF después de enviarlo o al intentarlo
            try:
                os.remove(qlsfile)
                logging.info(f"Archivo {qlsfile} eliminado exitosamente.")
            except OSError as e:
                logging.error(f"Error al eliminar el archivo {qlsfile}: {e}")
        else:
            # Si no se pudo obtener el email
            emails_fallidos += 1
            callsign_fallidos.append(safe_call_sign)
            logging.warning(f"No se pudo obtener el email para el callsign {safe_call_sign}.")

    # Mostrar resumen de envíos al finalizar el proceso
    logging.info("Resumen de envío de emails:")
    logging.info(f"Emails enviados exitosamente: {emails_enviados}")
    logging.info(f"Emails fallidos: {emails_fallidos}")
    if callsign_fallidos:
        logging.info("Lista de callsigns fallidos:")
        for callsign in callsign_fallidos:
            logging.info(f" - {callsign}")