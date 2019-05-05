'''Database link objects to MariaDB database'''

import pymysql
from pymysql.err import OperationalError
from settings import GRANT_USER, GRANT_USER_PASSWD, DB_PORT, \
                     DB_SOCKET, DB_CONNECT_MODE, DB_HOSTNAME,\
                     DB_INIT_FILE
import time

class Database():
    '''Database model for user to be abee to record Open Food Facts data
    localy'''

    _connection = None

    def __init__(self, username=None, password=None, db=None):
        super()

        if Database._connection:
            if Database._connection.open:
                Database._connection.close()
        if username == None:
            self._connect_database(user=GRANT_USER,
                                   passwd=GRANT_USER_PASSWD,
                                   db='information_schema')
            self._generateDatabase()
            self._generate_users_role()
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
                print("Failed connection between", user, "and", db)

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
    def send_request(request, values=None):
        '''Execute database request'''

        Database._connection.begin()
        cursor = Database._connection.cursor()
        try:
            if values:
                cursor.execute(request, values)
            else:
                cursor.execute(request)
        except OperationalError as e:
            print(e.args[0], e.args[1])
            Database._connection.rollback()
        Database._connection.commit()
        cursor.close()

    @staticmethod
    def ask_request(request, values=None):
        '''Return an iterator result for request question'''

        Database._connection.begin()
        cursor = Database._connection.cursor(pymysql.cursors.DictCursor)
        try:
            if values:
                cursor.execute(request, values)
            else:
                cursor.execute(request)
        except OperationalError as e:
            print(e.args[0], e.args[1])
            Database._connection.rollback()
        Database._connection.commit()
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
