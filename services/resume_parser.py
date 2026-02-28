import fitz
import re


SKILL_DATABASE = [
    "Python", "Java", "C++", "JavaScript",
    "React.js", "Node.js", "Express.js",
    "MongoDB", "MySQL",
    "Machine Learning", "Deep Learning",
    "TensorFlow", "PyTorch",
    "Docker", "AWS", "Git", "Linux",
    "RESTful APIs"
]


# -------------------------
# Extract raw text
# -------------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text("text")
    return text


# -------------------------
# Extract skills
# -------------------------
def extract_skills(text):
    found_skills = []

    for skill in SKILL_DATABASE:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return list(set(found_skills))


# -------------------------
# Extract projects
# -------------------------
def extract_projects(text):
    projects = []

    match = re.search(
        r'Projects\n(.*?)\nExperience',
        text,
        re.DOTALL
    )

    if not match:
        return projects

    project_section = match.group(1)
    lines = project_section.split("\n")

    current_project = None
    description_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Skip metadata lines
        if line.startswith("Live:") or line.startswith("Backend API:"):
            continue

        # Detect clean project title
        if (
            not line.startswith("•")
            and "–" in line
            and ".com" not in line
            and "GitHub" not in line
        ):
            if current_project:
                current_project["description"] = " ".join(description_lines)
                projects.append(current_project)

            current_project = {
                "name": line,
                "description": ""
            }
            description_lines = []

        elif line.startswith("•"):
            description_lines.append(line.replace("•", "").strip())

    if current_project:
        current_project["description"] = " ".join(description_lines)
        projects.append(current_project)

    return projects
    

# -------------------------
# Extract experience
# -------------------------
def extract_experience(text):
    experience = []

    match = re.search(
        r'Experience\n(.*?)\nEducation',
        text,
        re.DOTALL
    )

    if not match:
        return experience

    exp_section = match.group(1)
    lines = exp_section.split("\n")

    current_exp = None
    description_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if "Intern" in line or "Engineer" in line:
            if current_exp:
                current_exp["description"] = " ".join(description_lines)
                experience.append(current_exp)

            current_exp = {
                "role": line,
                "description": ""
            }
            description_lines = []

        elif line.startswith("•"):
            description_lines.append(line.replace("•", "").strip())

    if current_exp:
        current_exp["description"] = " ".join(description_lines)
        experience.append(current_exp)

    return experience


# -------------------------
# Master parse function
# -------------------------
def parse_resume(text):
    return {
        "skills": extract_skills(text),
        "projects": extract_projects(text),
        "experience": extract_experience(text)
    }