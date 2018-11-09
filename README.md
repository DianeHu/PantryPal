# PantryPal

## Loading Production Dataset

Our production dataset is not scraped from anywhere necessarily, because our functionality largely operates based on the API we’re using. Instead, our production dataset will be populated as time goes on by users creating accounts and creating their own pantries with their own ingredients. Therefore, there is no specific code for generating a “production” dataset, just the code we’re using in our app to populate our website and update our database. See test-production.sql for examples.

## Running Flask App Locally

### Start up the virtual environment in shell

To do this, go to the root level of the repository and use the following command (In a shell that is not Git Bash):

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




From this point, run app.py in the virtual environment, and navigate to the appropriate port in a browser,
typically http://127.0.0.1:5000/.

## Database
To use our database, run the following commands with the files in our repository:

```
createdb db_name
psql db_name -af create.sql
psl db_name -af load.sql
```

Perform the last command if you wish to use a few preloaded tuples, otherwise feel free to create your own. If you wish to now run commands on the database, run the command:

```
psql db_name
```
