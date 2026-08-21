# FileQA: Summarizer, Translator & Question Answerer

A small NLP toolkit for working with documents (PDF / DOCX), built mostly with
research papers in mind. Given a document, you can:

- **Summarize** it with an abstractive summarizer (T5).
- **Translate** the document or its summary into another language.
- **Ask questions** about it and get extractive answers (BERT fine-tuned on SQuAD2).

This started as a Google Colab notebook. Since notebooks don't render reliably
on GitHub, the code has been split into plain, runnable Python scripts that
work locally, no Colab dependency required. The original notebook
(`AJAY_SRIRAM_FileQA.ipynb`) is kept in the repo for
reference. Download the notebook and run the same.

## How to run

You can use either version, they contain the same logic:

- **Notebook version** (`AJAY_SRIRAM_FileQA.ipynb`) open it in
  [Google Colab](https://colab.research.google.com/) (there's an "Open in Colab" badge at
  the top of the notebook) or in Jupyter, then run the cells in order. It uses
  `google.colab.files.upload()` for file input, so it's meant for Colab, not a local
  Jupyter install.

  ```bash
  jupyter notebook AJAY_SRIRAM_FileQA.ipynb
  ```

- **Python script version** (recommended for local use / GitHub doesn't render the
  notebook's outputs) install the requirements once, then run the CLI scripts
  described below:

  ```bash
  pip install -r requirements.txt
  python summarize_translate.py path/to/document.pdf
  python question_answer.py path/to/document.pdf
  ```

## Features

| Script                    | What it does                                                                 |
|----------------------------|-------------------------------------------------------------------------------|
| `summarize_translate.py`  | Summarizes a PDF page-by-page, then optionally translates the full document. |
| `question_answer.py`      | Answers free-form questions about a PDF/DOCX, with optional summary + translation. |

## Project structure

```
FileQA-ML/
├── pdf_utils.py            # PDF/DOCX text extraction
├── summarizer.py           # T5-small abstractive summarization
├── translator.py           # googletrans-based language detection & translation
├── summarize_translate.py  # CLI: summarize + translate a PDF
├── question_answer.py      # CLI: ask questions about a document
├── requirements.txt
└── AJAY_SRIRAM_FileQA.ipynb   # original Colab notebook
```

## Installation

Requires Python 3.9+.

```bash
pip install -r requirements.txt
```

The first run of each script will also download the underlying models from
Hugging Face (`t5-small` for summarization, `deepset/bert-large-uncased-whole-word-masking-squad2`
for question answering), so the first invocation needs an internet connection
and may take a minute or two.

## Usage

### Summarize + translate a PDF

```bash
python summarize_translate.py path/to/document.pdf
```

This writes the summary to `summary.txt`. It will then ask if you want to
translate the document; if you say yes, it detects the source language,
asks for a target language code (e.g. `fr`, `de`, `hi`), and writes the
result to `translated_document.txt`.

### Ask questions about a document

```bash
python question_answer.py path/to/document.pdf
```

Supports `.pdf` and `.docx` files. Loads the document once, then lets you ask
as many questions as you like (type `exit` to stop). After each answer you
can optionally get a summary of the document and translate that summary.

## Models used

- **Summarization**: [`t5-small`](https://huggingface.co/google-t5/t5-small) via 🤗 Transformers.
- **Question answering**: [`deepset/bert-large-uncased-whole-word-masking-squad2`](https://huggingface.co/deepset/bert-large-uncased-whole-word-masking-squad2), a BERT-large model fine-tuned on SQuAD2.
- **Translation**: [`googletrans`](https://pypi.org/project/googletrans/) (unofficial Google Translate API wrapper).

## Notes on the conversion from the notebook

The original notebook was written to run in Google Colab and relied on
`google.colab.files.upload()` for file input, which only works inside Colab.
While converting it to standalone scripts, a few issues were also fixed:

- File input now comes from a local file path (CLI argument) instead of a
  Colab upload widget.
- The summarization model is now loaded once and reused, instead of being
  reloaded from disk on every single call.
- A missing `python-docx` import (`Document` was used but never imported) was added.
- A translation code block that ran unconditionally regardless of the
  yes/no prompt (due to an indentation bug in the notebook) now correctly
  only runs when translation is requested.
- The `.docx`/`.pdf` file reader no longer hardcodes a `.pdf` temp filename
  for every upload.

## Known limitations

- `googletrans==4.0.0-rc1` is an unofficial library that occasionally breaks
  when Google changes its translation endpoint (you may see errors like
  `the JSON object must be str, bytes or bytearray, not NoneType`). If
  translation stops working, consider swapping in a maintained alternative
  such as [`deep-translator`](https://pypi.org/project/deep-translator/) or
  the official Google Cloud Translation API.
- `t5-small` produces reasonable but not state-of-the-art summaries; swap in
  `t5-base` or `t5-large` in `summarizer.py` for better quality at the cost
  of speed/memory.
- Text is truncated to 512 tokens per chunk for summarization and per-page
  for the QA context, so very long documents are processed piecewise rather
  than holistically.
