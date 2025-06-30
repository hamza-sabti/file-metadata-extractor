#!/usr/bin/env python3
"""
Test script for File Metadata Extractor
Demonstrates API usage and validates functionality
"""

import requests
import json
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:5000"
TEST_FILES_DIR = "test_files"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return False

def test_file_upload(file_path):
    """Test file upload and metadata extraction"""
    if not os.path.exists(file_path):
        print(f"❌ Test file not found: {file_path}")
        return False
    
    print(f"📁 Testing upload for: {os.path.basename(file_path)}")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            metadata = response.json()
            print(f"✅ Upload successful!")
            print(f"📊 Extracted metadata:")
            print(json.dumps(metadata, indent=2))
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def create_test_files():
    """Create sample test files for demonstration"""
    print("📝 Creating test files...")
    
    # Create test directory
    os.makedirs(TEST_FILES_DIR, exist_ok=True)
    
    # Create a simple text file (not supported, for testing error handling)
    with open(f"{TEST_FILES_DIR}/test.txt", "w") as f:
        f.write("This is a test file that should not be supported.")
    
    print(f"✅ Test files created in {TEST_FILES_DIR}/")
    print("📋 Note: You can add your own PDF and image files to test with")

def main():
    """Main test function"""
    print("🧪 File Metadata Extractor - Test Suite")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("\n❌ Server is not running. Please start the application first:")
        print("   docker-compose up --build")
        print("   or")
        print("   python app.py")
        return
    
    print("\n" + "=" * 50)
    
    # Create test files
    create_test_files()
    
    print("\n" + "=" * 50)
    print("📋 Manual Testing Instructions:")
    print("1. Add your own PDF and image files to the 'test_files' directory")
    print("2. Run this script again to test with your files")
    print("3. Or use the web interface at http://localhost:5000")
    print("4. Or test with curl:")
    print("   curl -X POST -F 'file=@your_file.pdf' http://localhost:5000/upload")
    
    # Test with any existing files in test directory
    test_files = list(Path(TEST_FILES_DIR).glob("*"))
    if test_files:
        print(f"\n🔍 Found {len(test_files)} test files:")
        for file_path in test_files:
            print(f"   - {file_path.name}")
        
        print("\n📤 Testing file uploads...")
        for file_path in test_files:
            test_file_upload(str(file_path))
            print("-" * 30)

if __name__ == "__main__":
    main() 