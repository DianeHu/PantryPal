# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import os
from flask import Flask
from flask import (
    render_template, request, make_response, current_app, jsonify
)
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from google.oauth2 import id_token
from google.auth.transport import requests
from functools import update_wrapper
from misc import crossdomain
import requests as r
import json

app = Flask(__name__)

CLIENT_ID = "37356619128-u7hbclhbgqc5f2ivokut37mgh84dvo8c.apps.googleusercontent.com"
# [START example]
# Environment variables are defined in app.yaml.
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:pantry-password@127.0.0.1:5432/pantry-test"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
# default user is postgres not root
# "postgresql+psycopg2://postgres:pantry-password@/pantry-test?host=/cloudsql/pantrypal-316:us-east1:pantry-test"
#os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

key = "YOUR_SPOONACULAR_KEY" ## WARNING!!!
url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"
# X-Mashape-Key = os.environ['API_KEY']

db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipename = db.Column(db.String(255), nullable=False)
    instruction = db.Column(db.Text())
    url = db.Column(db.String(255))

    #children = relationship("Ingperrecipe")

    def __init__(self, recipename, instruction, url):
        self.recipename = recipename
        self.instruction = instruction
        self.url = url

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingname = db.Column(db.String(255), nullable=False, unique=True)

    #children = relationship("Ingperrecipe", "Pantry")

    def __init__(self, ingname):
        self.ingname = ingname

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)

    #children = relationship("Pantry")

    def __init__(self, username, email, latitude, longitude):
        self.username = username
        self.email = email
        self.latitude = latitude
        self.longitude = longitude

class Ingperrecipe(db.Model):
    recipeid = db.Column(db.ForeignKey(Recipe.id), primary_key=True)
    ingid = db.Column(db.ForeignKey(Ingredient.id), primary_key=True)

    def __init__(self, recipeid, ingid): ## Unsure if this is correct tbh
        self.recipeid = recipeid
        self.ingid = ingid

class Pantry(db.Model):
    userid = db.Column(db.ForeignKey(Users.id), primary_key=True)
    ingid = db.Column(db.ForeignKey(Ingredient.id), primary_key=True)

    def __init__(self, userid, ingid):
        self.userid = userid
        self.ingid = ingid

@app.route("/authenticate", methods=['GET', 'POST'])
@crossdomain(origin='*')
def auth():
    verify = verifyToken(request.args.get('token'))
    if verify:
        user = verify.get('name')
        em = verify.get('email')

        exists = Users.query.filter(Users.email == em).count()
        if exists == 0:
            us = Users(
                username = user,
                email = em,
                latitude = 0,
                longitude = 0
            )
            db.session.add(us)
            db.session.commit()
        return 'valid'
    else:
        return None

def verifyToken(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        userid = idinfo['sub']

        return idinfo
    except ValueError:
        return None

@app.route('/recipesforingredients', methods=['POST'])
@crossdomain(origin='*')
def recipesforingredients():
    user = verifyToken(request.values.get('token'))
    if user:
        data = request.data
        dataDict = json.loads(data)
        currPantry = dataDict.get('ingredients')
        payload = {'fillingredients': False,
                    'ingredients': currPantry,
                    'limitLicense': False,
                    'number': 10,
                    'ranking': 2
                    }
        head = {'X-Mashape-Key': key, 'Accept': 'application/json'}
        req = r.get(url, params = payload, headers = head)
        return jsonify(req.json()), 201
    else:
        return 'Invalid user', 401

@app.route('/')
@crossdomain(origin='*')
def create():
    db.create_all()
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/dropall')
@crossdomain(origin='*')
def dropall():
    db.drop_all()
    return 'Dropped!'

@app.route('/createuser', methods=['POST'])
def createuser(user, em):
    user = request.args.get('user')
    em = request.args.get('em')

    us = Users(
        username = user,
        email = em,
        latitude = 0,
        longitude = 0
    )
    db.session.add(us)
    db.session.commit()
    return 'Done!', 200

@app.route('/getpantry', methods=['GET'])
@crossdomain(origin='*')
def getpantry():
    user = verifyToken(request.args.get('token'))
    if user:
        currEmail = user.get('email')
        userId = Users.query.filter(Users.email == currEmail)[0].id
        currPantry = Pantry.query.filter(Pantry.userid == userId)
        ingIds = [p.ingid for p in currPantry]
        ingredients = Ingredient.query.filter(Ingredient.id.in_(ingIds))
        results = {'Ingredients': [i.ingname for i in ingredients]}
        return jsonify(results), 201
    else:
        return "Invalid user", 401

@app.route('/getcommunity', methods=['GET'])
@crossdomain(origin='*')
def getcommunity():
    user = verifyToken(request.args.get('token'))
    availUsers = []
    corrEmail = []
    ingreds = []
    if user:
        for val in Pantry.query.distinct(Pantry.userid): # get distinct users in pantry
            currId = val.userid # user id
            curr = Users.query.filter(Users.id == currId)[0]
            currName = curr.username # username
            currEmail = curr.email # email
            if currEmail != user.get('email'):
                availUsers.append(currName)
                corrEmail.append(currEmail)
                ingTemp = Pantry.query.filter(Pantry.userid == currId) # corresponding ingredients
                ings = [Ingredient.query.filter(Ingredient.id == p.ingid)[0].ingname for p in ingTemp] # get ing names
                ingreds.append(ings)

        results = [{'name': n, 'email': e, 'ingredients': i} for (n,e,i) in zip(availUsers, corrEmail, ingreds)]
        return jsonify(results), 201
    else:
        return "Invalid user", 401

@app.route("/modifyingredients", methods=['POST'])
@crossdomain(origin='*')
def modifyIngredients():
    ingredient = request.values.get('ingredient')
    ing = ''
    exists = Ingredient.query.filter(Ingredient.ingname == ingredient).count()

    if exists == 0:
        ingr = Ingredient(ingname = ingredient)

        db.session.add(ingr)
        db.session.flush()

        ing = ingr.id
        db.session.commit()
    else:
        ing = Ingredient.query.filter(Ingredient.ingname == ingredient)[0].id

    user = verifyToken(request.values.get('token'))
    shouldBeAdded = request.values.get('shouldBeAdded')
    if user:
        currEmail = user.get('email')
        userId = Users.query.filter(Users.email == currEmail)[0].id

        if shouldBeAdded == "1":
            exists = Pantry.query.filter(Pantry.ingid == ing and Pantry.userid == userId).count()
            if exists == 0:
                p = Pantry(userid = userId, ingid = ing)
                db.session.add(p)
                db.session.commit()
                return ("Success", 201)
            else:
                return ("Already in pantry", 201)

        elif shouldBeAdded == "0":
            exists = Pantry.query.filter(Pantry.ingid == ing and Pantry.userid == userId)
            if exists.count() != 0:
                exists.delete()
            db.session.commit()
            return("Success", 201)
        else:
            return ("Should be added was invalid", 401) # check that 401 is the right error
    else:
        return ("Invalid user", 401)

@app.route("/getingredients", methods=['GET'])
def getIngredients():
    ings = Ingredient.query.all()
    results = {'Ingredients': [i.ingname for i in ings]}
    return jsonify(results), 200

@app.route("/adding/<string:val>")
def adding(val):
    ing = Ingredient(ingname = val)
    db.session.add(ing)
    db.session.commit()
    return val, 200

if __name__ == '__main__':
    #app.run(host='10.197.36.110', port=8080, debug=True)
    app.run(host='127.0.0.1', port=8080)
# [END app]
