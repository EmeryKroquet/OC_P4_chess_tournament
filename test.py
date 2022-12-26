from tinydb import TinyDB


class MainDatabase:

    def __init__(self):
        # self.database = TinyDB("db.json")
        # self.util = MainController(database=self.database)
        self.db = TinyDB("data/db.json", indent=2)

        self.match_table = None
        self.round_table = None
        self.tournament_table = None
        self.player_table = None

        self.load_database()

    def load_database(self):
        self.player_table = self.db.table("players")
        self.tournament_table = self.db.table("tournaments")
        self.round_table = self.db.table("rounds")
        self.match_table = self.db.table("matches")

        # self.load_players()
        # self.load_tournaments()
