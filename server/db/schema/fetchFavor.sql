SELECT
	f.id,
	c.name as category,
	r.title,
	r.thumbnail
FROM favor as f
JOIN recipe as r ON f.recipe_id = r.id
JOIN category as c ON r.category_id = c.id;