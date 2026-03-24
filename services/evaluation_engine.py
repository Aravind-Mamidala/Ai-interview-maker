import random
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---- STEMMING SUPPORT ----
import nltk
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
# --------------------------

# -------------------------------------
# Generic Software Engineering Questions
# -------------------------------------

GENERAL_QUESTIONS = [

    {
        "question": "What are REST principles?",
        "reference_answer": "REST is an architectural style that uses stateless communication between client and server. It relies on resources identified by URIs and standard HTTP methods like GET, POST, PUT, and DELETE. It emphasizes scalability, cacheability, and a uniform interface."
    },

    {
        "question": "Difference between PUT and PATCH?",
        "reference_answer": "PUT replaces the entire resource while PATCH updates only specific fields of a resource. PUT is idempotent and usually requires the full object, whereas PATCH modifies partial data."
    },

    {
        "question": "How do you debug complex issues?",
        "reference_answer": "Debugging complex issues involves reproducing the problem, analyzing logs and stack traces, isolating the failing component, testing hypotheses, and using debugging tools or breakpoints. After identifying the root cause, the fix is implemented and verified through testing."
    },

    {
        "question": "What is middleware in Express.js?",
        "reference_answer": "Middleware in Express.js is a function that runs during the request-response cycle. It has access to the request object, response object, and the next function. Middleware is used for tasks such as logging, authentication, validation, and error handling."
    },

    {
        "question": "Explain the Global Interpreter Lock (GIL).",
        "reference_answer": "The Global Interpreter Lock is a mutex used in CPython that ensures only one thread executes Python bytecode at a time. It simplifies memory management but limits parallel execution of CPU-bound threads."
    },

    {
        "question": "Explain multithreading vs multiprocessing in Python.",
        "reference_answer": "Multithreading runs multiple threads within the same process sharing memory, but in CPython it is limited by the GIL. Multiprocessing uses multiple processes with separate memory spaces and allows true parallel execution on multiple CPU cores."
    },

    {
        "question": "What is caching and why is it important?",
        "reference_answer": "Caching stores frequently accessed data in fast memory to reduce database queries and improve application performance. Systems often use tools like Redis or in-memory caches."
    },

    {
        "question": "What are microservices?",
        "reference_answer": "Microservices is an architectural style where applications are built as small independent services communicating through APIs. Each service handles a specific business capability and can be deployed independently."
    },

    {
        "question": "What is horizontal vs vertical scaling?",
        "reference_answer": "Horizontal scaling adds more machines or servers to distribute load, while vertical scaling increases resources such as CPU or RAM on a single machine."
    },

    {
        "question": "What is a load balancer?",
        "reference_answer": "A load balancer distributes incoming network traffic across multiple servers to ensure high availability, reliability, and efficient resource usage."
    }

]

# -------------------------------------
# Skill Based Question Templates
# -------------------------------------

SKILL_QUESTIONS = {

    "Python": [
        (
            "Explain decorators in Python.",
            "Decorators are functions that modify the behavior of another function without changing its code. They wrap a function and add additional functionality such as logging or authentication."
        ),
        (
            "What are generators in Python?",
            "Generators are functions that return an iterator using yield. They allow lazy evaluation and generate values one at a time instead of storing them all in memory."
        )
    ],

    "React.js": [
        (
            "Explain the useEffect hook in React.",
            "useEffect is used to handle side effects in React functional components such as API calls or subscriptions. It runs after rendering and can be controlled using dependency arrays."
        ),
        (
            "What is the virtual DOM?",
            "The virtual DOM is a lightweight JavaScript representation of the real DOM. React updates the virtual DOM first and then efficiently updates the real DOM using a diffing algorithm."
        )
    ],

    "Node.js": [
        (
            "What is event-driven architecture in Node.js?",
            "Node.js uses an event-driven architecture where operations run asynchronously and callbacks or events handle responses without blocking the main thread."
        ),
        (
            "What is the event loop?",
            "The event loop is the mechanism that allows Node.js to perform non-blocking operations by delegating tasks to the system and processing callbacks when they are completed."
        )
    ]

}

