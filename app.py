# import streamlit as st
# from models import (
#     profile_management,
#     disease_prediction,
#     treatment_plan,
#     health_analytics,
#     patient_chat,
#     xray_analysis,
#     voice_query,
#     document_summary
# )

# # 🧬 Page Configuration
# st.set_page_config(
#     page_title="HealthAI Assistant",
#     page_icon="🧬",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Define options
# module_options = {
#     "📋 Profile & Vitals": profile_management.patient_profile_ui,
#     "💊 Treatment Plan": treatment_plan.treatment_plan_ui,
#     "🔍 Disease Prediction": disease_prediction.disease_prediction_ui,
#     "📊 Health Analytics": health_analytics.run_health_analytics,
#     "🗣️ Patient Chat": patient_chat.patient_chat_ui,
#     "🩻 X-Ray Analysis": xray_analysis.xray_analysis_ui,
#     "📁 Medical Report Summary": document_summary.document_summary_ui,
#     "🎙️ Voice Query": voice_query.voice_query_ui,
# }

# # Initialize session state to track active module
# if "selected_module" not in st.session_state:
#     st.session_state.selected_module = "🏠 Dashboard"

# # --- Main Dashboard UI ---
# if st.session_state.selected_module == "🏠 Dashboard":
#     st.title("🏥 HealthAI Dashboard")
#     st.markdown("**Explore AI-powered healthcare features:**")
    
#     cols = st.columns(3)
#     keys = list(module_options.keys())

#     for idx, key in enumerate(keys):
#         with cols[idx % 3]:
#             st.subheader(key)
#             if st.button(f"Launch {key}", key=f"btn_{key}"):
#                 st.session_state.selected_module = key
#                 st.rerun()

# # --- Load Selected Feature ---
# elif st.session_state.selected_module in module_options:
#     st.button("🔙 Back to Dashboard", on_click=lambda: st.session_state.update({"selected_module": "🏠 Dashboard"}))
#     st.header(st.session_state.selected_module)
#     module_options[st.session_state.selected_module]()

import streamlit as st

# ✅ Must be first command
st.set_page_config(page_title="HealthAI", layout="wide")

# --- Theme toggle setup ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# Define colors
if st.session_state.theme == "dark":
    bg_color = "#0F111A"
    text_color = "#FFFFFF"
    card_color = "rgba(255, 255, 255, 0.05)"
    accent_color = "#00BFFF"
else:
    bg_color = "#F5F7FA"
    text_color = "#000000"
    card_color = "rgba(255, 255, 255, 0.7)"
    accent_color = "#007BFF"

# --- Custom CSS: Glassmorphism + Theme Toggle + Buttons ---
st.markdown(
    f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .main {{
            background-color: {bg_color};
        }}
        .theme-toggle {{
            position: absolute;
            top: 15px;
            right: 20px;
        }}
        .stButton > button {{
            background: linear-gradient(135deg, {accent_color}, #6dd5fa);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            transition: 0.3s ease;
        }}
        .stButton > button:hover {{
            box-shadow: 0 0 10px {accent_color};
            transform: scale(1.05);
        }}
        .card {{
            background: {card_color};
            padding: 1.5rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0px 4px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
            color: {text_color};
        }}
        .module-tile {{
            font-weight: bold;
            font-size: 1.1rem;
            color: {accent_color};
            margin-top: 0.5rem;
        }}
        h1 {{
            color: {accent_color};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Theme toggle button (top right)
st.markdown('<div class="theme-toggle">', unsafe_allow_html=True)
st.button("🌞" if st.session_state.theme == "light" else "🌙", on_click=toggle_theme)
st.markdown('</div>', unsafe_allow_html=True)

# --- Logo & Title ---
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 30px;">
    <div style="display: flex; align-items: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/3063/3063826.png" width="50" style="margin-right: 10px;" />
        <h1 style="margin: 0;">HealthAI</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Import Module UIs ---
from models import (
    profile_management,
    disease_prediction,
    treatment_plan,
    health_analytics,
    patient_chat,
    xray_analysis,
    voice_query,
    document_summary
)

# --- Dashboard Navigation ---
module_options = {
    "📋 Profile & Vitals": profile_management.patient_profile_ui,
    "💊 Treatment Plan": treatment_plan.treatment_plan_ui,
    "🔍 Disease Prediction": disease_prediction.disease_prediction_ui,
    "📊 Health Analytics": health_analytics.run_health_analytics,
    "🗣️ Patient Chat": patient_chat.patient_chat_ui,
    "🩻 X‑Ray Analysis": xray_analysis.xray_analysis_ui,
    "📁 Report Summary": document_summary.document_summary_ui,
    "🎙️ Voice Query": voice_query.voice_query_ui,
}

if "selected_module" not in st.session_state:
    st.session_state.selected_module = "🏠 Dashboard"

# --- Main Dashboard ---
if st.session_state.selected_module == "🏠 Dashboard":
    st.subheader("Explore AI-powered Healthcare Features")
    cols = st.columns(4, gap="medium")
    keys = list(module_options.keys())
    for i, key in enumerate(keys):
        with cols[i % 4]:
            if st.button(key, key=f"tile_{key}"):
                st.session_state.selected_module = key
                st.experimental_rerun()
            st.markdown(f'<div class="card"><div class="module-tile">{key}</div></div>', unsafe_allow_html=True)
else:
    if st.button("🔙 Back to Dashboard"):
        st.session_state.selected_module = "🏠 Dashboard"
        st.experimental_rerun()

    st.markdown(f"## {st.session_state.selected_module}")
    module_options[st.session_state.selected_module]()

# --- Footer ---
st.markdown(
    f"<div style='text-align:center; margin-top:50px; color:{text_color};'>© 2025 <b>HealthAI</b> | Built with ❤️ using Streamlit</div>",
    unsafe_allow_html=True
)
    