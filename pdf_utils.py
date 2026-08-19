"""Helpers for reading text out of local PDF and DOCX files."""
import os

import fitz  # PyMuPDF

try:
    from docx import Document
except ImportError:
    Document = None


def extract_page_texts(pdf_path):
    """Return a list of strings, one per page, extracted from a PDF file."""
    doc = fitz.open(pdf_path)
    return [doc[page_num].get_text() for page_num in range(doc.page_count)]


def extract_pdf_text(pdf_path):
    """Return the full text of a PDF file as a single string."""
    return "\n\n".join(extract_page_texts(pdf_path))


def extract_docx_text(docx_path):
    """Return the full text of a .docx file as a single string."""
    if Document is None:
        raise ImportError(
            "python-docx is required to read .docx files. Install it with `pip install python-docx`."
        )
    doc = Document(docx_path)
    return " ".join(paragraph.text for paragraph in doc.paragraphs)


def read_file(file_path):
    """Read a local .pdf or .docx file and return its text content."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_pdf_text(file_path)
    elif ext == ".docx":
        return extract_docx_text(file_path)
    raise ValueError(f"Unsupported file type: {ext}. Supported types: .pdf, .docx")
