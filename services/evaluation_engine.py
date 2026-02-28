import re
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


FILLER_WORDS = ["um", "uh", "like", "basically", "actually", "you know"]

TECH_TERMS = [
    "api", "database", "authentication", "authorization",
    "frontend", "backend", "server", "client",
    "scalable", "performance", "optimization",
    "schema", "react", "node", "mongodb",
    "python", "javascript", "thread", "async",
    "security", "deployment", "cache"
]


def evaluate_answer(answer, reference_answer):

    original_answer = answer
    answer = answer.lower()
    reference_answer = reference_answer.lower()

    total_score = 0
    feedback = []

    # ==================================================
    # 1️⃣ Length Score (15)
    # ==================================================
    words = answer.split()
    word_count = len(words)

    length_score = min(15, int(word_count / 6))
    if word_count < 20:
        feedback.append("Answer is too short and lacks depth.")

    total_score += length_score


    # ==================================================
    # 2️⃣ Structure Score (10)
    # ==================================================
    sentences = re.split(r'[.!?]', answer)
    sentences = [s for s in sentences if s.strip() != ""]

    if len(sentences) < 2:
        structure_score = 5
        feedback.append("Answer lacks proper structure.")
    else:
        structure_score = 10

    total_score += structure_score


    # ==================================================
    # 3️⃣ Filler Word Penalty (10)
    # ==================================================
    filler_count = sum(answer.count(word) for word in FILLER_WORDS)
    filler_score = max(0, 10 - filler_count * 2)

    if filler_count > 2:
        feedback.append("Too many filler words used.")

    total_score += filler_score


    # ==================================================
    # 4️⃣ Vocabulary Richness (10)
    # ==================================================
    unique_words = len(set(words))
    if word_count > 0:
        richness_ratio = unique_words / word_count
    else:
        richness_ratio = 0

    vocab_score = int(richness_ratio * 10)
    total_score += vocab_score

    if richness_ratio < 0.4:
        feedback.append("Vocabulary usage is repetitive.")


    # ==================================================
    # 5️⃣ Technical Density (15)
    # ==================================================
    tech_hits = sum(1 for term in TECH_TERMS if term in answer)
    tech_score = min(15, tech_hits * 2)

    total_score += tech_score

    if tech_hits == 0:
        feedback.append("Technical depth appears weak.")


    # ==================================================
    # 6️⃣ Semantic Similarity (30)
    # ==================================================
    try:
        vectorizer = TfidfVectorizer(stop_words='english')

        tfidf_matrix = vectorizer.fit_transform(
            [answer, reference_answer]
        )

        similarity = cosine_similarity(
            tfidf_matrix[0:1], tfidf_matrix[1:2]
        )[0][0]

        semantic_score = int(similarity * 30)

    except:
        semantic_score = 0

    total_score += semantic_score

    if semantic_score < 8:
        feedback.append("Answer does not align well with expected explanation.")


    # ==================================================
    # 7️⃣ Nonsense Detection
    # ==================================================
    if semantic_score < 5 and tech_hits < 2:
        total_score -= 10
        feedback.append("Response appears irrelevant or lacks correctness.")


    # ==================================================
    # Final Clamp
    # ==================================================
    total_score = max(0, min(100, total_score))


    return {
        "total_score": total_score,
        "length_score": length_score,
        "structure_score": structure_score,
        "filler_score": filler_score,
        "vocab_score": vocab_score,
        "tech_score": tech_score,
        "semantic_score": semantic_score,
        "feedback": feedback
    }