COPY category (id, name)
FROM '/var/lib/postgresql/csvs/category.csv'
DELIMITER ',' CSV HEADER;

COPY ingredient (id, name)
FROM '/var/lib/postgresql/csvs/ingredient.csv'
DELIMITER ',' CSV HEADER;

COPY recipe (id, title, level, title_desc, thumbnail, image, category_id, view)
FROM '/var/lib/postgresql/csvs/recipe.csv'
DELIMITER ',' CSV HEADER;

COPY recipe_ingredient (id, recipe_id, ingredient_id, name, amount)
FROM '/var/lib/postgresql/csvs/recipe_ingredient.csv'
DELIMITER ',' CSV HEADER;

COPY favor (id, recipe_id)
FROM '/var/lib/postgresql/csvs/favor.csv'
DELIMITER ',' CSV HEADER;

COPY recipe_step (id, recipe_id, step, content, images, thumbnails)
FROM '/var/lib/postgresql/csvs/recipe_step.csv'
DELIMITER ',' CSV QUOTE '"' HEADER;