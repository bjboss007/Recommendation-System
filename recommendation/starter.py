from recommendation.models import *
from recommendation import bcrypt, db
from recommendation import create_app
from recommendation.user.questions import questions
from pathlib import Path

app = create_app()
app.test_request_context().push()


def starter():
    art_arm = Arm(name = "Art")
    comm_arm = Arm(name = "Commercial")
    sci_arm = Arm(name = "Science")

    math = Subject(name = "Mathematics")
    bio = Subject(name = "Biology")
    chem = Subject(name = "Chemistry")
    phy = Subject(name = "Physics")

    acc = Subject(name = "Accounting")
    eco = Subject(name = "Economics")
    comm = Subject(name = "Commerce")

    lit = Subject(name = "Lit-In-English")
    crk = Subject(name = "CRK")
    gov = Subject(name = "Government")
    hit = Subject(name = "History")

    art_arm.arm_subjects = [math,lit,crk,gov,hit]
    comm_arm.arm_subjects = [math,acc,eco,comm]
    sci_arm.arm_subjects = [math,bio,chem,phy]
    
    db.session.add_all([art_arm, comm_arm, sci_arm])
    
    for quest in questions:
        question = Question(name = quest['question'], answer = quest['answer'])
        options = []
        for opt in quest['options']:
            option = Option(name = opt)
            options.append(option)
        question.options = options
        db.session.add(question)

    db.session.commit()