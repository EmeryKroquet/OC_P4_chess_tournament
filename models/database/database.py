from tinydb import TinyDB


class Database:
    def __init__(self, place: str):
        self.place = place
        self.players = {}
        self.tournaments = {}

        self.db = None
        self.load_database()

    def create_empty_database(self):
        """Crée un fichier JSON de base de données vide si nécessaire."""
        with open(self.place, "w+") as f:
            f.write("{}")

    def load_database(self):
        """ Charger un objet dans un fichier """
        try:
            self.db = TinyDB(self.place)
        except FileNotFoundError:
            self.create_empty_database()
            self.load_database()

# f"{self.place}.json"
