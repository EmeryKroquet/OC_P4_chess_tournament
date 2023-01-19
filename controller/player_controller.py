from models.player import Player
from models.match import Match
from controller.main_database import MainDatabase


class PlayerController:
    """Génère des rondes et leurs correspondances.
    Attributs :
        joueur (dict[Joueur]) : Dict des joueurs participants.
    """

    def __init__(self, players: dict[Player]):
        """Constructor for PlayerController.

        Args:
            players (dict[Player]): Dict of participating players.
        """

        self.players = players

    def sort_by_rating(self):
        """Trie les joueurs selon leur classement.
        Retourne :
            liste[Joueur] : Liste des joueurs classés par leur classement (croissant).
        """
        return sorted(self.players, key=lambda x: x.rating)

    @classmethod
    def sort_by_points(cls, rating_table: dict):
        """Sort players from a rating_table by points.

        Args:
            rating_table (dict): Dict of players to be sorted.

        Returns:
            list[Player]: List of players ordered by points (descending).
        """

        return sorted(rating_table, key=rating_table.get, reverse=True)

    def show_player_from_id(self, player_id: str):
        """Searches through participating players for given unique id.

        Args:
            player_id (str): Player's unique id to be searched.

        Returns:
            Player: Corresponding Player object.
        """

        for player in self.players:
            if player.id_number == int(player_id):
                return player

    @classmethod
    def players_have_already_met(cls, matches: list[tuple[Player]], id_1: str, id_2: str):
        """Searches through a list of matches for an already existing match between the two given players.

        Args:
            matches (list[tuple[Player]]): List of players pairing, corresponding to past matches.
            id_1 (str): First player unique id.
            id_2 (str): Second player unique id.

        Returns:
            bool: Players have already met.
        """

        player_1_vs_player_2 = (int(id_1), int(id_2))
        player_2_vs_player_1 = (int(id_2), int(id_1))
        return player_1_vs_player_2 in matches or player_2_vs_player_1 in matches

    def generate_first_round(self):
        """Generates the first round following Swiss-system.

        Returns:
            list[Match]: List of generated matches.
        """

        sorted_players = self.sort_by_rating()

        return [(sorted_players[i], sorted_players[i + len(self.players) // 2]) for i in range(len(self.players) // 2)]

    @classmethod
    def generate_other_round(cls, rating_table: dict):
        """Génère un tour, autre que le premier, selon le système suisse.
        Args :
            rating_table:
        Retourne :
            list[Match] : Liste des matchs générés.
        """
        matches = []
        sorted_players = cls.sort_by_points(rating_table=rating_table)

        while len(sorted_players) != 0:
            for opponent in range(1, len(sorted_players)):
                id_1 = sorted_players[0]
                id_2 = sorted_players[opponent]

                player_1 = MainDatabase().util.get_player_object_from_id_str(player_id=id_1)
                player_2 = MainDatabase().util.get_player_object_from_id_str(player_id=id_2)

                if not cls.players_have_already_met(matches=matches, id_1=id_1, id_2=id_2):
                    matches.append((player_1, player_2))
                    del sorted_players[0]
                    del sorted_players[opponent - 1]
                    break

        return matches
