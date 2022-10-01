from tinydb import TinyDB


class Database:
    def __init__(self, place: str):
        self.place = place
        self.players = {}
        self.tournaments = {}

        self.db = None
        self.load_database()

    def create_empty_database(self):
        """Creates an empty database JSON file if needed."""

        with open(self.place, "w+") as f:
            f.write("{}")

    def load_database(self):
        """ Charger un objet dans un fichier JSON """

        try:
            self.db = TinyDB(f"{self.place}.json")
        except FileNotFoundError:
            self.create_empty_database()
            self.load_database()

# f"{self.place}.json"
