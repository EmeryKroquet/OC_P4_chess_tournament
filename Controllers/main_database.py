import json

from tinydb import Query, table, TinyDB

from Models.match import Match
from Models.player import Player
from Models.round import Round
from Models.tournament import Tournament


class MainDatabase:

    def __init__(self):
        # self.database = Database("db")
        # self.util = MainController(database=self.database)

        self.db = TinyDB("db.json", indent=2)

        self.players = {}
        self.tournaments = {}

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

        self.load_players()
        self.load_tournaments()

    def load_players(self):
        for player in self.player_table:
            self.create_player(
                first_name=player["first name"],
                last_name=player["last name"],
                date_of_birth=player["date of birth"],
                gender=player["gender"],
                rating=player["rating"],
                id_number=player["id"],
                delete_player=player["deleted player"],
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
            id_number = self.found_next_id(self.player_table)
        player = Player(gender.upper(), first_name, last_name, rating,
                        date_of_birth, id_number, delete_player, )
        self.save_player(player=player, save_db=save_db)
        return id_number

    def save_player(self, player: Player, save_db: bool = False):
        """Sauvegarder un objet Player dans TinyDB."""
        self.players[player.id_number] = player

        if save_db:
            return
        query = Query()
        self.player_table.upsert(
            {
                "first name": player.first_name,
                "last name": player.last_name,
                "date of birth": player.date_of_birth,
                "gender": player.gender,
                "rating": int(player.rating),
                "id": int(player.id_number),
                "deleted player": player.delete_player,
            },
            query.id == int(player.id_number),
        )

    def delete_player(self, player: Player):
        player.delete_player = True
        self.save_player(player=player)

    def load_tournaments(self):
        """Utilise la table TinyDB “Tournois" pour créer des objets Joueur."""
        for tournament in self.tournament_table:
            self.create_tournament(
                name=tournament["name"],
                place=tournament["place"],
                date=tournament["date"],
                numbers_of_tours=tournament["number of tours"],
                time_control=tournament["time control"],
                description=tournament["description"],
                id_number=tournament["id"],
                is_round_ended=tournament["round ended"],
                players=tournament["players"],
                rating_table=tournament["rating table"],
                save_db=True
            )

    def get_tournaments_info(self):
        self.db = TinyDB("db.json")
        print(self.db)
        with open("db.json", "r") as file:
            data = json.load(file)
            print(data)

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
            id_number = self.found_next_id(self.tournament_table)

            # Créer la liste requise d'objets Player à partir des identifiants des joueurs.
        player_list = [self.players[player] for player in players]

        # Créer une table de classement vide si elle n'existe pas encore.
        if not rating_table:
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
        players_id = [player.id_number for player in tournament.players]

        self.tournament_table.upsert(
            {
                "name": tournament.name,
                "place": tournament.place,
                "date": tournament.date,
                "number of tours": int(tournament.numbers_of_tours),
                "time control": tournament.time_control,
                "description": tournament.description,
                "players": players_id,
                "rating table": tournament.rating_table,
                "round ended": tournament.is_round_ended,
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
        self.tournament_table.remove(query.id == int(tournament.id_number))
        del self.tournaments[int(tournament.id_number)]

    def load_rounds(self, tournament_id: int = None):
        for tour in self.round_table:
            if tour["tournament id"] != tournament_id:
                continue
            self.create_round(
                round_number=tour["round number"],
                tournament_id=tour["tournament id"],
                id_number=tour["id"],
                save_db=True
            )

    def create_round(self, round_number: int, tournament_id: int,
                     id_number: int = 0,
                     save_db: bool = False):

        if id_number == 0:
            id_number = self.found_next_id(self.round_table)
            created_round = Round(round_number=round_number, tournament_id=tournament_id, id_number=id_number)
            self.save_round(tour=created_round, save_db=save_db)
            return id_number

    def save_round(self, tour: Round, save_db: bool = False):
        self.tournaments[tour.tournament_id].tours[tour.id_number] = tour
        if save_db:
            return
        query = Query()
        self.round_table.upsert(
            {
                "round number": tour.round_number,
                "tournament id": int(tour.tournament_id),
                "id": int(tour.id_number),
            },
            query.id == int(tour.id_number)
        )

    def delete_round(self, tour: Round):
        for match in tour.matches:
            self.delete_match(match=tour.matches[match])
            query = Query()
            self.round_table.remove(query.id == int(tour.id_number))

    def load_matches(self, tournament_id: int):
        for match in self.match_table:
            if match["tournament ID"] != tournament_id:
                continue
            player_1 = self.players[match["player 1"]]
            player_2 = self.players[match["player 2"]]
            players = (player_1, player_2)

            self.create_match(
                players=players,
                tournament_id=match["tournament ID"],
                round_id=match["round ID"],
                winner=match["winner"],
                id_number=match["id"],
                save_db=True
            )

    def create_match(
            self, players: tuple, tournament_id: int,
            round_id: int, winner: int, id_number: int = 0,
            save_db: bool = False
    ):
        if id_number == 0:
            id_number = self.found_next_id(self.match_table)

            match = Match(
                players=players,
                tournament_id=tournament_id,
                round_id=round_id,
                player_winner=winner,
                id_number=id_number
            )

            self.save_match(match=match, save_db=save_db)

    def save_match(self, match: Match, save_db: bool = False):
        self.tournaments[match.tournament_id].tours[match.round_id].matches[match.id_number] = match
        if save_db:
            return
        query = Query()
        self.match_table.upsert(
            {
                "player 1": match.player_1.id_number,
                "player 2": match.player_2.id_number,
                "winner": match.player_winner,
                "tournament ID": int(match.tournament_id),
                "round ID": int(match.round_id),
                "id": int(match.id_number),
            },
            query.id == int(match.id_number)
        )

    def delete_match(self, match: Match):
        query = Query()
        self.match_table.remove(query.id == int(match.id_number))

    def update_table_rating(self, tournament_id: int, player_id: int, winner_point: float):
        tournament = self.tournaments[tournament_id]
        tournament.rating_table[str(player_id)] += winner_point
        self.save_tournament(tournament=tournament)

    def found_tournament_in_progression(self):
        query = Query()
        return self.tournament_table.search(query["Est Terminé"] is False)

    @staticmethod
    def found_next_id(table_: table.Table):
        if len(table_) == 0:
            return 1
        query = Query()
        next_ = 1
        while len(table_.search(query.id >= next_)) > 0:
            next_ += 1
        return next_
