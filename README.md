# OC-openFoodFacts
Utilisez les données publiques de l'OpenFoodFacts

## Backlog

1. install environment
    1. libraries: PyQt5 & mysql & requests (std libs: os & sys)
    1. install, config and create database with MySQL (MariaDB)
    1. add database config access file and auto-generate database tables at first start
    1. create tables and relations: [users, substitutes, shops, substitute_shops]

1. create appllication UI design with QtDesigner
    1. Main window (look at model screenshot)
        1. a search group box mode with 2 alternates toggles buttons on "list OpenFoodFacts" or "List local"
        1. user box
            1. button signin (call signin dialog box), appears when no user connected
            1. button signup (call signup dialog box), appears when no user connected
            1. disconnect button (disconnect user), appear when user is connect
        1. List selected categories (send request for populate foods list)
        1. List selected foods (send a request to populate food substitution)
        1. Widget view of food substitution (name, description, shops list)
    1. Dialog boxes
        1. signup
        1. signin
        1. record local DB state (failed or success)
        1. user auhtentification failed

1. Source code (use of Qt5 slots mecanism)
    1. Embed ui design to python code
        1. create QApplication mainwondow
        1. import ui
    1. create links for dialog boxes call
    1. create links to buttons to actions
    1. signin code
    1. signup code
    1. disconnect code
    1. openfoodfacts mode (from http request to OpenFoodFacts JSON API access)
        1. populate categories QList view
        1. populate foods list view on selected category from list category
        1. populate food sustitution view from food selection
    1. local mode (from local database)
        1. populate categories QList view
        1. populate foods list view on selected category from list category
        1. populate food sustitution view from food selection
        
## Todo list tasks

## Running tasks

## task done
