SELECT
	r.id,
	title,
	title_desc,
	view,
	level,
	thumbnail,
	image,
	category_id,
	c.name as category
FROM recipe as r
JOIN category as c ON r.category_id = c.id
WHERE r.id = %(id)s;