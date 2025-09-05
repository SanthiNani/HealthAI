# import streamlit as st
# import datetime
# import matplotlib.pyplot as plt
# import pandas as pd
# from utils.helper import update_patient_record, get_patient_record, log_event

# def patient_profile_ui():
#     st.header("🩺 Patient Profile & Vitals Entry")

#     patient_id = st.text_input("Patient ID (Unique)", placeholder="e.g. santhi123").strip()

#     if patient_id:
#         st.subheader("👤 Patient Information")
#         with st.form("vitals_form"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 name = st.text_input("Full Name")
#                 age = st.number_input("Age", min_value=0, max_value=120, step=1)
#                 gender = st.selectbox("Gender", ["Male", "Female", "Other"])
#             with col2:
#                 bp = st.text_input("Blood Pressure (e.g. 120/80)")
#                 pulse = st.number_input("Pulse Rate (bpm)", min_value=30, max_value=200, value=72)
#                 temperature = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, value=36.5)

#             st.markdown("#### 📝 Medical Details")
#             symptoms = st.text_area("Symptoms", placeholder="e.g. headache, nausea").strip()
#             diagnosis = st.text_area("Diagnosis", placeholder="e.g. viral fever").strip()
#             treatment = st.text_area("Prescribed Treatment", placeholder="e.g. Paracetamol 500mg").strip()

#             submitted = st.form_submit_button("✅ Save Visit")

#             if submitted:
#                 if not (name and symptoms and diagnosis):
#                     st.error("🚫 Please fill in required fields: Full Name, Symptoms, and Diagnosis.")
#                 else:
#                     visit = {
#                         "bp": bp.strip(),
#                         "pulse": pulse,
#                         "temperature": temperature,
#                         "symptoms": symptoms,
#                         "diagnosis": diagnosis,
#                         "treatment": treatment,
#                         "timestamp": datetime.datetime.now().isoformat()
#                     }

#                     metadata = {
#                         "name": name.strip(),
#                         "age": age,
#                         "gender": gender
#                     }

#                     update_patient_record(patient_id, visit, metadata)
#                     st.success("✅ Visit saved and patient data updated!")
#                     log_event("info", f"Patient data saved for {patient_id}")

#         st.divider()
#         st.subheader("📊 Patient Visit History & Vitals Analytics")

#         record = get_patient_record(patient_id)
#         if not record:
#             st.warning("⚠️ No records found.")
#             return

#         metadata = record.get("metadata", {})
#         visits = record.get("visits", [])

#         if metadata:
#             st.markdown(
#                 f"👤 **{metadata.get('name', 'Unknown')}**, {metadata.get('age', 'N/A')} years, {metadata.get('gender', 'N/A')}"
#             )

#         if visits:
#             st.markdown(f"🗂️ **Total Visits:** {len(visits)}")

#             df = pd.DataFrame(visits)
#             df['timestamp'] = pd.to_datetime(df['timestamp'])
#             df = df.sort_values('timestamp', ascending=False)

#             st.markdown("### 🕓 Visit History Table")
#             st.dataframe(df[["timestamp", "symptoms", "diagnosis", "bp", "pulse", "temperature"]].fillna("N/A"))

#             # Vitals chart
#             st.markdown("### 📈 Vitals Over Time")
#             df = df.sort_values("timestamp")
#             fig, ax = plt.subplots()

#             plotted = False
#             if "pulse" in df.columns and df["pulse"].notnull().any():
#                 ax.plot(df['timestamp'], df['pulse'], marker='o', label='Pulse (bpm)')
#                 plotted = True
#             if "temperature" in df.columns and df["temperature"].notnull().any():
#                 ax.plot(df['timestamp'], df['temperature'], marker='s', label='Temp (°C)', color='orange')
#                 plotted = True

#             if plotted:
#                 ax.set_xlabel("Visit Date")
#                 ax.set_ylabel("Vitals")
#                 ax.set_title("Vitals Trend Over Time")
#                 ax.grid(True)
#                 ax.legend()
#                 st.pyplot(fig)
#             else:
#                 st.info("Vitals data not sufficient to generate chart.")
#         else:
#             st.info("No visit data yet.")

import streamlit as st
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from utils.helper import update_patient_record, get_patient_record, log_event

