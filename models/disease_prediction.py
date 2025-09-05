# import streamlit as st
# from utils.health_llm import generate_streaming_text
# from utils.helper import log_event

# # Predict disease based on symptoms using LLM
# def predict_disease(symptoms: str) -> str:
#     try:
#         prompt = (
#             "You are an intelligent and reliable healthcare assistant.\n"
#             "Based on the patient's symptoms listed below, predict the most likely disease or condition.\n\n"
#             f"Symptoms: {symptoms}\n\n"
#             "Please respond with only the disease name or diagnosis."
#         )

#         # Call the updated generate_streaming_text without 'stream' argument
#         response = ""
#         for chunk in generate_streaming_text(prompt, max_new_tokens=50, temperature=0.7):
#             response += chunk

#         prediction = response.strip().split("\n")[0]
#         log_event("disease_prediction", f"Symptoms: {symptoms} => Prediction: {prediction}")
#         return prediction

#     except Exception as e:
#         log_event("error", f"Disease prediction error: {e}")
#         return "⚠️ Unable to predict disease at the moment."


# # Streamlit UI for disease prediction
# def disease_prediction_ui():
#     st.header("🩺 Disease Prediction")
#     st.write("Enter the symptoms you're experiencing, and the AI will try to predict the most likely condition.")

#     symptoms = st.text_area("Symptoms", placeholder="e.g. high fever, fatigue, rashes on skin")
#     if st.button("Predict"):
#         if symptoms.strip():
#             with st.spinner("Analyzing symptoms..."):
#                 diagnosis = predict_disease(symptoms)
#                 st.success(f"🧾 **Predicted Disease:** {diagnosis}")
#         else:
#             st.warning("⚠️ Please enter some symptoms to get a prediction.")

import streamlit as st
from utils.health_llm import generate_streaming_text
from utils.helper import log_event

# Predict disease based on symptoms using LLM
def predict_disease(symptoms: str) -> str:
    try:
        prompt = (
            "You are an intelligent and reliable healthcare assistant.\n"
            "Based on the patient's symptoms listed below, predict the most likely disease or condition.\n\n"
            f"Symptoms: {symptoms}\n\n"
            "Please respond with only the disease name or diagnosis."
        )

        response = ""
        for chunk in generate_streaming_text(prompt, max_new_tokens=50, temperature=0.7):
            response += chunk

        prediction = response.strip().split("\n")[0]
        log_event("disease_prediction", f"Symptoms: {symptoms} => Prediction: {prediction}")
        return prediction

    except Exception as e:
        log_event("error", f"Disease prediction error: {e}")
        return "⚠️ Unable to predict disease at the moment."


# 🌟 Modern, Beautiful UI for Disease Prediction
def disease_prediction_ui():
    st.markdown("""
        <style>
            .disease-box {
                background-color: #1a1c23;
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 0 15px rgba(0, 255, 255, 0.08);
                margin-top: 2rem;
            }
            .symptom-input textarea {
                background-color: #0e1117 !important;
                color: white !important;
                border: 1px solid #4d4d4d !important;
                border-radius: 12px;
                font-size: 1.1rem;
            }
            .btn-predict button {
                background-color: #00c9a7 !important;
                color: black !important;
                font-weight: bold;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-size: 1rem;
            }
            .diagnosis-box {
                background-color: #22262f;
                border-left: 5px solid #00c9a7;
                padding: 1rem;
                margin-top: 1.5rem;
                border-radius: 8px;
                font-size: 1.2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🧠 Disease Prediction")
    st.markdown("Use our intelligent AI assistant to get a **potential diagnosis** based on your symptoms.")

    st.markdown('<div class="disease-box">', unsafe_allow_html=True)

    st.markdown("### 📝 Enter Your Symptoms")
    symptoms = st.text_area(
        label="",
        placeholder="e.g. high fever, fatigue, rashes on skin",
        key="symptoms_input",
        height=150,
        label_visibility="collapsed"
    )

    predict_col, _ = st.columns([1, 5])
    with predict_col:
        predict = st.button("🔍 Predict Disease", use_container_width=True)

    if predict:
        if symptoms.strip():
            with st.spinner("🔬 Analyzing symptoms using HealthAI..."):
                diagnosis = predict_disease(symptoms)
            st.markdown(f'<div class="diagnosis-box">🧾 <strong>Predicted Disease:</strong> {diagnosis}</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter some symptoms to receive a prediction.")

    st.markdown("</div>", unsafe_allow_html=True)
