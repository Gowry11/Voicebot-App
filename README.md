# AI Voicebot (Zero-Setup | Groq API + Streamlit)

This is a simple, user-friendly GenAI voicebot designed to work directly in any browser with zero setup.
Non-technical users can click Record, speak naturally, and hear the assistant respond with AI-generated voice.

## Features
- Browser Voice Recording — No drivers or installations needed
- Speech-to-Text (Whisper) — Fast and accurate transcription
- AI Conversational Reply (LLaMA) — Short, English-only answers
- AI Voice Output (TTS) — Speaks the reply aloud
- Fully Web-hosted — No API key required from users
- Zero Setup — No downloads, no coding, no installations

## Technologies Used
- Streamlit — Web UI + audio recorder
- Groq API — Whisper STT + LLaMA LLM
- gTTS — Text-to-speech
- Python
- Streamlit Cloud — Deployment platform

## Project Structure
voicebot-app/
app.py              #Main Streamlit application
requirements.txt    #Python dependencies
README.md           #Project documentation
.gitignore          #Ignored files (env, mp3, wav, etc.)

## Live Demo
Access the deployed voicebot here:
https://your-app-name.streamlit.app/

## Running Locally (Optional)
(Local setup is NOT required for users — only for development.)
pip install -r requirements.txt
streamlit run app.py

## requirements.txt
streamlit
python-dotenv
groq
gtts

## Note:
This project intentionally avoids system-level audio libraries like sounddevice, scipy, and pydub to remain fully compatible with Streamlit Cloud.

## Author
Gowry
AI & Data Science Enthusiast


