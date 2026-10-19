import logging
import os

import httpx
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate


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
    "<div class='subtitle'>AI-Powered Movie Information Extraction using LangChain + Mistral</div>",
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


def mistral_error_message(error):
    """Turn a provider status into a safe, actionable UI message."""
    status_code = error.response.status_code

    messages = {
        400: "Mistral rejected the request. Check the configured model and input.",
        401: "Mistral rejected the API key. Update MISTRAL_API_KEY in Streamlit Secrets.",
        403: "This Mistral account cannot access the selected model. Check the account permissions or choose another model.",
        404: "The configured Mistral model was not found. Check MISTRAL_MODEL in Streamlit Secrets.",
        422: "Mistral could not process this request. Try shorter plain-text input.",
        429: "The Mistral rate or usage limit has been reached. Check the account quota and billing, then try again.",
    }

    if status_code >= 500:
        return "Mistral is temporarily unavailable. Please try again shortly."

    return messages.get(
        status_code,
        f"Mistral returned an unexpected error (HTTP {status_code}). Please try again.",
    )


api_key = get_setting("MISTRAL_API_KEY")

if not api_key:
    st.error(
        "Mistral API key is missing. Set MISTRAL_API_KEY in Streamlit Secrets "
        "or in a local .env file."
    )
    st.stop()

model_name = get_setting("MISTRAL_MODEL", "mistral-small-latest")

llm = ChatMistralAI(
    model=model_name,
    temperature=0.3,
    api_key=api_key,
    max_retries=2,
    timeout=60,
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
        except httpx.HTTPStatusError as error:
            logger.exception(
                "Mistral request failed with HTTP %s",
                error.response.status_code,
            )
            st.error(mistral_error_message(error))
        except httpx.RequestError:
            logger.exception("Could not connect to Mistral")
            st.error("Could not connect to Mistral. Check the network and try again.")
        except Exception:
            logger.exception("Unexpected movie extraction failure")
            st.error("The extraction failed unexpectedly. Please try again.")
        else:
            st.success("Extraction Complete!")

            st.markdown("## 📋 Extracted Information")

            st.markdown(
                f"""
<div class="result-box">

{response.content}

</div>
""",
                unsafe_allow_html=True
            )

            st.download_button(
                label="📥 Download Result",
                data=response.content,
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

CineSage extracts structured movie information from natural language descriptions using **LangChain** and **Mistral AI**.

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
