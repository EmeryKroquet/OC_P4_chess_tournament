import typer

from Models.database.main_database import MainDatabase
from Models.player import Player
import tools.tools as _TOOLS


class PlayerController:

    def __init__(self, players: dict[Player]):
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
        """Recherche dans une liste de matchs un match déjà existant entre les deux joueurs donnés."""
        player_1_vs_player_2 = (int(id_player_1), int(id_player_2))
        player_2_vs_player_1 = (int(id_player_2), int(id_player_1))

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
        sorted_players = self.sort_players_by_rating()

        for i in range(0, int(len(self.players) / 2)):
            matches.append((sorted_players[i], sorted_players[i + int(len(self.players) / 2)]))
        return matches

    @classmethod
    def generate_next_round(cls, rating_table: dict):
        list_of_matches = []

        sort_player = cls.sort_players_by_points(rating_table=rating_table)
        while len(sort_player) != 0:
            for opponent in range(1, len(sort_player)):
                player_1 = sort_player[0]
                player_2 = sort_player[opponent]

                player_1 = MainDatabase().util.get_player_by_id_string(player_id=player_1)
                player_2 = MainDatabase().util.get_player_by_id_string(player_id=player_2)

                if not cls.players_already_playing(matches=list_of_matches, id_player_1=player_1,
                                                   id_player_2=player_2):

                    list_of_matches.append((player_1, player_2))
                    del sort_player[0]
                    del sort_player[opponent - 1]
                    break
        return list_of_matches

    @classmethod
    def player_choice(cls):
        """Prompts the user to select a player in database."""

        if MainDatabase().util.if_player_in_database_empty():
            return None

        cls.players_all_list()

        choice = ""
        while not cls.player_exists(choose_id=choice):
            choice = typer.prompt("Sélectionnez un joueur")

        return MainDatabase().util.get_player_by_id_string(player_id=choice)

    @staticmethod
    def players_all_list():
        """Lists all existing players."""

        _TOOLS.print_info("liste des joueurs existants:")

        all_players = MainDatabase().util.get_players_by_id()

        for player in all_players:
            if player.delete_player:
                continue

            player_id = typer.style(str(player.id_number))
            typer.echo(f"{player_id}. {player.first_name} {player.last_name}")

    @staticmethod
    def player_exists(choose_id: str, players_ids=None):
        if players_ids is None:
            players_ids = []
        if len(choose_id) == 0:
            return False
        if not choose_id.isnumeric():
            _TOOLS.error_message("entrez le numéro du joueur devant son nom")
            return False
        if int(choose_id) in players_ids:
            _TOOLS.error_message(f"le joueur numéro {choose_id} a déjà été ajouté")
            return False
        if MainDatabase().util.if_player_id_in_database(player_id=int(choose_id)):
            if MainDatabase().util.get_player_from_id_str(player_id=choose_id).delete_player:
                return False
            return True
        _TOOLS.error_message(f"pas de joueur avec le numéro {choose_id}")
        return False
