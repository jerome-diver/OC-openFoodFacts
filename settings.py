'''Settings and  global variables file'''

# -- m y S Q L   S E T T I N G S  --

GRANT_USER = 'root'
    # protect password by pass a environment OS variable
GRANT_USER_PASSWD = "overaquaworks@2"
DB_PORT = 3306
DB_SOCKET = ""
    # can be "socket" or "tcp"
DB_CONNECT_MODE = "tcp"
DB_HOSTNAME = "localhost"
DB_INIT_FILE = "assets/sql/request.sql"


# --  G L O B A L    V A R I A B L E S  --