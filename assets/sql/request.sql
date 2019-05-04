CREATE DATABASE IF NOT EXISTS openfoodfacts_substitutes;
USE openfoodfacts_substitutes;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    family_name VARCHAR(64), 
    nick_name VARCHAR(64), 
    username VARCHAR(16));
CREATE TABLE IF NOT EXISTS foods (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    name_ VARCHAR(128), 
    description text);
CREATE TABLE IF NOT EXISTS shops (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    name_ VARCHAR(128),
    url_ VARCHAR(256),
    score VARCHAR(1),
    address TEXT,
    url VARCHAR(256));
CREATE TABLE IF NOT EXISTS user_foods (
    user_id INT, 
    food_id INT,
    CONSTRAINT fk_user_foods__users_id 
        FOREIGN KEY (user_id) 
        REFERENCES users (id) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE,
    CONSTRAINT fk_user_foods__foods_id
        FOREIGN KEY (food_id) 
        REFERENCES foods (id) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE,
    CONSTRAINT unique_user_foods
        UNIQUE (user_id, food_id));
CREATE TABLE IF NOT EXISTS food_substitutes (
    food_id INT, 
    substitute_id INT,
    CONSTRAINT fk_food_substitutes__foods_id  
        FOREIGN KEY (food_id) 
        REFERENCES foods (id) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE,
    CONSTRAINT fk_food_substitutes__substitute_id
        FOREIGN KEY (substitute_id)  
        REFERENCES foods (id) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE,
    CONSTRAINT unique_food_substitutes
        UNIQUE (food_id, substitute_id));
CREATE TABLE IF NOT EXISTS food_shops (
    food_id INT, 
    shop_id INT, 
    CONSTRAINT fk_food_shops__foods_id
        FOREIGN KEY (food_id) 
        REFERENCES foods (id) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE,
    CONSTRAINT fk_user_foods__shops_id
        FOREIGN KEY (shop_id) 
        REFERENCES shops (id) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE,
    CONSTRAINT unique_food_shops
        UNIQUE (shop_id, food_id));
CREATE ROLE IF NOT EXISTS openfoodfacts_role;
GRANT SELECT, INSERT, UPDATE, DELETE, SHOW VIEW
  ON openfoodfacts_substitutes.* TO openfoodfacts_role;