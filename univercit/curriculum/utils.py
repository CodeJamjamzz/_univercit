from django.db import connection, DatabaseError
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
    

def get_course(course_id):
    with connection.cursor() as cursor:
        cursor.callproc("get_course", [course_id])
        return dictfetchall(cursor)[0]
    

def create_course(course_id, name, desc, programs):
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                    "create_course",
                    [course_id, name, desc, programs]
                )
            
        return {"success": True}

    except DatabaseError as e:
        error_code = e.args[0]
        error_message = e.args[1]

        return {
            "success": False,
            "error": error_message
        }
    

def update_course(course_id, name, desc, programs):
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                    "update_course",
                    [course_id, name, desc, programs]
                )
            
            return {"success": True}
    
    except DatabaseError as e:
        error_code = e.args[0]
        error_message = e.args[1]

        return {
            "success": False,
            "error": error_message
        }
    

def delete_course(course_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc("delete_course", [course_id])
        
        return {"success": True}    
    
    except DatabaseError as e:
        error_code = e.args[0]
        error_message = e.args[1]

        return {
            "success": False,
            "error": error_message
        }
        
    
def create_program(code, name, desc, courses):
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                    "create_program",
                    [code, name, desc, courses]
                )
            
        return {"success": True}

    except DatabaseError as e:
        error_code = e.args[0]
        error_message = e.args[1]

        return {
            "success": False,
            "error": error_message
        }
    

def update_program(code, name, desc, courses):
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                    "update_program",
                    [code, name, desc, courses]
                )
            
        return {"success": True}

    except DatabaseError as e:
        error_code = e.args[0]
        error_message = e.args[1]

        return {
            "success": False,
            "error": error_message
        }
    

def delete_program(program_code):
    try:
        with connection.cursor() as cursor:
            cursor.callproc("delete_program", [program_code])
        
        return {"success": True}    
    
    except DatabaseError as e:
        error_code = e.args[0]
        error_message = e.args[1]

        return {
            "success": False,
            "error": error_message
        }