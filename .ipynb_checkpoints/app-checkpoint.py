import streamlit as st
import time
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript

from services.resume_parser import extract_text_from_pdf, extract_skills
from services.question_engine import generate_questions
from utils.text_cleaner import clean_resume_text


# ---------------------------
# 1️⃣ Initialize Session State
# ---------------------------
if "started" not in st.session_state:
    st.session_state.started = False

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "start_time" not in st.session_state:
    st.session_state.start_time = None


# ---------------------------
# 2️⃣ UI Title
# ---------------------------
st.title("AI Interview Maker")


# ---------------------------
# 3️⃣ Role Selection
# ---------------------------
role = st.selectbox(
    "Select role:",
    ["Full Stack Developer",
     "Machine Learning Engineer"]
)


# ---------------------------
# 4️⃣ Resume Upload
# ---------------------------
uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

if uploaded_file and not st.session_state.started:

    raw_text = extract_text_from_pdf(uploaded_file)
    clean_text = clean_resume_text(raw_text)
    skills = extract_skills(clean_text)

    st.subheader("Extracted Skills")
    st.write(skills)

    if st.button("Start Interview"):

        st.session_state.questions = generate_questions(skills, role)
        st.session_state.current_q = 0
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.session_state.answers = {}

        st.rerun()


# ---------------------------
# 5️⃣ Interview Mode
# ---------------------------
if st.session_state.started:

    elapsed = time.time() - st.session_state.start_time
    remaining = 600 - int(elapsed)

    minutes = max(0, remaining // 60)
    seconds = max(0, remaining % 60)

    st.subheader(f"⏳ Time Remaining: {minutes}:{seconds:02d}")

    if remaining <= 0:
        st.warning("Time's up! Interview Ended.")
        st.session_state.started = False

    else:

        if st.session_state.current_q < len(st.session_state.questions):

            question = st.session_state.questions[st.session_state.current_q]

            st.subheader(f"Question {st.session_state.current_q + 1}")
            st.write(question)

            # Inject speech recognition JS
            components.html("""
                <button onclick="startDictation()">🎙 Start Recording</button>
                <button onclick="stopDictation()">⏹ Stop Recording</button>
                <p><strong>Transcript:</strong></p>
                <textarea id="output" rows="5" style="width:100%;"></textarea>

                <script>
                var recognition;
                var finalTranscript = "";

                function startDictation() {
                    if (!('webkitSpeechRecognition' in window)) {
                        alert("Speech Recognition not supported.");
                    } else {
                        recognition = new webkitSpeechRecognition();
                        recognition.continuous = true;
                        recognition.interimResults = false;
                        recognition.lang = "en-US";

                        recognition.onresult = function(event) {
                            finalTranscript =
                                event.results[event.results.length - 1][0].transcript;
                            document.getElementById("output").value = finalTranscript;
                            window.parent.postMessage(
                                {type: "TRANSCRIPT", text: finalTranscript},
                                "*"
                            );
                        };

                        recognition.start();
                    }
                }

                function stopDictation() {
                    if (recognition) {
                        recognition.stop();
                    }
                }
                </script>
            """, height=300)

            # Capture transcript from JS
            transcript = st_javascript("""
                new Promise((resolve) => {
                    window.addEventListener("message", (event) => {
                        if (event.data.type === "TRANSCRIPT") {
                            resolve(event.data.text);
                        }
                    });
                });
            """)

            if transcript:
                st.session_state.answers[st.session_state.current_q] = transcript

            if st.button("Next Question"):
                st.session_state.current_q += 1
                st.rerun()

        else:
            st.success("Interview Completed!")
            st.session_state.started = False

            st.subheader("Your Answers:")
            st.write(st.session_state.answers)