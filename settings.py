'''Settings and  global variables file'''

import os

# -- m y S Q L   S E T T I N G S  --

GRANT_USER = 'root'
    # protect password by pass a environment OS variable
#GRANT_USER_PASSWD = os.getenv("HOME")
GRANT_USER_PASSWD = os.getenv("MARIA_ROOT_PASSWD")
print("get env ==>", GRANT_USER_PASSWD)
DB_PORT = 3306
DB_SOCKET = "/run/mysqld/mysqld.sock"
    # can be "socket" or "tcp"
DB_CONNECT_MODE = "TCP"
DB_HOSTNAME = "localhost"
DB_INIT_FILE = "assets/sql/request.sql"


# --  G L O B A L    V A R I A B L E S  --