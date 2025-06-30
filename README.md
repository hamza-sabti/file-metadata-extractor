# 📁 File Metadata Extractor

A robust Flask-based web application that extracts comprehensive metadata from various file types including PDFs and images. Built with Docker containerization for easy deployment and scalability.

## 🚀 Features

- **Multi-format Support**: Extract metadata from PDFs, PNG, JPG, JPEG, GIF, BMP, TIFF, and WebP files
- **Rich Metadata Extraction**:
  - **General**: File size, creation date, modification date, MIME type
  - **PDFs**: Author, Creator, Title, Subject, Page count, Creation/Modification dates
  - **Images**: Resolution, Format, Color mode, EXIF data (camera make/model, datetime, copyright)
- **Web Interface**: Beautiful, responsive UI for easy file upload and metadata viewing
- **RESTful API**: JSON endpoints for programmatic access
- **Docker Support**: Complete containerization with health checks
- **Production Ready**: Nginx reverse proxy configuration included

## 🏗️ Project Structure

```
File Metadata Extractor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Multi-service orchestration
├── nginx.conf           # Nginx reverse proxy config
├── .dockerignore        # Docker build exclusions
├── .gitignore          # Git exclusions
└── README.md           # Project documentation
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.11)
- **PDF Processing**: PyPDF2
- **Image Processing**: Pillow (PIL)
- **File Type Detection**: python-magic
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx (production)

## 📦 Installation & Setup

### Option 1: Docker (Recommended)

#### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd File-Metadata-Extractor

# Build and run with Docker Compose
docker-compose up --build

# Access the application
open http://localhost:5000
```

#### Production Deployment
```bash
# Run with nginx reverse proxy
docker-compose --profile production up --build

# Access via nginx on port 80
open http://localhost
```

### Option 2: Local Development

#### Prerequisites
- Python 3.11+
- pip

#### Setup
```bash
# Clone the repository
git clone https://github.com/hamza-sabti/file-metadata-extractor.git
cd File-Metadata-Extractor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access the application
open http://localhost:5000
```

## 🎯 Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Click "Choose File" and select a supported file type
3. Click "Extract Metadata" to process the file
4. View the extracted metadata in a formatted display

### API Endpoints

#### Upload File and Get Metadata
```bash
POST /upload
Content-Type: multipart/form-data

# Example using curl
curl -X POST -F "file=@document.pdf" http://localhost:5000/upload
```

#### Health Check
```bash
GET /api/health

# Example response
{
  "status": "healthy",
  "service": "File Metadata Extractor",
  "version": "1.0.0"
}
```

### Example API Response

#### PDF File Response
```json
{
  "file_size": 245760,
  "creation_date": "2024-01-15T10:30:00",
  "modification_date": "2024-01-15T10:30:00",
  "mime_type": "application/pdf",
  "file_extension": ".pdf",
  "pdf_author": "John Doe",
  "pdf_creator": "Adobe Acrobat",
  "pdf_title": "Sample Document",
  "pdf_page_count": 5
}
```

#### Image File Response
```json
{
  "file_size": 1024000,
  "creation_date": "2024-01-15T10:30:00",
  "modification_date": "2024-01-15T10:30:00",
  "mime_type": "image/jpeg",
  "file_extension": ".jpg",
  "image_width": 1920,
  "image_height": 1080,
  "image_mode": "RGB",
  "image_format": "JPEG",
  "exif_make": "Canon",
  "exif_model": "EOS 5D Mark IV",
  "exif_datetime_original": "2024:01:15 10:30:00"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment mode |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |
| `MAX_CONTENT_LENGTH` | `16MB` | Maximum file upload size |

### File Size Limits

- Default maximum file size: 16MB
- Configurable via `app.config['MAX_CONTENT_LENGTH']`

### Supported File Types

| Extension | MIME Type | Metadata Extracted |
|-----------|-----------|-------------------|
| `.pdf` | `application/pdf` | Author, Creator, Title, Pages, Dates |
| `.png`, `.jpg`, `.jpeg` | `image/*` | Resolution, Format, EXIF data |
| `.gif`, `.bmp`, `.tiff`, `.webp` | `image/*` | Resolution, Format, Color info |

## 🐳 Docker Commands

### Build Image
```bash
docker build -t file-metadata-extractor .
```

### Run Container
```bash
docker run -p 5000:5000 file-metadata-extractor
```

### View Logs
```bash
docker-compose logs -f file-metadata-extractor
```

### Stop Services
```bash
docker-compose down
```

## 🧪 Testing

### Manual Testing
1. Upload different file types through the web interface
2. Verify metadata extraction accuracy
3. Test error handling with invalid files

### API Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test file upload
curl -X POST -F "file=@test.pdf" http://localhost:5000/upload
```

## 🔒 Security Considerations

- File uploads are validated for allowed extensions
- Files are processed in temporary directory (`/tmp/uploads`)
- Uploaded files are automatically cleaned up after processing
- Secure filename handling with `secure_filename()`
- Maximum file size limits enforced

## 🚀 Deployment

### Production Deployment
```bash
# Build and run with production profile
docker-compose --profile production up -d

# Scale the service
docker-compose up -d --scale file-metadata-extractor=3
```

### Environment-Specific Configurations
- **Development**: Use local setup with debug mode
- **Staging**: Use Docker without nginx
- **Production**: Use Docker with nginx reverse proxy

## 📝 API Documentation

### Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/` | Web interface | HTML |
| POST | `/upload` | Upload file and get metadata | JSON |
| GET | `/api/health` | Health check | JSON |

### Error Responses

```json
{
  "error": "Error description"
}
```

Common error codes:
- `400`: Bad request (invalid file, unsupported type)
- `413`: File too large
- `500`: Internal server error

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **File upload fails**: Check file size limits and supported formats
2. **Docker build fails**: Ensure Docker is running and has sufficient resources
3. **Permission errors**: Check file permissions in upload directory
4. **Port conflicts**: Change port mapping in docker-compose.yml

### Logs
```bash
# View application logs
docker-compose logs file-metadata-extractor

# View nginx logs (production)
docker-compose logs nginx
```

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

---

**Built with ❤️ using Flask, Docker, and modern DevOps practices** 
