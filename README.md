# OC Projet 4 Chess Tournament  Manager

## Comment préparer et installer l'environement du projet 
Chess tournament est une application pour le jeu d’echecs qui permet de gérer l'appariement des joueurs dans un tournoi.
Ce projet est développé en suivant l’architecture MVC et POO (Programmation Orientés Objets) en langage python. 
En développant cette application nous avons suis installer des differents packages pour le développement et le fonction de l’application en premier : 
La version de python utiliser est [Python 3.9](https://www.python.org/downloads/release/python-390)
```sh 
Merci de noté que ce programme marche unique sur le système Macos !
```
### Pour l’installer ? 
Il faut en premier créer un environnement virtuel à l’aide [pyenv virtualenvironment](https://pypi.org/project/virtualenv-pyenv/):
Voilà la commande à suivre : 
Sur votre environnement système MacOs, appuyer sur ``` control + ` ``` , une petite fenêtre de recherche vous ouvres et taper “terminal” une fois dans le terminal entrer cette commande :
## Utilisation de pyenv pour installer python
Entrez cette commande en spécifiant la version de python utiliser dans ce projet sinon si vous disposez deja d’autres versions de python dans votre système, pyenv vous permet d’utiliser different version de python dans vos projets c’est des plus grands avantage d’utiliser pyenv : 
```sh 
$ pyenv install 3.9.5 
```
Si vous rencontrez des difficultés à installer voici une commande :

```
$brew install openssl readline sqlite3 xz zlib
````
Cette commande s'appuie sur Homebrew et installe les quelques dépendances pour les utilisateurs de macOS. 
Pour plus de lecture allez sur le site de [Real Python](https://realpython.com/intro-to-pyenv/#specifying-your-python-version)

## Création de l’environnement virtual avec pyenv 
La création d'un environnement virtuel se fait en une seule commande :
dabord dans votre terminal créer un dossier OC_P4_Chess_Tournament à l’aide de commande : 
```sh 
$ mkdir OC_P4_Chess_Tournament
```
Placez-vous dans le dossier du projet en entrer cette commande :
```
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
Après vous entrer cette commande en vous plaçant dans le dossier du projet : 

```
$ pyenv activate <environment_name>
````

Pour desactiver l’environement entrer ci-ci : 

```
$ pyenv deactivate
````
## Les pré requis avant l’utilisation du programme 
D’abord vous cloner l’application en local sur votre machine. Pour ce faire, suivez ces étapes suivants:
sur votre machine créer un dossier OC_P4_Chess_Tournament avec la commande : 
```sh 
$ mkdir OC_P4_Chess_Tournament
````
```
$ cd OC_P4_Chess_Tournament 
```
 entrer dans votre terminal ces commandes : 
 ``` 
git clone https://github.com/EmeryKroquet/OC_P4_chess_tournament.git
````

Installer TinyDB pour la gestion simple de base de données à l’aide commande : 

```
$ pip install tinydb 
```
Installer requirements.tx à l’aide de commande : 

```
$ pip install -r requirements.txt 
```
De cette façon, vous installerez tous les paquets nécessaires à l'exécution de ce programme.

Comment exécuter ce programme ?
Pour exécuter ce programme  dans votre terminal taper :
```
python main.py
```
## Comment utiliser ce programme ?
Le menu principale se présente de cette façon : 
```
1. Gérer les Tournois
2. Gérer les joueurs
3. Générer des rapports

0. Quitter

```
La première chose que vous devriez faire ; 
entre 1 vous affiche le menu du tournament qui se présente comme suit : 

```
1.Rependre un tournoi
2.Créer un nouveau tournoi
3.Modifier un tournoi
4.Supprimer un tournoi
5.Afficher tous les tournois

0.Retour au menu
```
Si vous entrez 2 dans le menu principal il vous affiche le menu des joueurs et il se présente comme suit : 
```
1. Créer un nouveau joueur
2. Modifier un joueur
3. Supprimer un joueur
4. Afficher tous les joueurs

0. Retour au menu
```
Ensuite si vous entrez 3 il vous affiche le menu des rapports et il se présente comme suit :
```
1 Rapport des Joueurs
2 Rapport des Tournois
0 Retour 
```
En entrant 1 dans le menu des rapports il vous affiches le 
```
1 Rapport par Nom 
2 Rapports par Classement
0 Retour
```
## Comment jouer le jeu ? 

## Comment générer des rapports avec flak8-html ?
