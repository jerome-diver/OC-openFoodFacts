# OC-openFoodFacts
Utilisez les données publiques de l'OpenFoodFacts

![OpenFoodFacts + OC](assets/images/openfoodfacts+oc.png)

## Trello board
I use [Trello board](https://trello.com/b/2EKEGLIA/oc-python-projet-5-openfoodfacts) to manage agile Doc Driven Development technic

## OpenClassRooms Python Path
This is an OpenClassRooms [Python Path project number 5](https://openclassrooms.com/fr/projects/157/assignment)

## Langage used
Python-3

## Database used
I'm sorry, i had to use MySQL or MariaDB...
So you should install this database server and why not create a 
dedicated admin user for the application ?
database name will be "openfoodfacts_substitutes"

## Libraries dependancies
- PyQt5
- pymysql
- os
- sys
- [openfoodfacts](https://github.com/openfoodfacts/openfoodfacts-python)

look at requirements.tx file, i used virtualenv to install virtual python-3 environment

## How to install

- clone the project
- move inside the project directory
- install required libraries
- create an environment variable for GRANT admin user of MariaDB named 
MARIA_GRANT_OFF_USER
- create an environment variable for GRANT MariaDB user password named 
GRANT_MARIADB_OFF_PASSWD
```bash
git clone https://github.com/jerome-diver/OC-openFoodFacts
cd OC-openFoodFacts
pip install -r requirements.txt
export GRANT_MARIADB_OFF_USER="my_admin"
export GRANT_MARIADB_OFF_PASSWD="my_admin_passord"
```
(a good idea is to export theses variables inside your shell user source 
script: ~/.bashrc or ~/.zshrc or whatever you use to be able to no have to 
do that each time you want to start the application)
```bash
vim ~/.zshrc
[G o]
export GRANT_MARIADB_OFF_USER="my_admin"
export GRANT_MARIADB_OFF_PASSWD="my_admin_passord"
[ESC :wq]
```
(and an other one good idea is to install and run this application from a 
virtual environment, but you should know already to do that...)

## RUN
move back to the directory of the project and start:
```bash
cd ..
python OC-openFoodFacts
```

