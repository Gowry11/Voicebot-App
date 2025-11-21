import streamlit as st
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import tempfile
import os
from groq import Groq
from dotenv import load_dotenv

# Load Groq key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Groq Voicebot", layout="centered")
st.title("🎤 Voicebot (Groq API – Free)")
st.write("Click **Start Recording**, speak, then **Stop & Process**.")

duration = 5
sample_rate = 44100

if "recording" not in st.session_state:
    st.session_state.recording = False

def record_audio():
    st.write("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    st.write("Recording complete!")
    return recording

if st.button("🎙 Start Recording"):
    st.session_state.audio = record_audio()

if st.button("🔁 Stop & Process"):
    if "audio" not in st.session_state:
        st.error("No audio recorded!")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            wav.write(temp_audio.name, sample_rate, st.session_state.audio)
            audio_path = temp_audio.name

        st.audio(audio_path)

        # -------------------------------
        # SPEECH-TO-TEXT (Groq Whisper)
        # -------------------------------
        with open(audio_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=f,
                model="whisper-large-v3",
                response_format="text"
            )

        st.subheader("📝 Transcription")
        st.write(str(transcription))   # FIX: ensure text is printed

       # -------------------------------
# LLM REPLY (Short + English Only)
# -------------------------------
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": 
         "You are a concise English-speaking assistant. "
         "Always reply in English. "
         "Reply in maximum 1–2 sentences only. "
         "Never reply in any other language."},
        {"role": "user", "content": transcription}
    ]
)

reply = completion.choices[0].message.content

st.subheader("🤖 Voicebot Response")
st.write("🗨 Assistant:", reply)

