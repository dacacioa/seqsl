import string
import os
import logging
from reportlab.lib.pagesizes import A6, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.platypus.frames import Frame
from reportlab.platypus import PageTemplate
from reportlab.lib.units import mm

def create_pdf(output_filename, image_path, registro):
    try:
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

        # Imprimir mensaje de éxito en la creación del PDF
        logging.info(f"PDF '{output_filename}' generado correctamente.")

    except Exception as e:
        # Imprimir mensaje de error en caso de fallo
        logging.error(f"Error al generar el PDF '{output_filename}': {e}")

def extraer_campos(nombre_fichero):
    # Lista para almacenar los valores extraídos de cada campo
    datos_extraidos = []

    # Abrir el fichero en modo lectura
    with open(nombre_fichero, 'r', encoding='utf-8') as archivo:
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
