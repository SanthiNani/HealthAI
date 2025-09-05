# import streamlit as st
# from utils.helper import (
#     get_all_patient_ids,
#     get_patient_record,
#     save_patient_db,
#     log_event
# )
# from utils.health_llm import generate_streaming_text  # Updated LLM streaming generator


# def treatment_plan_ui():
#     st.header("💊 AI-Powered Treatment Plan")

#     patient_ids = get_all_patient_ids()
#     if not patient_ids:
#         st.info("No patients available.")
#         return

#     selected_id = st.selectbox("Select a patient", options=patient_ids)

#     if not selected_id:
#         return

#     patient_data = get_patient_record(selected_id)
#     visits = patient_data.get("visits", [])

#     if not visits:
#         st.warning("No visit history available for this patient.")
#         return

#     recent_visit = visits[-1]

#     st.markdown("### 📝 Latest Visit Info")
#     st.write(f"🗓️ Date: {recent_visit.get('timestamp', '')[:10]}")
#     st.write(f"🩺 Symptoms: `{recent_visit.get('symptoms', 'N/A')}`")
#     st.write(f"🏥 Diagnosis: `{recent_visit.get('diagnosis', 'N/A')}`")

#     if st.button("🧠 Generate AI Treatment Plan"):
#         symptoms = recent_visit.get("symptoms", "")
#         diagnosis = recent_visit.get("diagnosis", "")

#         if not symptoms or not diagnosis:
#             st.error("Both symptoms and diagnosis are required for treatment planning.")
#             return

#         with st.spinner("Generating treatment plan..."):
#             prompt = (
#                 "You are a trusted medical assistant.\n"
#                 f"Patient symptoms: {symptoms}\n"
#                 f"Diagnosis: {diagnosis}\n\n"
#                 "Provide a clear, structured, step-by-step, medically accurate treatment plan:\n"
#                 "Treatment Plan:"
#             )

#             output_box = st.empty()
#             full_response = ""

#             try:
#                 # No `stream=True` argument — handled inside `generate_streaming_text`
#                 for chunk in generate_streaming_text(prompt, max_new_tokens=300, temperature=0.7):
#                     full_response += chunk
#                     output_box.markdown(f"```markdown\n{full_response.strip()}\n```")
#             except Exception as e:
#                 log_event("error", f"Streaming failed: {e}")
#                 st.error("⚠️ Failed to generate treatment plan.")
#                 return

#             if not full_response.strip():
#                 st.warning("⚠️ Sorry, the AI could not generate a valid response.")
#             else:
#                 recent_visit["ai_treatment_plan"] = full_response.strip()
#                 save_patient_db(selected_id, patient_data)
#                 log_event("treatment_plan", f"Generated for patient: {selected_id}")
#                 st.success("✅ Treatment Plan Generated")


import streamlit as st
from utils.helper import (
    get_all_patient_ids,
    get_patient_record,
    save_patient_db,
    log_event
)
from utils.health_llm import generate_streaming_text

def treatment_plan_ui():
    st.markdown("""
        <style>
        .stSelectbox > div { background-color: #f5f9ff; padding: 0.3rem 0.5rem; border-radius: 5px; }
        .treatment-box {
            background-color: #f8f9fa;
            padding: 1.2rem;
            border-radius: 8px;
            border-left: 5px solid #4A90E2;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            font-family: 'Segoe UI', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("💊 AI-Powered Treatment Planner")

    st.markdown("Let our smart assistant guide your patient's treatment with precision and clarity. 💡")

    patient_ids = get_all_patient_ids()
    if not patient_ids:
        st.info("⚠️ No patients found in the database.")
        return

    selected_id = st.selectbox("📋 Select Patient", options=patient_ids)

    if not selected_id:
        return

    patient_data = get_patient_record(selected_id)
    visits = patient_data.get("visits", [])

    if not visits:
        st.warning("⚠️ This patient does not have any visit history.")
        return

    recent_visit = visits[-1]

    st.markdown("### 🧾 Latest Visit Summary")
    with st.container():
        st.markdown(f"📅 **Date:** `{recent_visit.get('timestamp', '')[:10]}`")
        st.markdown(f"🩺 **Symptoms:** `{recent_visit.get('symptoms', 'N/A')}`")
        st.markdown(f"🏥 **Diagnosis:** `{recent_visit.get('diagnosis', 'N/A')}`")

    st.markdown("---")

    if st.button("🧠 Generate AI Treatment Plan"):
        symptoms = recent_visit.get("symptoms", "")
        diagnosis = recent_visit.get("diagnosis", "")

        if not symptoms or not diagnosis:
            st.error("🚫 Both symptoms and diagnosis must be present to generate a treatment plan.")
            return

        with st.spinner("💬 AI is analyzing... Please wait."):
            prompt = (
                "You are a trusted medical assistant.\n"
                f"Patient symptoms: {symptoms}\n"
                f"Diagnosis: {diagnosis}\n\n"
                "Provide a clear, structured, step-by-step, medically accurate treatment plan:\n"
                "Treatment Plan:"
            )

            output_box = st.empty()
            full_response = ""

            try:
                for chunk in generate_streaming_text(prompt, max_new_tokens=300, temperature=0.7):
                    full_response += chunk
                    output_box.markdown(
                        f"<div class='treatment-box'><pre>{full_response.strip()}</pre></div>",
                        unsafe_allow_html=True
                    )
            except Exception as e:
                log_event("error", f"Streaming failed: {e}")
                st.error("❌ An error occurred while generating the treatment plan.")
                return

            if not full_response.strip():
                st.warning("⚠️ Sorry, the AI could not generate a valid response.")
            else:
                recent_visit["ai_treatment_plan"] = full_response.strip()
                save_patient_db(selected_id, patient_data)
                log_event("treatment_plan", f"Generated for patient: {selected_id}")
                st.success("✅ AI Treatment Plan successfully generated and saved.")

