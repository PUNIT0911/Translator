import streamlit as st
from googletrans import Translator

st.title("🌍 Language Translator")

text = st.text_input("Enter text to translate")
lang = st.selectbox("Translate to", ["hi", "gu", "fr", "de", "es"])

if text:
    translator = Translator()
    translated = translator.translate(text, dest=lang)
    st.success(f"Translated: {translated.text}")
