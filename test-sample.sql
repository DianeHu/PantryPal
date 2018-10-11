SELECT uid, name FROM User WHERE longitude>50 AND longitude<80 AND latitude>50 AND latitude<80;
SELECT name FROM Ingredients WHERE name='tomato' or name='cheese';
SELECT url, name FROM Recipe WHERE name LIKE 'tomato%';