# -------------------------------------
# Project Based Questions
# -------------------------------------

PROJECT_QUESTIONS = [

    (
        "Explain the architecture you used in {project}.",
        "A good answer should explain the system architecture, technologies used, data flow, and how components interact."
    ),

    (
        "What improvements would you make to {project} today?",
        "A good answer should discuss scalability, performance optimization, better architecture, caching, or improved user experience."
    ),

    (
        "What was the most challenging problem while building {project}?",
        "A good answer should explain a technical challenge, debugging approach, and the final solution."
    ),

    (
        "How would you scale {project} to 1 million users?",
        "A good answer should discuss load balancing, caching, database scaling, CDN usage, and cloud deployment."
    )

]

# -------------------------------------
# Experience Based Questions
# -------------------------------------

EXPERIENCE_QUESTIONS = [

    (
        "What was your biggest technical challenge as {role}?",
        "A good answer should describe a real problem faced during work, the debugging process, and how it was solved."
    ),

    (
        "What did you learn during your role as {role}?",
        "A good answer should explain technical skills learned, tools used, and lessons gained from real-world development."
    ),

    (
        "How did you collaborate with your team during {role}?",
        "A good answer should explain teamwork, version control usage, communication, and problem solving in a team environment."
    )

]

# -------------------------------------
# Main Question Generator
# -------------------------------------

def generate_questions(resume_data, role):

    questions = []

    skills = resume_data.get("skills", [])
    projects = resume_data.get("projects", [])
    experience = resume_data.get("experience", [])

    # Add general questions
    questions.extend(GENERAL_QUESTIONS)

    # Add skill based questions
    for skill in skills:
        if skill in SKILL_QUESTIONS:
            for q, a in SKILL_QUESTIONS[skill]:
                questions.append({
                    "question": q,
                    "reference_answer": a
                })

    # Add project questions
    for proj in projects:
        project_name = proj["name"]

        for q, a in PROJECT_QUESTIONS:
            questions.append({
                "question": q.replace("{project}", project_name),
                "reference_answer": a
            })

    # Add experience questions
    for exp in experience:
        role_name = exp["role"]

        for q, a in EXPERIENCE_QUESTIONS:
            questions.append({
                "question": q.replace("{role}", role_name),
                "reference_answer": a
            })

    random.shuffle(questions)

    return questions[:5]

# -------------------------------------
# Evaluation Engine
# -------------------------------------

model = SentenceTransformer('all-MiniLM-L6-v2')

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

# Programming
"algorithm","data structure","time complexity","space complexity",
"optimization","recursion","iteration","dynamic programming",
"greedy algorithm","backtracking","divide and conquer",
"hashing","hash table","binary search","two pointer",
"sliding window","bit manipulation","graph","tree","binary tree",
"binary search tree","heap","priority queue","stack","queue",
"linked list","trie","segment tree","disjoint set","union find",

# Concurrency
"thread","process","concurrency","parallelism",
"multithreading","multiprocessing","mutex","lock","deadlock",
"race condition","synchronization","semaphore","atomic operation",

# Backend
"api","rest","restful","endpoint","request","response","http",
"https","middleware","authentication","authorization",
"jwt","token","session","stateless","stateful","cookie",
"rate limiting","throttling","web server","application server",

# Databases
"database","sql","nosql","mongodb","mysql","postgresql",
"redis","cassandra","dynamodb","query","index","indexing",
"schema","replication","sharding","transaction",
"acid","consistency","isolation","durability",
"normalization","denormalization","foreign key",
"primary key","database optimization",

# Scalability
"scalability","horizontal scaling","vertical scaling",
"load balancer","cluster","distributed system",
"high availability","fault tolerance","auto scaling",
"replication","distributed computing",

