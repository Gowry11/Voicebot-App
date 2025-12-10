import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from gtts import gTTS

# Load Groq API Key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="AI Voicebot", layout="centered")
st.title("🎤 AI Voicebot (Groq API – Listen & Speak)")
st.write("Record your voice, the bot will transcribe and speak back to you.")

# 1️⃣ AUDIO INPUT
audio_data = st.audio_input("🎙 Click below to record your question:")

if audio_data is not None:
    # Save audio
    with open("temp.wav", "wb") as f:
        f.write(audio_data.getvalue())
    st.audio("temp.wav")

    # 2️⃣ SPEECH → TEXT
    try:
        with open("temp.wav", "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=f,
                model="whisper-large-v3",
                response_format="text"
            )
    except Exception:
        st.error("⚠️ Could not transcribe audio. Please try again.")
        st.stop()

    st.subheader("📝 Transcription")
    st.write(transcription)

    # 3️⃣ AI RESPONSE
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are a concise English-speaking assistant. "
                    "Always reply in English using 1–2 sentences."
                },
                {"role": "user", "content": transcription}
            ]
        )
        reply = completion.choices[0].message.content
    except Exception:
        st.error("⚠️ AI could not generate a response. Try again.")
        st.stop()

    st.subheader("🤖 Assistant Response")
    st.write("🗨️", reply)

    # 4️⃣ TEXT → SPEECH (TTS) — CLOUD SAFE VERSION
    try:
        tts = gTTS(reply, lang="en")
        tts.save("response.mp3")

        st.subheader("🔊 Voice Output")
        with open("response.mp3", "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

    except Exception:
        st.error("⚠️ Could not generate voice output.")

