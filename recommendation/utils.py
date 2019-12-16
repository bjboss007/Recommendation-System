import pandas as pd
from flask import jsonify
from recommendation.models import User, Arm, Subjectrating, Subject, UserInfo

def mapping(key):
    mapping = pd.read_csv("recommendation/mapping.csv")
    result = mapping[mapping["CAREER INTEREST_enc"] == key]["CAREER INTEREST"].unique()[0]
    return result


def parseData(user):
    subjects = user.userinfo.subjects
    userObj = {}
    userObj["age"] = float(user.userinfo.age)
    userObj["IQ"] = float("{0:.2f}".format(user.userinfo.iq))
    userObj["arm"] = user.userinfo.arm.name
    subjectArr = {}
    for subject in subjects:
        subject_name = Subject.query.get(subject.subject_id)
        subjectArr[subject_name.name] = subject.rating
    userObj["subjects"] =  subjectArr
    data = jsonify(userObj)
    return data

def correctForm(user: object):
    dataform = []
    science_padding = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    data = parseData(user).get_json()
    if data["arm"] == "Science":
        for sub in data["subjects"]:
            dataform = [data["age"],data["IQ"],float(data["subjects"]["Mathematics"]),float(data["subjects"]["Biology"]),float(data["subjects"]["Physics"]),float(data["subjects"]["Chemistry"])]+science_padding
    elif data["arm"] == "Art":
        for sub in data["subjects"]:
            dataform = [data["age"],data["IQ"],float(data["subjects"]["Mathematics"]),0.0,0.0,0.0,0.0,0.0,0.0,float(data["subjects"]["Government"]),float(data["subjects"]["Lit-in-English"]),float(data['subjects']["History"]),float(data['subjects']["CRK"])]
    elif data["arm"] == "Commercial":
        for sub in data["subjects"]:
            dataform = [data["age"],data["IQ"],float(data['subjects']["Mathematics"]),0.0,0.0,0.0,float(data['subjects']["Accounting"]),float(data['subjects']["Commerce"]),float(data['subjects']["Economics"])]     
    return dataform