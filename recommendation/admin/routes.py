from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import login_user, current_user,logout_user,login_required
from recommendation.models import User
from recommendation import bcrypt, db
import os

admin = Blueprint('admin', __name__)


# @admin.route("/login", methods = ["GET","POST"])
# def login():
#     if request.method == "POST":
#         if request.form["username"] == "admin@gmail" and request.form["password"] == "password":
#             login(admin)
    
    
     