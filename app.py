from flask import Flask, render_template, request, send_file
import os
import fitz
from PIL import Image

app = Flask(__name__)

def pdf_to_png(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap()
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        image.save(image_path)
    pdf_document.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join('uploads', uploaded_file.filename)
            uploaded_file.save(file_path)
            output_folder = 'output'
            os.makedirs(output_folder, exist_ok=True)
            pdf_to_png(file_path, output_folder)
            return send_file(os.path.join(output_folder, 'page_1.png'), as_attachment=True)
    return 'Error'

if __name__ == '__main__':
    app.run(debug=True)
