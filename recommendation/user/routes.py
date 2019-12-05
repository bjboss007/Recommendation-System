from flask import Blueprint, redirect, render_template, url_for, flash, request, jsonify
from flask_login import login_user, current_user,logout_user,login_required
from recommendation.models import User, Role, Arm, Subjectrating, Subject
from recommendation import bcrypt, db
from .forms import RegistrationForm, LoginForm, UpdateForm, SubjectForm
from .questions import questions
import os



users = Blueprint('users', __name__)

@users.route('/', methods = ['GET','POST'])
@users.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in ','info')
        return redirect(url_for('users.account'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful ','success')
            flash(f'Please edit your profile to complete the registration', 'info')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash(f'Login Unsuccessful, Please check your email and password ','danger')
    return render_template("login.html", title = 'Login', form=form)


@users.route("/users/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in ','info')
        return redirect(url_for('main.account'))
    
    form = RegistrationForm()
    role = Role.query.filter_by(name = "User").first()
    arm = Arm.query.filter_by(name="Science").first()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data,
            role = role,
            age = 19,
            arm = arm
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Your account has been created! You are now able to loggin','success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title = 'Register', form = form)
    
@users.route("/register/<arm>")
def subjects(arm):
    subjectArr = []
    arm_sub = Arm.query.filter_by(name = arm).first()
    for subject in arm_sub.arm_subjects:
        subjectObj = {}
        subjectObj["id"] = subject.id
        subjectObj["name"] = subject.name
        subjectArr.append(subjectObj)
    return jsonify({"subjects" : subjectArr})
    

@users.route('/users/update', methods = ['GET','POST'])
@login_required
def update():
    
    if request.method == "POST":
        
        print(request.form["age"])
        print(dict(request.form.items()))
        for entity in request.form.items():
            print(entity, end = "\n")
        return redirect(url_for('users.question'))
    return render_template('test.html', title = 'Update',  user = current_user)


@users.route("/logout", methods = ["GET"])
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/users/account', methods = ['GET','POST'])
@login_required
def account():
    form =  UpdateForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            filename = os.path.join('http://localhost:5000/static/images',picture_file)
            current_user.image_file = filename
    
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash(f'Account Updated successfully','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username 
    return render_template("account.html", title="Account", form = form, user = current_user)


@users.route('/reset_request', methods = ['GET','POST'])
def reset_request():
    return render_template('login.html', title = 'Login', form = form)


@users.route("/question", methods = ['GET','POST'])
def question():
    proposed = questions
    incoming = {}
 
    if request.method == "POST":
        count = 0
        for i,j in request.form.lists():
            incoming[i] = j[0]
        for question in proposed:
            for i in incoming.keys():
                if question["id"] == int(i):
                    if incoming[i] == question["answer"]:
                        count+=1            
        # return redirect(url_for('users.account'))
        print("*"*90)
        print("This is the incoming data : {}".format(count))
        
    return render_template('question.html', title = 'Question', proposed = questions)

