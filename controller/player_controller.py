from models.player import Player
from models.match import Match
from controller.main_database import MainDatabase


class PlayerController:
    """Génère des rondes et leurs correspondances.
        joueur (dict[Joueur]) : Dict des joueurs participants.
    """

    def __init__(self, players: dict[Player]):
        """Constructor pour PlayerController.
            players (dict[Player]): Dict pour le participant players.
        """
        self.players = players

    def sort_player_by_rating(self):
        """Trie les joueurs selon leur classement.
            liste[Joueur] : Liste des joueurs classés par leur classement (croissant).
        """
        return sorted(self.players, key=lambda x: x.rating)

    @classmethod
    def sort_player_by_points(cls, rating_table: dict):
        """Trier les joueurs d'une table d'évaluation par points.
            rating_table (dict) : Dict des joueurs à trier.
            list[Player] : Liste des joueurs classés par points (en ordre décroissant).
        """

        return sorted(rating_table, key=rating_table.get, reverse=True)

    def show_player_from_id(self, player_id: str):
        """Recherche parmi les joueurs participants pour un identifiant unique donné.
            player_id (str) : L'identifiant unique du joueur à rechercher.
            Player : Objet joueur correspondant.
        """
        for player in self.players:
            if player.id_number == int(player_id):
                return player

    @classmethod
    def players_already_involved(cls, matches: list[tuple[Player]], id_1: str, id_2: str):
        """Recherche dans une liste de matchs un match déjà existant entre les deux joueurs donnés.
            matches (liste [tuple [Player]]) : Liste d'appariements de joueurs, correspondant à des matchs passés.
            id_1 (str) : Identifiant unique du premier joueur.
            id_2 (str) : Identifiant unique du deuxième joueur.
            bool : Les joueurs se sont déjà rencontrés.
        """
        player_1_vs_player_2 = (int(id_1), int(id_2))
        player_2_vs_player_1 = (int(id_2), int(id_1))
        return player_1_vs_player_2 in matches or player_2_vs_player_1 in matches

    def generate_first_round(self):
        """Génère le premier tour selon le système suisse.
            list[Match] : Liste des correspondances générées.
        """
        sorted_players = self.sort_player_by_rating()
        return [(sorted_players[i], sorted_players[i + len(self.players) // 2]) for i in range(len(self.players) // 2)]

    @classmethod
    def generate_next_round(cls, rating_table: dict):
        """Génère un tour, autre que le premier, selon le système suisse.
            list [Match] : Liste des matchs générés.
        """
        matches = []
        sorted_players = cls.sort_player_by_points(rating_table=rating_table)

        while len(sorted_players) != 0:
            for opponent in range(1, len(sorted_players)):
                id_player_1 = sorted_players[0]
                id_player_2 = sorted_players[opponent]

                player_1 = MainDatabase().util.get_player_object_from_id_str(player_id=id_player_1)
                player_2 = MainDatabase().util.get_player_object_from_id_str(player_id=id_player_2)

                if not cls.players_already_involved(matches=matches, id_1=id_player_1, id_2=id_player_2):
                    matches.append((player_1, player_2))
                    del sorted_players[0]
                    del sorted_players[opponent - 1]
                    break
        return matches
