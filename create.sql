CREATE TABLE User
(uid INT NOT NULL PRIMARY KEY,
 latitude NUMERIC NOT NULL CHECK(latitude <= 90 AND latitude >= -90),
 longitude NUMERIC NOT NULL CHECK(longitude <= 180 AND longitude >= -180),
 name VARCHAR(256) NOT NULL
 );

CREATE TABLE Ingredients
(name VARCHAR(256) NOT NULL,
measurement VARCHAR(256) NOT NULL,
price_per_unit NUMERIC NOT NULL,
PRIMARY KEY (name)
);

CREATE TABLE UserPantry(
uid INT NOT NULL,
pantryid INT NOT NULL,
PRIMARY KEY(uid),
PRIMARY KEY(pantryid),
FOREIGN KEY uid REFERENCES user(uid)
);

CREATE TABLE PantryIngredients(
pantryid INT NOT NULL,
ingredient_name VARCHAR(256) NOT NULL,
quantity NUMERIC NOT NULL,
PRIMARY KEY pantryid,
PRIMARY KEY ingredient_name,
FOREIGN KEY ingredient_name REFERENCES Ingredients(name),
FOREIGN KEY pantryid REFERENCES UserPantry(pantryid)
);

CREATE TABLE Recipe(
	-- Recipe's key is changed to be a name 
name VARCHAR(256) NOT NULL,
url VARCHAR(256) NOT NULL,
PRIMARY KEY name,
PRIMARY KEY url 
);
