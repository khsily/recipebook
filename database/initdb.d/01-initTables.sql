-- 테이블 생성
CREATE TABLE IF NOT EXISTS category (
	id SERIAL PRIMARY KEY,
	name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredient (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS recipe (
	id SERIAL PRIMARY KEY,
	category_id INTEGER REFERENCES category (id),
	title TEXT NOT NULL,
	title_desc TEXT,
	view INTEGER DEFAULT 0 NOT NULL,
	level INTEGER NOT NULL,
	thumbnail TEXT NOT NULL,
	image TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipe_step (
	id SERIAL PRIMARY KEY,
	recipe_id INTEGER REFERENCES recipe (id),
	step INTEGER NOT NULL,
	images TEXT[] NOT NULL,
	thumbnails TEXT[] NOT NULL,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipe_ingredient (
	id SERIAL PRIMARY KEY,
	recipe_id INTEGER REFERENCES recipe (id),
	ingredient_id INTEGER REFERENCES ingredient (id),
	name TEXT,
	amount VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS favor (
	id SERIAL PRIMARY KEY,
	recipe_id INTEGER REFERENCES recipe (id)
);

CREATE TABLE IF NOT EXISTS combination (
	id SERIAL PRIMARY KEY,
	combination TEXT[] NOT NULL
);
