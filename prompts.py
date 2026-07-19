"""Prompt builders for CaptionCraft AI."""


def build_caption_prompt(
    post_description: str,
    platform: str,
    tone: str,
    caption_length: str,
    language: str,
    hashtag_count: int,
    include_emojis: bool,
    number_of_captions: int,
    include_call_to_action: bool,
    target_audience: str,
    custom_keywords: str,
    image_uploaded: bool,
) -> str:
    description = post_description.strip() or "Use the uploaded image as the main context."
    audience = target_audience.strip() or "General social media audience"
    keywords = custom_keywords.strip() or "No mandatory keywords"

    return f"""
You are an expert social media strategist and copywriter.

Create exactly {number_of_captions} unique captions.

Post description: {description}
Platform: {platform}
Tone: {tone}
Length: {caption_length}
Language: {language}
Target audience: {audience}
Keywords to include: {keywords}
Hashtags per caption: {hashtag_count}
Emojis: {'Use suitable emojis naturally.' if include_emojis else 'Do not use emojis.'}
Call to action: {'Include a natural CTA.' if include_call_to_action else 'CTA is optional.'}
Image attached: {'Yes. Analyse it carefully and do not invent details.' if image_uploaded else 'No.'}

Requirements:
- Make every caption meaningfully different.
- Match the selected platform, tone, length and language.
- Put hashtags on a separate final line.
- Do not invent names, achievements, places or statistics.
- Number results as Caption 1:, Caption 2:, and so on.
- Return only the captions.
""".strip()


def build_regeneration_prompt(caption: str) -> str:
    return f"""
Rewrite this social media caption so it feels fresh, engaging and unique,
while preserving its meaning and general style:

{caption}

Keep hashtags on a separate final line.
Return only the rewritten caption.
""".strip()
