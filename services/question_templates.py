# ----------------------------
# Skill-based Questions
# ----------------------------

SKILL_QUESTIONS = {

    "Python": [
        {
            "question": "Explain the Global Interpreter Lock (GIL).",
            "reference": "The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time. It simplifies memory management but limits CPU-bound parallelism."
        },
        {
            "question": "Explain multithreading vs multiprocessing in Python.",
            "reference": "Multithreading shares memory but is limited by the GIL in CPython, making it better for I/O-bound tasks. Multiprocessing creates separate processes enabling true parallelism for CPU-bound tasks."
        }
    ],

    "React.js": [
        {
            "question": "Explain the useEffect hook in React.",
            "reference": "useEffect handles side effects in functional components. It runs after render and depends on a dependency array. It can also return a cleanup function."
        }
    ],

    "Node.js": [
        {
            "question": "What is middleware in Express.js?",
            "reference": "Middleware are functions that execute during the request-response cycle in Express. They have access to req, res, and next, and are used for logging, authentication, validation, and more."
        }
    ],

    "RESTful APIs": [
        {
            "question": "What are REST principles?",
            "reference": "REST principles include client-server architecture, statelessness, cacheability, uniform interface, layered system, and resource-based communication using HTTP methods."
        },
        {
            "question": "Difference between PUT and PATCH?",
            "reference": "PUT replaces the entire resource and is idempotent, while PATCH partially updates specific fields of a resource."
        }
    ]
}


# ----------------------------
# Project-based Templates
# ----------------------------

PROJECT_TEMPLATES = [
    {
        "question_template": "Explain the architecture you used in {project_name}.",
        "reference_template": "The architecture of {project_name} should follow a layered client-server model with REST APIs, proper database schema design, authentication, modular structure, and scalability considerations."
    },
    {
        "question_template": "How would you scale {project_name} to 1 million users?",
        "reference_template": "Scaling {project_name} should involve horizontal scaling, load balancing, database indexing, caching like Redis, CDN usage, monitoring, and optimized API performance."
    },
    {
        "question_template": "What improvements would you make to {project_name} today?",
        "reference_template": "Improvements to {project_name} could include performance optimization, caching, improved database indexing, better security measures, scalability enhancements, and enhanced user experience."
    }
]


# ----------------------------
# Experience-based Templates
# ----------------------------

EXPERIENCE_TEMPLATES = [
    {
        "question_template": "What was your biggest technical challenge as {role}?",
        "reference_template": "A strong answer should describe a real technical challenge, debugging process, solution approach, and measurable impact achieved in the role of {role}."
    }
]


# ----------------------------
# Behavioral Questions
# ----------------------------

BEHAVIORAL_TEMPLATES = [
    {
        "question": "How do you debug complex issues?",
        "reference": "A systematic debugging approach includes reproducing the issue, analyzing logs, isolating components, using debugging tools, profiling performance, and preventing future issues."
    }
]