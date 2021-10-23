-- TODO: 파라미터 받도록 수정
SELECT
	r.id,
	r.category_id,
	c.name AS category,
	r.title,
	r.title_desc,
	r.view,
	r.level,
	r.thumbnail,
	STRING_AGG(i.name, ',') AS ingredients
FROM 
	recipe AS r
JOIN 
	category AS c
	ON r.category_id = c.id
JOIN 
	recipe_ingredient AS ri
	ON r.id = ri.recipe_id
JOIN
	ingredient AS i 
	ON ri.ingredient_id = i.id
WHERE 
	(r.category_id = ANY (%(categories)s) OR %(categories)s IS NULL)
AND 
	r.id = ANY (
		SELECT recipe_id FROM recipe_ingredient
		WHERE (ingredient_id = ANY (%(ingredients)s) OR %(ingredients)s IS NULL)
	)
GROUP BY r.id, c.name
ORDER BY r.id ASC
LIMIT %(limit)s OFFSET %(offset)s;