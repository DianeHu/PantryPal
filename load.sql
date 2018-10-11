INSERT INTO User VALUES
 	(001, 0, 0),
 	(002, 1, 2),
 	(003, 3, 4);

INSERT INTO Ingredients VALUES
	('Flour', 'lbs', 1),
	('Sugar', 'g', 3),
	('Milk', 'cups', 2);

INSERT INTO UserPantry VALUES
	(001, 001),
	(002, 003),
	(003, 002);

INSERT INTO PantryIngredients VALUES
	(001, 'Flour', 3),
	(002, 'Sugar', 5),
	(003, 'Milk', 4);

INSERT INTO Recipe VALUES
	('Curry chicken', 'http://example.com'),
	('Pad thai", 'http://example2.com'),
	('Noodles', 'http://example3.com');
