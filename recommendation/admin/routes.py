from flask import Blueprint, redirect, render_template, url_for, flash, request, jsonify
from flask_login import login_user, current_user,logout_user,login_required
# from recommendation.models import User
from recommendation.models import  Question, Option, Arm, User
from recommendation import db
from recommendation.user.forms import LoginForm
from recommendation.admin.forms import OptionForm
# from .forms import Question
import os

admin = Blueprint('admin', __name__)

# @admin.route("/admin/login", methods = ["GET","POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email = form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password,form.password.data):
#             if user.email == "admin@gmail.com":
#                 login_user(user, remember = form.remember.data)
#                 return redirect(url_for('admin.usersListView'))
#             else:
#                 flash(f'Login Unsuccessful, Please check your email and password ','danger')
#     return render_template('login.html', title ="Login", form= form)

@admin.route("/admin/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@admin.route("/admin/add-questions", methods= ['GET','POST'])
def addQuestion():
    if request.method == "POST":
        entries = list(request.form.items())
        options = []
        question = Question()
        question.name = request.form["question"]
        question.answer = request.form["answer"]
        for i in entries:
            if i[0].startswith("option"):
                options.append(i[1])
        for option in options:
            if option != "":
                optionn = Option(name = option)
                db.session.add(optionn)
                question.options.append(optionn)
        db.session.add(question)
        db.session.commit()
        flash(f'Question successful added','success')
    return render_template('admin/question.html', title = "Add-question")

@admin.route("/admin/list-users")
def usersList():
    page = request.args.get('page', 1, type = int)
    users = [ user  for user in User.query.all() if user.email != 'admin@gmail.com']
    userlist = []
    for user in users:
        userObj = {}
        userObj["username"] = user.username
        userObj["arm"] = user.userinfo.arm.name if user.userinfo != None else ""
        userObj["IQ"] = user.userinfo.iq if user.userinfo != None else ""
        userObj["career"] = user.userinfo.career if user.userinfo != None else ""
        userObj["re_course"] = user.userinfo.re_course if user.userinfo != None else ""
        userlist.append(userObj)
    return jsonify({"data":userlist})

@admin.route("/admin/list-arms")
def armsList():
    page = request.args.get('draw')
    length = request.args.get('length')
    arms = Arm.query.all()
    # if int(length) == -1:
    #     arms = Arm.query.all()
    # else:
    #     arms = Arm.query.paginate(page = 1, per_page = int(length)).items
    armsList = []
    for arm in arms:
        armObj = {}
        armObj["id"] = arm.id
        armObj["name"] = arm.name
        armsList.append(armObj)
    return jsonify({'data' :armsList})


@admin.route("/admin/users-list")
def usersListView():
    return render_template("admin/users-list.html", title = "Users - List")


@admin.route("/admin/add-arm", methods = ['GET','POST'])
def addArm():
    if request.method == "POST":
        enteries = [x for x in list(request.form.items())]
        for arm in entries:
            arm_obj = Arm.query.filter_by(name = arm)
            if arm_obj:
                continue
            else:
                arm_obj = Arm(name= arm)
            db.session.add(arm_obj)
        db.session.commit()
    return render_template("admin/arm-list.html", title = "Arms")


@admin.route("/admin/<id>/add-subjects")
def addSubjects(id):
    arm = Arm.query.get_or_404(id)
    if request.method == "POST":
        subjects = []
        entries = [x[1] for x in list(request.form.items())]
        if arm:
            subjects = arm.arm_subjects
            for subject in subjects:
                if (subject in entries):
                    continue
                else:
                    subj = Subject(name = x)
                    arm.arm_subjects.append(x)
        db.session.commit()
    
    return render_template("admin/add-subjects.html", title = "Add-subjects", arm = arm)


