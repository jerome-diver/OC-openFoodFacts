'''Database link objects to MariaDB database'''

import re
import pymysql
from pymysql.err import *
from PyQt5.QtCore import pyqtSignal, QObject

from settings import GRANT_USER, GRANT_USER_PASSWD, DB_PORT, \
    DB_SOCKET, DB_CONNECT_MODE, DB_HOSTNAME, \
    DB_INIT_FILE, DEBUG_MODE


class Database(QObject):
    '''Database model for user to be abee to record Open Food Facts data
    localy'''

    _connection = None
    status_message = pyqtSignal(str)

    def __init__(self, username=None, password=None, database=None):
        super().__init__()
        if Database._connection:
            if Database._connection.open:
                Database._connection.close()
        if username is None:
            self._connect_database(user=GRANT_USER,
                                   passwd=GRANT_USER_PASSWD,
                                   database='information_schema')
        else:
            self._connect_database(user=username,
                                   passwd=password,
                                   database=database)
            self.connect_to_off_db()

    def _connect_database(self, user=None, passwd=None,
                          database=None):
        '''Connection to database with exception handle'''

        try:
            if DB_CONNECT_MODE == "SOCKET":
                Database._connection = pymysql.connect(
                    unix_socket=DB_SOCKET,
                    user=user,
                    password=passwd,
                    database=database)

            elif DB_CONNECT_MODE == "TCP":
                Database._connection = pymysql.connect(
                    host=DB_HOSTNAME,
                    port=DB_PORT,
                    user=user,
                    password=passwd,
                    database=database)
        except ConnectionError:
            self.status_message.emit("Failed connection between",
                                     user, "and", database)

    def disconnect_database(self):
        '''Disconnect to the database'''

        Database._connection.close()

    def connect_to_off_db(self):
        '''Connect the current user on database'''

        # request = "SET ROLE openfoodfacts_role;"
        # self.send_request(request)
        request = "USE openfoodfacts_substitutes;"
        self.send_request(request)

    def __del__(self):
        if Database._connection:
            if Database._connection.open:
                Database._connection.close()

    @staticmethod
    def send_request(request, values=None, many=False):
        '''Execute database request'''

        cursor = None
        try:
            Database._connection.begin()
            cursor = Database._connection.cursor()
            if DEBUG_MODE:
                print("request :", request)
            if values:
                if DEBUG_MODE:
                    print("for values:", values)
                if many:
                    cursor.executemany(request, values)
                else:
                    cursor.execute(request, values)
            else:
                if many:
                    cursor.executemany(request)
                else:
                    cursor.execute(request)
            Database._connection.commit()
        except OperationalError as error:
            if DEBUG_MODE:
                print(error.args[0], error.args[1])
            Database._connection.rollback()
            Database.status_message.emit("Erreur lors de l'exécution de "
                                         "la requête SQL dans la base de "
                                         "donnée")
        except IntegrityError as e:
            if DEBUG_MODE:
                print(e.args[0], e.args[1])
            Database._connection.rollback()
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def ask_request(request, values=None):
        '''Return an iterator result for request question'''

        cursor = None
        try:
            Database._connection.begin()
            cursor = Database._connection.cursor(pymysql.cursors.DictCursor)
            if DEBUG_MODE:
                print("request :", request)
            if values:
                if DEBUG_MODE:
                    print("for values:", values)
                cursor.execute(request, values)
            else:
                cursor.execute(request)
            Database._connection.commit()
        except OperationalError as e:
            if DEBUG_MODE:
                print(e.args[0], e.args[1])
            Database._connection.rollback()
        except IntegrityError as e:
            if DEBUG_MODE:
                print(e.args[0], e.args[1])
            Database._connection.rollback()
        finally:
            if cursor:
                cursor.close()
        return cursor

    def generate_database(self):
        '''Create database, tables and roles'''

        with open(DB_INIT_FILE, 'r') as requests_file:
            sql_requests = requests_file.read()
            for request in sql_requests.split(';'):
                if request != "":
                    if DEBUG_MODE:
                        print(request)
                    self.send_request(request)

    def generate_users_role(self):
        '''From users list of openfoodfacts_substitutes,
        generate users role of the mariadb database'''

        request = "SELECT username FROM users;"
        for row in self.ask_request(request):
            request = "GRANT SELECT, INSERT, DELETE, UPDATE, SHOW VIEW ON " \
                      "openfoodfacts_substitutes.* TO %s ;"
            values = (row['username'])
            self.send_request(request, values)

    def create_user(self, username, password):
        '''Create a database user to ba able to login with roles'''

        request = "CREATE OR REPLACE USER %s IDENTIFIED BY %s;"
        values = (username, password)
        self.send_request(request, values)
        request = "GRANT %s TO %s;"
        values = ('openfoodfacts_role', username)
        self.send_request(request, values)

    def record_user(self, username, nick_name, family_name):
        '''Record an entry inside Table Users'''

        request = """
            INSERT INTO users 
                (family_name, nick_name, username) 
                VALUES (%s, %s, %s);"""
        values = (family_name, nick_name, username)
        self.send_request(request, values)

    def exist_username(self, username):
        '''Return if record users.username for username exist'''

        db_cursor = Database._connection.cursor()
        request = "SELECT id FROM users WHERE username=%s;"
        values = (username)
        db_cursor.execute(request, values)
        data = db_cursor.fetchone()
        exist = True if data else False
        db_cursor.close()
        return exist

    def update_categories(self, off_categories):
        '''Will update categories table of openfoodfacts_substitutes
        database'''

        def db_categories_status(off_cat, cat):
            '''Return status variables list:
            "Missing", "Unknown" and "ToUpdate"
            of categories table records'''

            off_cat_id_list = []
            missing_categories = []
            categories_to_update = []
            cat_id_list = [category["id"] for category in cat]
            for off_category in off_cat:
                flag_finder = False
                is_fr = re.match(r'^fr:', off_category["id"])
                is_en = re.match(r'^en:', off_category["id"])
                is_latin = re.match(r'[0-9a-zA-z\s]', off_category["name"])
                no_en = re.match(r'^[^e][^n][^:]', off_category["name"])
                if is_latin and no_en and (is_fr or is_en):
                    off_cat_id_list.append(off_category["id"])
                    for category in cat:
                        if off_category["id"] == category["id"]:
                            if off_category["name"] != category["name"]:
                                categories_to_update.append(
                                    {"id": category["id"],
                                     "name": category["name"]})
                            flag_finder = True
                    if not flag_finder:
                        missing_categories.append((off_category["id"],
                                                   off_category["name"]))
            unknown_categories = [cat_id for cat_id in cat_id_list if
                                  cat_id not in off_cat_id_list]
            return (unknown_categories,
                    missing_categories,
                    categories_to_update)

        categories = []
        request = "SELECT id, name FROM categories;"
        for row in self.ask_request(request):
            categories.append(row)

        unknown, missing, to_update = db_categories_status(off_categories,
                                                           categories)
        if to_update:
            request = "UPDATE categories SET name=%s WHERE id=%s ;"
            for fields in to_update:
                self.send_request(request, (fields["name"], fields["id"]))
        if missing:
            request = "INSERT INTO categories (id, name) " \
                      "VALUES (%s, %s) ;"
            self.send_request(request, missing, True)
        if unknown:
            request = "DELETE FROM categories WHERE id=%s ;"
            for id in unknown:
                self.send_request(request, (id))

    def new_record(self, category_id, food, substitutes_details,
                   user_id):
        '''Record new entry for selected substitutes and linked
        correspondant category and food selected and products details'''

        request = """
                INSERT IGNORE INTO food_substitutes 
                    (food_code, substitute_code) 
                    VALUES (%s, %s);"""
        # add foods, shops, food_shops records :
        if DEBUG_MODE:
            print("get this product:", food)
        food_selected_code = food["codes_tags"][1]
        shops = []
        for shop in food["stores_tags"]:
            shops.append(shop)
        food_selected_details = (
            food["product_name_fr"],
            food["ingredients_text"],
            food["nutrition_grades_tags"][0],
            food["brands_tags"],
            food["packaging"],
            food["url"],
            food["image_front_url"],
            shops
        )
        try:
            self._record_product(user_id, category_id, food_selected_code,
                                 food_selected_details)
            for code, details in substitutes_details.items():
                    self._record_product(user_id, category_id, code, details)
                    values = (food_selected_code, code)
                    self.send_request(request, values)
            return True
        except Error as error:
            self.status_message.emit("Il y a eu un problème d'enregistrement "
                                     "des données dans la base")
            return False

    def _record_product(self, user_id, category_id, food_code, details):
        """Record a full detailed content for tables:
        foods, shops, food_shops, user_foods, food_categories"""

        request = {
            "food_categories": """
                INSERT INTO food_categories 
                        (food_code, category_id) 
                        VALUES (%s, %s);""",
            "foods": """
                INSERT INTO foods 
                    (code, name, description, score, 
                    brand, packaging, url, image_url) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
            "shops": """
                INSERT INTO shops (name) VALUES (%s) 
                    ON DUPLICATE KEY UPDATE name=VALUE(name);""",
            "food_shops": """
                INSERT IGNORE INTO food_shops 
                    (food_code, shop_name) 
                    VALUES (%s, %s);""",
            "user_foods": """
                INSERT INTO user_foods 
                    (user_id, food_code) 
                    VALUES (%s, %s);""" }
        try:
            values = (food_code,) + details[0:7]
            self.send_request(request["foods"], values)
            values = (user_id, food_code)
            self.send_request(request["user_foods"], values)
            values = (food_code, category_id)
            self.send_request(request["food_categories"], values)
            if details[7]:
                for shop in details[7]:
                    value = (shop,)
                    self.send_request(request["shops"], value)
                    values = (food_code, shop)
                    self.send_request(request["food_shops"], values)
        except Error as error:
            if DEBUG_MODE:
                print("problem for record in database")



