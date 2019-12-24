from flask import Blueprint, redirect, render_template, url_for, flash, request, jsonify
from flask_login import login_user, current_user,logout_user,login_required
from recommendation.models import User
from recommendation.models import  Question, Option
from recommendation import bcrypt, db
from recommendation.user.forms import LoginForm
from recommendation.admin.forms import OptionForm
# from .forms import Question
import os

admin = Blueprint('admin', __name__)

@admin.route("/admin/login", methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.email).first()
        if user.Username == "admin@gmail.com":
            login_user(user)
        else:
            flash(f'Login Unsuccessful, Please check your email and password ','danger')
    return render_template('login.html', title ="Login", form= form)

@admin.route("/admin/logout")
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

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
    # users = User.query.paginate(page, per_page = 5)
    users = User.query.all()
    userlist = []
    for user in users:
        userObj = {}
        userObj["username"] = user.username
        userObj["arm"] = user.userinfo.arm.name if user.userinfo != None else ""
        userObj["IQ"] = user.userinfo.iq if user.userinfo != None else ""
        userObj["career"] = user.userinfo.career if user.userinfo != None else ""
        userObj["re_course"] = user.userinfo.re_course if user.userinfo != None else ""
        userlist.append(userObj)
        
    return jsonify({"users":userlist})