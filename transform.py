from reportlab.lib.pagesizes import landscape, A6
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Table, TableStyle, Image
from reportlab.lib import colors
import random
import string

def generate_random_words():
    # Generar palabras aleatorias
    word_length = random.randint(5, 10)
    return ''.join(random.choice(string.ascii_letters) for _ in range(word_length))

def create_pdf(output_filename, image_path):
    # Tamaño de la página A6 en formato apaisado
    width, height = landscape(A6)

    # Crear el objeto SimpleDocTemplate en formato apaisado sin márgenes
    pdf_document = SimpleDocTemplate(output_filename, pagesize=landscape(A6), leftMargin=0, rightMargin=0, bottomMargin=0, topMargin=0)

    # Crear un PageTemplate con la imagen de fondo
    background_frame = Frame(0, 0, width, height, showBoundary=0)
    background_template = PageTemplate(id='background_template', frames=[background_frame])

    # Agregar la imagen de fondo al PageTemplate usando el lienzo
    def add_background(canvas, doc):
        canvas.drawImage(image_path, 0, 0, width, height)

    background_template.beforeDrawPage = add_background

    # Añadir el PageTemplate al documento
    pdf_document.addPageTemplates([background_template])

    # Datos de la tabla
    table_data = [
        [generate_random_words(), '', '', '', '', ''],
        ['', '', '', '', '', '']
    ]

    # Crear la tabla
    table = Table(table_data, colWidths=[width/6]*6, rowHeights=[height*0.05]*2)
    table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Agregar la tabla al contenido del documento
    pdf_content = [table]

    # Construir el documento PDF
    pdf_document.build(pdf_content)

if __name__ == "__main__":
    # Nombre del archivo de salida PDF
    output_filename = "documento_a6_con_tabla.pdf"

    # Ruta de la imagen de fondo
    image_path = "alella.jpg"  # Reemplazar con la ruta de tu imagen

    # Crear el PDF con la imagen de fondo y la tabla en la parte inferior
    create_pdf(output_filename, image_path)
