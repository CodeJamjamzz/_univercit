"""
    SCRIPT FOR ADDING MOCK DATA TO SERVER
    1. run 'py manage.py shell'
    2. copy and paste code below to shell and execute
"""

from datetime import datetime

from curriculum.models import Program, Course
from discussion.models import Forum, Thread, Comment

from univercit.discussion.models import Comment

course_id = Course.objects.create(
    course_id="CSIT321",
    course_desc="Applications Development"
)
program_id = Program.objects.create(
    program_id=1,
    program_code="BSCS",
    program_desc="Bachelor of Science in Computer Science",
    courses=course_id
)

forum_id = Forum.objects.create(
    forumId=1,
    forumTitle="Postman",
    forumDesc="Mock HTTP requests",
    courseId=course_id
)

thread_id = Thread.objects.create(
    threadTitle="How to mock POST requests",
    forumId=forum_id,
    dateCreated=datetime.now(),
    studentId=None
)

comment1_id = Comment.objects.create(
    commentId=1,
    content="What the title says. I'm having a hard time understanding postman",
    threadId=thread_id
)