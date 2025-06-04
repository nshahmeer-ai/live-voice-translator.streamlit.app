import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os

language_dict = {
    'English': 'en',
    'Urdu': 'ur',
    'Hindi': 'hi',
    'French': 'fr',
    'German': 'de',
    'Arabic': 'ar',
    'Spanish': 'es',
    'Chinese': 'zh-cn'
}


def speak(text, lang):
    if text.strip() == "":
        return
    tts = gTTS(text=text, lang=lang)
    filename = "temp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def listen_and_translate_continuous():
    src_lang_name = source_lang.get()
    tgt_lang_name = target_lang.get()
    src = language_dict[src_lang_name]
    tgt = language_dict[tgt_lang_name]

    recognizer = sr.Recognizer()
    translator = Translator()

    with sr.Microphone() as source:
        try:
            status_label.config(text=f"Listening in {src_lang_name}...")
            root.update()
            recognizer.adjust_for_ambient_noise(source)

            while True:
                try:
                    audio = recognizer.listen(
                        source, timeout=5, phrase_time_limit=15)
                    text = recognizer.recognize_google(audio, language=src)

                    input_text.set(f"You said: {text}")
                    translated = translator.translate(text, src=src, dest=tgt)
                    translated_text.set(f"Translated: {translated.text}")
                    speak(translated.text, tgt)

                    status_label.config(text="Listening again...")
                    root.update()

                except sr.UnknownValueError:
                    status_label.config(
                        text="Could not understand audio. Try again...")
                    root.update()
                    continue
                except sr.WaitTimeoutError:
                    status_label.config(text="No speech detected. Waiting...")
                    root.update()
                    continue
                except Exception as e:
                    translated_text.set("Error: " + str(e))
                    status_label.config(text="Unexpected error. Stopping.")
                    root.update()
                    break

        except Exception as e:
            print("Microphone or recognition error:", e)


# GUI setup
root = tk.Tk()
root.title("Live Voice Translator")
root.geometry("450x300")
root.resizable(False, False)

tk.Label(root, text="Select Input Language:").pack()
source_lang = ttk.Combobox(root, values=list(language_dict.keys()))
source_lang.set("Urdu")
source_lang.pack()

tk.Label(root, text="Select Output Language:").pack()
target_lang = ttk.Combobox(root, values=list(language_dict.keys()))
target_lang.set("English")
target_lang.pack()

tk.Button(root, text="Translate Continuously",
          command=listen_and_translate_continuous).pack(pady=10)

input_text = tk.StringVar()
translated_text = tk.StringVar()
status_label = tk.Label(root, text="")
status_label.pack()

tk.Label(root, textvariable=input_text, wraplength=400, fg="blue").pack()
tk.Label(root, textvariable=translated_text, wraplength=400, fg="green").pack()

root.mainloop()
