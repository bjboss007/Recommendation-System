from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import login_user, current_user,logout_user,login_required
from recommendation.models import User, Question
from recommendation import bcrypt, db
from recommendation.user.forms import LoginForm
from .forms import Question
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

@admin.route("/admin/add-questions")
def addQuestion():
    question = Question.query.first()
    if len(question.options) == 0:
        flash("empty Phone provided")
    
    form = Question()
    if form.validate_on_submit():
        form.populate_obj(question)
        db.session.commit()
        flash("Question Successfully save")
    
    return render_template('admin/question.html', title = "Add-question", form = form)