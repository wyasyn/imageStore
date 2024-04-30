from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid  # To generate unique filenames
from waitress import serve

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded files

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        # Generate a unique filename to avoid overwriting existing files
        unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)

        # Construct the image URL
        image_url = request.url_root + file_path

        return jsonify({'message': 'File uploaded successfully', 'image_url': image_url}), 200

@app.route('/uploads/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    serve(app, host="0.0.0.0")
