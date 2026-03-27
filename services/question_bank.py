QUESTION_BANK = {

    "Software Engineering": {

        # -------------------------------
        # GENERAL QUESTIONS
        # -------------------------------
        "General": [
            {
                "question": "What are REST principles?",
                "reference_answer": "REST is an architectural style that uses stateless communication between client and server. It relies on resources identified by URIs and standard HTTP methods like GET, POST, PUT, and DELETE. It emphasizes scalability, cacheability, and a uniform interface."
            },
            {
                "question": "Difference between PUT and PATCH?",
                "reference_answer": "PUT replaces the entire resource while PATCH updates only specific fields of a resource."
            },
            {
                "question": "How do you debug complex issues?",
                "reference_answer": "Debugging involves reproducing the issue, checking logs, isolating components, and testing fixes."
            },
            {
                "question": "What is middleware in Express.js?",
                "reference_answer": "Middleware functions process requests before reaching the final route handler."
            },
            {
                "question": "Explain the Global Interpreter Lock (GIL).",
                "reference_answer": "GIL ensures only one thread executes Python bytecode at a time."
            },
            {
                "question": "Explain multithreading vs multiprocessing in Python.",
                "reference_answer": "Multithreading shares memory but is limited by GIL, multiprocessing uses separate processes."
            },
            {
                "question": "What is caching and why is it important?",
                "reference_answer": "Caching stores frequently used data to improve performance."
            },
            {
                "question": "What are microservices?",
                "reference_answer": "Microservices are small independent services communicating via APIs."
            },
            {
                "question": "What is horizontal vs vertical scaling?",
                "reference_answer": "Horizontal adds machines, vertical increases resources."
            },
            {
                "question": "What is a load balancer?",
                "reference_answer": "Distributes traffic across servers."
            }
        ],

        # -------------------------------
        # SKILL QUESTIONS
        # -------------------------------
        "Skills": {
            "Python": [
                {
                    "question": "Explain decorators in Python.",
                    "reference_answer": "Decorators modify functions without changing their code."
                },
                {
                    "question": "What are generators in Python?",
                    "reference_answer": "Generators yield values lazily using 'yield'."
                }
            ],

            "React.js": [
                {
                    "question": "Explain the useEffect hook in React.",
                    "reference_answer": "useEffect handles side effects and runs after render."
                },
                {
                    "question": "What is the virtual DOM?",
                    "reference_answer": "Virtual DOM is a lightweight representation of the real DOM."
                }
            ],

            "Node.js": [
                {
                    "question": "What is event-driven architecture in Node.js?",
                    "reference_answer": "Node uses asynchronous event-driven architecture."
                },
                {
                    "question": "What is the event loop?",
                    "reference_answer": "Handles async operations without blocking."
                }
            ]
        },

        # -------------------------------
        # PROJECT QUESTIONS
        # -------------------------------
        "Project": [
            {
                "question_template": "Explain the architecture you used in {project}.",
                "reference_template": "Explain architecture, components, and data flow."
            },
            {
                "question_template": "What improvements would you make to {project} today?",
                "reference_template": "Discuss scalability, performance, UX improvements."
            },
            {
                "question_template": "What was the most challenging problem while building {project}?",
                "reference_template": "Explain challenge and solution."
            },
            {
                "question_template": "How would you scale {project} to 1 million users?",
                "reference_template": "Discuss load balancing, caching, DB scaling."
            }
        ],

        # -------------------------------
        # EXPERIENCE QUESTIONS
        # -------------------------------
        "Experience": [
            {
                "question_template": "What was your biggest technical challenge as {role}?",
                "reference_template": "Explain real-world problem and solution."
            },
            {
                "question_template": "What did you learn during your role as {role}?",
                "reference_template": "Explain skills and tools learned."
            },
            {
                "question_template": "How did you collaborate with your team during {role}?",
                "reference_template": "Explain teamwork and communication."
            }
        ]
    }
}