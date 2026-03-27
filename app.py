import streamlit as st
import time
import whisper
import tempfile

from streamlit_mic_recorder import mic_recorder

from services.resume_parser import extract_text_from_pdf, parse_resume
from services.question_engine import generate_questions
from utils.tts import speak_question
from services.evaluation_engine import evaluate_answer


model = whisper.load_model("base")


def speech_to_text(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        result = model.transcribe(tmp_path)
        return result["text"]

    except Exception as e:
        st.error(f"Speech recognition failed: {e}")
        return ""


# SESSION
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

if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = None


st.title("AI Interview Maker")

role = st.selectbox(
    "Select role:",
    [
        "Full Stack Developer",
        "Frontend Developer",
        "Backend Developer",
        "Software Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "DevOps Engineer",
        "Cloud Engineer"
    ]
)

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])


if uploaded_file and not st.session_state.started:

    raw_text = extract_text_from_pdf(uploaded_file)
    resume_data = parse_resume(raw_text)

    if st.button("Start Interview"):

        st.session_state.questions = generate_questions(resume_data, role)

        if not st.session_state.questions:
            st.error("No questions generated.")
            st.stop()

        st.session_state.started = True
        st.session_state.current_q = 0
        st.session_state.start_time = time.time()
        st.session_state.answers = {}

        st.rerun()


if st.session_state.started:

    elapsed = time.time() - st.session_state.start_time
    remaining = 600 - int(elapsed)

    st.subheader(f"⏳ Time Remaining: {remaining//60}:{remaining%60:02d}")

    if st.session_state.current_q < len(st.session_state.questions):

        q_data = st.session_state.questions[st.session_state.current_q]

        question = q_data["question"]
        reference_answer = q_data["reference_answer"]

        # 🔥 FIX TIMER
        if st.session_state.question_start_time is None:
            st.session_state.question_start_time = time.time()

        st.subheader(f"Question {st.session_state.current_q + 1}")
        st.write(question)
        # ---------------------------
# 🎤 Voice Recorder (RESTORE THIS)
# ---------------------------
        st.write("🎤 Record your answer")

        audio = mic_recorder(
            start_prompt="Start Recording",
            stop_prompt="Stop Recording",
            just_once=True,
            key=f"recorder_{st.session_state.current_q}"
        )

        if audio and "bytes" in audio:

            voice_text = speech_to_text(audio["bytes"])

            if voice_text:
                st.success("Voice detected")
                st.write("🗣 Recognized:", voice_text)

                st.session_state[f"answer_{st.session_state.current_q}"] = voice_text

                st.rerun()

        audio_file = speak_question(question)
        st.audio(audio_file)

        answer = st.session_state.get(
            f"answer_{st.session_state.current_q}", 
            ""
        )

        answer = st.text_area(
            "Your Answer:",
            value=answer,
            key=f"answer_{st.session_state.current_q}"
        )

        if answer and st.button("Next Question"):

            end_time = time.time()
            start_time = st.session_state.question_start_time

            st.session_state.answers[st.session_state.current_q] = {
                "answer": answer,
                "start_time": start_time,
                "end_time": end_time
            }

            st.session_state.question_start_time = None
            st.session_state.current_q += 1
            st.rerun()

    else:

        st.success("Interview Completed!")

        total = 0
        results = []

        for i, data in st.session_state.answers.items():

            q_data = st.session_state.questions[i]

            result = evaluate_answer(
                data["answer"],
                q_data["reference_answer"],
                data["start_time"],
                data["end_time"]
            )

            total += result["total_score"]

            results.append((q_data["question"], data["answer"], result))

        overall = total // len(results) if results else 0

        st.subheader(f"Overall Score: {overall}/100")

        for q, a, r in results:
            st.write("Q:", q)
            st.write("A:", a)
            st.write("Score:", r["total_score"])
            st.write("Emotion:", r["emotion"])
            st.write("Fluency:", r["fluency_score"])
            st.write("Confidence:", r["confidence_score"])

            for f in r["feedback"]:
                st.write("-", f)

            st.markdown("---")