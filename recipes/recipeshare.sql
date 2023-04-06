SELECT * FROM recipeshare_erd.recipes;
SELECT * FROM users;
SELECT * FROM recipes;

-- create a recipe
INSERT INTO recipes (name, descriptions, instructions, date, under30, user_id)
VALUES ('Pasta','Great Pasta','Make it', '2023-10-10',1,1);

-- get all recipes with users
SELECT * FROM recipes
JOIN users
ON recipes.user_id = users.id;

-- get one recipe
SELECT * FROM recipes
WHERE id = 1;

-- get one recipe and its user
SELECT * FROM recipes
JOIN users
ON recipes.user_id = users.id
WHERE recipes.id = 3;

-- update recipe
UPDATE recipes
SET
name = "hello",
descriptions = "yyy"
WHERE id = 1;

-- delete a recipe
DELETE from recipes
WHERE id = 1;
DELETE from recipes

