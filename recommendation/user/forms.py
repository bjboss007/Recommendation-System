
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, SelectField, FormField, FieldList
from wtforms.widgets.html5 import NumberInput
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from recommendation.models import User, Arm, Subject

    
class RegistrationForm(FlaskForm):
    username = StringField('username', validators = [DataRequired(), Length(min = 2, max = 20)] )
    email = StringField('email', validators= [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    confirm_password = PasswordField('confirm_password', validators = [DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("Username taken ! Please choose another")
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("Email Already taken. Please choose another one")
    
    def validate_password(self, password):
        p_email = self.email.data.split('@')[0]
        if password.data.lower() == p_email.lower():
            raise ValidationError("You cannot use your email as your passwork, consider choosing another one")


    
class LoginForm(FlaskForm):
    email = StringField('email', validators= [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
    
class SubjectForm(FlaskForm):
    name = StringField('name',validators = [DataRequired()])
    rating = IntegerField('rating', widget = NumberInput(min = 0, max = 5))
    
    
class UpdateForm(FlaskForm):
    username = StringField('username',validators = [DataRequired()])
    email = StringField('email',validators = [DataRequired(), Email()])
    age = IntegerField('age', validators = [DataRequired()], widget=NumberInput())
    arms = SelectField('Arms')
    subjects = FieldList(FormField(SubjectForm))
    submit = SubmitField('Update')
    