import re
import nltk


class TextProcessor:
    """Preprocess and tokenize cybersecurity descriptions."""

    def __init__(self):
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def clean_text(self, text):
        if not isinstance(text, str):
            raise ValueError("Input text must be a string.")

        text = text.lower()
        text = re.sub(r"[^a-z0-9\s\-_.]", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def tokenize(self, text):
        cleaned = self.clean_text(text)
        return self.tokenizer.tokenize(cleaned)

    def process(self, text):
        cleaned = self.clean_text(text)
        tokens = self.tokenizer.tokenize(cleaned)

        return {
            "cleaned_text": cleaned,
            "tokens": tokens,
            "token_count": len(tokens),
            "character_count": len(cleaned)
        }
