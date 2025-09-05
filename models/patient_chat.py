import streamlit as st
from utils.health_llm import generate_streaming_text
from utils.helper import log_event

# Attempt to import optional audio input
try:
    from st_audiorec import st_audiorec
except ImportError:
    st_audiorec = None

def patient_chat_ui():
    st.markdown("""
        <style>
        .chat-bubble {
            background-color: #1c1c1e;
            color: #fff;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
        }
        .user-msg {
            background-color: #0a84ff;
            color: white;
        }
        .ai-msg {
            background-color: #2c2c2e;
            color: white;
        }
        .follow-up-button > button {
            background-color: #262730 !important;
            color: #fff !important;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: 1px solid #3c3c3c;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("💬 Patient Chat Assistant")
    st.caption("Intelligent, empathetic AI assistant to help with your health queries.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 🎙️ Voice input
    user_input = ""
    audio_text = ""
    if st_audiorec:
        with st.expander("🎙️ Use Voice Input", expanded=False):
            audio_bytes = st_audiorec()
            if audio_bytes:
                st.info("Audio captured. (Speech-to-text feature not yet implemented)")
                audio_text = "What are the symptoms of diabetes?"  # Placeholder
                st.write(f"Recognized Text: `{audio_text}`")
    else:
        st.info("🎙️ Voice input module not installed. Proceeding with text input.")

    # 🧾 Chat Form UI
    with st.form("chat_form"):
        typed_input = st.text_input("Type your health question:", placeholder="e.g. What are the symptoms of diabetes?")
        submit = st.form_submit_button("Ask HealthAI")

    user_input = typed_input.strip() if typed_input.strip() else audio_text.strip()

    if submit and user_input:
        with st.spinner("HealthAI is thinking..."):
            try:
                prompt = (
                    "You are an empathetic healthcare assistant.\n"
                    "Answer the following question clearly and professionally.\n\n"
                    f"Question: {user_input}\n\n"
                    "Answer:"
                )

                st.session_state.chat_history.append(("🧑 You", user_input))

                # Streamed AI Response
                with st.chat_message("ai"):
                    stream_output = st.empty()
                    full_response = ""
                    for token in generate_streaming_text(prompt, max_new_tokens=300, temperature=0.7):
                        full_response += token
                        stream_output.markdown(full_response + "▌")
                    stream_output.markdown(full_response)

                st.session_state.chat_history.append(("🤖 HealthAI", full_response.strip()))
                log_event("chat", f"User: {user_input} => AI: {full_response.strip()}")

                # 🔁 Follow-up suggestions
                st.markdown("#### 🔁 Follow-up Suggestions:")
                follow_ups = [
                    "Can you explain more about this condition?",
                    "What should I ask my doctor?",
                    "Are there any medications or treatments?",
                    "What lifestyle changes help?"
                ]
                for suggestion in follow_ups:
                    if st.button(suggestion, key=suggestion, help="Ask this as a follow-up", type="secondary"):
                        st.session_state.chat_history.append(("🧑 You", suggestion))
                        st.rerun()

            except Exception as e:
                st.session_state.chat_history.append(("🤖 HealthAI", "⚠️ An error occurred."))
                log_event("error", f"Chat error: {e}")

    # 📜 Chat History Display
    st.markdown("---")
    for speaker, message in st.session_state.chat_history:
        class_name = "user-msg" if "You" in speaker else "ai-msg"
        st.markdown(f'<div class="chat-bubble {class_name}"><b>{speaker}:</b><br>{message}</div>', unsafe_allow_html=True)

    # Scroll to bottom script
    st.markdown("<div id='scroll-to-bottom'></div>", unsafe_allow_html=True)
    st.markdown("""
        <script>
            var element = document.getElementById("scroll-to-bottom");
            element.scrollIntoView({behavior: "smooth"});
        </script>
    """, unsafe_allow_html=True)
