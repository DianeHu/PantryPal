INSERT INTO Users VALUES
 	(001, 50, 50, 'Kevin'),
 	(002, 50, 50, 'Diane'),
 	(003, 50, 50, 'Jarod');

INSERT INTO Ingredients VALUES
	('Flour', 'lbs', 1),
	('Sugar', 'g', 3),
	('Milk', 'cups', 2);

INSERT INTO UserPantry VALUES
	(001, 004),
	(002, 002),
	(003, 003);

INSERT INTO PantryIngredients VALUES
	(004, 'Flour', 3),
	(002, 'Sugar', 2),
	(003, 'Milk', 4);

INSERT INTO Recipe VALUES
	('Curry chicken', 'http://example.com'),
	('Pad thai', 'http://example2.com'),
	('Tomato Soup', 'http://example3.com');
