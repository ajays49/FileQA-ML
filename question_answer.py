"""
Ask questions about a local PDF or DOCX document, with optional summarization and translation.

Usage:
    python question_answer.py path/to/document.pdf
"""
import argparse

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

from pdf_utils import read_file
from summarizer import summarize_pages
from translator import translate_text

QA_MODEL_NAME = "deepset/bert-large-uncased-whole-word-masking-squad2"


def load_qa_pipeline():
    model = AutoModelForQuestionAnswering.from_pretrained(QA_MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(QA_MODEL_NAME)
    return pipeline("question-answering", model=model, tokenizer=tokenizer)


def main():
    parser = argparse.ArgumentParser(description="Ask questions about a document.")
    parser.add_argument("file_path", help="Path to a .pdf or .docx file.")
    args = parser.parse_args()

    print("Loading question-answering model...")
    qa_pipeline = load_qa_pipeline()

    context = read_file(args.file_path)

    while True:
        question = input("\nAsk a question ('exit' to stop): ").strip()
        if question.lower() == "exit":
            print("Exiting...")
            break
        if not question:
            continue

        answer = qa_pipeline(question=question, context=context)["answer"]
        print("Answer:")
        print(answer.replace("\n", " "))

        if input("Summarize the document? (yes/no): ").strip().lower() == "yes":
            page_texts = context.split("\n\n")
            full_summary = summarize_pages(page_texts)
            print("\nSummary:")
            print(full_summary)

            if input("Translate the summary? (yes/no): ").strip().lower() == "yes":
                target_language = input("Enter the target language code (e.g. 'fr' for French): ").strip()
                try:
                    translated_text = translate_text(full_summary, dest=target_language)
                    print("\nTranslated Text:")
                    print(translated_text)
                except Exception as e:
                    print(f"Error during translation: {e}")


if __name__ == "__main__":
    main()
