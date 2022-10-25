from Models.database.database import Database
from Models.tournament import Tournament


class MainController:

    def __init__(self, database: Database):
        """Constructor de Database."""
        self.database = database

    def if_tournament_id_in_database(self, tournament_id: int):
        if tournament_id in self.database.tournaments:
            return True
        else:
            return False

    def if_payer_id_in_database(self, player_id: int):
        if player_id in self.database.players:
            if self.database.players[player_id].delete_player:
                return False
            else:
                return True
        else:
            return False

    def if_tournament_in_database_empty(self):
        if len(self.database.tournaments) == 0:
            return True
        else:
            return False

    def if_player_in_database_empty(self):
        if len(self.database.players) == 0:
            return True
        else:
            return False

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
        player_ids = sorted(self.database.players, key=lambda x: x)
        list_of_players = []
        for id_number in player_ids:
            if self.database.players[id_number].delete_player:
                continue
            list_of_players.append(self.database.players[id_number])
        return list_of_players

    def get_payer_by_name(self, player_name: dict = None):
        if player_name is None:
            player_name = self.database.players
            print(player_name)
        sort_player = sorted(player_name, key=lambda x: player_name[x].last_name)

        list_of_players = []
        for id_number in sort_player:
            if self.database.players[id_number].delete_player:
                continue
            list_of_players.append(self.database.players[id_number])
        return list_of_players

    def get_players_by_rating(self, player_name: dict = None):
        if player_name is None:
            player_name = self.database.players
            sort_player = sorted(player_name, key=lambda x: player_name[x].rating, reverse=True)

            list_of_players = []
            for id_number in sort_player:
                if self.database.players[id_number].delete_player:
                    continue
                list_of_players.append(self.database.players[id_number])
            return list_of_players

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

    def get_player_by_id_string(self, player_id: str):
        for player in self.database.players:
            if str(player) == player_id:
                return self.database.players[player]

    def get_player_name_from_id(self, player_id: int):
        for player in self.database.players:
            if self.database.players[player].id_number == player_id:
                name = f"{self.database.players[player].first_name} {self.database.players[player].last_name}"
                return name

    def get_players_names(self, players_name: list):

        return [self.get_player_name_from_id(player_id=i) for i in players_name]

    def get_all_tournaments_existing(self):
        list_of_tournament = []
        for tournament_id in self.database.tournaments:
            list_of_tournament.append(self.database.tournaments[tournament_id])
        return list_of_tournament

    def get_tournament_in_progression(self):
        list_of_tournament = []
        for tournament in self.database.tournaments:
            if not self.database.tournaments[tournament].is_round_ended:
                list_of_tournament.append(self.database.tournaments[tournament])
        return list_of_tournament

    def get_formate_rating_table(self, rating_table: dict):
        rating_list = [(k, v) for k, v in sorted(rating_table.items(), key=lambda item: item[1], reverse=True)]
        format_rating_table = []

        for player in rating_list:
            format_rating_table.append((self.get_player_name_from_id(player_id=int(player[0])), player[1]))

        return format_rating_table

