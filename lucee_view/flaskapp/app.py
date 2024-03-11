from flask import Flask, request, jsonify, make_response
import fitz  # PyMuPDF, install with: pip install pymupdf
from docx import Document
import io
import os
import hashlib
import psycopg2
import psycopg2.extras
from datetime import datetime
from dotenv import load_dotenv
app = Flask(__name__)

# Database connection parameters
load_dotenv()
DB_PASS = os.getenv('lucee')
DB_HOST = os.getenv('db')
DB_NAME = os.getenv('lucee')
DB_USER = os.getenv('lucee')
def get_db_connection():
    conn = psycopg2.connect(
        host='db',
        database='lucee',
        user='lucee',
        password='lucee')
    return conn

def pdf_to_text(pdf_data):
    with fitz.open(stream=pdf_data, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def docx_to_text(docx_data):
    doc = Document(docx_data)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def generate_file_hash(file_content):
    """Generate SHA-256 hash of file content."""
    hash_obj = hashlib.sha256()
    hash_obj.update(file_content)
    return hash_obj.hexdigest()

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume part"}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    allowed_extensions = {'pdf', 'docx'}
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        file_content = file.read()
        file_hash = generate_file_hash(file_content)
        file_name = file.filename
        upload_time = datetime.now()

        # Extract text content based on file extension
        text_content = ''
        if file.filename.endswith('.pdf'):
            text_content = pdf_to_text(io.BytesIO(file_content))
        elif file.filename.endswith('.docx'):
            text_content = docx_to_text(io.BytesIO(file_content))

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Insert the extracted text_content instead of file_content
            cur.execute("INSERT INTO resume_uploads (resume_hash, file_name, upload_time, resume_text) VALUES (%s, %s, %s, %s)", 
                        (file_hash, file_name, upload_time, text_content))
            conn.commit()
            cur.close()
            conn.close()

            response = make_response(jsonify({"message": "Resume uploaded successfully"}), 200)
            # Setting a cookie with the resume hash. Adjust the max_age as needed.
            response.set_cookie('resume_hash', file_hash, max_age=60*60*24*30)  # 30 days
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file format"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')