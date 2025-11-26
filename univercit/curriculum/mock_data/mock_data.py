# in the cmd use the script 'python manage.py shell' and paste all the script below
from curriculum.models import Program, Course

# === COURSES ===
courses_data = {
    "CS101": ("Introduction to Computer Science",
              "An introductory course that explores the fundamentals of computer science, covering how computers work, basic programming concepts, algorithms, problem solving, and the role of computing in modern society. Students gain foundational skills that prepare them for advanced subjects."),
    "CS102": ("Object-Oriented Programming",
              "This course introduces structured programming using classes, objects, inheritance, and encapsulation. Students will design modular programs and learn how object-oriented design solves software complexity."),
    "CS201": ("Data Structures and Algorithms",
              "Covers core data structures such as arrays, linked lists, stacks, queues, trees, and hash tables. Students learn sorting, searching, complexity analysis, and algorithmic problem solving."),
    "CS301": ("Computer Architecture",
              "A study of how computers are physically organized and how processors execute instructions. Topics include CPU pipelines, memory hierarchy, instruction sets, and low-level programming concepts."),
    "CS401": ("Operating Systems",
              "Explores how modern operating systems manage processes, memory, storage, and hardware scheduling. Includes multiprocessing, synchronization, file systems, and OS design principles."),
    "CS402": ("Software Engineering",
              "Introduces software development methodologies including Agile, SDLC, testing, documentation, and project planning. Students learn how real-world software teams build scalable systems."),
    "CS403": ("Database Systems",
              "Covers fundamentals of relational databases, SQL, schema design, normalization, transactions, indexing, and database management. Includes implementation of real projects."),
    "CS404": ("Computer Networks",
              "Introduces networking architectures, protocols, and communication models. Covers TCP/IP, routing, switching, network layers, security, and distributed systems."),
    "CS405": ("Artificial Intelligence",
              "Presents foundational concepts in AI such as search algorithms, heuristics, machine learning, neural networks, pattern recognition, and real-world AI applications."),
    "CS406": ("Human–Computer Interaction",
              "Focuses on designing systems for usability and accessibility. Covers interaction models, UX research, UI prototyping, visual design principles, and user testing."),
    "MATH201": ("Discrete Mathematics",
              "A course covering mathematical foundations used in computing: logic, sets, combinatorics, graph theory, number systems, proofs, and discrete structures."),
    "MATH302": ("Calculus II",
              "Continuation of Calculus I including integration techniques, series, multivariable calculus, vector functions, and real-world mathematical modeling."),
    "MATH101": ("College Algebra",
              "Covers functions, linear systems, polynomial expressions, inequalities, and algebraic manipulations used in engineering and computer science."),
    "MATH301": ("Advanced Calculus",
              "Higher-level concepts in real analysis, differentiation, continuity, integration theory, and advanced problem solving."),
    "IT101": ("Introduction to Information Technology",
              "Overview of computer systems, IT infrastructures, software, network fundamentals, digital literacy, and the role of IT professionals in modern organizations."),
    "IT201": ("Systems Analysis and Design",
              "Covers requirements gathering, system modeling, UML, prototyping, project lifecycle planning, and approaches to designing enterprise systems."),
    "IT301": ("Web Technologies",
              "Students learn front-end and server-side web development using modern frameworks, APIs, client/server models, and responsive design concepts."),
    "IT302": ("Network Administration",
              "Introduces enterprise network setup, server management, routing, switching, security, and troubleshooting in a professional IT environment."),
    "IT303": ("Cloud Computing",
              "Explores cloud models (IaaS, PaaS, SaaS), virtualization, distributed computing, storage, containerization, and scalable services."),
    "BUS101": ("Introduction to Business Management",
              "Provides an overview of business operations, strategic planning, HR, economics, entrepreneurship, and corporate ethics."),
    "BUS201": ("Project Management",
              "Covers planning, scheduling, stakeholder management, risk analysis, Agile/Scrum frameworks, and professional project execution.")
}

# Create courses
for course_id, (name, desc) in courses_data.items():
    Course.objects.get_or_create(
        course_id=course_id,
        defaults={"course_name": name, "course_desc": desc}
    )


# === PROGRAMS ===
program_data = {
    "BSCS": (
        "Bachelor of Science in Computer Science",
        "A program focused on computational theory, software development, algorithms, and advanced computing concepts. Students learn programming, system design, artificial intelligence, networking, and research preparation for careers in technology, academia, and software engineering."
    ),
    "BSIT": (
        "Bachelor of Science in Information Technology",
        "A practical and industry-oriented program centered on IT infrastructure, system administration, cybersecurity, networking, and software deployment. Students are trained to maintain, support, and innovate digital business solutions."
    ),
    "BSMATH": (
        "Bachelor of Science in Mathematics",
        "A theoretical and application-based mathematics program covering calculus, algebra, statistics, optimization, and computational mathematics. Graduates are prepared for research, analytics, finance, and scientific computing."
    ),
    "BSIS": (
        "Bachelor of Science in Information Systems",
        "A business-focused technology program specializing in organizational information systems, enterprise architecture, data management, and process optimization. Graduates bridge business strategy with technology implementation."
    ),
    "BSECE": (
        "Bachelor of Science in Electronics Engineering",
        "A core engineering curriculum covering electronics, telecommunications, circuit design, digital systems, embedded computing, and signal processing. Prepares graduates for engineering practice, design, and industrial innovation."
    ),
}

program_objects = {}
for code, (name, desc) in program_data.items():
    program, created = Program.objects.get_or_create(
        program_code=code,
        defaults={"program_name": name, "program_desc": desc}
    )
    program_objects[code] = program


# === COURSE ASSIGNMENTS ===
program_courses = {
    "BSCS": ["CS101","CS102","CS201","CS301","CS401","CS402","CS404","CS405","CS406","MATH201","MATH302"],
    "BSIT": ["IT101","IT201","IT301","IT302","IT303","CS101","CS403"],
    "BSMATH": ["MATH101","MATH201","MATH301","MATH302","CS201"],
    "BSIS": ["IT201","IT302","CS403","CS402","BUS101","BUS201"],
    "BSECE": ["MATH101","MATH301","CS405","CS401","CS301"]
}

for program_code, course_list in program_courses.items():
    program = program_objects[program_code]
    program.courses.set([Course.objects.get(course_id=c) for c in course_list])
