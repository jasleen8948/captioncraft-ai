"""CaptionCraft AI — Streamlit entry point."""

import os
import time

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from ai_service import GeminiCaptionService
from components import (
    caption_card,
    empty_state,
    loading_message,
    render_features,
    render_hero,
    render_metric_cards,
    render_sidebar,
)
from pdf_utils import create_pdf
from prompts import build_caption_prompt, build_regeneration_prompt
from styles import apply_styles
from utils import build_caption_text, history_item, parse_captions


st.set_page_config(
    page_title="CaptionCraft AI",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY was not found. Add it to your .env file.")
    st.code("GEMINI_API_KEY=your_actual_api_key", language="text")
    st.stop()

service = GeminiCaptionService(api_key)

DEFAULT_STATE = {
    "caption_history": [],
    "latest_captions": "",
    "favorites": [],
    "total_generated_count": 0,
}
for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, list) else value

settings = render_sidebar()
render_hero()

input_column, output_column = st.columns([1.1, 0.9], gap="large")

with input_column:
    with st.container(border=True):
        st.markdown("### 📝 Post Context")
        post_description = st.text_area(
            "What is your post description?",
            placeholder=(
                "Describe the image details, storytelling, or post topic...\n"
                "Example: A cozy Sunday reading spot with soft lighting."
            ),
            height=150,
        )
        audience_column, keyword_column = st.columns(2)
        with audience_column:
            target_audience = st.text_input(
                "Audience Profile",
                placeholder="e.g. food lovers, devs, students...",
            )
        with keyword_column:
            custom_keywords = st.text_input(
                "Keywords to Include",
                placeholder="e.g. aesthetic, cozy, morning...",
            )
        uploaded_image = st.file_uploader(
            "Attach Post Image (optional)",
            type=["jpg", "jpeg", "png", "webp"],
        )
        generate_button = st.button(
            "✨ Generate Caption",
            type="primary",
            use_container_width=True,
        )

if generate_button:
    if not post_description.strip() and uploaded_image is None:
        st.warning("Please enter a post description or upload an image.")
    else:
        prompt = build_caption_prompt(
            post_description=post_description,
            target_audience=target_audience,
            custom_keywords=custom_keywords,
            image_uploaded=uploaded_image is not None,
            **settings,
        )
        loader = st.empty()
        for emoji, message in [
            ("✨", "Understanding your post..."),
            ("💡", "Thinking creatively..."),
            ("🎀", "Writing beautiful captions..."),
            ("🌸", "Adding hashtags..."),
        ]:
            with loader.container():
                loading_message(emoji, message)
            time.sleep(0.35)

        try:
            generated = service.generate(prompt, uploaded_image)
            st.session_state.latest_captions = generated
            st.session_state.total_generated_count += len(parse_captions(generated))
            st.session_state.caption_history.insert(
                0,
                history_item(generated, settings["platform"], settings["tone"]),
            )
            st.session_state.caption_history = st.session_state.caption_history[:10]
            loader.empty()
            st.rerun()
        except Exception as error:
            loader.empty()
            st.error("Unable to generate captions.")
            st.caption(f"Technical details: {error}")

with output_column:
    with st.container(border=True):
        st.markdown("### 🚀 Workspace & Preview")

        if uploaded_image is not None:
            try:
                uploaded_image.seek(0)
                st.image(Image.open(uploaded_image), use_container_width=True)
                uploaded_image.seek(0)
            except Exception:
                st.error("The selected image could not be opened.")

        if st.session_state.latest_captions:
            captions = parse_captions(st.session_state.latest_captions)

            for index, caption in enumerate(captions, start=1):
                caption_card(index, caption)
                download_col, favorite_col, regenerate_col = st.columns(3)

                with download_col:
                    st.download_button(
                        "⬇️ Download",
                        data=caption,
                        file_name=f"caption_{index}.txt",
                        mime="text/plain",
                        key=f"download_{index}",
                        use_container_width=True,
                    )

                with favorite_col:
                    is_favorite = caption in st.session_state.favorites
                    if st.button(
                        "❤️ Pinned" if is_favorite else "🤍 Pin to Favs",
                        key=f"favorite_{index}",
                        use_container_width=True,
                    ):
                        if is_favorite:
                            st.session_state.favorites.remove(caption)
                        else:
                            st.session_state.favorites.append(caption)
                        st.rerun()

                with regenerate_col:
                    if st.button(
                        "🔄 Regenerate",
                        key=f"regenerate_{index}",
                        use_container_width=True,
                    ):
                        try:
                            with st.spinner("Composing a fresh variation..."):
                                replacement = service.generate(
                                    build_regeneration_prompt(caption),
                                    uploaded_image,
                                )
                            captions[index - 1] = replacement
                            st.session_state.latest_captions = build_caption_text(captions)
                            st.session_state.total_generated_count += 1
                            st.rerun()
                        except Exception as error:
                            st.error(f"Regenerate failed: {error}")

            st.divider()
            st.markdown("#### 📦 Export All Captions")
            st.code(st.session_state.latest_captions, language=None)
            txt_col, pdf_col, clear_col = st.columns(3)
            with txt_col:
                st.download_button(
                    "⬇️ Export TXT",
                    st.session_state.latest_captions,
                    "ai_generated_captions.txt",
                    "text/plain",
                    use_container_width=True,
                )
            with pdf_col:
                st.download_button(
                    "📄 Export PDF",
                    create_pdf(captions),
                    "ai_generated_captions.pdf",
                    "application/pdf",
                    use_container_width=True,
                )
            with clear_col:
                if st.button("🗑️ Clear Results", use_container_width=True):
                    st.session_state.latest_captions = ""
                    st.rerun()
        else:
            empty_state()

st.write("")
render_metric_cards(
    settings["platform"],
    settings["language"],
    st.session_state.total_generated_count,
)
render_features()

if st.session_state.favorites:
    st.divider()
    with st.container(border=True):
        st.markdown("### ❤️ Favorite Captions")
        for index, favorite in enumerate(list(st.session_state.favorites), start=1):
            caption_card(index, favorite)
            col_download, col_remove = st.columns(2)
            with col_download:
                st.download_button(
                    "⬇️ Download Favorite",
                    favorite,
                    f"favorite_caption_{index}.txt",
                    "text/plain",
                    key=f"favorite_download_{index}",
                    use_container_width=True,
                )
            with col_remove:
                if st.button(
                    "🗑️ Remove Pin",
                    key=f"remove_favorite_{index}",
                    use_container_width=True,
                ):
                    st.session_state.favorites.remove(favorite)
                    st.rerun()

st.divider()
with st.container(border=True):
    st.markdown("### 🕘 Recent Generations")
    if not st.session_state.caption_history:
        st.info("Your caption history is currently empty. Captions generated will be saved here.")
    else:
        if st.button("Clear History", key="clear_history"):
            st.session_state.caption_history = []
            st.rerun()

        for index, item in enumerate(st.session_state.caption_history, start=1):
            label = f"🏷️ {item['platform']} · {item['tone']} · {item['created_at']}"
            with st.expander(label):
                st.write(item["captions"])
                st.download_button(
                    "Download",
                    item["captions"],
                    f"caption_history_{index}.txt",
                    "text/plain",
                    key=f"history_download_{index}",
                )

st.markdown("---")
st.markdown(
    '<div style="text-align:center; opacity:.65; padding-bottom:1.5rem; font-size:.85rem;">Made with ❤️ using Python, Streamlit & Google Gemini AI</div>',
    unsafe_allow_html=True,
)
