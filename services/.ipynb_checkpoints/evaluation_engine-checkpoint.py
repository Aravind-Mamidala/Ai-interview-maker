import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model ONCE
model = SentenceTransformer('all-MiniLM-L6-v2')

FILLER_WORDS = ["um", "uh", "like", "basically", "actually", "you know"]

TECHNICAL_TERMS = [

# Core Programming
"algorithm","data structure","complexity","optimization",
"memory","thread","process","concurrency","parallelism",
"multithreading","multiprocessing","mutex","lock",

# Backend
"api","rest","endpoint","request","response","http",
"middleware","authentication","authorization",
"jwt","token","session","stateless",

# Databases
"database","sql","nosql","mongodb","mysql","postgresql",
"query","index","indexing","schema","replication",
"sharding","transaction","consistency",

# Scalability
"scalability","horizontal scaling","vertical scaling",
"load balancer","cluster","distributed system",
"high availability","fault tolerance",

# Performance
"caching","redis","memcached","latency","throughput",
"performance","optimization","pagination",

# DevOps
"docker","container","kubernetes","deployment",
"ci","cd","pipeline","monitoring","logging",

# Architecture
"microservices","monolith","event driven",
"message queue","pubsub","service architecture",

# Frontend
"react","virtual dom","component","hook","useeffect",
"state management","render","frontend",

# Networking
"dns","tcp","udp","protocol","cdn","gateway"

]

def evaluate_answer(answer, reference_answer):

    score = 0
    feedback = []

    answer_lower = answer.lower()
    reference_lower = reference_answer.lower()

    # ---------------------------------
    # 1️⃣ Length Score (10)
    # ---------------------------------
    word_count = len(answer.split())
    length_score = min(10, int(word_count / 8))
    score += length_score

    if word_count < 20:
        feedback.append("Answer is too short.")

    # ---------------------------------
    # 2️⃣ Filler Word Penalty (10)
    # ---------------------------------
    filler_count = sum(answer_lower.count(word) for word in FILLER_WORDS)
    filler_score = max(0, 10 - filler_count * 2)
    score += filler_score

    if filler_count > 3:
        feedback.append("Too many filler words.")

    # ---------------------------------
    # 3️⃣ Structure Score (10)
    # ---------------------------------
    sentences = re.split(r'[.!?]', answer)
    sentences = [s for s in sentences if s.strip() != ""]
    
    if len(sentences) >= 3:
        structure_score = 10
    elif len(sentences) == 2:
        structure_score = 6
    else:
        structure_score = 3
        feedback.append("Answer lacks structure.")
    
    score += structure_score

    # ---------------------------------
    # 4️⃣ Technical Term Coverage (20)
    # ---------------------------------
    tech_hits = sum(1 for term in TECHNICAL_TERMS if term in answer_lower)
    tech_score = min(20, tech_hits * 3)
    score += tech_score

    if tech_hits < 2:
        feedback.append("Technical depth appears weak.")

    # ---------------------------------
    # 5️⃣ Semantic Similarity (40)
    # ---------------------------------
    try:
        embeddings = model.encode([answer, reference_answer])
        similarity = cosine_similarity(
            [embeddings[0]], [embeddings[1]]
        )[0][0]

        semantic_score = int(similarity * 40)
    except:
        semantic_score = 0

    score += semantic_score

    if semantic_score < 15:
        feedback.append("Answer does not align well with expected explanation.")

    # ---------------------------------
    # 6️⃣ Vocabulary Diversity (10)
    # ---------------------------------
    unique_words = len(set(answer_lower.split()))
    diversity_ratio = unique_words / max(1, word_count)

    vocab_score = int(diversity_ratio * 10)
    score += vocab_score

    # Final cap
    final_score = min(100, score)

    return {
        "total_score": final_score,
        "semantic_score": semantic_score,
        "technical_score": tech_score,
        "structure_score": structure_score,
        "vocab_score": vocab_score,
        "feedback": feedback
    }