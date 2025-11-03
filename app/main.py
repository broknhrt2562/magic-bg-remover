from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from rembg import remove
from PIL import Image
import io
import uuid
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/remove-bg', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            unique_id = str(uuid.uuid4())[:8]
            new_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}{file_ext}"
            
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(input_path)
            
            output_filename = f"processed_{new_filename}"
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
            
            with open(input_path, 'rb') as i:
                with open(output_path, 'wb') as o:
                    input_image = i.read()
                    output_image = remove(input_image)
                    o.write(output_image)
            
            processed_url = f'/processed/{output_filename}'
            return jsonify({
                'success': True,
                'processed_url': processed_url,
                'filename': f'no-bg-{new_filename}'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    print("Starting Background Remover application...")
    app.run(debug=True, host='0.0.0.0', port=5001)