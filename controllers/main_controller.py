from tinydb import Query, table

from models.database.main_database import MainDatabase
from models.database.database import Database
from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MainController(metaclass=SingletonMeta):

    def __init__(self):
        self.database = Database("db")
        self.util = MainDatabase(database=self.database)

        self.matches_table = None
        self.rounds_table = None
        self.players_table = None
        self.tournaments_table = None
        self.load_database()

    def load_database(self):
        """Instancie les différentes tables dans les attributs et charge leur contenu
            en créant les objets correspondants.
            """
        self.players_table = self.database.db.table("Players")
        self.tournaments_table = self.database.db.table("Tournaments")
        self.rounds_table = self.database.db.table("Rounds")
        self.matches_table = self.database.db.table("Matches")

        self.load_players()
        self.load_tournaments()

    def load_players(self):
        """Utilise la table TinyDB "Players" pour créer des objets Player."""
        for player in self.players_table:
            self.create_player(
                first_name=player["First Name"],
                last_name=player["Last Name"],
                date_of_birth=player["Date of Birth"],
                gender=player["Gender"],
                rating=player["Rating"],
                id_number=player["id"],
                delete_player=player["Deleted Player"],
                save_db=True,
            )

    def create_player(
            self,
            first_name: str,
            last_name: str,
            date_of_birth: str,
            gender: str,
            rating: int,
            id_number: int = 0,
            delete_player: bool = False,
            save_db: bool = False,
    ):
        if id_number == 0:
            id_number = self.found_next_id(self.players_table)
        player = Player(gender.upper(), first_name.capitalize(), last_name.capitalize(), rating,
                        date_of_birth, id_number, delete_player,)
        self.save_player(player=player, save_db=save_db)
        return id_number

    def save_player(self, player: Player, save_db: bool = False):
        """Sauvegarder un objet Player dans TinyDB."""
        self.database.players[player.id_number] = player

        if save_db:
            return
        query = Query()
        self.players_table.upsert(
            {
                "First Name": player.first_name,
                "Last Name": player.last_name,
                "Date of Birth": player.date_of_birth,
                "Gender": player.gender,
                "Rating": int(player.rating),
                "id": int(player.id_number),
                "Deleted Player": player.delete_player,
            },
            query.id == int(player.id_number),
        )

    def delete_player(self, player: Player):
        player.delete_player = True
        self.save_player(player=player)

    def load_tournaments(self):
        """Utilise la table TinyDB “Tournois" pour créer des objets Joueur."""
        for tournament in self.tournaments_table:
            self.create_tournament(
                name=tournament["Name"],
                place=tournament["Place"],
                date=tournament["Date"],
                numbers_of_tours=tournament["Number of Tours"],
                time_control=tournament["Time Control"],
                description=tournament["Description"],
                id_number=tournament["id"],
                is_round_ended=tournament["Round ended"],
                players=tournament["Players"],
                rating_table=tournament["Rating table"],
                save_db=True
            )

    def create_tournament(
            self,
            name: str,
            place: str,
            date: str,
            numbers_of_tours: int,
            time_control: str,
            description: str,
            players: list[int],
            rating_table: dict,
            id_number: int = 0,
            is_round_ended: bool = False,
            save_db: bool = False
    ):

        if id_number == 0:
            id_number = self.found_next_id(self.tournaments_table)
            # Créer la liste requise d'objets Player à partir des identifiants des joueurs.
        player_list = []

        for player in players:
            player_list.append(self.database.players[player])
        # Créer une table de classement vide si elle n'existe pas encore.
        if len(rating_table) == 0:
            for player in players:
                rating_table[str(player)] = 0

        tournament = Tournament(
            name=name,
            place=place,
            date=date,
            numbers_of_tours=numbers_of_tours,
            time_control=time_control,
            description=description,
            id_number=id_number,
            is_round_ended=is_round_ended,
            players=player_list,
            rating_table=rating_table
        )

        self.save_tournament(tournament=tournament, save_db=save_db)
        return id_number

    def save_tournament(self, tournament: Tournament, save_db: bool = False):
        if save_db:
            return
        query = Query()
        players_id = []

        for player in tournament.players:
            players_id.append(player.id_number)

        self.tournaments_table.upsert(
            {
                "Name": tournament.name,
                "Place": tournament.place,
                "Date": tournament.date,
                "Number of Tours": int(tournament.numbers_of_tours),
                "Time Control": tournament.time_control,
                "Description": tournament.description,
                "Players": players_id,
                "Rating table": tournament.rating_table,
                "Round ended": tournament.is_round_ended,
                "id": int(tournament.id_number),
            },
            query.id == int(tournament.id_number)
        )

    def delete_tournament(self, tournament: Tournament):
        self.load_rounds(tournament_id=tournament.id_number)
        self.load_matches(tournament_id=tournament.id_number)

        for tour in tournament.tours:
            self.delete_round(tour=tournament.tours[tour])

        query = Query()
        self.tournaments_table.remove(query.id == int(tournament.id_number))
        del self.database.tournaments[int(tournament.id_number)]

    def load_rounds(self, tournament_id: int = None):
        for tour in self.rounds_table:
            if tour["Tournament id"] != tournament_id:
                continue
            self.create_round(
                round_number=tour["Round number"],
                tournament_id=tour["Tournament id"],
                id_number=tour["id"],
                save_db=True
            )

    def create_round(self, round_number: int, tournament_id: int,
                     id_number: int = 0,
                     save_db: bool = False):

        if id_number == 0:
            id_number = self.found_next_id(self.rounds_table)
            created_round = Round(round_number=round_number, tournament_id=tournament_id, id_number=id_number)
            self.save_round(tour=created_round, save_db=save_db)
            return id_number

    def save_round(self, tour: Round, save_db: bool = False):
        self.database.tournaments[tour.tournament_id].tours[tour.id_number] = tour
        if save_db:
            return
        query = Query()
        self.rounds_table.upsert(
            {
                "Round number": tour.round_number,
                "Tournament id": int(tour.tournament_id),
                "id": int(tour.id_number),
            },
            query.id == int(tour.id_number)
        )

    def delete_round(self, tour: Round):
        for match in tour.matches:
            self.delete_match(match=tour.matches[match])
            query = Query()
            self.rounds_table.remove(query.id == int(tour.id_number))

    def load_matches(self, tournament_id: int):
        for match in self.matches_table:
            if match["Tournament ID"] != tournament_id:
                continue
            player_1 = self.database.players[match["Player 1"]]
            player_2 = self.database.players[match["Player 2"]]
            players = (player_1, player_2)

            self.create_match(
                players=players,
                tournament_id=match["Tournament ID"],
                round_id=match["Round ID"],
                winner=match["Winner"],
                id_number=match["id"],
                save_db=True
            )

    def create_match(
            self, players: tuple, tournament_id: int,
            round_id: int, winner: int, id_number: int = 0,
            save_db: bool = False
    ):
        if id_number == 0:
            id_number = self.found_next_id(self.matches_table)

            match = Match(
                players=players,
                tournament_id=tournament_id,
                round_id=round_id,
                player_winner=winner,
                id_number=id_number
            )

            self.save_match(match=match, save_db=save_db)

    def save_match(self, match: Match, save_db: bool = False):
        self.database.tournaments[match.tournament_id].tours[match.round_id].matches[match.id_number] = match
        if save_db:
            return
        query = Query()
        self.matches_table.upsert(
            {
                "Player 1": match.player_1.id_number,
                "Player 2": match.player_2.id_number,
                "Winner": match.player_winner,
                "Tournament ID": int(match.tournament_id),
                "Round ID": int(match.round_id),
                "id": int(match.id_number),
            },
            query.id == int(match.id_number)
        )

    def delete_match(self, match: Match):
        query = Query()
        self.matches_table.remove(query.id == int(match.id_number))

    @staticmethod
    def found_next_id(table_: table.Table):
        if len(table_) == 0:
            return 1
        query = Query()
        next_ = 1
        while len(table_.search(query.id >= next_)) > 0:
            next_ += 1
        return next_

    def update_rating(self, tournament_id: int, player_id: int, winner_point: float):
        tournament = self.database.tournaments[tournament_id]
        tournament.rating_table[str(player_id)] += winner_point
        self.save_tournament(tournament=tournament)

    def found_tournament_in_progress(self):
        query = Query()
        result = self.tournaments_table.search(query["Est Terminé"] is False)
        return result
