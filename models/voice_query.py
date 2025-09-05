import streamlit as st
import torch
import torchaudio
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.helper import log_event
import os
from tempfile import NamedTemporaryFile
from huggingface_hub import login, HfApi

# Ensure Hugging Face login (assumes you've already logged in via CLI)
# login()  # Uncomment if needed to enforce login during runtime

# ✅ Load Whisper model (for transcription)
@st.cache_resource
def load_whisper_model():
    try:
        processor = AutoProcessor.from_pretrained("openai/whisper-large-v3", use_auth_token=True)
        model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v3", use_auth_token=True)
        return processor, model
    except Exception as e:
        log_event("error", f"Failed to load Whisper model: {e}")
        st.error("❌ Whisper model loading failed. Please ensure it's accessible and you've authenticated.")
        raise e

# ✅ Use medical model (Falcon-7B or fallback)
@st.cache_resource
def load_medical_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct", use_auth_token=True)
        model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b-instruct", use_auth_token=True)
        return tokenizer, model
    except Exception as e:
        log_event("error", f"Failed to load Falcon model: {e}")
        st.error("❌ Falcon model loading failed. Make sure you have access to `tiiuae/falcon-7b-instruct`.")
        raise e

def transcribe_audio(audio_path):
    processor, model = load_whisper_model()
    waveform, sample_rate = torchaudio.load(audio_path)

    inputs = processor(waveform[0], sampling_rate=sample_rate, return_tensors="pt")
    with torch.no_grad():
        predicted_ids = model.generate(**inputs)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription

def ask_health_question(query):
    tokenizer, model = load_medical_model()

    prompt = (
        "You are a helpful and reliable medical assistant.\n"
        f"Patient Question: {query}\n\n"
        "Provide a medically accurate and empathetic response:"
    )

    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=256, temperature=0.6)

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response.split("response:")[-1].strip()

def voice_query_ui():
    st.markdown("""
        <style>
            .main {
                background-color: #f5f7fa;
                padding: 2rem;
                border-radius: 10px;
            }
            .stApp {
                background-image: linear-gradient(160deg, #e0f7fa 0%, #ffffff 100%);
                background-size: cover;
            }
            .stButton>button {
                background: linear-gradient(to right, #4facfe, #00f2fe);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            .stTextInput>div>div>input {
                border-radius: 8px;
            }
            .audio-card {
                padding: 1rem;
                background-color: #ffffffdd;
                border-radius: 10px;
                margin-bottom: 1rem;
                box-shadow: 0px 0px 8px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🎙️ Voice-Based Health Assistant")
    st.markdown("Upload a **voice query (WAV/MP3)** and receive a transcribed & AI-generated medical response below:")

    with st.container():
        audio_file = st.file_uploader("🔊 Upload your voice file", type=["wav", "mp3"])

        if audio_file:
            with NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp:
                tmp.write(audio_file.read())
                temp_path = tmp.name

            with st.container():
                st.markdown("### 🎧 Audio Preview")
                st.audio(temp_path, format="audio/wav")

            if st.button("🧠 Transcribe and Analyze", use_container_width=True):
                with st.spinner("🔍 Transcribing your voice and generating response..."):
                    try:
                        transcription = transcribe_audio(temp_path)

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("### 📝 Transcription")
                            st.success(transcription)

                        with col2:
                            st.markdown("### 💬 AI Medical Response")
                            response = ask_health_question(transcription)
                            st.info(response)

                        log_event("voice_query", f"Q: {transcription} => A: {response}")
                    except Exception as e:
                        st.error(f"❌ Error processing voice query: {e}")

            os.remove(temp_path)
