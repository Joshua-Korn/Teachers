from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.teacher import Teacher
from flask_app.models.plan import Plan
from flask import flash

db = "teacher_coop"

class Comment:
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.plan_id = data["plan_id"]
        self.teacher_id = data["teacher_id"]
        self.plan_teacher_id = data["plan_teacher_id"]
        self.plan = None
        self.teacher = None

    @classmethod
    def leave_comment(cls, data):
        query = '''
            INSERT INTO comments (content, plan_id, teacher_id, plan_teacher_id)
            VALUES (%(content)s, %(plan_id)s, %(teacher_id)s, %(plan_teacher_id)s);
        '''
        connectToMySQL(db).query_db(query, data)
    
    @classmethod
<<<<<<< HEAD
    def get_comment(cls,data):
        query = "SELECT * FROM comments where id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

=======
    def get_comment(cls, data):
        query = "SELECT * FROM comments where id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
        
    
>>>>>>> 3c3549ff48f01f98fe10df4b6699a28397135d8c
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def get_all_by_plan_with_plan_teacher(cls, data):
        query = '''
            SELECT *
            FROM comments C
            RIGHT OUTER JOIN plans P on C.plan_id = P.id
            LEFT JOIN teachers T ON C.teacher_id = T.id
            WHERE P.id = %(id)s
            ORDER BY C.created_at;
        '''
        results = connectToMySQL(db).query_db(query, data)
        comments = []
        for row in results:
            comment_obj = cls(row)
            plan_info = {
                "id" : row["P.id"],
                "title" : row["title"],
                "subject" : row["subject"],
                "grade_level" : row["grade_level"],
                "topic" : row["topic"],
                "materials" : row["materials"],
                "description" : row["description"],
                "created_at" : row["P.created_at"],
                "updated_at" : row["P.updated_at"],
                "teacher_id" : row["teacher_id"],
                "plan_teacher_id" : row["plan_teacher_id"]
            }
            comment_obj.plan = Plan(plan_info)
            teacher_info = {
                "id" : row["T.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "subject" : row["subject"],
                "grade" : row["grade"],
                "password" : row["password"],
                "created_at" : row["T.created_at"],
                "updated_at" : row["T.updated_at"]
            }
            comment_obj.sender = Teacher(teacher_info)
            comments.append(comment_obj)
        return comments