# Performance
"caching","redis","memcached","latency","throughput",
"performance","optimization","profiling","benchmarking",
"pagination","lazy loading","compression","cdn",

# DevOps
"docker","container","containerization","kubernetes",
"deployment","ci","cd","pipeline","continuous integration",
"continuous deployment","monitoring","logging",
"prometheus","grafana","terraform","ansible",

# Architecture
"microservices","monolith","event driven architecture",
"message queue","pubsub","service architecture",
"service mesh","api gateway","service discovery",
"event streaming","domain driven design",

# Message Brokers
"kafka","rabbitmq","activemq","message broker",
"event streaming","stream processing",

# Frontend
"react","angular","vue","virtual dom","component",
"hook","useeffect","usestate","state management",
"redux","context api","render","frontend",
"responsive design","single page application",

# Networking
"dns","tcp","udp","protocol","cdn","gateway",
"http protocol","websocket","socket","load balancing",
"reverse proxy","nginx","apache server",

# Security
"encryption","hashing","ssl","tls","oauth",
"authentication","authorization","csrf","xss",
"input validation","secure communication",

# Cloud
"aws","azure","gcp","cloud computing","serverless",
"lambda","ec2","s3","cloud storage",
"distributed storage","edge computing",

# Machine Learning
"machine learning","deep learning","neural network",
"training data","model training","feature engineering",
"supervised learning","unsupervised learning",
"classification","regression","clustering",
"decision tree","random forest","svm","kmeans",
"gradient descent","loss function","overfitting",
"underfitting","cross validation",

# Software Engineering
"software architecture","design pattern",
"mvc","solid principles","clean architecture",
"unit testing","integration testing","test coverage",
"version control","git","github","pull request",
"code review","debugging","logging system"
]

# ---- STEM HELPER FUNCTION ----

def stem_text(text):

    words = re.findall(r'\b\w+\b', text.lower())

    stems = []

    for w in words:
        stems.append(stemmer.stem(w))

    return stems


# ---- PREPROCESS TECH TERMS ----

STEMMED_TECH_TERMS = set()

for term in TECHNICAL_TERMS:

    words = term.lower().split()

    for w in words:
        STEMMED_TECH_TERMS.add(stemmer.stem(w))

def evaluate_answer(answer, reference_answer):

    score = 0
    feedback = []

    answer_lower = answer.lower()

    word_count = len(answer.split())
    length_score = min(10, int(word_count / 8))
    score += length_score

    if word_count < 20:
        feedback.append("Answer is too short.")

    filler_count = sum(answer_lower.count(word) for word in FILLER_WORDS)
    filler_score = max(0, 10 - filler_count * 2)
    score += filler_score

    if filler_count > 3:
        feedback.append("Too many filler words.")

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

    tech_hits = sum(1 for term in TECHNICAL_TERMS if term in answer_lower)

# ---- STEM BASED DETECTION ----
    answer_stems = stem_text(answer)

    for stem_word in answer_stems:
        if stem_word in STEMMED_TECH_TERMS:
            tech_hits += 1
# ------------------------------

    tech_score = min(20, tech_hits * 3)
    score += tech_score

    if tech_hits < 2:
        feedback.append("Technical depth appears weak.")

    try:
        embeddings = model.encode([answer, reference_answer])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        semantic_score = int(similarity * 40)
    except:
        semantic_score = 0

    score += semantic_score

    if semantic_score < 15:
        feedback.append("Answer does not align well with expected explanation.")

    unique_words = len(set(answer_lower.split()))
    diversity_ratio = unique_words / max(1, word_count)

    vocab_score = int(diversity_ratio * 10)
    score += vocab_score

    final_score = min(100, score)

    return {
        "total_score": final_score,
        "semantic_score": semantic_score,
        "technical_score": tech_score,
        "structure_score": structure_score,
        "vocab_score": vocab_score,
        "feedback": feedback
    }