from flask_app import app
from flask import session, redirect, request
from flask_app.models.comment import Comment
from flask_app.models.plan import Plan

@app.route("/leave_comment/<int:plan_id>", methods=["post"])
def add_comment(plan_id):
    if "teacher_id" in session:
        plan = Plan.get_one({"id":plan_id})
        comment_info = {
            "content": request.form["comment"],
            "plan_id": plan_id,
            "teacher_id": session["teacher_id"],
            "plan_teacher_id": plan.teacher_id
        }
        Comment.leave_comment(comment_info)
        return redirect(f'/plan/{plan_id}')
    return redirect("/")

@app.route('/delete/comment/<int:id>')
def delete_comment(id):
    if 'teacher_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Comment.delete(data)
    return redirect('/dashboard')