'''Settings and  global variables file'''

import os

CWD = os.path.dirname(os.path.abspath(__file__))

# -- m y S Q L   S E T T I N G S  --

GRANT_USER = os.getenv("MARIA_GRANT_OFF_USER")
    # protect password by pass a environment OS variable
#GRANT_USER_PASSWD = os.getenv("HOME")
GRANT_USER_PASSWD = os.getenv("MARIA_GRANT_OFF_PASSWD")
DB_PORT = 3306
MARIA_RUN_DIR = os.path.dirname("/run/mysqld/")
DB_SOCKET = os.path.join(MARIA_RUN_DIR, "mysqld.sock")
    # can be "socket" or "tcp"
DB_CONNECT_MODE = "TCP"
DB_HOSTNAME = "localhost"
DB_INIT_FILE = os.path.join(CWD, "assets/sql/request.sql")

# --  G L O B A L    V A R I A B L E S  --

NUTRISCORE_A = os.path.join(CWD, "assets/images/nutriscore A.png")
NUTRISCORE_B = os.path.join(CWD, "assets/images/nutriscore B.png")
NUTRISCORE_C = os.path.join(CWD, "assets/images/nutriscore C.png")
NUTRISCORE_D = os.path.join(CWD, "assets/images/nutriscore D.png")
NUTRISCORE_E = os.path.join(CWD, "assets/images/nutriscore E.png")

REQUEST_PAGE_SIZE = 20
