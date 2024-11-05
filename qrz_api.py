import requests
import xml.etree.ElementTree as ET

# Variable global debug
debug = False  # Cambiar a False para desactivar las impresiones

# Función para imprimir solo si debug es True
def debug_print(message):
    if debug:
        print(message)

def get_api_key(username, password):
    # URL para la llamada GET
    url = "https://xmldata.qrz.com/xml/current/"

    # Parámetros a enviar en la solicitud GET
    params = {
        'username': username,
        'password': password
    }

    # Mostrar la petición GET completa solo si debug está activado
    debug_print(f"Realizando la petición GET a: {url} con los parámetros: {params}")

    # Realizar la solicitud GET
    response = requests.get(url, params=params)

    # Imprimir la respuesta completa del servidor solo si debug está activado
    debug_print("Respuesta del servidor:")
    debug_print(response.text)  # Esto imprimirá el contenido XML completo

    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        try:
            # Parsear el XML de la respuesta
            root = ET.fromstring(response.text)

            # El espacio de nombres en el XML (namespace)
            namespaces = {'ns': 'http://xmldata.qrz.com'}

            # Buscar el campo <Key> en el XML usando el espacio de nombres
            key_element = root.find('.//ns:Session/ns:Key', namespaces)

            # Si el campo <Key> se encuentra, devolver su valor
            if key_element is not None:
                api_key = key_element.text
                debug_print(f"Valor de Key: {api_key}")
                return api_key
            else:
                raise ValueError("Campo <Key> no encontrado en la respuesta XML.")
        except ET.ParseError:
            raise ValueError("Error al parsear el XML de la respuesta.")
    else:
        raise ValueError(f"Error en la solicitud GET: {response.status_code}")

def consulta_email(apikey, call):

    # URL para la llamada GET
    url = "https://xmldata.qrz.com/xml/current/"

    # Parámetros para la consulta con la key y el callsign
    params = {
        's': apikey,
        'callsign': call
    }

    # Mostrar la petición GET completa solo si debug está activado
    debug_print(f"Realizando la petición GET a: {url} con los parámetros: {params}")

    # Realizar la solicitud GET
    response = requests.get(url, params=params)

    # Imprimir la respuesta completa del servidor solo si debug está activado
    debug_print("Respuesta del servidor para consulta_email:")
    debug_print(response.text)  # Esto imprimirá el contenido XML completo

    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        try:
            # Parsear el XML de la respuesta
            root = ET.fromstring(response.text)

            # El espacio de nombres en el XML (namespace)
            namespaces = {'ns': 'http://xmldata.qrz.com'}

            # Buscar el campo <email> en el XML usando el espacio de nombres
            email_element = root.find('.//ns:Callsign/ns:email', namespaces)

            # Si el campo <email> se encuentra, devolver su valor
            if email_element is not None:
                debug_print(f"El email de {call} es: {email_element.text}")
                return email_element.text
            else:
                debug_print(f"No se encontró el campo <email> para el callsign {call}.")
                return None
        except ET.ParseError:
            debug_print("Error al parsear el XML de la respuesta.")
            return None
    else:
        debug_print(f"Error en la solicitud GET para consulta_email: {response.status_code}")
        return None
