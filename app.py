from flask import Flask, jsonify, request, Response
import json
from settings import *
from UserModel import User
from functools import wraps
from RecordsModel import Records

import jwt, datetime


app.config['SECRET_KEY'] = 'or_elazar'


@app.route('/signup',methods=['POST'])
def user_signup():
    request_data = request.get_json()
    if not("username" in request_data and "password" in request_data):
        errorMsg = {
            "error":"Invalid user  was passed in this request",
            "helpString":"Data passed in similar to this : {'username':'my_name','password':my_password}"
        }
        response = Response(json.dumps(errorMsg),status=400,mimetype='application/json')
        return response
    username = str(request_data['username'])
    password = str(request_data['password'])
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=500)
    token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
    User.create_user(request_data['username'],request_data['password'] ,token)
    return token 


@app.route('/login', methods=['POST'])
def user_login():
    request_data= request.get_json()
    if not("username" in request_data and "password" in request_data):
        errorMsg = {
            "error":"Invalid user  was passed in this request",
            "helpString":"Data passed in similar to this : {'username':'my_name','password':my_password}"
        }
        response = Response(json.dumps(errorMsg),status=400,mimetype='application/json')
        return response
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.user_password_match(username,password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=500)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        User.update_token(username,token)
        return token 
    else:
        errorMsg = "Invalid username or password"
        response = Response(json.dumps(errorMsg),status=400,mimetype='application/json')
        return response


@app.route('/list')
def get_listings():
    request_data = request.get_json()
    if not (User.is_user_valid(request_data['username'])):
        errorMsg = "invalid username"
        response = Response(json.dumps(errorMsg),status=400,mimetype='application/json')
        return response
    token = User.get_user(request_data['username']).token
    try:
        jwt.decode(token, app.config['SECRET_KEY'])
        return jsonify({'records':Records.get_user_records(request_data['username'])})
    except:
        errorMsg = "invalid token"
        response = Response(json.dumps(errorMsg),status=400,mimetype='application/json')
        return response

#exemple = {
#   'username': 'or',
#   'records':[
#     {
#        'superhero': 'Hawkeye',
#        'power': 'bow'
#      },
#      {
#       'superhero': 'the Flash',
#       'power': 'super speed'
#      }
#   ]
#}


def valid_put_request_data(request_data):
    if not ("username" in request_data and "records" in request_data):
        return False
    for rec in request_data['records']:
        if not ("superhero" in rec and "power" in rec):
            return False
    else:
        return True

@app.route('/add_records',methods=['PUT'])
def add_listing():
    request_data = request.get_json()
    if not valid_put_request_data(request_data):
        invalidObjectErrorMsg = ["Invalid object was passed in this request",
        "data passed in similar to this:",
        "{",
        "'username': 'or',",
        "'records':[",
        "{'superhero': 'Hawkeye','power': 'bow' }"
        ]
        response = Response(json.dumps(invalidObjectErrorMsg), status=400,mimetype='application/json')
        return response
    if not (User.is_user_valid(request_data['username'])):
        errorMsg = "invalid username"
        response = Response(json.dumps(errorMsg),status=400,mimetype='application/json')
        return response
    token = User.get_user(request_data['username']).token
    try:
        jwt.decode(token, app.config['SECRET_KEY'])
        i = 0
        for rec in request_data['records']:
            Records.add_record(request_data['username'],rec['superhero'],rec['power'])
            i+=1
        return str(i)
    except:
        errorMsg = "invalid token"
        response = Response(json.dumps(errorMsg),status=400,mimetype='application/json')
        return response


app.run(port=8888)