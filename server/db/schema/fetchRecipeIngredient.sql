SELECT
    ri.id,
    ri.ingredient_id,
    amount,
    ri.name AS name,
    i.name AS default_name
FROM recipe_ingredient AS ri
JOIN ingredient as i ON ri.ingredient_id = i.id
WHERE recipe_id = %(id)s;