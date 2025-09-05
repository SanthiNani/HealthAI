import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.helper import log_event
import PyPDF2
import torch

# ✅ HuggingFace Model
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

@st.cache_resource
def load_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_auth_token=True)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            use_auth_token=True
        )
        return tokenizer, model
    except Exception as e:
        log_event("error", f"Model load failed: {e}")
        st.error("❌ Could not load Mistral-7B model. Ensure proper access.")
        raise e

def read_uploaded_file(file):
    try:
        if file.name.endswith(".txt"):
            return file.read().decode("utf-8")
        elif file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(file)
            return "\n".join(page.extract_text() or "" for page in pdf_reader.pages).strip()
        else:
            return ""
    except Exception as e:
        log_event("error", f"File parsing failed: {e}")
        return ""

def summarize_document(text):
    tokenizer, model = load_model()
    prompt = (
        "You are a professional medical summarization assistant.\n"
        "Read the following medical report and provide a structured, accurate summary:\n\n"
        f"{text}\n\n"
        "Summary:"
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=350,
            temperature=0.6,
            top_k=50,
            top_p=0.9
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    summary_start = decoded.lower().find("summary:")
    return decoded[summary_start + len("summary:"):].strip() if summary_start != -1 else decoded.strip()


def document_summary_ui():
    st.markdown(
        "<h2 style='color:#4FC3F7; text-align:center;'>📄 AI-Powered Medical Report Summarizer</h2>",
        unsafe_allow_html=True
    )
    st.markdown("<p style='text-align:center;'>Upload your medical report as PDF or TXT and receive a detailed AI-generated summary.</p>", unsafe_allow_html=True)
    st.markdown("---")

    file = st.file_uploader("📤 Upload Report (PDF or TXT)", type=["pdf", "txt"])

    if file:
        raw_text = read_uploaded_file(file)

        if raw_text:
            st.markdown("### 🔍 Document Preview")
            st.text_area("Extracted Text", raw_text[:3000], height=250, key="preview")

            if st.button("🧠 Generate Summary", use_container_width=True):
                with st.spinner("🌀 Analyzing the document and generating summary..."):
                    try:
                        summary = summarize_document(raw_text)
                        st.markdown("### ✅ AI-Generated Summary")
                        st.markdown(
                            f"<div style='padding:20px; background-color:#e3f2fd; border-radius:10px; font-size:16px;'>{summary}</div>",
                            unsafe_allow_html=True
                        )
                        log_event("document_summary", f"{file.name} => {summary[:100]}...")
                    except Exception as e:
                        st.error(f"❌ Failed to summarize: {e}")
                        log_event("error", f"Document summarization failed: {e}")
        else:
            st.error("⚠️ Could not extract text from the uploaded file.")
