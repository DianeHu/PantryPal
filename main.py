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
import requests

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

key = "Not posted, fix yaml later too"
url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"
# X-Mashape-Key = os.environ['API_KEY']

db = SQLAlchemy(app)
# db.create_all()

# class Recipe(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ingredient = db.Column(db.String(255))
#
#     def __init__(self, ingredient):
#         self.ingredient = ingredient

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
    ingname = db.Column(db.String(255), nullable=False)

    #children = relationship("Ingperrecipe", "Pantry")

    def __init__(self, ingname):
        self.ingname = ingname

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)

    #children = relationship("Pantry")

    def __init__(self, username, email, latitude, longitude):
        self.username = userName
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

### FOR THE FOLLOWING FUNCTIONS:
# call verifyToken on request.args.get('token') as in /authenticate
# use .get('email') attribute of the returned dictionary to identify user (primary key)

@app.route('/recipesforingredients', methods=['GET'])
def recipesforingredients():
    # user = verifyToken(request.args.get('token'))
    # if user:
    #     currEmail = user.get('email')
    #     userId = Users.query.filter(Users.email == currEmail)[0].id
    #     currPantry = Pantry.query.filter(Pantry.userid == userId)
    #     ingIds = [p.ingid for p in currPantry]
    #     ingredients = Ingredient.query.filter(Ingredient.id.in_(ingIds))
    #     currPantry = [i.ingname for i in ingredients]
    #     payload = {'fillingredients': False,
    #                 'ingredients': currPantry,
    #                 'limitLicense': False,
    #                 'number': 10,
    #                 'ranking': 2
    #                 }
    #     head = {'X-Mashape-Key': key, 'Accept': 'application/json'}
    #     r = requests.get(url, params = payload, headers = head)
    #     return jsonify(r.json()), 201
    # else:
    #     return 'Invalid user', 401

    currEmail = "dianehu24@gmail.com"
    userId = Users.query.filter(Users.email == currEmail)[0].id
    currPantry = Pantry.query.filter(Pantry.userid == userId)
    ingIds = [p.ingid for p in currPantry]
    ingredients = Ingredient.query.filter(Ingredient.id.in_(ingIds))
    currPantry = [i.ingname for i in ingredients]
    payload = {'fillingredients': False,
                'ingredients': currPantry,
                'limitLicense': False,
                'number': 10,
                'ranking': 2
                }
    head = {'X-Mashape-Key': key, 'Accept': 'application/json'}
    r = requests.get(url, params = payload, headers = head)
    return jsonify(r.json()), 201


@app.route('/')
def hello():
    db.create_all()
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/getpantry', methods=['GET'])
def getpantry():
    # user = verifyToken(request.args.get('token'))
    # if user:
    #     currEmail = user.get('email')
    #     userId = Users.query.filter(Users.email == currEmail)[0].id
    #     currPantry = Pantry.query.filter(Pantry.userid == userId)
    #     ingIds = [p.ingid for p in currPantry]
    #     ingredients = Ingredient.query.filter(Ingredient.id.in_(ingIds))
    #     results = {'Ingredients': [i.ingname for i in ingredients]}
    #     return jsonify(results), 201
    # else:
    #     return "Invalid user", 401

        currEmail = "dianehu24@gmail.com"
        userId = Users.query.filter(Users.email == currEmail)[0].id
        currPantry = Pantry.query.filter(Pantry.userid == userId)
        ingIds = [p.ingid for p in currPantry]
        ingredients = Ingredient.query.filter(Ingredient.id.in_(ingIds))
        results = {'Ingredients': [i.ingname for i in ingredients]}
        return jsonify(results), 201


@app.route("/modifyingredients/<string:ingredient>/<int:shouldBeAdded>", methods=['POST'])
def modifyIngredients(ingredient, shouldBeAdded):
    # user = verifyToken(request.args.get('token'))
    # if user:
    #
    #     currEmail = user.get('email')
    #     userId = Users.query.filter(Users.email == currEmail)[0].id
    #     ing = Ingredient.query.filter(Ingredient.ingname == ingredient)[0].id
    #
    #     if shouldBeAdded == 1:
    #         p = Pantry(userid = userId, ingid = ing)
    #         db.session.add(p)
    #         db.session.commit()
    #         return ("Success", 201)
    #
    #     elif shouldBeAdded == 0:
    #         Pantry.query.filter(Pantry.ingid == ing and Pantry.userid == userId).delete()
    #         db.session.commit()
    #         return("Success", 201)
    #     else:
    #         return (None, 401) # check that 401 is the right error
    # else:
    #     return ("Invalid user", 401)

    currEmail = "dianehu24@gmail.com"
    userId = Users.query.filter(Users.email == currEmail)[0].id
    ing = Ingredient.query.filter(Ingredient.ingname == ingredient)[0].id

    if shouldBeAdded == 1:
        p = Pantry(userid = userId, ingid = ing)
        db.session.add(p)
        db.session.commit()
        return ("Success", 201)
    elif shouldBeAdded == 0:
        Pantry.query.filter(Pantry.ingid == ing and Pantry.userid == userId).delete()
        db.session.commit()
        return("Success", 201)
    else:
        return (None, 401) # check that 401 is the right error

@app.route("/getingredients", methods=['GET'])
def getIngredients():
    ings = Ingredient.query.all()
    results = {'Ingredients': [i.ingname for i in ings]}
    return jsonify(results), 200

@app.route("/testadd/<string:val>")
def testadd(val):
    ing = Ingredient(ingname = val)
    db.session.add(ing)
    db.session.commit()
    return val, 200

@app.route('/test')
def test():
    rec = Recipe(
        recipeName = "Test",
        instruction = "Do something",
        url = "www.test.com"
    )

    db.session.add(rec)
    db.session.commit()

    recipes = Recipe.query.limit(10)

    results = ['Recipe: {}'.format(r.recipeName) for r in recipes]

    output = 'Last 10 recipe names: \n{}'.format('\n'.join(results))

    return output, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
# [END app]
