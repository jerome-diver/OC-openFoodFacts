'''User model exist after authentication
it empty if not'''

import pymysql


class User():
    
    def __init__(self, family, nick, username):
        self._family = family
        self._nick = nick
        self._username = username
        self.substitutes_selections = []

