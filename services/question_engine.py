import random
from services.question_templates import (
    SKILL_QUESTIONS,
    PROJECT_TEMPLATES,
    EXPERIENCE_TEMPLATES,
    BEHAVIORAL_TEMPLATES
)


def generate_questions(resume_data, role, total_questions=5):

    questions_pool = []

    # --------------------------
    # Skill-based
    # --------------------------
    
    # Skill-based
    for skill in resume_data["skills"]:
        if skill in SKILL_QUESTIONS:
            for q in SKILL_QUESTIONS[skill]:
                questions_pool.append({
                    "question": q["question"],
                    "reference_answer": q["reference"]
                })

    # --------------------------
    # Project-based
    # --------------------------
    for project in resume_data["projects"]:
        for template in PROJECT_TEMPLATES:
            questions_pool.append({
                "question": template["question_template"].format(
                    project_name=project["name"]
                ),
                "reference_answer": template["reference_template"].format(
                    project_name=project["name"]
                )
            })

    # --------------------------
    # Experience-based
    # --------------------------
    for exp in resume_data["experience"]:
        for template in EXPERIENCE_TEMPLATES:
            questions_pool.append({
                "question": template["question_template"].format(
                    role=exp["role"]
                ),
                "reference_answer": template["reference_template"].format(
                    role=exp["role"]
                )
            })

    # --------------------------
    # Behavioral
    # --------------------------
    for q in BEHAVIORAL_TEMPLATES:
        questions_pool.append({
            "question": q["question"],
            "reference_answer": q["reference"]
        })

    # Remove duplicates
    unique_questions = []
    seen = set()

    for q in questions_pool:
        if q["question"] not in seen:
            unique_questions.append(q)
            seen.add(q["question"])

    random.shuffle(unique_questions)

    return unique_questions[:total_questions]