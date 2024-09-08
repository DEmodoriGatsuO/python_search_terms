import logging
from docx import Document
import win32com.client

def read_word(file_path):
    try:
        if file_path.endswith('.docx'):
            return read_docx(file_path)
        elif file_path.endswith('.doc'):
            return read_doc(file_path)
    except Exception as e:
        logging.error(f"Error reading Word file {file_path}: {e}")
        return ""

def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def read_doc(file_path):
    word = win32com.client.Dispatch("Word.Application")
    doc = word.Documents.Open(file_path)
    text = doc.Content.Text
    doc.Close()
    word.Quit()
    return text