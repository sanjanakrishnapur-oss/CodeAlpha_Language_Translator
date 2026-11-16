import streamlit as st
import requests
import html

# Page settings
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

# App heading
st.title("🌍 AI Language Translator")
st.write("Translate text between different languages instantly.")

st.divider()

# Supported languages
languages = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi",
    "Tamil": "ta",
    "German": "de"
}

# Language selection
col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "Source Language",
        list(languages.keys())
    )

with col2:
    target = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=1
    )

# Text input
text = st.text_area(
    "Enter your text",
    placeholder="Type something to translate...",
    height=150
)

# Translation function
def translate_text(text, source, target):

    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": f"{source}|{target}"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    if data.get("responseStatus") != 200:
        raise ValueError(data.get("responseDetails", "Translation failed."))

    translated = data["responseData"]["translatedText"]

    return html.unescape(translated)


# Translate button
if st.button("🌐 Translate Now", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text.")

    elif source == target:
        st.warning("Please select two different languages.")

    else:
        try:
            with st.spinner("Translating..."):
                result = translate_text(
                    text,
                    languages[source],
                    languages[target]
                )

            st.session_state["translation"] = result

        except requests.RequestException:
            st.error("Unable to connect. Check your internet connection.")

        except (ValueError, KeyError) as error:
            st.error(f"Translation error: {error}")


# Display result
if "translation" in st.session_state:
    st.subheader("✨ Translated Text")

    st.code(
    st.session_state["translation"],
    language=None
)

    st.caption("Select and copy the translated text above.")

st.divider()
st.caption("Developed as part of CodeAlpha AI Internship")