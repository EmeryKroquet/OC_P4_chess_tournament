from tinydb import TinyDB


class Database:
    """Modèle pour base de données, encapsule un objet TinyDB et les objets créés.
    Attributs :
        place (str) : Le chemin local pour le fichier JSON de TinyDB.
        Players (dict) : Les objets Player créés à partir de la base de données.
        Tournois (dict) : Les objets tournois créés à partir de la base de données.
        Database (tinydb.database.TinyDB) : L'objet TinyDB créé à partir du fichier JSON.
    """

    def __init__(self, place: str):
        """Constructeur pour la base de données. Initie le chargement de TinyDB.
        Arguments :
            place (str) : Le chemin local pour le fichier JSON de TinyDB.
        """
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
        """Charge un objet TinyDB à partir d'un fichier JSON."""
        try:
            self.db = TinyDB(self.place, indent=2)
        except FileNotFoundError:
            self.create_empty_database()
            self.load_database()
