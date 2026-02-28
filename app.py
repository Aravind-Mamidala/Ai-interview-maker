import streamlit as st
import time

from services.resume_parser import extract_text_from_pdf, parse_resume
from services.question_engine import generate_questions
from utils.text_cleaner import clean_resume_text

from services.evaluation_engine import evaluate_answer


# ---------------------------
# 🔹 Initialize Session State
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
# 🔹 UI
# ---------------------------
st.title("AI Interview Maker")

role = st.selectbox(
    "Select role:",
    ["Full Stack Developer",
     "Machine Learning Engineer"]
)

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])


# ---------------------------
# 🔹 Resume Processing
# ---------------------------
if uploaded_file and not st.session_state.started:

    raw_text = extract_text_from_pdf(uploaded_file)

    # 🔍 DEBUG RAW TEXT
    st.subheader("RAW TEXT DEBUG")

    st.write("Length of raw_text:", len(raw_text))

    st.code(raw_text[:2000])
    
    resume_data = parse_resume(raw_text)

    st.subheader("Parsed Resume Data")
    st.write(resume_data)

    if st.button("Start Interview"):
        st.session_state.questions = generate_questions(resume_data, role)
        st.session_state.current_q = 0
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.session_state.answers = {}
        st.rerun()

# ---------------------------
# 🔹 Interview Mode
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

            question_data = st.session_state.questions[st.session_state.current_q]
            question = question_data["question"]
            reference_answer = question_data["reference_answer"]
            
            st.subheader(f"Question {st.session_state.current_q + 1}")
            st.write(question)

            answer = st.text_area(
                "Type your answer here:",
                key=f"answer_{st.session_state.current_q}"
            )

            if answer.strip() != "":
                if st.button("Next Question"):
                    st.session_state.answers[st.session_state.current_q] = answer
                    st.session_state.current_q += 1
                    st.rerun()
            else:
                st.info("Please type your answer before proceeding.")

        else:
            st.success("Interview Completed!")
            st.session_state.started = False

            st.subheader("Evaluation Report")

            total_interview_score = 0
            detailed_results = []

            for q_index, answer in st.session_state.answers.items():

                question_data = st.session_state.questions[q_index]

                question = question_data["question"]
                reference_answer = question_data["reference_answer"]

                result = evaluate_answer(answer, reference_answer)

                total_interview_score += result["total_score"]

                detailed_results.append({"question": question,"answer": answer,"score": result["total_score"],"feedback": result["feedback"]
    })
            if detailed_results:
                overall_score = int(total_interview_score / len(detailed_results))
            else:
                overall_score = 0

            st.subheader(f"Overall Interview Score: {overall_score} / 100")

            for idx, res in enumerate(detailed_results, 1):
                st.markdown(f"### Question {idx}")
                st.write("**Question:**", res["question"])
                st.write("**Your Answer:**", res["answer"])
                st.write("**Score:**", res["score"])
                if res["feedback"]:
                    st.write("**Feedback:**")
                    for fb in res["feedback"]:
                        st.write("-", fb)
                st.markdown("---")