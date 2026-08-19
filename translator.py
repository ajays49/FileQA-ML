"""Language detection and translation using googletrans."""
from googletrans import Translator

_translator = Translator()


def detect_language(text):
    """Detect the language of a piece of text. Returns a language code (e.g. 'en')."""
    return _translator.detect(text).lang


def translate_text(text, dest, src=None):
    """Translate text into the dest language code. Auto-detects the source language if src is None."""
    kwargs = {"dest": dest}
    if src:
        kwargs["src"] = src
    result = _translator.translate(text, **kwargs)
    if result is None or not result.text:
        raise RuntimeError("Translation failed or returned an empty response.")
    return result.text


def translate_pages(page_texts, dest, src=None):
    """Translate a list of page texts, skipping/logging any that fail, and join the results."""
    translated = []
    for page_text in page_texts:
        if not page_text.strip():
            continue
        try:
            translated.append(translate_text(page_text, dest=dest, src=src))
        except Exception as e:
            print(f"Error during translation: {e}")
    return " ".join(translated)
