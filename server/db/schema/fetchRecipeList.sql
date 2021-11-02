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
	ARRAY_AGG(i.name) AS ingredients
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
	(r.id = ANY (%(ids)s) OR %(ids)s IS NULL)
GROUP BY r.id, c.name
ORDER BY ARRAY_POSITION(%(ids)s, r.id)
LIMIT %(limit)s OFFSET %(offset)s;