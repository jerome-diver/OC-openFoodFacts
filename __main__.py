'''Main program for openFoodFacts substitution search food'''

from controller import Controller, Authentication

if __name__ == "__main__":
    GENERAL_CONTROLLER = Controller()
    AUTHENTICATION = Authentication(GENERAL_CONTROLLER)
