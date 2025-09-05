# models/xray_analysis.py

import streamlit as st
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
from utils.helper import log_event

# Cache the model and processor to avoid reloading on every run
@st.cache_resource
def load_xray_model():
    try:
        model_id = "microsoft/maira-2"

        processor = AutoProcessor.from_pretrained(
            model_id,
            trust_remote_code=True
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )

        return processor, model
    except Exception as e:
        log_event("error", f"Failed to load MAIRA-2 model: {e}")
        st.error(f"🚨 Error loading MAIRA-2 model: {e}")
        raise e


# Analyze a given X-ray image and return AI-generated report
def analyze_xray_image(image: Image.Image) -> str:
    try:
        processor, model = load_xray_model()

        inputs = processor(images=image, return_tensors="pt").to(model.device)

        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=300,
                do_sample=True,
                temperature=0.7
            )

        result = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        log_event("xray_report", f"Generated Report: {result[:200]}...")
        return result

    except Exception as e:
        log_event("error", f"X-ray analysis failed: {e}")
        return "⚠️ AI model failed to generate a valid X-ray report."


# Streamlit UI to upload and analyze X-ray
def xray_analysis_ui():
    st.markdown(
        """
        <style>
            .xray-container {
                background-color: #1e1e1e;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                color: white;
            }
            .xray-header {
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 1rem;
                color: #00ffd5;
            }
            .upload-label {
                font-size: 1.1rem;
                font-weight: 600;
            }
            .report-box {
                background-color: #2e2e2e;
                padding: 1rem;
                border-radius: 10px;
                margin-top: 1rem;
                font-size: 1rem;
                color: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="xray-container">', unsafe_allow_html=True)

    st.markdown('<div class="xray-header">📸 AI-Powered Chest X-Ray Analysis</div>', unsafe_allow_html=True)
    st.markdown("Let the advanced **MAIRA-2** model analyze your X-ray and generate a medical report.")

    uploaded_image = st.file_uploader("🖼️ Upload a Chest X-ray Image", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image).convert("RGB")
        st.image(image, caption="✅ Uploaded X-ray", use_column_width=True)

        if st.button("🧠 Analyze X-ray with MAIRA-2"):
            with st.spinner("🔍 Generating AI-powered report..."):
                report = analyze_xray_image(image)
                st.markdown('<div class="report-box">', unsafe_allow_html=True)
                st.markdown(f"### 📄 AI-Generated Medical Report", unsafe_allow_html=True)
                st.success(report)
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
