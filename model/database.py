'''Database link objects to MariaDB database'''

import pymysql
from pymysql.err import OperationalError
from PyQt5.QtCore import pyqtSignal, QObject
from settings import GRANT_USER, GRANT_USER_PASSWD, DB_PORT, \
                     DB_SOCKET, DB_CONNECT_MODE, DB_HOSTNAME,\
                     DB_INIT_FILE
import re

class Database(QObject):
    '''Database model for user to be abee to record Open Food Facts data
    localy'''

    _connection = None
    status_message = pyqtSignal(str)

    def __init__(self, username=None, password=None, db=None):
        super()

        if Database._connection:
            if Database._connection.open:
                Database._connection.close()
        if username == None:
            self._connect_database(user=GRANT_USER,
                                   passwd=GRANT_USER_PASSWD,
                                   db='information_schema')
        else:
            self._connect_database(user=username,
                                   passwd=password,
                                   db=db)
            self._connect_to_off_db()

    def _connect_database(self, user=None, passwd=None,
                         db=None, socket=None):
        '''Connection to database with exception handle'''

        try:
            if DB_CONNECT_MODE == "SOCKET":
                Database._connection = pymysql.connect(
                                                unix_socket=DB_SOCKET,
                                                user=user,
                                                password=passwd,
                                                database=db)

            elif DB_CONNECT_MODE == "TCP":
                Database._connection = pymysql.connect(host=DB_HOSTNAME,
                                                port=DB_PORT,
                                                user=user,
                                                password=passwd,
                                                database=db)
        except ConnectionError:
                self.status_message.emit("Failed connection between", user,
                                         "and", db)

    def _connect_to_off_db(self):
        '''Connect the current user on database'''

        #request = "SET ROLE openfoodfacts_role;"
        #self.send_request(request)
        request =  "USE openfoodfacts_substitutes;"
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
            if values:
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
        except OperationalError as e:
            print(e.args[0], e.args[1])
            Database._connection.rollback()
            Database.status_message.emit("Erreur lors de l'exécution de "
                                "la requête SQL dans la base de donnée")
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
            if values:
                cursor.execute(request, values)
            else:
                cursor.execute(request)
            Database._connection.commit()
        except OperationalError as e:
            print(e.args[0], e.args[1])
            Database._connection.rollback()
        finally:
            if cursor:
                cursor.close()
        return cursor


    def _generateDatabase(self):
        '''Create database, tables and roles'''

        with open(DB_INIT_FILE, 'r') as requests_file:
            sql_requests = requests_file.read()
            for request in sql_requests.split(';'):
                if request != "":
                    self.send_request(request)

    def _generate_users_role(self):
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

        request = "INSERT INTO users (family_name, nick_name, username) VALUES (%s, %s, %s);"
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
            cat_id_list = [ category["id"] for category in cat ]
            for off_category in off_cat:
                flag_finder = False
                is_fr = re.match(r'^fr:', off_category["id"])
                is_en = re.match(r'^en:', off_category["id"])
                is_latin = re.match(r'[0-9a-zA-z\s]', off_category["name"])
                no_en = re.match(r'^[^e][^n][^:]', off_category["name"])
                if is_latin and no_en and ( is_fr or is_en ):
                    off_cat_id_list.append(off_category["id"])
                    for category in cat:
                        if off_category["id"] == category["id"]:
                            if off_category["name"] != category["name"]:
                                categories_to_update.append(
                                    { "id": category["id"],
                                      "name" : category["name"]})
                            flag_finder = True
                    if not flag_finder:
                        missing_categories.append( (off_category["id"],
                                                    off_category["name"]) )
            unknown_categories = [ cat_id for cat_id in cat_id_list if
                                   cat_id not in off_cat_id_list ]
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
