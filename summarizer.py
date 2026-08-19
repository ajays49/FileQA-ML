"""Abstractive summarization using a T5-small model."""
from transformers import T5ForConditionalGeneration, T5Tokenizer

_MODEL_NAME = "t5-small"
_model = None
_tokenizer = None


def _load_model():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        _model = T5ForConditionalGeneration.from_pretrained(_MODEL_NAME)
        _tokenizer = T5Tokenizer.from_pretrained(_MODEL_NAME)
    return _model, _tokenizer


def abstractive_summarization(text):
    """Summarize a single chunk of text using T5-small."""
    if not text or not text.strip():
        return ""
    model, tokenizer = _load_model()
    input_ids = tokenizer.encode(
        "summarize: " + text, return_tensors="pt", max_length=512, truncation=True
    )
    summary_ids = model.generate(
        input_ids, max_length=150, length_penalty=2.0, num_beams=4, early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


def summarize_pages(page_texts):
    """Summarize a list of page/paragraph texts and join the results into one summary."""
    summaries = [abstractive_summarization(page) for page in page_texts if page.strip()]
    return " ".join(summaries)
