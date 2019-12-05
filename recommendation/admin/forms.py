from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, TextAreaField, FieldList, FormField
from wtforms.widgets.html5 import NumberInput
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from recommendation.models import User 


class Question(FlaskForm):
    question = TextAreaField("Question", validators=[DataRequired()])
    answer = StringField("answer", validators = [DataRequired()])
    options = FieldList(FormField(Option), min_entries = 2 )
    submit = SubmitField("submit")
    
class Option(FlaskForm):
    name = StringField("Option", validators = [DataRequired()])

