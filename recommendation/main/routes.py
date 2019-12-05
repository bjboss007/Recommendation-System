from flask import Blueprint, url_for, request, render_template
from recommendation.user.forms import LoginForm
from recommendation.models import User
from flask_login import current_user



main = Blueprint('main', __name__)


# @main.route('/home', methods=['GET', 'POST'])
# def ():



@main.route('/about')
def about():
    return render_template('about.html', title = "About Page")

@main.route('/home')
def home():
    return render_template('login.html', title = "About Page")
