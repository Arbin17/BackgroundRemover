from flask import Flask, request, render_template, send_file, redirect,url_for
import os
import cv2
import numpy as np
from rembg import remove
from PIL import Image
app = Flask(__name__)

# Create a directory to save uploaded images
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        output_path = remove_background(file_path)
        return redirect(url_for('show_image', filename=os.path.basename(output_path)))

@app.route('/uploads/<filename>')
def show_image(filename):
    # Render the template with the processed image filename
    return render_template('show_image.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)


def remove_background(file_path):
    
    with Image.open(file_path) as img:
        # Remove the background
        output = remove(img)
        
        # Save the result
        output_path = os.path.join(UPLOAD_FOLDER, 'output.png')
        output.save(output_path)
    return output_path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
