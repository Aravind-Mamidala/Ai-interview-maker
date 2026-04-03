import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.fluency_analyzer import calculate_wpm, estimate_pauses, fluency_score

import nltk
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

model = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------------------
# KEEP YOUR FULL FILLER WORDS ✅
# -------------------------------
FILLER_WORDS = [
"um","uh","like","basically","actually","you know","i mean","sort of","kind of",
"well","so","okay","right","hmm","ah","uhh","umm","huh",
"you see","to be honest","honestly","literally","maybe","probably",
"i guess","i think","i feel","in a way","somehow","more or less",
"at the end of the day","stuff like that","things like that",
"something like","and yeah","and so","you know what i mean",
"if that makes sense","kind of like","sorta","just","really",
"pretty much","basically speaking","generally speaking",
"technically speaking","to some extent","in some sense",
"believe me","trust me","well basically","you could say",
"the thing is","the point is","what i mean is","the idea is",
"like i said","like i mentioned","as i said","as i mentioned",
"let me think","let me see","hold on","wait","hmm yeah",
"you know basically","i would say","i would think"
]

TECHNICAL_TERMS = [
"algorithm","data structure","time complexity","space complexity",
"optimization","recursion","iteration","dynamic programming","multithreading","multiprocessing","thread","process",
"gil","cpu","cpu-bound","io","io-bound",
"parallelism","concurrency","memory","shared memory",
"core","multi-core","synchronization","react","virtual dom","diffing","reconciliation",
"scaling","load balancing","distributed system",
"database","caching","api","server","latency",
"iterator","generator","yield","memory efficient"
]

