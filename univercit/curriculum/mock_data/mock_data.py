# in the cmd use the script 'python manage.py shell' and paste all the script below

from curriculum.models import Program, Course

# --- Create Courses ---

course_data = {
    "CS101": "Introduction to Computer Science",
    "CS102": "Programming Fundamentals",
    "CS201": "Data Structures & Algorithms",
    "CS301": "Operating Systems",
    "CS401": "Artificial Intelligence",
    "CS402": "Machine Learning",
    "CS403": "Database Systems",
    "CS404": "Software Engineering",
    "CS405": "Networks & Communications",
    "CS406": "Computer Security",

    "IT101": "Intro to IT",
    "IT201": "Computer Hardware",
    "IT301": "Web Development I",
    "IT302": "Web Development II",
    "IT303": "Cloud Computing",

    "MATH101": "College Algebra",
    "MATH201": "Discrete Math",
    "MATH301": "Calculus I",
    "MATH302": "Calculus II",

    "BUS101": "Introduction to Business",
    "BUS201": "Business Organization",
}

for c_id, c_desc in course_data.items():
    Course.objects.get_or_create(
        course_id=c_id,
        defaults={
            "course_name": c_id,
            "course_desc": c_desc
        }
    )

print("=== Courses Created ===")


# --- Create Programs ---

program_data = {
    "BSCS": {
        "name": "Bachelor of Science in Computer Science",
        "courses": [
            "CS101", "CS102", "CS201", "CS301", "CS401", "CS402",
            "CS404", "CS405", "CS406", "MATH201", "MATH302",
        ]
    },
    "BSIT": {
        "name": "Bachelor of Science in Information Technology",
        "courses": [
            "IT101", "IT201", "IT301", "IT302", "IT303",
            "CS101", "CS403",
        ]
    },
    "BSMATH": {
        "name": "Bachelor of Science in Mathematics",
        "courses": [
            "MATH101", "MATH201", "MATH301", "MATH302", "CS201",
        ]
    },
    "BSIS": {
        "name": "Bachelor of Science in Information Systems",
        "courses": [
            "IT201", "IT302", "CS403", "CS402", "BUS101", "BUS201",
        ]
    },
    "BSECE": {
        "name": "Bachelor of Science in Electronics Engineering",
        "courses": [
            "MATH101", "MATH301", "CS405", "CS401", "CS301",
        ]
    },
}

for code, data in program_data.items():
    program, created = Program.objects.get_or_create(
        program_code=code,
        defaults={
            "program_name": data["name"],
            "program_desc": f"{data['name']} program"
        }
    )
    # Assign courses
    program.courses.set(Course.objects.filter(course_id__in=data["courses"]))
    program.save()

print("=== Programs Created & Courses Linked ===")
