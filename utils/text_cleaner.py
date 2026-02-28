import re

def clean_resume_text(text):
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])([&+])', r'\1 \2', text)
    text = re.sub(r'([&+])([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace("–", " - ")
    text = text.replace("—", " - ")
    return text.strip()