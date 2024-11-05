import random
import string
import os
from reportlab.lib.pagesizes import A6, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.platypus.frames import Frame
from reportlab.platypus import PageTemplate
from reportlab.lib.units import mm
from qrz_api import consulta_email, get_api_key

def generate_random_words():
    # Generar palabras aleatorias
    word_length = random.randint(5, 10)
    return ''.join(random.choice(string.ascii_letters) for _ in range(word_length))

def create_pdf(output_filename, image_path, registro):
    # Tamaño de la página A6 en formato apaisado
    width, height = landscape(A6)

    # Crear el objeto SimpleDocTemplate en formato apaisado sin márgenes
    pdf_document = SimpleDocTemplate(output_filename, pagesize=landscape(A6), leftMargin=0, rightMargin=0, bottomMargin=0, topMargin=0)

    # Márgenes laterales
    left_margin = 10 * mm
    right_margin = 10 * mm

    # Crear un PageTemplate con la imagen de fondo
    def add_background(canvas, doc):
        canvas.drawImage(image_path, 0, 0, width, height)

    background_frame = Frame(0, 0, width, height, showBoundary=0)
    background_template = PageTemplate(id='background_template', frames=[background_frame], onPage=add_background)
    pdf_document.addPageTemplates([background_template])

    # Datos de la tabla: cabecera y datos del registro individual
    table_data = [
        ['Station', 'Date', 'Time', 'Freq', 'Mode', 'RST'],
        registro  # Agregamos el registro como fila en la tabla
    ]

    # Crear la tabla ajustando los anchos de las columnas
    table = Table(table_data, colWidths=[(width - left_margin - right_margin) / 6] * 6, rowHeights=[height * 0.05] * 2)

    # Estilo de la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#FFFFFFFB")),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('BOX', (0, 0), (-1, -1), 1, colors.white)
    ]))

    # Espaciador para controlar el espacio antes de la tabla
    space_above_table = height - (height * 0.15)

    # Crear el contenido del PDF con espaciador y tabla
    pdf_content = [
        Spacer(1, space_above_table),
        table
    ]

    # Construir el documento PDF
    pdf_document.build(pdf_content)

def extraer_campos(nombre_fichero):
    # Lista para almacenar los valores extraídos de cada campo
    datos_extraidos = []

    # Abrir el fichero en modo lectura
    with open(nombre_fichero, 'r') as archivo:
        for linea in archivo:
            registro = []
            campos = {
                "CALL": "<CALL",
                "QSO_DATE": "<QSO_DATE",
                "TIME_ON": "<TIME_ON",
                "FREQ": "<FREQ",
                "MODE": "<MODE",
                "RST_SENT": "<RST_SENT"
            }
            
            for etiqueta in campos.values():
                inicio = linea.find(etiqueta)
                if inicio != -1:
                    inicio_valor = linea.find(">", inicio) + 1
                    fin_valor = linea.find(" ", inicio_valor)
                    if fin_valor == -1:
                        fin_valor = len(linea)
                    valor = linea[inicio_valor:fin_valor]
                    
                    if etiqueta == "<QSO_DATE":
                        # Separar la fecha y formatear de YYYYMMDD a DD-MM-YYYY
                        fecha = f"{valor[6:8]}-{valor[4:6]}-{valor[0:4]}"
                        registro.append(fecha)  # Agregar fecha al registro
                    elif etiqueta == "<TIME_ON":
                        # Transformar TIME_ON de HHMMSS a HH:MM:SS
                        hora = f"{valor[:2]}:{valor[2:4]}:{valor[4:6]}"
                        registro.append(hora)  # Agregar hora al registro
                    else:
                        registro.append(valor)
            
            if registro:
                datos_extraidos.append(registro)

    return datos_extraidos

# Datos para la autenticación
username = 'kk'
password = 'kk'

apikey = get_api_key(username, password)

if __name__ == "__main__":
    # Ruta de la imagen de fondo
    image_path = "alella.jpg"  # Reemplazar con la ruta de tu imagen

    # Crear carpeta de salida si no existe
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Extraer los datos de los registros
    registros = extraer_campos('qso.adi')

    # Crear un PDF individual por cada registro extraído
    for registro in registros:
        call_sign = registro[0]  # Suponemos que CALL es el primer elemento del registro
        # Nombre del archivo usando CALL, asegurando que no tenga caracteres inválidos
        safe_call_sign = "".join(c for c in call_sign if c.isalnum() or c in ("_", "-"))  # Filtrar caracteres inválidos
        email = consulta_email(apikey, safe_call_sign) # Obtener el email usando la función que ahora llama a get_api_key internamente
        if email:
            print(f"El email del callsign {safe_call_sign} es: {email}")
            output_filename = os.path.join(output_folder, f"{safe_call_sign}.pdf")  # Ruta completa del archivo
            create_pdf(output_filename, image_path, registro)
        else:
            print(f"No se pudo obtener el email para el callsign {safe_call_sign}.")

