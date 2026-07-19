"""Theme loader."""

import base64
from pathlib import Path

import streamlit as st


ROOT_STYLE = """
:root {
    --background-color: #120D14;
    --card-background: rgba(35, 24, 37, 0.88);
    --border-color: rgba(255, 143, 190, 0.30);
    --text-color: #FFF7FB;
    --secondary-text: #D8C7D2;
    --muted-text: #A994A2;
    --header-color: #FFF7FB;
    --sidebar-bg: #1C141D;
    --shadow-glow: rgba(255, 95, 162, 0.15);
    --input-bg: #1C141D;
    --primary-pink: #FF5FA2;
    --secondary-pink: #FF8FBE;
    --accent-pink: #FFC1DA;
}
"""


def apply_styles() -> None:
    css_path = Path(__file__).with_name("styles.css")
    css = css_path.read_text(encoding="utf-8")

    background = """
    .stApp {
        background-color: var(--background-color) !important;
        background-image:
            radial-gradient(circle at 10% 20%, rgba(255,95,162,.08), transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(255,143,190,.06), transparent 45%) !important;
        background-attachment: fixed !important;
    }
    """

    image_path = Path(__file__).with_name("background.jpg")
    if image_path.exists():
        image_data = base64.b64encode(image_path.read_bytes()).decode()
        background = f"""
        .stApp {{
            background-image:
                linear-gradient(rgba(18,13,20,.86), rgba(18,13,20,.93)),
                url('data:image/jpeg;base64,{image_data}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
        """

    st.markdown(
        f"<style>{ROOT_STYLE}{background}{css}</style>",
        unsafe_allow_html=True,
    )
