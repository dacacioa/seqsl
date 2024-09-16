import random
import string
from reportlab.lib.pagesizes import A6, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.platypus.frames import Frame
from reportlab.platypus import PageTemplate
from reportlab.lib.units import mm

def generate_random_words():
    # Generar palabras aleatorias
    word_length = random.randint(5, 10)
    return ''.join(random.choice(string.ascii_letters) for _ in range(word_length))

def create_pdf(output_filename, image_path):
    # Tamaño de la página A6 en formato apaisado
    width, height = landscape(A6)

    # Crear el objeto SimpleDocTemplate en formato apaisado sin márgenes
    pdf_document = SimpleDocTemplate(output_filename, pagesize=landscape(A6), leftMargin=0, rightMargin=0, bottomMargin=0, topMargin=0)

    # Márgenes laterales que deseas aplicar (en mm)
    left_margin = 10 * mm
    right_margin = 10 * mm

    # Crear un PageTemplate con la imagen de fondo
    def add_background(canvas, doc):
        canvas.drawImage(image_path, 0, 0, width, height)

    background_frame = Frame(0, 0, width, height, showBoundary=0)
    background_template = PageTemplate(id='background_template', frames=[background_frame], onPage=add_background)

    # Añadir el PageTemplate al documento
    pdf_document.addPageTemplates([background_template])

    # Datos de la tabla
    table_data = [
        ['Date', 'UTC', 'Band', 'Mode', 'RST', 'QSL'],
        ['16/09/2024', '10:00', '20m', 'FT8', '59', '']
    ]

    # Crear la tabla con márgenes laterales ajustando los anchos de las columnas
    table = Table(table_data, colWidths=[(width - left_margin - right_margin) / 6] * 6, rowHeights=[height * 0.05] * 2)

    # Estilo de la tabla: fondo negro y letras blancas en la primera y segunda fila, texto centrado
    table.setStyle(TableStyle([
        # Estilo para la primera fila
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        
        # Estilo para la segunda fila
        ('BACKGROUND', (0, 1), (-1, 1), colors.black),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.white),
        
        # Alineación del texto
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        
        # Bordes y cuadrícula en color blanco
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('BOX', (0, 0), (-1, -1), 1, colors.white)
    ]))

    # Espaciador para controlar el espacio antes de la tabla
    space_above_table = height - (height * 0.15)  # Ajusta el porcentaje para controlar la posición (15%)

    # Crear un spacer y añadir la tabla, dejando márgenes laterales
    pdf_content = [
        Spacer(1, space_above_table),  # Espacio encima de la tabla
        table
    ]

    # Construir el documento PDF
    pdf_document.build(pdf_content)

if __name__ == "__main__":
    # Nombre del archivo de salida PDF
    output_filename = "output.pdf"

    # Ruta de la imagen de fondo
    image_path = "alella.jpg"  # Reemplazar con la ruta de tu imagen

    # Crear el PDF con la imagen de fondo y la tabla en la parte inferior con márgenes laterales
    create_pdf(output_filename, image_path)
