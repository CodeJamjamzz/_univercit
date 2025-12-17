"""
    SCRIPT FOR ADDING MOCK DATA TO SERVER
    1. run 'py manage.py shell'
    2. copy and paste code below to shell and execute
"""

from datetime import datetime

from curriculum.models import Program, Course
from discussion.models import Forum, Thread, Comment


cs_course = Course.objects.get(course_id="CS101")
# initialization of data first to be used in the discussions for cs101
forums_to_create = [
    Forum(
        forum_title="Welcome to CS101",
        forum_desc="Feel free to introduce yourselves and find other like-minded individuals here!",
        course_id=cs_course
    ),
    Forum(
        forum_title="Introduction to C",
        forum_desc="Basics of C, setting up your IDE (VS Code/CodeBlocks), and Hello World.",
        course_id=cs_course
    ),
    Forum(
        forum_title="Variables",
        forum_desc="Discussing int, float, char, constants, and basic format specifiers.",
        course_id=cs_course
    ),
    Forum(
        forum_title="Functions",
        forum_desc="Understanding modular coding, parameters, return types, and prototypes.",
        course_id=cs_course
    ),
    Forum(
        forum_title="Arrays",
        forum_desc="Working with 1D and 2D arrays, and iterating through data sets.",
        course_id=cs_course
    ),
    Forum(
        forum_title="Loops",
        forum_desc="Help with for loops, while loops, do-while loops, and if-else logic.",
        course_id=cs_course
    ),
    Forum(
        forum_title="Pointers",
        forum_desc="Memory addresses, dereferencing, pointer arithmetic, and void pointers.",
        course_id=cs_course
    ),
    Forum(
        forum_title="Recursion",
        forum_desc="Functions calling themselves, stack overflow issues, and base cases.",
        course_id=cs_course
    ),
]

Forum.objects.bulk_create(forums_to_create)