# -------------------------------
# STEM FUNCTIONS
# -------------------------------
def stem_text(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return [stemmer.stem(w) for w in words]

STEMMED_TECH_TERMS = set()
for term in TECHNICAL_TERMS:
    for w in term.split():
        STEMMED_TECH_TERMS.add(stemmer.stem(w))

# -------------------------------
# EMOTION
# -------------------------------
def detect_emotion(confidence, fluency, pauses, filler_count, word_count):

    if confidence >= 8 and fluency >= 8:
        return "Confident 😄"

    if pauses > 4 or filler_count > 5:
        return "Nervous 😟"

    if word_count < 15:
        return "Uncertain 🤔"

    if fluency < 5:
        return "Hesitant 😐"

    return "Neutral 🙂"


# =====================================
# MAIN FUNCTION
# =====================================
def evaluate_answer(answer, reference_answer, start_time, end_time):
    if start_time is None or end_time is None:
        duration = 1
    else:
        duration = end_time - start_time

    if duration <= 0:
        duration = 1

    score = 0
    feedback = []
    answer_lower = answer.lower()
    word_count = len(answer.split())

    # -------------------------------
    # FLUENCY
    # -------------------------------
    wpm = calculate_wpm(answer, start_time, end_time)
    pauses = estimate_pauses(answer, duration)
    fluency = fluency_score(wpm, pauses)

    # -------------------------------
    # LENGTH
    # -------------------------------
    length_score = min(10, int(word_count / 8))
    score += length_score

    if word_count < 10:
        feedback.append("Answer is too short.")

    # -------------------------------
    # FILLERS
    # -------------------------------
    filler_count = sum(
        len(re.findall(rf'\b{re.escape(word)}\b', answer_lower))
        for word in FILLER_WORDS
    )
    filler_score = max(0, 10 - filler_count * 2)
    score += filler_score

    if filler_count > 3:
        feedback.append("Too many filler words.")

    # -------------------------------
    # STRUCTURE (RELAXED)
    # -------------------------------
    sentences = [s for s in re.split(r'[.!?]', answer) if s.strip()]

    if len(sentences) >= 2:
        structure_score = 10
    elif len(sentences) == 1 and word_count > 12:
        structure_score = 6
    else:
        structure_score = 3
        feedback.append("Answer lacks structure.")

    score += structure_score

    # -------------------------------
    # EXPLANATION
    # -------------------------------
    avg_len = word_count / max(1, len(sentences))
    explanation_score = 5

    if avg_len > 8:
        explanation_score += 2

    if any(w in answer_lower for w in ["because", "therefore", "so", "as a result"]):
        explanation_score += 3

    score += explanation_score

    # -------------------------------
    # TECH DEPTH
    # -------------------------------
    tech_hits = sum(1 for term in TECHNICAL_TERMS if term in answer_lower)
    tech_score = min(15, tech_hits * 2)
    score += tech_score

    # -------------------------------
    # SEMANTIC
    # -------------------------------
    similarity = 0
    try:
        embeddings = model.encode([answer, reference_answer])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        semantic_score = int(similarity * 35)
        score += semantic_score
    except:
        semantic_score = 0

    if tech_hits < 2 and semantic_score < 20:
        feedback.append("Technical depth appears weak.")

    if semantic_score < 15:
        feedback.append("Answer does not align well with expected explanation.")

    # -------------------------------
    # SPECIAL CASE: IDK
    # -------------------------------
    if answer_lower.strip() in ["i dont know", "i don't know", "no idea"]:
        score = min(score, 10)
        feedback.append("Answer shows lack of knowledge.")

    # -------------------------------
    # VOCAB
    # -------------------------------
    unique_words = len(set(answer_lower.split()))
    score += int((unique_words / max(1, word_count)) * 10)

    # -------------------------------
    # CONFIDENCE
    # -------------------------------
    confidence = 10
    if pauses > 3: confidence -= 2
    if filler_count > 3: confidence -= 2
    if word_count < 15: confidence -= 2
    confidence = max(3, confidence)

    emotion = detect_emotion(confidence, fluency, pauses, filler_count, word_count)

    # -------------------------------
    # FINAL ADD
    # -------------------------------
    score += fluency * 2
    score += confidence * 2

    # -------------------------------
    # LOW QUALITY
    # -------------------------------
    if word_count < 10 and similarity < 0.4:
        score = min(score, 30)
        feedback.append("Answer is irrelevant or lacks depth.")

    # -------------------------------
    # REPETITION DETECTION
    # -------------------------------
    sentences = [s.strip() for s in re.split(r'[.!?]', answer) if s.strip()]
    if len(sentences) >= 3 and len(set(sentences)) == 1:
        score = min(score, 20)
        feedback.append("Answer is repetitive and lacks meaningful content.")

    # -------------------------------
    # SPAM
    # -------------------------------
    words = answer_lower.split()
    unique_ratio = len(set(words)) / max(1, len(words))

    if unique_ratio < 0.4:
        score -= 10
        feedback.append("Answer contains repetition/spam.")

# -------------------------------
# GIBBERISH DETECTION (SMART FIX)
# -------------------------------
    words = re.findall(r'\b[a-zA-Z]+\b', answer_lower)

    if len(words) > 5:   # only check if meaningful length
        valid_words = sum(1 for w in words if len(w) > 2)
        valid_ratio = valid_words / len(words)

    # ALSO check semantic
    valid_ratio = 1   # default safe value

    if valid_ratio < 0.5 and similarity < 0.3:
        score = min(score, 20)
        feedback.append("Answer appears to be meaningless or gibberish.")
    # -------------------------------
    # EMOTION FIX
    # -------------------------------
    if "lack of knowledge" in " ".join(feedback).lower():
        emotion = "Uncertain 🤔"

    if "repetitive" in " ".join(feedback).lower():
        emotion = "Uncertain 🤔"

    # -------------------------------
    # FINAL SCORE
    # -------------------------------
    final_score = min(100, score)

    return {
        "total_score": final_score,
        "semantic_score": semantic_score,
        "technical_score": tech_score,
        "structure_score": structure_score,
        "vocab_score": int((unique_words / max(1, word_count)) * 10),
        "fluency_score": fluency,
        "confidence_score": confidence,
        "wpm": wpm,
        "pauses": pauses,
        "emotion": emotion,
        "feedback": feedback
    }