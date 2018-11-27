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
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)

# [START example]
# Environment variables are defined in app.yaml.
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:pantry-password@127.0.0.1:5432/pantry-test"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
# default user is postgres not root
# "postgresql+psycopg2://postgres:pantry-password@/pantry-test?host=/cloudsql/pantrypal-316:us-east1:pantry-test"
#os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# db.create_all()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(255))

    def __init__(self, ingredient):
        self.ingredient = ingredient

@app.route('/')
def hello():
    db.create_all()
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/test')
def test():
    rec = Recipe(
        ingredient = "Tomato"
    )

    db.session.add(rec)
    db.session.commit()

    recipes = Recipe.query.limit(10)

    results = ['Recipe: {}'.format(r.ingredient) for r in recipes]

    output = 'Last 10 ingredients: \n{}'.format('\n'.join(results))

    return output, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
# [END app]
