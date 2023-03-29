from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.plan import Plan
from flask_app.models.teacher import Teacher
from flask_app.models.comment import Comment

@app.route('/new/plan')
def new_plan():
    if 'teacher_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['teacher_id']
    }
    return render_template('new_plan.html',teacher=Teacher.get_by_id(data))

@app.route('/add/plan',methods=['post'])
def create_plan():
    if 'teacher_id' not in session:
        return redirect('/logout')
    if not Plan.validate_plan(request.form):
        return redirect('/new/plan')
    data = {
        "title": request.form["title"],
        "subject": request.form["subject"],
        "grade_level": request.form["grade_level"],
        "topic": request.form["topic"],
        "materials": request.form["materials"],
        "description": request.form["description"],
        "teacher_id": session["teacher_id"]
    }
    Plan.save(data)
    return redirect('/dashboard')

@app.route('/edit/plan/<int:id>')
def edit_plan(id):
    if 'teacher_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    teacher_data = {
        "id":session['teacher_id']
    }
    return render_template("edit.html",edit=Plan.get_one(data),teacher=Teacher.get_by_id(teacher_data))

@app.route('/update/plan',methods=['post'])
def update_plan():
    if 'teacher_id' not in session:
        return redirect('/logout')
    if not Plan.validate_plan(request.form):
        return redirect('/new/plan')
    data = {
        "title": request.form["title"],
        "subject": request.form["subject"],
        "grade_level": request.form["grade_level"],
        "topic": request.form["topic"],
        "materials": request.form["materials"],
        "description": request.form["description"],
        "id": request.form["id"]
    }
    Plan.update(data)
    return redirect(f'/plan/{request.form["id"]}')

@app.route('/plan/<int:id>')
def plan_details(id):
    if 'teacher_id' not in session:
        return redirect('/logout')
    plan_info = Plan.get_one_with_teacher({"id": id}) 
    comment_list = Comment.get_all_by_plan_with_plan_teacher({"id": id})
    print(f"comment_obj = {comment_list}")
    teacher_data = {
        "id":session['teacher_id']
    }
    return render_template("plan_details.html",plan=plan_info,comments=comment_list,teacher=Teacher.get_by_id(teacher_data))

@app.route('/delete/plan/<int:id>')
def delete_plan(id):
    if 'teacher_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Plan.delete(data)
    return redirect('/dashboard')

@app.route('/plans/<string:subject>')
def subject_plans(subject):
    if 'teacher_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['teacher_id']
    }
    return render_template("subject_plans.html",teacher=Teacher.get_by_id(data),plans=Plan.get_all_by_subject({'subject':subject}),subject=subject)

@app.route('/grades/<string:grade_level>')
def grade(grade_level):
    if 'teacher_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['teacher_id']
    }
    return render_template("grade_plans.html",teacher=Teacher.get_by_id(data),plans=Plan.get_all_by_grade({'grade_level':grade_level}),grade_level=grade_level)
