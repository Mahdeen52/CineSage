import logging
import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


logger = logging.getLogger(__name__)

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="CineSage",
    page_icon="🎬",
    layout="wide"
)

# ==========================
# Custom CSS
# ==========================
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.title{
    text-align:center;
    font-size:48px;
    font-weight:800;
    color:#FF4B4B;
}

.subtitle{
    text-align:center;
    font-size:18px;
    color:#BBBBBB;
    margin-bottom:30px;
}

.stTextArea textarea{
    border-radius:15px;
    font-size:16px;
}

div.stButton > button{
    width:100%;
    border-radius:12px;
    height:55px;
    font-size:18px;
    font-weight:bold;
    background:#FF4B4B;
    color:white;
}

.result-box{
    padding:20px;
    border-radius:15px;
    background:#1E1E1E;
    border:1px solid #444;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:50px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# Header
# ==========================
st.markdown("<div class='title'>🎬 CineSage</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='subtitle'>AI-Powered Movie Information Extraction using LangChain + Gemini</div>",
    unsafe_allow_html=True
)

# ==========================
# Load Model
# ==========================

load_dotenv()


def get_setting(name, default=""):
    """Read local environment variables first, then Streamlit Secrets."""
    value = os.getenv(name, "").strip()
    if value:
        return value

    try:
        value = st.secrets.get(name, default)
    except Exception:
        # A local Streamlit run may not have a secrets.toml file.
        value = default

    return str(value).strip()


def provider_status_code(error):
    """Extract an HTTP-like status code from Google or LangChain errors."""
    status_code = getattr(error, "status_code", None)
    if status_code is None:
        status_code = getattr(error, "code", None)
    if callable(status_code):
        status_code = status_code()
    if hasattr(status_code, "value"):
        status_code = status_code.value
    if status_code is None and getattr(error, "response", None) is not None:
        status_code = getattr(error.response, "status_code", None)

    try:
        return int(status_code)
    except (TypeError, ValueError):
        return None


def gemini_error_message(error):
    """Turn a provider status into a safe, actionable UI message."""
    status_code = provider_status_code(error)

    messages = {
        400: "Gemini rejected the request. Check the configured model and input.",
        401: "Gemini rejected the API key. Update GEMINI_API_KEY in Streamlit Secrets.",
        403: "This Gemini API key cannot access the selected model. Check the key's project and permissions.",
        404: "The configured Gemini model was not found. Check GEMINI_MODEL in Streamlit Secrets.",
        429: "The Gemini free-tier limit has been reached. Wait for the quota to reset, then try again.",
    }

    if status_code is not None and status_code >= 500:
        return "Gemini is temporarily unavailable. Please try again shortly."

    if status_code is None:
        return "Could not complete the Gemini request. Check the app logs and try again."

    return messages.get(
        status_code,
        f"Gemini returned an unexpected error (HTTP {status_code}). Please try again.",
    )


def response_text(response):
    """Return only user-visible text from a LangChain AI message."""
    content = response.content
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, str):
                text_parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text")
                if text:
                    text_parts.append(text)
        return "\n".join(text_parts)

    return str(content)


api_key = get_setting("GEMINI_API_KEY")

if not api_key:
    st.error(
        "Gemini API key is missing. Set GEMINI_API_KEY in Streamlit Secrets "
        "or in a local .env file."
    )
    st.stop()

model_name = get_setting("GEMINI_MODEL", "gemini-3.6-flash")

llm = ChatGoogleGenerativeAI(
    model=model_name,
    temperature=0.3,
    api_key=api_key,
    max_retries=2,
    timeout=60,
    max_tokens=4096,
)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert movie information extraction assistant.

Extract:

- Movie Name
- Genre
- Director
- Release Year
- Main Cast
- Plot
- Setting
- Themes
- IMDb Rating
- Awards
- Runtime
- Language
- Country
- Keywords
- Summary

If unavailable write "Not Mentioned".

Return in a clean markdown format.
"""
    ),
    (
        "human",
        """
Movie Description:

{movie_description}
"""
    )
])

chain = prompt | llm

# ==========================
# Input
# ==========================
movie_description = st.text_area(
    "Paste a movie description",
    height=280,
    placeholder="Example:\n\nInterstellar is a 2014 science fiction film directed by Christopher Nolan..."
)

col1, col2 = st.columns([1,1])

with col1:
    extract = st.button("✨ Extract Information")

with col2:
    clear = st.button("🗑 Clear")

if clear:
    st.rerun()

# ==========================
# Output
# ==========================
if extract:

    if movie_description.strip() == "":
        st.warning("Please enter a movie description.")
    else:

        try:
            with st.spinner("Analyzing movie description..."):
                response = chain.invoke({
                    "movie_description": movie_description
                })
        except Exception as error:
            logger.exception(
                "Gemini movie extraction failed with status %s",
                provider_status_code(error),
            )
            st.error(gemini_error_message(error))
        else:
            result_text = response_text(response)
            st.success("Extraction Complete!")

            st.markdown("## 📋 Extracted Information")

            with st.container(border=True):
                st.markdown(result_text)

            st.download_button(
                label="📥 Download Result",
                data=result_text,
                file_name="movie_information.txt",
                mime="text/plain"
            )

# ==========================
# Sidebar
# ==========================
with st.sidebar:

    st.title("🎥 CineSage")

    st.markdown("---")

    st.markdown("""
### About

CineSage extracts structured movie information from natural language descriptions using **LangChain** and **Google Gemini**.

### Features

- 🎬 Movie Metadata
- ⭐ Ratings
- 👥 Cast
- 🎭 Genre
- 📖 Story
- 🏆 Awards
- 🔑 Keywords
- 📝 Summary
""")

    st.markdown("---")

    st.caption("Built with ❤️ using Streamlit")

# ==========================
# Footer
# ==========================
st.markdown(
    "<div class='footer'>© 2026 CineSage • AI Movie Information Extractor</div>",
    unsafe_allow_html=True
)
