from time import sleep

import typer

from controllers.tournament_controller import TournamentController
import tools.tool as _TOOLS
from controllers.main_controller import MainController
from models.match import Match


class PlayMenu:

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
        decorator = typer.style(
            " - - ",
            bold=True,
        )
        separator = typer.style(
            " - ",
            bold=True,
        )
        tournament_number = typer.style(
            f"Tournoi {self.tournament_controller.tournament.id_number}")
        round_number = typer.style(
            f"Round {self.tournament_controller.current_round_number}")
        match_number = typer.style(
            f"Match {self.tournament_controller.current_match_number}")

        typer.echo("\n" + decorator +
                   tournament_number +
                   separator + round_number +
                   separator + match_number +
                   decorator)

    @classmethod
    def introduce_match(cls, match: Match):
        """Affiche les noms et le classement des joueurs du match en cours."""
        player_1_title = typer.style(
            "Joueur 1: ",
            bold=True,
        )
        player_1_name = typer.style(
            "{first_name_1} {last_name_1} ".format(
                first_name_1=match.player_1.first_name,
                last_name_1=match.player_1.last_name,
            ))
        player_1_rating = typer.style(
            f"({match.player_1.rating})")

        player_1_presentation = player_1_title + player_1_name + player_1_rating

        versus = typer.style(
            " vs ",
            bold=True,
        )
        player_2_title = typer.style(
            "Joueur 2: ",
            bold=True,
        )
        player_2_name = typer.style(
            "{first_name_2} {last_name_2} ".format(
                first_name_2=match.player_2.first_name,
                last_name_2=match.player_2.last_name,
            ))
        player_2_rating = typer.style(
            f"({match.player_2.rating})")

        player_2_presentation = player_2_title + player_2_name + player_2_rating

        typer.echo(player_1_presentation + versus + player_2_presentation)

    @classmethod
    def ask_for_winner(cls):
        """Invite l'utilisateur à saisir un gagnant.
        Retourne :
            str : Le vainqueur du match.
            ("1" pour le joueur 1,
             "2" pour le joueur 2,
             "nul" pour un match nul).
        """
        winner = ""
        while winner.lower() not in ["1", "2", "nul"]:
            winner = typer.prompt("Entrez le gagnant (1, 2, ou nul)")
        return winner.lower()

    def show_final_rating(self):
        """Affiche le classement final."""
        typer.echo("\n")
        _TOOLS.message_success("TOURNOI TERMINÉ")
        _TOOLS.print_info("classement final:")
        rating_table = MainController().util.get_format_rating_table(
            rating_table=self.tournament_controller.tournament.rating_table)
        i = 1
        for player in rating_table:
            rating = typer.style(f"{i} -", bold=True)
            player_name = player[0]
            points = str(player[1])
            typer.echo(f"{rating} {player_name} ({points} points)")
            i += 1

            typer.echo("\n")
            sleep(5)
