# from tinydb import TinyDB, Query
# import json
#
# from Controllers.main_database import MainDatabase
#
# # db = TinyDB("db.json")
#
#
# class Database(MainDatabase):
#
#     def __init__(self, place: str):
#         """ constructor de Database. Initialise the database TinyDB
#             place (str): fichier JSON local pour TinyDB
#         """
#         super().__init__()
#         self.place = place
#         self.players = {}
#         self.tournaments = {}
#
#         self.db = None
#         self.load_database()
#
#     # @staticmethod
#     def get_database_info(self):
#         """Retourne la base de données sous forme de dictionnaire"""
#         self.db = TinyDB("db.json")
#         print(self.db)
#         print(self.db.all())
#         with open("db.json", "r") as file:
#             data = json.load(file)
#             print(data)
#         return data
#
#     def create_empty_database(self):
#         """Crée un fichier db de base de données vide si nécessaire."""
#
#         with open(self.place, "w+") as f:
#             f.write("\n")
#
#     def load_database(self):
#         """ Charger un objet dans un fichier json."""
#
#         try:
#             self.db = TinyDB(f"{self.place}.json", indent=4)
#         except FileNotFoundError:
#             self.create_empty_database()
#             self.load_database()
#             # self.get_database_info()
