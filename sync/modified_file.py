import os
import hashlib
from flask import Flask, request, send_from_directory, jsonify
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")  # Secure: Read from environment

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        print(f"[UPLOAD] File saved to: {filepath}")

        with open(filepath, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        return jsonify({
            'message': 'File uploaded',
            'filename': filename,
            'md5': file_hash
        }), 201

    return jsonify({'message': 'Invalid file type'}), 400

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({'files': files})

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404

@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return jsonify({'message': 'File not found'}), 404

    os.remove(path)
    print(f"[DELETE] Deleted file: {path}")
    return jsonify({'message': f'{filename} deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
