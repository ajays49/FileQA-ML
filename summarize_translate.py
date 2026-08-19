"""
Summarize a PDF document and optionally translate it.

Usage:
    python summarize_translate.py path/to/document.pdf
"""
import argparse
import time

from pdf_utils import extract_page_texts
from summarizer import summarize_pages
from translator import detect_language, translate_pages


def main():
    parser = argparse.ArgumentParser(description="Summarize (and optionally translate) a PDF document.")
    parser.add_argument("pdf_path", help="Path to the PDF file to summarize.")
    parser.add_argument("-o", "--output", default="summary.txt", help="Path to save the summary text.")
    args = parser.parse_args()

    page_texts = extract_page_texts(args.pdf_path)

    print("Summarizing...")
    start_time = time.time()
    full_summary = summarize_pages(page_texts)
    print(f"Time taken for summarization: {time.time() - start_time:.2f} seconds")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(full_summary)
    print(f"Summary saved to '{args.output}'.")

    translate_required = input("Do you want to translate the document? (yes/no): ").strip().lower()
    if translate_required == "yes":
        document_language = detect_language(page_texts[0]) if page_texts else "en"
        target_language = input(
            f"The document is in '{document_language}'. Enter the language code to translate to (e.g. 'fr'): "
        ).strip()

        print("Translating...")
        start_time = time.time()
        translated_document = translate_pages(page_texts, dest=target_language, src=document_language)
        print(f"Time taken for translation: {time.time() - start_time:.2f} seconds")

        translated_path = "translated_document.txt"
        with open(translated_path, "w", encoding="utf-8") as f:
            f.write(translated_document)
        print(f"Translated document saved to '{translated_path}'.")


if __name__ == "__main__":
    main()
