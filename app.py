import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load Groq API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit Page Setup
st.set_page_config(page_title="Groq Voicebot", layout="centered")
st.title("🎤 Voicebot (Groq API – Free)")
st.write("Record your voice and get an instant reply.")

# --------------------------------------
# 1️⃣ BROWSER AUDIO RECORDER
# --------------------------------------
st.subheader("🎙 Record your voice")

audio_data = st.audio_input("Click to record:")

if audio_data is not None:
    # Save uploaded/recorded audio as temp file
    with open("temp.wav", "wb") as f:
        f.write(audio_data.getvalue())

    st.audio("temp.wav")

    # --------------------------------------
    # 2️⃣ SPEECH-TO-TEXT (Groq Whisper)
    # --------------------------------------
    with open("temp.wav", "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3",
            response_format="text"
        )

    st.subheader("📝 Transcription")
    st.write(transcription)

    # --------------------------------------
    # 3️⃣ LLM RESPONSE (Short English Only)
    # --------------------------------------
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content":
                "You are a concise English-speaking assistant. "
                "Always reply in English. "
                "Reply in 1–2 sentences only."
            },
            {"role": "user", "content": transcription}
        ]
    )

    reply = completion.choices[0].message.content

    st.subheader("🤖 Voicebot Response")
    st.write("🗨 Assistant:", reply)


