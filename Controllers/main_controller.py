import json

from tinydb import TinyDB

from Controllers.main_database import MainDatabase

from Models.tournament import Tournament


class MainController:

    def __init__(self, database: MainDatabase):
        """Constructor de Database."""
        self.database = database

    def if_tournament_id_in_database(self, tournament_id: int):
        """Vérifie si l'identifiant d'un tournoi donné existe dans la base de données."""

        """retourne : bool: tournament id in database"""
        return tournament_id in self.database.tournaments

    def if_payer_id_in_database(self, player_id: int):
        if player_id in self.database.players:
            return not self.database.players[player_id].delete_player
        else:
            return False

    def if_tournament_in_database_empty(self):
        return len(self.database.tournaments) == 0

    def if_player_in_database_empty(self):
        return len(self.database.players) == 0

    @staticmethod
    def get_all_matches(tournament: Tournament):
        list_of_match = []

        for round_id in tournament.tours:
            for match_id in tournament.tours[round_id].matches:
                player_1 = tournament.tours[round_id].matches[match_id].player_1
                player_2 = tournament.tours[round_id].matches[match_id].player_2
                list_of_match.append((player_1.id_number, player_2.id_number))
                return list_of_match

    def get_players_by_id(self):
        print(self.database.__dict__)
        player_ids = sorted(self.database.players, key=lambda x: x)
        return [self.database.players[id_number] for id_number in player_ids if
                not self.database.players[id_number].delete_player]

    def get_payer_by_name(self, player_name: dict = None):
        if player_name is None:
            player_name = self.database.players
            print(player_name)
        sort_player = sorted(player_name, key=lambda x: player_name[x].last_name)

        return [self.database.players[id_number] for id_number in sort_player if
                not self.database.players[id_number].delete_player]

    def get_players_by_rating(self, player_name: dict = None):
        if player_name is None:
            player_name = self.database.players
            sort_player = sorted(player_name, key=lambda x: player_name[x].rating, reverse=True)

            return [self.database.players[id_number] for id_number in sort_player if
                    not self.database.players[id_number].delete_player]

    def get_tournament_by_id(self):
        sort_player = sorted(self.database.tournaments, key=lambda x: x)
        list_of_tournament = []
        for id_number in sort_player:
            list_of_tournament.append(self.database.tournaments[id_number])
            return list_of_tournament

    def get_tournament_by_id_string(self, tournament_id: str):
        for tournament in self.database.tournaments:
            if str(tournament) == tournament_id:
                return self.database.tournaments[tournament]

    def get_tournaments_info(self):
        db = TinyDB("db.json")
        print(db)
        with open("db.json", "r") as file:
            data = json.load(file)
            print(data)

    def get_player_by_id_string(self, player_id: str):
        for player in self.database.players:
            if str(player) == player_id:
                return self.database.players[player]

    def get_player_name_from_id(self, player_id: int):
        for player in self.database.players:
            if self.database.players[player].id_number == player_id:
                return f"{self.database.players[player].first_name} {self.database.players[player].last_name}"

    def get_players_names(self, players_name: list):

        return [self.get_player_name_from_id(player_id=i) for i in players_name]

    def get_all_tournaments_existing(self):
        return [self.database.tournaments[tournament_id] for tournament_id in self.database.tournaments]

    def get_tournament_in_progression(self):
        return [self.database.tournaments[tournament_id] for tournament_id in self.database.tournaments
                if not self.database.tournaments[tournament_id].is_round_ended]

    def get_formate_rating_table(self, rating_table: dict):
        rating_list = list(sorted(rating_table.items(), key=lambda item: item[1], reverse=True))

        return [(self.get_player_name_from_id(player_id=int(player[0])), player[1]) for player in rating_list]