def patient_profile_ui():
    st.markdown("<h1 style='color:#4CAF50;'>🏥 Patient Profile & Vitals Dashboard</h1>", unsafe_allow_html=True)

    with st.container():
        st.markdown("## 🔐 Enter Patient ID")
        patient_id = st.text_input("Patient ID (Unique)", placeholder="e.g. santhi123").strip()

    if patient_id:
        st.markdown("---")
        st.markdown("## 🧍‍♂️ Patient Vitals Entry Form")

        with st.form("vitals_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("👤 Full Name")
                age = st.number_input("🎂 Age", min_value=0, max_value=120, step=1)
                gender = st.selectbox("⚧️ Gender", ["Male", "Female", "Other"])
            with col2:
                bp = st.text_input("🩸 Blood Pressure (e.g. 120/80)")
                pulse = st.number_input("💓 Pulse Rate (bpm)", min_value=30, max_value=200, value=72)
                temperature = st.number_input("🌡️ Body Temperature (°C)", min_value=30.0, max_value=45.0, value=36.5)

            st.markdown("### 📝 Medical Notes")
            symptoms = st.text_area("🤒 Symptoms", placeholder="e.g. headache, nausea").strip()
            diagnosis = st.text_area("🔬 Diagnosis", placeholder="e.g. viral fever").strip()
            treatment = st.text_area("💊 Prescribed Treatment", placeholder="e.g. Paracetamol 500mg").strip()

            submitted = st.form_submit_button("✅ Save Patient Visit")

            if submitted:
                if not (name and symptoms and diagnosis):
                    st.error("🚫 Please fill in required fields: Full Name, Symptoms, and Diagnosis.")
                else:
                    visit = {
                        "bp": bp.strip(),
                        "pulse": pulse,
                        "temperature": temperature,
                        "symptoms": symptoms,
                        "diagnosis": diagnosis,
                        "treatment": treatment,
                        "timestamp": datetime.datetime.now().isoformat()
                    }

                    metadata = {
                        "name": name.strip(),
                        "age": age,
                        "gender": gender
                    }

                    update_patient_record(patient_id, visit, metadata)
                    st.success("✅ Visit saved successfully!")
                    log_event("info", f"Patient data saved for {patient_id}")

        st.markdown("---")
        st.markdown("## 📈 Patient History & Vitals Trends")

        record = get_patient_record(patient_id)
        if not record:
            st.warning("⚠️ No records found.")
            return

        metadata = record.get("metadata", {})
        visits = record.get("visits", [])

        if metadata:
            st.markdown(f"""
                <div style='background-color:#f1f1f1; padding:10px; border-radius:5px;'>
                <strong>👤 Name:</strong> {metadata.get('name', 'Unknown')}<br>
                <strong>🎂 Age:</strong> {metadata.get('age', 'N/A')}<br>
                <strong>⚧️ Gender:</strong> {metadata.get('gender', 'N/A')}
                </div>
            """, unsafe_allow_html=True)

        if visits:
            st.markdown(f"**🗂️ Total Visits:** `{len(visits)}`")

            df = pd.DataFrame(visits)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp', ascending=False)

            st.markdown("### 📋 Visit History Table")
            st.dataframe(df[["timestamp", "symptoms", "diagnosis", "bp", "pulse", "temperature"]].fillna("N/A"), use_container_width=True)

            st.markdown("### 📊 Vitals Trend Over Time")
            df = df.sort_values("timestamp")
            fig, ax = plt.subplots(figsize=(8, 4))

            plotted = False
            if "pulse" in df.columns and df["pulse"].notnull().any():
                ax.plot(df['timestamp'], df['pulse'], marker='o', label='Pulse (bpm)', color='#2196F3')
                plotted = True
            if "temperature" in df.columns and df["temperature"].notnull().any():
                ax.plot(df['timestamp'], df['temperature'], marker='s', label='Temperature (°C)', color='#FF9800')
                plotted = True

            if plotted:
                ax.set_xlabel("Visit Date")
                ax.set_ylabel("Vitals")
                ax.set_title("Vitals Over Time")
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.legend()
                st.pyplot(fig)
            else:
                st.info("📉 Not enough vitals data to display a chart.")
        else:
            st.info("ℹ️ No visit data yet.")
