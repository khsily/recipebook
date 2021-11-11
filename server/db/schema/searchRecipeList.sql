SELECT
	r.id,
	r.category_id,
	c.name AS category,
	r.title,
	r.title_desc,
	r.view,
	r.level,
	r.thumbnail,
	COUNT(DISTINCT ri.ingredient_id) FILTER (WHERE ri.ingredient_id = ANY(%(ingredients)s)) as counts,
	SUM(DISTINCT i.score) FILTER (WHERE ri.ingredient_id = ANY(%(ingredients)s)) as score,
	ARRAY_AGG(i.name ORDER BY ri.ingredient_id = ANY(%(ingredients)s) DESC) AS ingredients
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
ORDER BY ARRAY_POSITION(%(ids)s, r.id), score DESC, counts DESC, id ASC
LIMIT %(limit)s OFFSET %(offset)s;