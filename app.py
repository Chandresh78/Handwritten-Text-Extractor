from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import easyocr
import io

app = Flask(__name__)
CORS(app)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        app.logger.error('No image file provided')
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))
    
    app.logger.info('Image received and opened successfully')
    
    try:
        results = reader.readtext(image)
        extracted_text = "\n".join([result[1] for result in results])
        app.logger.info('Text extraction successful')
        return jsonify({"extracted_text": extracted_text})
    except Exception as e:
        app.logger.error(f'Error during text extraction: {e}')
        return jsonify({"error": "Failed to extract text"}), 500

if __name__ == '__main__':
    app.run(debug=True)
