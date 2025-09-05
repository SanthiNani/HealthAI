# utils/health_llm.py

import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
import threading
from utils.helper import log_event

# Load model from Hugging Face
MODEL_ID = "microsoft/phi-1_5"

# Cache the model and tokenizer to avoid reloading on every run
@st.cache_resource(show_spinner="🔄 Loading AI model...")
def load_model():
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch_dtype)
    model.to("cuda" if torch.cuda.is_available() else "cpu")
    return tokenizer, model

# Load model and tokenizer at module level
tokenizer, model = load_model()

# Streaming text generator
def generate_streaming_text(prompt, max_new_tokens=300, temperature=0.6):
    if not prompt.strip():
        yield "⚠️ Prompt is empty. Please enter valid input."
        return

    try:
        # Prepare streaming generator
        streamer = TextIteratorStreamer(
            tokenizer,
            skip_prompt=True,
            skip_special_tokens=True
        )
        
        # Tokenize input and move to appropriate device
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        generation_kwargs = {
            **inputs,
            "streamer": streamer,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "do_sample": True
        }

        # Run model.generate in a separate thread to allow real-time streaming
        thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
        thread.start()

        # Yield tokens one by one
        for token in streamer:
            yield token

    except Exception as e:
        log_event("error", f"Streaming generation failed: {e}")
        yield "⚠️ Failed to generate treatment plan."
