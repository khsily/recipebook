SELECT * FROM recipe_step
WHERE recipe_id = %(id)s
ORDER BY step ASC;