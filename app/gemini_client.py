"""Thin wrapper around google-genai client for text generation."""
from google import genai
from typing import Optional


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model: str = 'gemini-2.5-flash'):
        # If api_key is None, genai.Client() will try to pick credentials from env.
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = genai.Client()
        self.model = model


    def generate_text(self, prompt: str, **kwargs) -> str:
        """Call models.generate_content and return text. kwargs passed to the SDK call.
        Example: generate_text('Explain X')
        """
        # Official minimal usage: client.models.generate_content(model="gemini-2.5-flash", contents="...")
        resp = self.client.models.generate_content(model=self.model, contents=prompt, **kwargs)
        # The SDK commonly exposes `.text` on the response when text is returned.
        # Fallback: convert to string.
        return getattr(resp, 'text', str(resp))