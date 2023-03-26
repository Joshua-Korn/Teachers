from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

db = "teacher_coop"

class Teacher:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.grade = data['grade']
        self.subject = data['subject']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO teachers (first_name,last_name,email,password,grade,subject) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s, %(grade)s, %(subject)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM teachers;"
        results = connectToMySQL(db).query_db(query)
        teachers = []
        for row in results:
            teachers.append( cls(row))
        return teachers
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM teachers WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM teachers WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_by_grade(cls,data):
        query = "SELECT * FROM teachers WHERE grade = %(grade)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_by_subject(cls,data):
        query = "SELECT * FROM teachers WHERE subject = %(subject)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])
    
    @staticmethod
    def validate_register(teacher):
        is_valid = True
        query = "SELECT * FROM teachers WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,teacher)
        if len(results) > 0:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(teacher['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(teacher['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(teacher['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(teacher['grade']) < 3:
            flash("Please enter a grade","register")
            is_valid= False
        if len(teacher['subject']) < 3:
            flash("Please choose a subject","register")
            is_valid= False
        if len(teacher['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if teacher['password'] != teacher['confirm']:
            flash("Passwords don't match","register")
        return is_valid
    