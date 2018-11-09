CREATE TABLE Users
(uid INT NOT NULL PRIMARY KEY,
 latitude NUMERIC NOT NULL CHECK(latitude <= 90 AND latitude >= -90),
 longitude NUMERIC NOT NULL CHECK(longitude <= 180 AND longitude >= -180),
 name VARCHAR(20) NOT NULL
 );

 CREATE TABLE Ingredients
(name VARCHAR(20) NOT NULL,
measurement VARCHAR(20) NOT NULL,
price_per_unit NUMERIC NOT NULL,
PRIMARY KEY (name)
);

CREATE TABLE UserPantry(
uid INT NOT NULL REFERENCES Users(uid),
pantryid INT NOT NULL UNIQUE,
PRIMARY KEY(uid, pantryid)
);

CREATE TABLE PantryIngredients(
pantryid INT NOT NULL REFERENCES UserPantry(pantryid),
ingredient_name VARCHAR(20) NOT NULL references Ingredients(name),
quantity NUMERIC NOT NULL,
PRIMARY KEY (pantryid, ingredient_name)
);

CREATE TABLE Recipe(
        -- Recipe's key is changed to be a name
name VARCHAR(20) NOT NULL,
url VARCHAR(20) NOT NULL,
PRIMARY KEY (name, url)
);
