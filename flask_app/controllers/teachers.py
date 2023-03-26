from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.teacher import Teacher
from flask_app.models.plan import Plan 

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['post'])
def register():

    if not Teacher.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "grade": request.form['grade'],
        "subject": request.form['subject'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Teacher.save(data)
    session['teacher.id'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['post'])
def login():
    teacher = Teacher.get_by_email(request.form)

    if not teacher:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(teacher.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['teacher_id'] = teacher.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'teacher_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['teacher_id']
    }
    return render_template("dashboard.html",teacher=Teacher.get_by_id(data), plans=Plan.get_all())



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')