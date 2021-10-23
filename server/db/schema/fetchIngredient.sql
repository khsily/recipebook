SELECT * FROM ingredient
WHERE (id = ANY (%(ingredients)s) OR %(ingredients)s IS NULL);