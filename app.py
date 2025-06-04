import streamlit as st
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import tempfile

# Language mapping dictionary
lang_dict = {lang.title(): code for code, lang in LANGUAGES.items()}

# Top common languages
popular_langs = ['English', 'Urdu', 'Hindi', 'Arabic', 'French', 'German', 'Spanish']

st.set_page_config(page_title="Live Voice Translator", layout="centered")
st.title("🎙️ Live Voice Translator")
st.markdown("Speak continuously and get real-time translation and audio playback!")

# Language selection
source_lang = st.selectbox(
    " Select Input Language", options=popular_langs + sorted(lang_dict.keys()), index=1)
target_lang = st.selectbox(
    "🗣️ Select Output Language", options=popular_langs + sorted(lang_dict.keys()), index=0)

st.info("Click the button and speak. Your voice will be translated and played.")

# Translate button
if st.button(" Start Live Translation"):
    src = lang_dict[source_lang]
    tgt = lang_dict[target_lang]

    recognizer = sr.Recognizer()
    translator = Translator()

    with sr.Microphone() as source:
        st.success(f"Listening in {source_lang}... Speak now.")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language=src)
            st.write(f" **You said:** {text}")

            translated = translator.translate(text, src=src, dest=tgt)
            st.write(f"**Translated:** {translated.text}")

            # Text to Speech
            tts = gTTS(text=translated.text, lang=tgt)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                audio_file = open(fp.name, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                
        except sr.UnknownValueError:
            st.error("Could not understand audio. Try again.")
        except sr.WaitTimeoutError:
            st.warning(" No speech detected.")
        except Exception as e:
            st.error(f" Error: {str(e)}")

