# resume_reader.py
import os
from PyPDF2 import PdfReader
from docx import Document

def extract_text(file_path):
    """
    Extract text from a resume file (.txt, .pdf, .docx)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif ext == ".docx":
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        raise ValueError("Unsupported file type. Use .txt, .pdf, or .docx")