"""Gemini API integration."""

from google import genai
from PIL import Image


class GeminiCaptionService:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash") -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, uploaded_image=None) -> str:
        if uploaded_image is not None:
            uploaded_image.seek(0)
            image = Image.open(uploaded_image).convert("RGB")
            contents = [prompt, image]
        else:
            contents = prompt

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        return response.text.strip()
