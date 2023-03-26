from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.teacher import Teacher

db = "teacher_coop"

class Plan:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.subject = data['subject']
        self.grade_level = data['grade_level']
        self.topic = data['topic']
        self.materials = data['materials']
        self.description = data['description']
        self.teacher_id = data['teacher_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.teacher = []
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO plans (title, subject, grade_level, topic, materials, description, teacher_id) VALUES (%(title)s,%(subject)s,%(grade_level)s,%(topic)s,%(materials)s,%(description)s,%(teacher_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM plans;"
        results =  connectToMySQL(db).query_db(query)
        all_plans = []
        for row in results:
            all_plans.append( cls(row) )
        return all_plans
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM plans WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def get_all_by_subject(cls,data):
        query = "SELECT * FROM plans WHERE subject = %(subject)s;"
        results = connectToMySQL(db).query_db(query,data)
        subject_plans = {data["subject"]:[]}
        for row in results:
            subject_plans[data["subject"]].append( cls(row) )
        return subject_plans
    
    @classmethod
    def get_all_by_grade(cls,data):
        query = "SELECT * FROM plans WHERE grade_level = %(grade_level)s;"
        results = connectToMySQL(db).query_db(query,data)
        grade_plans = {data["grade_level"]:[]}
        for row in results:
            grade_plans[data["grade_level"]].append(cls(row))
        return grade_plans
    
    @classmethod
    def get_all_by_subject_and_grade(cls,data):
        query = "SELECT * FROM plans WHERE subject = %(subject)s AND grade_level = %(grade_level)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def get_one_with_teacher(cls, data):
        query = '''
            SELECT * 
            FROM plans P
            LEFT JOIN teachers T ON T.id = P.teacher_id
            WHERE P.id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        plan_obj = cls(results[0])
        for row in results:
            teacher_info = {
                "id" : row["T.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "grade" : row["grade"],
                "subject" : row["subject"],
                "created_at" : row["T.created_at"],
                "updated_at" : row["T.updated_at"]
            }
            plan_obj.teacher = Teacher(teacher_info)
        return plan_obj
    
    @classmethod
    def update(cls, data):
        query = "UPDATE plans SET title=%(title)s, subject=%(subject)s, grade_level=%(grade_level)s, topic=%(topic)s, materials=%(materials)s, description=%(description)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM plans WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_plan(plan):
        is_valid = True
        if len(plan['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters","plan")
        if len(plan['subject']) < 3:
            is_valid = False
            flash("Subject must be at least 3 characters","plan")
        if len(plan['grade_level']) < 1:
            is_valid = False
            flash("Please select a grade level","plan")
        if len(plan['topic']) < 3:
            is_valid = False
            flash("Topic must be at least 3 characters","plan")
        if len(plan['materials']) < 3:
            is_valid = False
            flash("Materials must be at least 3 characters","plan")
        if len(plan['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","plan")
        return is_valid