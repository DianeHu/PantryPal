# PantryPal
## Running Flask App Locally

### Start up the virtual environment in shell

Go to the root level of the repository and use the following command (In a shell that is not Git Bash):

#### Mac/Linux
```
. venv/bin/activate
```

#### Windows
```
venv\Scripts\activate
```

### Install Flask
run this command :
```
pip install Flask
```

### Database Setup

If you do not have Postgres downloaded on your local machine, do so now. You can do so at https://www.postgresql.org/download/.

Next, after activating the virtual environment, run the following command to install requirements for this project:

```
pip install -r requirements.txt
```
In a separate shell, create a new database by running this command. Make sure you keep the name the same:

```
createdb pantry-test
```

If you have Postgres installed correctly, and are running commands as a user with sufficient permissions, this should run fine. If you run into issues, please make sure you are either using your root database user, or that the user you are using (if not the root) has been given sufficient permissions to perform database operations.

To create the databases necessary, next return to the shell running your virtual environment, and run:

```
py create_tables.py
```

Now, go to https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients, and obtain a key for this API. When you have one, return to main.py and insert into the variable "key" whose current value is YOUR_SPOONACULAR_KEY.

You are now ready to start the application. In the shell running your virtual environment, type:

```
py main.py
```
In a new browser window, type in http://127.0.0.1:8080/. Your backend should now be running on that port.

### Deployment

To deploy, create a Google Cloud account, and set up a Postgres database. Download the gcloud CLI and create a Google App Engine instance. Replace the information in app.yaml with information specific to your instance, and deploy via the CLI. Further documentation can be found at https://cloud.google.com/appengine/docs/flexible/python/using-cloud-sql-postgres.
