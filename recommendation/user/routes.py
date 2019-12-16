from flask import Blueprint, redirect, render_template, url_for, flash, request, jsonify, abort
from flask_login import login_user, current_user,logout_user,login_required
from recommendation.models import User, Arm, Subjectrating, Subject, UserInfo
from recommendation import bcrypt, db
from .forms import RegistrationForm, LoginForm, UpdateForm, SubjectForm
from .questions import questions
import os
from pickle import load
import numpy as np
from recommendation.utils import mapping, correctForm
from pathlib import Path
import asyncio

root = Path(__file__).parent

users = Blueprint('users', __name__)

async def setup_recommender():
    try:
        learner = load(open("recommendation/original.pkl", 'rb'))
        return learner
    except RuntimeError as e:
        print(e)

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_recommender())]
learner = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

        

@users.route('/', methods = ['GET','POST'])
@users.route('/login', methods = ['GET','POST'])
def login():
    
    form = LoginForm()
    if current_user.is_authenticated:
        flash(f'You are already logged in ','info')
        return redirect(url_for('users.account'))
    
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)  
            try:
                if current_user.userinfo.re_course != '':
                    return redirect(url_for('users.account'))
            except Exception:
                return redirect(url_for('users.update'))
        else:
            flash(f'Login Unsuccessful, Please check your email and password ','danger')
    return render_template("login.html", title = 'Login', form=form)


@users.route("/users/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in ','info')
        return redirect(url_for('users.account'))
    
    form = RegistrationForm()
    arm = Arm.query.filter_by(name="Science").first()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data,
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
    if arm_sub == None:
        abort(404)
    else:
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
        entries = list(request.form.items())
        subjects = entries[2:len(entries)-2]
        arm = Arm.query.filter_by(name = request.form["arms"]).first()
        user_info = UserInfo()
        user_info.arm = arm
        user_info.age = request.form["age"]
        user_info.career = request.form["career"]
        user_info.iq = 0
        user_info.re_course = ''
        for subject in subjects:
            sub = Subject.query.filter_by(name = subject[0]).first()        
            sub_rating = Subjectrating(subject_id = sub.id, rating = subject[1])
            db.session.add(sub_rating)
            user_info.subjects.append(sub_rating)
        current_user.userinfo = user_info
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('users.question'))
    return render_template('test.html', title = 'Update',  user = current_user)


@users.route("/logout", methods = ["GET"])
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/users/account', methods = ['GET','POST'])
@login_required
def account():
    user = User.query.filter_by(username = current_user.username).first()
    flash(f'Welcome back','success')
    return render_template("account.html", title="Account", user = current_user)


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
        iq = float("{0:.2f}".format((100*count)/current_user.userinfo.age))
        current_user.userinfo.iq = iq
        db.session.commit()
        return redirect(url_for('users.result',score = count))
    return render_template('question.html', title = 'Question', proposed = questions)

@users.route("/question/result/<score>")
def result(score):
    user = User.query.filter_by(username = current_user.username).first()
    model_data = correctForm(user)
    prediction = learner.predict(model_data)
    recom_course = mapping(prediction[0])
    user.userinfo.re_course = recom_course
    db.session.commit()
    return render_template("result.html", score = score)

