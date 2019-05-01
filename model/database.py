'''Database link objects to MariaDB database'''

import pymysql
from settings import GRANT_USER, GRANT_USER_PASSWD, DB_PORT, \
                     DB_SOCKET, DB_CONNECT_MODE, DB_HOSTNAME,\
                     DB_INIT_FILE

class Database():

    _connection = None

    def __init__(self, username=None, password=None, db=None):
        super()
     #   if Database._connection:
     #       Database._connection.close()
        if username == None:
            try:
                Database._connection = pymysql.connect(DB_HOSTNAME,
                                                       GRANT_USER,\
                                                       GRANT_USER_PASSWD,
                                                       'test')
            except ConnectionError:
                print("Impossible to establish connection between grant "
                      "user and database")
            self._generateDatabase()
        else:
            try:
                Database._connection = pymysql.connect(DB_HOSTNAME,
                                                       username,
                                                       password, db)
            except ConnectionError:
                print("Impossible to establish connection between",
                      username, "and", db)

    def __del__(self):
        self._connection.close()

    def _generateDatabase(self):
        with open(DB_INIT_FILE, 'r') as requests_file:
            db_cursor = self._connection.cursor()
            sql_requests = requests_file.read()
            for request in sql_requests.split(';'):
                if request != "":
                    try:
                        db_cursor.execute(request)
                    except ConnectionError:
                        print("Failed to execute request:", request)
            db_cursor.close()

    def create_user(self, username, password):
        '''Create a database user to ba able to login with roles'''

        print("i have to create a new database user and give privileges role")

    def record_user(self, username, nick_name, family_name):
        '''Record an entry inside Table Users'''

        print("i have to record this user inside users table")

    def exist_username(self, username):
        '''Return if record users.username for username exist'''

        db_cursor = self._connection.cursor()
        db_cursor.execute("SELECT id FROM users WHERE username='{}';".format(
            username))
        data = db_cursor.fetchall()
        exist = True if data else False
        db_cursor.close()
        return exist
