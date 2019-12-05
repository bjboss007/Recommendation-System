from flask import current_app, request
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
from recommendation import db, login_manager, bcrypt
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))



user_subjects = db.Table('user_subjects',
    db.Column('subject_rating_id', db.Integer, db.ForeignKey('subject_rating.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), unique = True, nullable = False)
   email = db.Column(db.String(120), unique = True, nullable = False)
   password = db.Column(db.String(120), unique = True, nullable = False)
   image_file = db.Column(db.String(32))
   age = db.Column(db.Integer, nullable = False)
   role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
   arm_id = db.Column(db.Integer, db.ForeignKey('arms.id'))
   subjects = db.relationship('Subjectrating', secondary=user_subjects, lazy='subquery', backref=db.backref('users', lazy=True))
 
   
   def get_reset_token(self, expires_sec = 1800):
      s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
      return s.dumps({'user_id':self.id}).decode('utf-8')
   
   @staticmethod
   def verify_token(token):
      s = Serializer(current_app.config['SECRET_KEY'])
      try:
         user_id = s.loads(token)['user_id']
      except:
         return None
      return User.query.get(user_id)
   
   def __init__(self, **kwargs):
      if kwargs["email"] is not None : # and kwargs["image_file"] is None:
         self.image_file = hashlib.md5(kwargs["email"].encode('utf-8')).hexdigest()
      self.username = kwargs["username"]
      self.email = kwargs["email"]
      self.age = kwargs["age"]
      self.role = kwargs["role"]
      self.arm = kwargs["arm"]
      self.password = bcrypt.generate_password_hash(kwargs["password"]).decode('utf-8') 
      self.image_file = self.gravatar(self)
      
   
   def change_email(self):
      self.email = new_email
      self.image_file = hashlib.md5(
         self.email.encode('utf-8')).hexdigest()
      db.session.add(self)
      return True

   @staticmethod
   def gravatar(self, size=100, default='identicon', rating='g'):
      if request.is_secure:
         url = 'https://secure.gravatar.com/avatar'
      else:
         url = 'http://www.gravatar.com/avatar'
      hash = self.image_file or hashlib.md5(
         self.email.encode('utf-8')).hexdigest()
      
      return f'{url}/{hash}?s={size}&d={default}&r={rating}'
    
   def __repr__(self):
      return f"user('{self.username}','{self.email}','{self.image_file}')"

class Role(db.Model):
   __tablename__ = 'roles'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(64), unique=True)
   users = db.relationship('User', backref = 'role', lazy = 'dynamic')
   
   
   def __repr__(self):
      return f"Role '({self.name})'" 
   
arm_subjects = db.Table('arm_subjects',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True),
    db.Column('arm_id', db.Integer, db.ForeignKey('arms.id'), primary_key=True)
)

class Arm(db.Model):
   __tablename__ = 'arms'
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(32), nullable = False)
   # subjects = db.relationship('Subject', backref='subject', lazy = True)
   arm_subjects = db.relationship('Subject', secondary=arm_subjects, lazy='subquery',
        backref=db.backref('arm', lazy=True))
   users = db.relationship('User', backref = 'arm', lazy = 'dynamic')
   
   
   def __repr__(self):
      return f"Arm ('{self.name}')"


class Subject(db.Model):
   id = db.Column(db.Integer, primary_key = True, nullable = False)
   name = db.Column(db.String(120), unique = True, nullable = False)
   arm_id = db.Column(db.Integer, db.ForeignKey('arms.id'))
   subject_rating = db.relationship('Subjectrating', backref = 'subject_rating', lazy = True)
   
   def __repr__(self):
      return f"Subject ('{self.name}')"
   
class Subjectrating(db.Model):
   __tablename__ = "subject_rating"
   id = db.Column(db.Integer, primary_key = True, nullable = False)
   rating = db.Column(db.Integer, nullable = False)
   subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable = False)
   
      
class Question(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   question = db.Column(db.String(300), nullable = False, unique = False)
   answer = db.Column(db.String(20), nullable = False, unique = False)
   Options = db.relationship('Option', backref = 'option', lazy = True) 
   
   def __repr__(self):
      return f"Question ('{self.name}', '{self.answer}')"

class Option(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   Option = db.Column(db.String(50), nullable = False)
   question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable = False)
   
   def __repr__(self):
      return f"Option ('{self.name}'"
   
   
   