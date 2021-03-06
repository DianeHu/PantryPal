from flask import (
    render_template, request, make_response, current_app, jsonify
)
import connexion
from google.oauth2 import id_token
from google.auth.transport import requests
from functools import update_wrapper
from misc import crossdomain

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yml')

CLIENT_ID = "37356619128-u7hbclhbgqc5f2ivokut37mgh84dvo8c.apps.googleusercontent.com"

@app.route("/")
def main():
    return render_template('home.html')

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

# TODO
# # returns recipes for a specific user
@app.route("/getrecipes", methods=['GET'])
def getRecipes():
     user = verifyToken(request.args.get('token'))
     if user:
         userKey = user.get('email')
         # Gonna have to wait for the database to get the response
         myIngredients = getIngredients(userKey)
         responseData = jsonify(#Insert API call here) # Api Call with current Ingredients
         return (responseData, 200)
     else:
         return (None, 401)
#
# TODO
# # modify for a specific user
# # input: key value pairs of ingredient, shouldBeAdded
# # if shouldBeAdded is True, add to database, otherwise remove

@app.route("/modifyingredients/<string:ingredient>/<int:shouldBeAdded>", methods=['POST'])
def modifyIngredients(ingredient, shouldBeAdded):
    user = verifyToken(request.args.get('token'))
    if user:
        userKey = user.get('email')
        # Posting code here, not DB not setup so not sure yet
        response = jsonify(#tbd)
        return (response, 201)
    else:
        return (None, 401)

# TODO
# # return list of all ingredients
@app.route("/getingredients", methods=['GET'])
def getIngredients():
     user = verifyToken(request.args.get('token'))
     if user:
         userKey = user.get('email')
         myIngredients = jsonify(None) # Will have to change to make DB call when we get that set up
         return (myIngredients, 200)
     else:
         return (None, 401)






if __name__ == '__main__':
    app.run(debug=True)
