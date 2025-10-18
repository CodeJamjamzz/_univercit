"""
    SCRIPT FOR ADDING MOCK DATA TO SERVER
    1. run 'py mangage.py shell'
    2. copy and paste code below to shell and execute
"""

from datetime import datetime

from curriculum.models import Program, Course
from discussion.models import Forum, Thread

course_id = Course.objects.create(
    course_id="CSIT321",
    course_desc="Applications Development"
)
program_id = Program.objects.create(
    program_code="BSCS",
    program_desc="Bachelor of Science in Computer Science",
    courses=course_id
)

postman_id = Forum.objects.create(
    forumTitle="Postman",
    forumDesc="Mock HTTP requests",
    courseId=course_id
)
Thread.objects.create(
    threadTitle="How to mock POST requests",
    forumId=postman_id,
    dateCreated=datetime.now(),
    studentId=None
)