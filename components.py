"""Reusable Streamlit UI components."""

import html

import streamlit as st


PLATFORMS = ["Instagram", "LinkedIn", "Facebook", "X / Twitter", "YouTube", "Pinterest"]
TONES = [
    "Professional", "Casual", "Creative", "Funny", "Motivational",
    "Friendly", "Inspirational", "Minimal", "Luxury", "Storytelling",
]
LANGUAGES = ["English", "Hindi", "Hinglish", "Punjabi", "Spanish", "French", "German"]
LENGTHS = ["Very Short", "Short", "Medium", "Long"]


def render_sidebar() -> dict:
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; margin:.5rem 0 1.2rem;">
                <h2 style="margin:0; font-size:1.7rem; background:linear-gradient(135deg,#FF4FA3,#FF7EB6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">✨ CaptionCraft AI</h2>
                <p style="margin:4px 0 0; font-size:.8rem; opacity:.65;">Pinterest Luxury Social Copywriter</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        st.markdown("### ⚙️ OPTIONS")

        settings = {
            "platform": st.selectbox("📱 Target Platform", PLATFORMS),
            "tone": st.selectbox("🎭 Caption Tone", TONES),
            "caption_length": st.select_slider("📏 Length Standard", LENGTHS, value="Medium"),
            "language": st.selectbox("🌐 Language", LANGUAGES),
            "number_of_captions": st.slider("🎀 Number of Captions", 1, 5, 3),
            "hashtag_count": st.slider("🌸 Hashtags Count", 0, 15, 5),
            "include_emojis": st.toggle("✨ Include Emojis", value=True),
            "include_call_to_action": st.toggle("📢 Call-To-Action", value=False),
        }

        st.divider()
        st.markdown(
            '<div style="text-align:center; opacity:.5; font-size:.75rem;">Made with ❤️ using Python, Streamlit & Gemini AI</div>',
            unsafe_allow_html=True,
        )
        return settings


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-left">
                <div class="hero-badge">🎀 Powered by Gemini AI</div>
                <h1>✨ AI Caption Generator</h1>
                <div class="hero-subtitle">Create beautiful social media captions powered by AI.</div>
                <div class="hero-subtext">Generate Instagram, LinkedIn, Pinterest and X captions in seconds.</div>
            </div>
            <div class="floating-blobs-container">
                <div class="blob blob-1"></div>
                <div class="blob blob-2"></div>
                <div class="floating-icon">🎀</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(platform: str, language: str, total: int) -> None:
    values = [
        ("Gemini 2.5", "AI Model"),
        (platform, "Active Platform"),
        (language, "Language"),
        (str(total), "Total Generated"),
    ]
    for column, (value, label) in zip(st.columns(4), values):
        with column:
            st.markdown(
                f'<div class="metric-card"><div class="metric-val">{html.escape(value)}</div><div class="metric-lbl">{label}</div></div>',
                unsafe_allow_html=True,
            )


def render_features() -> None:
    st.markdown("### 🎀 App Features")
    features = [
        ("📱", "Platform Optimized", "Custom formatting matched to each platform."),
        ("🖼️", "Image Perception", "Understands visuals to create contextual copy."),
        ("🎀", "AI Creativity", "Flexible tone, language and length controls."),
        ("⚡", "Fast Generation", "Powered by Google's Gemini models."),
    ]
    for column, (icon, title, description) in zip(st.columns(4), features):
        with column:
            st.markdown(
                f'<div class="feature-card-lux"><div class="feature-icon">{icon}</div><h4>{title}</h4><p>{description}</p></div>',
                unsafe_allow_html=True,
            )


def caption_card(index: int, caption: str) -> None:
    safe = html.escape(caption).replace("\n", "<br>")
    st.markdown(
        f'<div class="caption-result-card"><div class="caption-num">✨ Caption {index}</div><div class="caption-content">{safe}</div></div>',
        unsafe_allow_html=True,
    )
    st.code(caption, language=None)


def empty_state() -> None:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-state-icon">✨</div>
            <h3>No Captions Generated Yet</h3>
            <p style="max-width:290px; margin:0 auto; font-size:.85rem; line-height:1.5; opacity:.8;">
                Fill in your post details, adjust the sidebar settings, and click Generate.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def loading_message(emoji: str, message: str) -> None:
    st.markdown(
        f'<div class="loading-state-card"><div class="loading-icon-pulse">{emoji}</div><div class="loading-text">{message}</div></div>',
        unsafe_allow_html=True,
    )
