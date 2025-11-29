from django.db import connection
from univercit.utils import dictfetchall

# Util functions

def get_courses(query=''):
    with connection.cursor() as cursor:
        cursor.callproc("get_courses", [query])
        return dictfetchall(cursor)


def get_programs(query=''):
    with connection.cursor() as cursor:
        cursor.callproc("get_programs", [query])
        return dictfetchall(cursor)
    

def get_courses_programs(course_id):
    with connection.cursor() as cursor:
        cursor.callproc("get_courses_programs", [course_id])
        return dictfetchall(cursor)