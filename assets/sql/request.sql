CREATE DATABASE IF NOT EXISTS openfoodfacts_substitutes;
USE openfoodfacts_substitutes;
CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    name VARCHAR(255)) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    family_name VARCHAR(63), 
    nick_name VARCHAR(63), 
    username VARCHAR(15)) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS foods (
    code VARCHAR(13) NOT NULL PRIMARY KEY,
    name VARCHAR(127),
    description TEXT,
    url VARCHAR(255),
    score ENUM('a','b','c','d','e') NOT NULL,
    brand VARCHAR(63),
    packaging VARCHAR(255),
    image_url VARCHAR(255)) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS shops (
    name VARCHAR(63) NOT NULL PRIMARY KEY) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS food_categories (
    food_code VARCHAR(13),
    category_id VARCHAR(255),
    CONSTRAINT fk_food_categories__food_code
        FOREIGN KEY (food_code)
        REFERENCES foods (code)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_food_categories__categories_id
        FOREIGN KEY (category_id)
        REFERENCES categories (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT unique_food_categoriee
        UNIQUE (food_code, category_id)) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS user_foods (
    user_id INT,
    food_code VARCHAR(13),
    CONSTRAINT fk_user_foods__users_id
        FOREIGN KEY (user_id)
        REFERENCES users (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_user_foods__foods_code
        FOREIGN KEY (food_code)
        REFERENCES foods (code)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT unique_user_foods
        UNIQUE (user_id, food_code)) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS food_substitutes (
    food_code VARCHAR(13),
    substitute_code varchar(13),
    user_id INT(11),
    CONSTRAINT fk_food_substitutes__foods_code
        FOREIGN KEY (food_code)
        REFERENCES foods (code)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_food_substitutes__substitute_code
        FOREIGN KEY (substitute_code)
        REFERENCES foods (code)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_food_substitutes__user_id
        FOREIGN KEY (user_id)
        REFERENCES users (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT unique_food_substitutes
        UNIQUE (food_code, substitute_code, user_id)) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS food_shops (
    food_code VARCHAR(13),
    shop_name VARCHAR(63),
    CONSTRAINT fk_food_shops__foods_code
        FOREIGN KEY (food_code)
        REFERENCES foods (code)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_user_foods__shops_name
        FOREIGN KEY (shop_name)
        REFERENCES shops (name)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT unique_food_shops
        UNIQUE (shop_name, food_code)) ENGINE = InnoDB;
CREATE ROLE IF NOT EXISTS openfoodfacts_role;
GRANT SELECT, INSERT, UPDATE, DELETE, SHOW VIEW, EXECUTE
  ON openfoodfacts_substitutes.* TO openfoodfacts_role;
CREATE TRIGGER IF NOT EXISTS foods_without_user
  AFTER DELETE ON user_foods FOR EACH ROW
    DELETE FROM foods WHERE code NOT IN
        (SELECT DISTINCT food_code FROM user_foods);
CREATE TRIGGER IF NOT EXISTS foods_without_substitute
  AFTER DELETE ON food_substitutes FOR EACH ROW
    DELETE FROM foods WHERE code NOT IN
        (SELECT DISTINCT substitute_code FROM food_substitutes)
      AND code NOT IN
        (SELECT DISTINCT food_code FROM food_substitutes);
CREATE TRIGGER IF NOT EXISTS shops_without_food
  AFTER DELETE ON food_shops FOR EACH ROW
    DELETE FROM shops WHERE name NOT IN
    (SELECT DISTINCT shop_name FROM food_shops);
CREATE DEFINER=openfoodfacts_role PROCEDURE IF NOT EXISTS
remove_foods_without_substitute()
  MODIFIES SQL DATA
    DELETE FROM foods WHERE code NOT IN
      (SELECT DISTINCT substitute_code FROM food_substitutes)
    AND code NOT IN
      (SELECT DISTINCT food_code FROM food_substitutes);
CREATE DEFINER=openfoodfacts_role PROCEDURE IF NOT EXISTS
remove_shops_without_food()
  MODIFIES SQL DATA
    DELETE FROM shops WHERE name NOT IN
      (SELECT DISTINCT shop_name FROM food_shops);
CREATE DEFINER=openfoodfacts_role PROCEDURE IF NOT EXISTS
remove_foods_without_user()
  MODIFIES SQL DATA
    DELETE FROM foods WHERE code NOT IN
      (SELECT DISTINCT food_code FROM user_foods);