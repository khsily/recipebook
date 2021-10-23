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
GROUP BY r.id, c.name
LIMIT 20 OFFSET 0;