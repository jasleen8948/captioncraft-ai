"""Small reusable helpers."""

import re
from datetime import datetime


def parse_captions(text: str) -> list[str]:
    if not text:
        return []

    text = text.replace("\r\n", "\n")
    pattern = re.compile(
        r"(?:\*+)?\s*Caption\s*(?:#)?\s*\d+\s*(?:\*+)?\s*[:.]?\s*(?:\*+)?\s*",
        re.IGNORECASE,
    )
    matches = list(pattern.finditer(text))

    if not matches:
        parts = [part.strip() for part in text.split("\n\n") if part.strip()]
        return parts or [text.strip()]

    captions = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        if content:
            captions.append(content)

    return captions or [text.strip()]


def build_caption_text(captions: list[str]) -> str:
    return "\n\n".join(
        f"Caption {index}:\n{caption}"
        for index, caption in enumerate(captions, start=1)
    )


def history_item(captions: str, platform: str, tone: str) -> dict[str, str]:
    return {
        "captions": captions,
        "platform": platform,
        "tone": tone,
        "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }
