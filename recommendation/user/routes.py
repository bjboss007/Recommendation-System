from flask import Blueprint, redirect, render_template, url_for, flash, request, jsonify, abort
from flask_login import login_user, current_user,logout_user,login_required
from recommendation.models import User, Arm, Subjectrating, Subject, UserInfo
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
            # flash(f'Login successful ','success')
            # flash(f'Please edit your profile to complete the registration', 'info')
            return redirect(next_page) if next_page else redirect(url_for('users.update'))
        else:
            flash(f'Login Unsuccessful, Please check your email and password ','danger')
    return render_template("login.html", title = 'Login', form=form)


@users.route("/users/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in ','info')
        return redirect(url_for('main.account'))
    
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
            
        for subject in subjects:
            print(subject)
            
            sub = Subject.query.filter_by(name = subject[0]).first()
            print(sub.id)
            
            sub_rating = Subjectrating(subject_id = sub.id, rating = subject[1])
            db.session.add(sub_rating)
            user_info.subjects.append(sub_rating)
        print(user_info.subjects)

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
        iq = (100*count)/current_user.userinfo.age
        current_user.userinfo.iq = iq
        db.session.commit()
        
        print("*"*90)
        print(current_user.userinfo.iq)
       
        print("This is the incoming data : {}".format(count))
        flash(f'Account Updated successfully','success')
        return redirect(url_for('users.result',score = count))
    return render_template('question.html', title = 'Question', proposed = questions)

@users.route("/question/result/<score>")
def result(score):
    return render_template("result.html", score = score)

# @users.route("/test")
def parseData():
    user = User.query.filter_by(username = "mob").first()
    subjects = user.userinfo.subjects
    userObj = {}
    userObj["age"] = user.userinfo.age
    userObj["IQ"] = float("{0:.2f}".format(user.userinfo.iq))
    userObj["arm"] = user.userinfo.arm.name
    subjectArr = {}
    for subject in subjects:
        subject_name = Subject.query.get(subject.subject_id)
        subjectArr[subject_name.name] = subject.rating
    userObj["subjects"] =  subjectArr
    data = jsonify(userObj)
    return data
    

dataform = []
science_padding = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
@users.route("/test")
def correctForm():
    data = parseData().get_json()
    print("*"*90)
 
    if data["arm"] == "Science":
        for sub in data["subjects"]:
            dataform = [data["age"],float(data["subjects"]["Mathematics"]),float(data["subjects"]["Biology"]),float(data["subjects"]["Physics"]),float(data["subjects"]["Chemistry"])]+science_padding
    elif data["arm"] == "Art":
        for sub in data["subjects"]:
            dataform = [data["age"],data["IQ"],float(data["subjects"]["Mathematics"]),0.0,0.0,0.0,0.0,0.0,0.0,float(data["subjects"]["Government"]),float(data["subjects"]["English"]),float(data['subjects']["History"]),float(data['subjects']["CRK"])]
    elif data["arm"] == "Commercial":
        for sub in data["subjects"]:
            dataform = [data["age"],data["IQ"],float(data['subjects']["Mathematics"]),0.0,0.0,0.0,float(data['subjects']["Accounting"]),float(data['subjects']["Commerce"]),float(data['subjects']["Economics"])]     
    return data
  
    