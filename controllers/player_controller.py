from models.database.main_database import MainController
from models.player import Player


class PlayerController:
    """Génère des rondes et leurs correspondances.
        Attributs :
            joueur (dict[Joueur]) : Dict des joueurs participants.
        """
    def __init__(self, players: dict[Player]):
        """Constructeur pour TournamentGenerator.
                Arguments :
                    joueurs (dict[Player]) : Dict des joueurs participants.
                """
        self.players = players

    def sort_by_rating(self):
        """Trie les joueurs selon leur classement.
                Retourne :
                    liste[Joueur] : Liste des joueurs classés par leur classement (croissant).
                """
        return sorted(self.players, key=lambda item: item.rating)

    @classmethod
    def sort_by_points(cls, rating_table: dict):
        """Trier les joueurs d'une table d'évaluation par points."""
        return sorted(rating_table, key=rating_table.get, reverse=True)

    def show_player_from_id(self, player_id: str):
        """Recherche parmi les joueurs participants pour un identifiant unique donné."""
        for player in self.players:
            if player.id_number == int(player_id):
                return player

    @classmethod
    def players_already_play(cls, matches: list[tuple[Player]], id_player1: str, id_player2: str):
        """Recherche dans une liste de matchs un match déjà existant entre les deux joueurs donnés."""
        player_1_vs_player_2 = (int(id_player1), int(id_player2))
        player_2_vs_player_1 = (int(id_player2), int(id_player1))

        if player_1_vs_player_2 in matches:
            return True
        elif player_2_vs_player_1 in matches:
            return True
        else:
            return False

    def generate_first_round(self):
        """Génère le premier tour selon le système suisse.
            Retourne la liste[Match] : Liste des correspondances générées
        """
        matches = []
        sorted_players = self.sort_by_rating()

        for i in range(0, int(len(self.players) / 2)):
            matches.append((sorted_players[i], sorted_players[i + int(len(self.players) / 2)]))
        return matches

    @classmethod
    def generate_next_round(cls, rating_table: dict):
        """Génère un tour, autre que le premier, selon le système suisse.
                Args :
                    matches (liste [Match]) : Liste des matchs passés.
                    Rating_table (dict) : Tableau des leaders actuel.
                Retourne :
                    list[Match] : Liste des matchs générés.
        """
        matches = []
        sorted_players = cls.sort_by_points(rating_table=rating_table)
        while len(sorted_players) != 0:
            for opponent in range(1, len(sorted_players)):
                id_player1 = sorted_players[0]
                id_player2 = sorted_players[opponent]

                player_1 = MainController().util.get_player_from_id_str(player_id=id_player1)
                player_2 = MainController().util.get_player_from_id_str(player_id=id_player2)

                if not cls.players_already_play(matches=matches, id_player1=id_player1, id_player2=id_player2):
                    matches.append((player_1, player_2))
                    del sorted_players[0]
                    del sorted_players[opponent - 1]
                    break

        return matches
