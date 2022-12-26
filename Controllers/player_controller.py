from Controllers.main_database import MainDatabase
from Models.player import Player


class PlayerController:

    def __init__(self, players: dict[Player]):
        """Constructor de PlyerController
        agr:
        players:(dict[Player]): dictionnaire des joueurs participants
        """
        self.players = players

    @staticmethod
    def sort_players_by_points(rating_table: dict):
        """Trier les joueurs d'une table d'évaluation par points."""
        return sorted(rating_table, key=rating_table.get, reverse=True)

    def show_player_from_id(self, player_id: str):
        """Recherche parmi les joueurs participants pour un identifiant unique donné."""
        for player in self.players:
            if player.id_number == int(player_id):
                return player

    def sort_players_by_rating(self):
        """Trie les joueurs selon leur classement."""
        return sorted(self.players, key=lambda item: item.rating)

    @staticmethod
    def players_already_playing(matches: list[tuple[Player]], id_player_1: str, id_player_2: str):
        """Recherche dans une liste de matchs un match déjà existant entre les deux joueurs donnés.
            Retourne:
            bool: joueurs deja jouer
        """

        player_1_vs_player_2 = (int(id_player_1), int(id_player_2))
        player_2_vs_player_1 = (int(id_player_2), int(id_player_1))
        return player_1_vs_player_2 in matches or player_2_vs_player_1 in matches

    def generate_first_round(self):
        """Génère le premier tour selon le système suisse.
            Retourne la liste[Match] : Liste des correspondances générées
        """
        sorted_players = self.sort_players_by_rating()

        return [(sorted_players[i], sorted_players[i + len(self.players) // 2]) for i in range(len(self.players) // 2)]

    @classmethod
    def generate_next_round(cls, rating_table: dict):
        matches = []

        sort_player = cls.sort_players_by_points(rating_table=rating_table)
        while len(sort_player) != 0:
            for opponent in range(1, len(sort_player)):
                id_player_1 = sort_player[0]
                id_player_2 = sort_player[opponent]

                player_1 = MainDatabase().util.get_player_by_id_string(player_id=id_player_1)
                player_2 = MainDatabase().util.get_player_by_id_string(player_id=id_player_2)

                if not cls.players_already_playing(matches=matches, id_player_1=id_player_1, id_player_2=id_player_2):

                    matches.append((player_1, player_2))
                    del sort_player[0]
                    del sort_player[opponent - 1]
                    break
        return matches
