'''Main program for openFoodFacts substitution search food'''

from controller import Controller, Authentication

if __name__ == "__main__":
    APPLICATION = Controller()
    AUTHENTICATION = Authentication(APPLICATION)
