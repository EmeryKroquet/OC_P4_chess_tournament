# OC_P4_chess_tournament

# OC Projet 4 Chess Tournament  Manager
## Comment préparer et installer l'environement du projet 
Chess tournament est une application pour le jeu d’echecs qui permet de gérer les appariement des joueurs dans un tournoi.
Ce projet est dévéloppé en suivant l’architecture MVC et POO (Programmation Orienté Objets) en langage python. 
En développant cette application nous avons suis installer des diffents packages pour le développement et le fonction de l’application en premier : 
La version de python utiliser est [Python 3.9](https://www.python.org/downloads/release/python-390)
### Pour l’installer ? 
Il faut en premier créer un environnement virtuel à l’aide [pyenv virtualenvironment](https://pypi.org/project/virtualenv-pyenv/):
Voilà la commande a suivre : 
Sur votre environnement système MacOs, appuyer sur ``` control + ` ``` , une petite fenêtre de recherche vous ouvres et taper “terminal” une fois dans le terminal entrer cette commande :
## Utilisation de pyenv pour installer python
Entrez cette commande en spécifiant la version de python utiliser dans ce projet sinon si vous disposez deja d’autres versions de python dans votre système, pyenv vous permet d’utiliser different version de python dans vos projets c’est des plus grands avantage d’utiliser pyenv : 
```sh 
$ pyenv install 3.9.5 
Si vous rencontrer de difficulter à installer voici une commande :
$brew install openssl readline sqlite3 xz zlib
````
Cette commande s'appuie sur Homebrew et installe les quelques dépendances pour les utilisateurs de macOS. 
Pour plus de lecture allez sur le site de  [Real Python](https://realpython.com/intro-to-pyenv/#specifying-your-python-version)

## Création de l’environnement virtual avec pyenv 
La création d'un environnement virtuel se fait en une seule commande :
dabord dans votre terminal créer un dossier OC_P4_Chess_Tournament à l’aide de commande : 
```sh 
$ mkdir OC_P4_Chess_Tournament
palcez-vous dans le dossier du projet en entrer cette commande : 
$ cd OC_P4_Chess_Tournament/  
````
dans le dossier du projet vous entrez la commande ci-dessous en spécifiant la version de python et nom de l’enviroonement :
```sh
$ pyenv virtualenv <python_version> <environment_name>
$ pyenv virtualenv 3.9.5 env
```
Maintenant vous activez l’environnement local avec la commande 
```
pyenv local env
```
Après  vous entrer cette commande en vous plaçant dans le dossier du projet : 
```
$ pyenv activate <environment_name>
Pour desactiver l’environement entrer ci-ci : 
$ pyenv deactivate
````
