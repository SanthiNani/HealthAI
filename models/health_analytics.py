# import streamlit as st
# import json
# import os

# from models.health_score_calculator import calculate_health_score
# from models.vitals_visualizer import generate_vital_chart
# from models.health_summary_generator import generate_health_summary


# def load_patient_data(filepath="data/patients.json"):
#     if not os.path.exists(filepath):
#         return {}
#     with open(filepath, "r") as file:
#         return json.load(file)


# def run_health_analytics():
#     st.title("🩺 Health Analytics Dashboard")

#     data = load_patient_data()
#     if not data:
#         st.warning("No patient data available.")
#         return

#     patient_ids = list(data.keys())
#     selected_patient_id = st.selectbox("Select a Patient ID", patient_ids)

#     if selected_patient_id:
#         datas = data[selected_patient_id]

#         st.subheader(f"Patient Details - {selected_patient_id}")
#         metadata = datas.get("metadata", {})
#         st.markdown(f"""
#         - **Name:** {metadata.get("name", "N/A")}
#         - **Age:** {metadata.get("age", "N/A")}
#         - **Gender:** {metadata.get("gender", "N/A")}
#         """)

#         visits = datas.get("visits", [])
#         if visits:
#             st.success(f"{len(visits)} visit(s) found.")
#         else:
#             st.warning("No visits available for this patient.")
#             return

#         # ✅ Vitals & Health Score Visualizations
#         vital_plot, score_plot = generate_vital_chart(selected_patient_id, data)
#         if vital_plot and score_plot:
#             st.image(vital_plot, caption="📊 Vital Signs Over Time", use_container_width=True)
#             st.image(score_plot, caption="📈 Health Score Trend", use_container_width=True)
#         else:
#             st.warning("Vitals or health score visualizations are unavailable.")

#         # ✅ Health Summary Download
#         st.markdown("---")
#         if st.button("📥 Download Health Summary as PDF"):
#             st.info("Generating Health Summary...")
#             pdf_path, filename = generate_health_summary(selected_patient_id, datas)
#             if pdf_path and os.path.exists(pdf_path):
#                 with open(pdf_path, "rb") as f:
#                     st.download_button("Download PDF", f, file_name=filename)
#             else:
#                 st.error("⚠️ Unable to generate summary.")


import streamlit as st
import json
import os
from models.health_score_calculator import calculate_health_score
from models.vitals_visualizer import generate_vital_chart
from models.health_summary_generator import generate_health_summary

def load_patient_data(filepath="data/patients.json"):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as file:
        return json.load(file)

def run_health_analytics():
    st.markdown("<h2 style='text-align:center; color:#3d6cb9;'>🩺 Health Analytics Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: -10px;'>", unsafe_allow_html=True)

    data = load_patient_data()
    if not data:
        st.warning("⚠️ No patient data available.")
        return

    st.markdown("### 👤 Select a Patient")
    patient_ids = list(data.keys())
    selected_patient_id = st.selectbox("Choose a Patient ID", patient_ids)

    if selected_patient_id:
        patient_data = data[selected_patient_id]
        metadata = patient_data.get("metadata", {})
        visits = patient_data.get("visits", [])

        with st.container():
            st.markdown("#### 🧾 Patient Information")
            col1, col2, col3 = st.columns(3)
            col1.metric("🧑 Name", metadata.get("name", "N/A"))
            col2.metric("🎂 Age", metadata.get("age", "N/A"))
            col3.metric("⚧️ Gender", metadata.get("gender", "N/A"))

        st.markdown("### 📅 Visit Summary")
        if visits:
            st.success(f"✅ Found **{len(visits)}** visit(s).")
        else:
            st.error("❌ No visit records found for this patient.")
            return

        # ✅ Vitals & Health Score Visualizations
        vital_plot, score_plot = generate_vital_chart(selected_patient_id, data)
        st.markdown("### 📈 Health Trends")
        chart_col1, chart_col2 = st.columns(2)
        if vital_plot:
            chart_col1.image(vital_plot, caption="📊 Vitals Over Time", use_container_width=True)
        else:
            chart_col1.warning("⚠️ Vitals chart not available.")

        if score_plot:
            chart_col2.image(score_plot, caption="📉 Health Score Trend", use_container_width=True)
        else:
            chart_col2.warning("⚠️ Health score chart not available.")

        # ✅ PDF Summary Section
        st.markdown("---")
        st.markdown("### 📥 Export Health Summary")
        with st.expander("Click to generate and download full health summary report"):
            if st.button("📄 Generate & Download PDF"):
                with st.spinner("🧠 Generating PDF..."):
                    pdf_path, filename = generate_health_summary(selected_patient_id, patient_data)
                    if pdf_path and os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f:
                            st.download_button("⬇️ Download Summary PDF", f, file_name=filename, mime="application/pdf")
                    else:
                        st.error("❌ Failed to generate summary.")
