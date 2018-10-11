# PantryPal

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
