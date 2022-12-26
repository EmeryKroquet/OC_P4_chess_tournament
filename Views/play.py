from time import sleep

from Controllers.tournament_controller import TournamentController
from Controllers.main_database import MainDatabase

import tools.tools as _TOOLS
from Models.match import Match


class PlayGameMenu:

    def __init__(self, tournament_id: int):
        self.tournament_controller = TournamentController(tournament_id=tournament_id)
        self.play_match()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def play_match(self):
        """Utilise la méthode de génération de match du gestionnaire
        de tournoi pour afficher un match jusqu'à la fin du tournoi. """
        while self.tournament_controller.generate_match() is not None:
            self.display_next_match(self.tournament_controller.generate_match())
        self.show_final_rating()

    def display_next_match(self, match: Match):
        """Lance les affichages d'informations et les invites pertinentes pour un Match donné."""
        self.display_tournament_in_progression()
        self.introduce_match(match=match)
        winner = self.ask_for_winner()
        self.tournament_controller.save_player_winner(match=match, winner=winner)

    def display_tournament_in_progression(self):
        """Affiche les numéros du tournoi, du tour et du match en cours."""
        self.tournament_controller.update_tournament_in_progression()
        decorator = _TOOLS.print_message(
            " - - ",

        )
        separator = _TOOLS.print_message(
            " - ",

        )
        tournament_number = _TOOLS.print_message(
            f"Tournoi {self.tournament_controller.tournament.id_number}")
        round_number = _TOOLS.print_message(
            f"Round {self.tournament_controller.current_round_number}")
        match_number = _TOOLS.print_message(
            f"Match {self.tournament_controller.current_match_number}")

        print("\n" + decorator +
              tournament_number +
              separator + round_number +
              separator + match_number +
              decorator)

    @staticmethod
    def introduce_match(match: Match):
        """Affiche les noms et le classement des joueurs du match en cours."""
        player_1_title = _TOOLS.print_message(
            "Joueur 1: ",

        )
        player_1_name = _TOOLS.print_message(
            f"First Name 1: {match.player_1.first_name} "
            f"Last Name 1: {match.player_1.last_name} "
        )
        player_1_rating = _TOOLS.print_message(
            f"({match.player_1.rating})")

        player_1_presentation = player_1_title + player_1_name + player_1_rating

        versus = _TOOLS.print_message(
            " vs ",

        )
        player_2_title = _TOOLS.print_message(
            "Joueur 2: ",

        )
        player_2_name = _TOOLS.print_message(
            f"First Name 2: {match.player_2.first_name}"
            f"Last Name 2: {match.player_2.last_name}"
        )
        player_2_rating = _TOOLS.print_message(
            f"({match.player_2.rating})")

        player_2_presentation = player_2_title + player_2_name + player_2_rating

        print(player_1_presentation + versus + player_2_presentation)

    @staticmethod
    def ask_for_winner():
        winner = ""
        while winner.lower() not in ["1", "2", "nul"]:
            winner = input("Entrez le gagnant (1, 2, ou nul)")
        return winner.lower()

    def show_final_rating(self):
        """Affiche le classement final."""
        print("\n")
        _TOOLS.message_success("TOURNOI TERMINÉ")
        _TOOLS.print_info("classement final: ")

        rating_table = MainDatabase().util.get_format_rating_table(
            rating_table=self.tournament_controller.tournament.rating_table)
        for i, player in enumerate(rating_table, start=1):
            rating = _TOOLS.print_message(f"{i} -")
            player_name = player[0]
            points = str(player[1])
            print(f"{rating} {player_name} ({points} points)")
            print("\n")
            sleep(5)
