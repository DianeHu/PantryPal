SELECT uid, name FROM User WHERE longitude>100 AND longitude<200 AND latitude>100 AND latitude<200;
SELECT name FROM Ingredients WHERE name='tomato' or name='cheese';
SELECT url, name FROM Recipe WHERE name LIKE 'tomato%';

