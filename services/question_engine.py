import random
from services.question_bank import QUESTION_BANK


def generate_questions(resume_data, role, total_questions=5):

    questions = []

    # -------------------------------
    # ROLE FETCH + SAFE FALLBACK
    # -------------------------------
    role_data = QUESTION_BANK.get(role)

    if not role_data:
        print("⚠️ Role not found → using fallback role")
        role_data = list(QUESTION_BANK.values())[0]

    # -------------------------------
    # GENERAL QUESTIONS
    # -------------------------------
    general_questions = role_data.get("General", [])

    if not general_questions:
        general_questions = [
            {
                "question": "Tell me about yourself",
                "reference_answer": "Explain your background, skills, and experience."
            }
        ]

    questions.extend([
        {**q, "category": "General"}
        for q in general_questions
    ])

    # -------------------------------
    # SKILL QUESTIONS
    # -------------------------------
    skills = resume_data.get("skills", [])
    skill_data = role_data.get("Skills", {})

    for skill in skills:
        if skill in skill_data:
            questions.extend([
                {**q, "category": skill}
                for q in skill_data[skill]
            ])

    # -------------------------------
    # PROJECT QUESTIONS
    # -------------------------------
    for proj in resume_data.get("projects", []):
        for template in role_data.get("Project", []):
            questions.append({
                "question": template["question_template"].format(project=proj.get("name", "your project")),
                "reference_answer": template["reference_template"],
                "category": "Project"
            })

    # -------------------------------
    # EXPERIENCE QUESTIONS
    # -------------------------------
    for exp in resume_data.get("experience", []):
        for template in role_data.get("Experience", []):
            questions.append({
                "question": template["question_template"].format(role=exp.get("role", "your role")),
                "reference_answer": template["reference_template"],
                "category": "Experience"
            })

    # -------------------------------
    # FINAL FALLBACK (VERY IMPORTANT)
    # -------------------------------
    if not questions:
        questions = [
            {
                "question": "Tell me about yourself",
                "reference_answer": "Explain your background.",
                "category": "Fallback"
            },
            {
                "question": "What are your strengths?",
                "reference_answer": "Discuss your strengths with examples.",
                "category": "Fallback"
            }
        ]

    # -------------------------------
    # REMOVE DUPLICATES
    # -------------------------------
    unique_questions = []
    seen = set()

    for q in questions:
        if q["question"] not in seen:
            unique_questions.append(q)
            seen.add(q["question"])

    random.shuffle(unique_questions)

    # -------------------------------
    # SMART CATEGORY SELECTION
    # -------------------------------
    selected = []
    used_categories = set()

    for q in unique_questions:
        if q["category"] not in used_categories:
            selected.append(q)
            used_categories.add(q["category"])

        if len(selected) == total_questions:
            break

    if len(selected) < total_questions:
        remaining = [q for q in unique_questions if q not in selected]
        selected.extend(remaining[:total_questions - len(selected)])

    return selected