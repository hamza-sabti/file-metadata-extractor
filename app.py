import os
import json
import magic
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
import PyPDF2
from PIL import Image
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'tiff': 'image/tiff',
    'webp': 'image/webp'
}

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_metadata(file_path):
    """Extract metadata from a file based on its type"""
    metadata = {}
    
    try:
        # Get basic file information
        file_stat = os.stat(file_path)
        metadata['file_size'] = file_stat.st_size
        metadata['creation_date'] = datetime.fromtimestamp(file_stat.st_ctime).isoformat()
        metadata['modification_date'] = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        metadata['file_path'] = str(file_path)
        
        # Detect file type using python-magic
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        metadata['mime_type'] = file_type
        
        # Extract file extension
        file_extension = Path(file_path).suffix.lower()
        metadata['file_extension'] = file_extension
        
        # Extract type-specific metadata
        if file_type == 'application/pdf':
            metadata.update(extract_pdf_metadata(file_path))
        elif file_type.startswith('image/'):
            metadata.update(extract_image_metadata(file_path))
        else:
            metadata['message'] = f"File type {file_type} is supported but no specific metadata extraction implemented"
            
    except Exception as e:
        metadata['error'] = str(e)
    
    return metadata

def extract_pdf_metadata(file_path):
    """Extract PDF-specific metadata"""
    pdf_metadata = {}
    
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get PDF info
            if pdf_reader.metadata:
                info = pdf_reader.metadata
                pdf_metadata['pdf_author'] = info.get('/Author', 'Unknown')
                pdf_metadata['pdf_creator'] = info.get('/Creator', 'Unknown')
                pdf_metadata['pdf_producer'] = info.get('/Producer', 'Unknown')
                pdf_metadata['pdf_title'] = info.get('/Title', 'Unknown')
                pdf_metadata['pdf_subject'] = info.get('/Subject', 'Unknown')
                pdf_metadata['pdf_creation_date'] = info.get('/CreationDate', 'Unknown')
                pdf_metadata['pdf_modification_date'] = info.get('/ModDate', 'Unknown')
            
            # Get page count
            pdf_metadata['pdf_page_count'] = len(pdf_reader.pages)
            
    except Exception as e:
        pdf_metadata['pdf_error'] = str(e)
    
    return pdf_metadata

def extract_image_metadata(file_path):
    """Extract image-specific metadata"""
    image_metadata = {}
    
    try:
        with Image.open(file_path) as img:
            # Get image dimensions
            image_metadata['image_width'] = img.width
            image_metadata['image_height'] = img.height
            image_metadata['image_mode'] = img.mode
            image_metadata['image_format'] = img.format
            
            # Get EXIF data if available
            if hasattr(img, '_getexif') and img._getexif():
                exif = img._getexif()
                if exif:
                    # Common EXIF tags
                    exif_tags = {
                        271: 'make',
                        272: 'model',
                        306: 'datetime',
                        36867: 'datetime_original',
                        33432: 'copyright'
                    }
                    
                    for tag_id, tag_name in exif_tags.items():
                        if tag_id in exif:
                            image_metadata[f'exif_{tag_name}'] = exif[tag_id]
            
            # Get color palette info for indexed images
            if img.mode == 'P' and img.palette:
                image_metadata['image_palette_mode'] = img.palette.mode
                image_metadata['image_palette_size'] = len(img.palette.palette)
                
    except Exception as e:
        image_metadata['image_error'] = str(e)
    
    return image_metadata

@app.route('/')
def index():
    """Render the main upload page"""
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Metadata Extractor</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }
            .upload-form {
                text-align: center;
                margin-bottom: 30px;
            }
            .file-input {
                margin: 20px 0;
                padding: 10px;
                border: 2px dashed #ddd;
                border-radius: 5px;
                background: #fafafa;
            }
            .submit-btn {
                background: #007bff;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            .submit-btn:hover {
                background: #0056b3;
            }
            .result {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 5px;
                white-space: pre-wrap;
                font-family: monospace;
                max-height: 500px;
                overflow-y: auto;
            }
            .supported-files {
                margin-top: 20px;
                padding: 15px;
                background: #e9ecef;
                border-radius: 5px;
            }
            .error {
                color: #dc3545;
                background: #f8d7da;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📁 File Metadata Extractor</h1>
            
            <div class="upload-form">
                <form method="POST" action="/upload" enctype="multipart/form-data">
                    <div class="file-input">
                        <input type="file" name="file" accept=".pdf,.png,.jpg,.jpeg,.gif,.bmp,.tiff,.webp" required>
                    </div>
                    <button type="submit" class="submit-btn">Extract Metadata</button>
                </form>
            </div>
            
            <div class="supported-files">
                <h3>Supported File Types:</h3>
                <ul>
                    <li><strong>PDFs:</strong> Author, Creator, Title, Page count, Creation date</li>
                    <li><strong>Images:</strong> Resolution, Format, Color mode, EXIF data (PNG, JPG, GIF, BMP, TIFF, WebP)</li>
                </ul>
            </div>
            
            {% if result %}
                <div class="result">
                    <h3>📊 Extracted Metadata:</h3>
                    {{ result }}
                </div>
            {% endif %}
            
            {% if error %}
                <div class="error">
                    <strong>Error:</strong> {{ error }}
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and return metadata as JSON"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported'}), 400
        
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract metadata
        metadata = get_file_metadata(file_path)
        
        # Clean up the uploaded file
        try:
            os.remove(file_path)
        except:
            pass  # Ignore cleanup errors
        
        return jsonify(metadata)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'File Metadata Extractor',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 