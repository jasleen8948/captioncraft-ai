"""PDF export helpers."""

import html
from io import BytesIO

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def create_pdf(captions: list[str]) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48,
        title="CaptionCraft AI - Generated Captions",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitlePink",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=HexColor("#FF4FA3"),
        alignment=TA_CENTER,
        spaceAfter=24,
    )
    label_style = ParagraphStyle(
        "CaptionLabel",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=HexColor("#FF5FA2"),
        spaceBefore=8,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "CaptionBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=16,
        textColor=HexColor("#3D2735"),
        spaceAfter=18,
    )

    story = [Paragraph("AI Generated Captions", title_style), Spacer(1, 6)]
    for index, caption in enumerate(captions, start=1):
        safe_text = html.escape(caption).replace("\n", "<br/>")
        story.extend(
            [
                Paragraph(f"Caption {index}", label_style),
                Paragraph(safe_text, body_style),
                Spacer(1, 8),
            ]
        )

    document.build(story)
    buffer.seek(0)
    return buffer.getvalue()
