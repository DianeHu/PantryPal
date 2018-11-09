SELECT * from Users;
SELECT ingredient_name FROM PantryIngredients as p1, Users as p3, UserPantry as p2 WHERE p3.name='Diane' AND p1.pantryid=p2.pantryid AND p2.uid=p3.uid;
SELECT uid, name FROM Users WHERE longitude>50 AND longitude<80 AND latitude>50 AND latitude<80;
SELECT name FROM Ingredients WHERE name='tomato' or name='cheese';
SELECT url, name FROM Recipe WHERE name LIKE 'Tomato%';

INSERT INTO Recipe VALUES
	('Noodlessss Soup', 'http://noodlesss.com');
SELECT url, name FROM Recipe WHERE name LIKE 'Noodle%';
INSERT INTO Users VALUES
 	(005, 90, 90, 'Emily');
SELECT longitude, latitude FROM Users WHERE name='Emily';

INSERT INTO Ingredients VALUES
	('Eggs', 'Number', 6);
INSERT INTO UserPantry VALUES
	(005, 005);
INSERT INTO PantryIngredients VALUES
	(005, 'Eggs', 3),
    (005, 'Flour', 1);
SELECT ingredient_name FROM PantryIngredients as p1, Users as p3, UserPantry as p2 WHERE p3.name='Emily' AND p1.pantryid=p2.pantryid AND p2.uid=p3.uid;
DELETE FROM PantryIngredients WHERE pantryid=5 AND ingredient_name='Flour';
