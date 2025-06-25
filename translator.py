import streamlit as st
from googletrans import Translator
from gtts import gTTS
import datetime
import os
import pandas as pd
import altair as alt
import numpy as np  # NEW: NumPy added


# Extended language support
language_dict = {
    "English": "en", "Tamil": "ta", "Hindi": "hi", "French": "fr", "Japanese": "ja",
    "Spanish": "es", "German": "de", "Gujarati": "gu", "Korean": "ko", "Italian": "it",
    "Chinese": "zh-cn", "Arabic": "ar", "Russian": "ru", "Marathi": "mr", "Portuguese": "pt",
    "Bengali": "bn", "Urdu": "ur", "Turkish": "tr", "Malay": "ms", "Swahili": "sw"
}

# Set Streamlit page configuration
st.set_page_config(page_title="🌐 Super Translator AI Studio", layout="wide")

# Custom CSS for enhanced modern UI
st.markdown("""
    <style>
    body {
        background-color: #eef2f7;
    }
    .title-style {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        color: #005792;
        margin-bottom: 0px;
    }
    .subtitle-style {
        font-size: 18px;
        text-align: center;
        color: #444;
        margin-top: 0px;
    }
    .translated-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #d4d4d4;
        margin-top: 15px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.05);
    }
    .footer {
        text-align: center;
        font-size: 14px;
        margin-top: 40px;
        color: #777;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 10px;
        border-left: 5px solid #005792;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown('<div class="title-style">🌐 Super Translator AI Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-style">Your all-in-one multilingual translator and voice assistant!</div>', unsafe_allow_html=True)

# Input section
st.markdown("---")
text = st.text_area("📝 Enter Text to Translate:", height=150)
language_names = st.selectbox("🌍 Choose Language to Translate To:", options=sorted(language_dict.keys()))
dest = language_dict[language_names]

# Extra Options
col1, col2 = st.columns(2)
save_audio = col1.checkbox("💾 Save Translation & Audio")
display_code = col2.checkbox("📋 Show Language Code")
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Translator instance
translator = Translator()
translation_log = []

# Translation and audio
if text and dest:
    try:
        translated = translator.translate(text, dest=dest, src="en")
        trans_text = translated.text

        st.markdown('<div class="translated-box">', unsafe_allow_html=True)
        st.markdown("**🔤 Translated Text:**")
        st.write(trans_text)
        st.markdown('</div>', unsafe_allow_html=True)

        tts = gTTS(text=trans_text, lang=dest)
        audio_filename = f"voice_{timestamp}.mp3"
        tts.save(audio_filename)
        st.audio(audio_filename)

        if save_audio:
            with open("translations_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"[{timestamp}] ENGLISH: {text} | {language_names.upper()}: {trans_text}\n")
            st.success(f"✔️ Translation and audio saved as {audio_filename}")

        if display_code:
            st.markdown("### 🗂 Language Information")
            st.dataframe({"Selected Language": [language_names], "Language Code": [dest]})

        # Collect for chart
        if os.path.exists("language_chart_log.csv"):
            df_chart = pd.read_csv("language_chart_log.csv")
        else:
            df_chart = pd.DataFrame(columns=["Language"])

        df_chart = pd.concat([df_chart, pd.DataFrame({"Language": [language_names]})], ignore_index=True)
        df_chart.to_csv("language_chart_log.csv", index=False)

    except Exception as e:
        st.error(f"🚨 Error: {e}")
else:
    st.markdown('<div class="info-box">👉 Please enter some text and select a language above to begin translation.</div>', unsafe_allow_html=True)

# Show language usage chart
if os.path.exists("language_chart_log.csv"):
    df_chart = pd.read_csv("language_chart_log.csv")
    language_counts = df_chart["Language"].value_counts().reset_index()
    language_counts.columns = ["Language", "Count"]

    st.markdown("### 📊 Translation Usage Bar Chart")
    chart = alt.Chart(language_counts).mark_bar().encode(
        x=alt.X("Language", sort="-y"),
        y="Count",
        tooltip=["Language", "Count"],
        color=alt.Color("Language", legend=None)
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)

    st.markdown("### 🥧 Translation Usage Pie Chart")
    pie_chart = alt.Chart(language_counts).mark_arc().encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Language", type="nominal"),
        tooltip=["Language", "Count"]
    ).properties(height=400)
    st.altair_chart(pie_chart, use_container_width=True)

    # NumPy usage: display average and max
    counts_array = np.array(language_counts["Count"])
    st.markdown("### 📐 NumPy Stats")
    st.write("Average translations per language:", np.mean(counts_array))
    st.write("Most translations in one language:", np.max(counts_array))

# Footer
st.markdown('<div class="footer">Made with ❤️ using Streamlit, Google Translate, and gTTS | Designed by You 🔥</div>', unsafe_allow_html=True)
