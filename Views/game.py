import typer

import views.tools as _HELPER

from time import sleep

from controller.tournament_controller import TournamentController
from models.match import Match
from controller.main_database import MainDatabase


class GameMenu:
    """View displayed during a game.
        tournament_controller (TournamentController):
        Object handling tournament generation, progression and saving.
    """

    def __init__(self, tournament_id: int):
        """Constructor for GameMenu. Initiates the match generation.
            tournament_id (int): Unique id of the tournament to be played.
        """
        self.tournament_controller = TournamentController(tournament_id=tournament_id)
        self.play()
        _HELPER.go_back_to_menu(current_view=self.__class__.__name__)

    def play(self):
        """Uses the match generating method of the tournament handler to display a match until tournament's ending."""
        while self.tournament_controller.generate_match() is not None:
            self.display_next_match(self.tournament_controller.generate_match())
        self.ending_splash()

    def display_next_match(self, match: Match):
        """Initiates relevant info displays and prompts for a given Match.
        Args:
            match (Match): Match object to be displayed.
        """
        self.display_tournament_progression()
        self.introduce_match(match=match)
        winner = self.ask_for_winner()
        self.tournament_controller.save_winner(match=match, winner=winner)

    def display_tournament_progression(self):
        """Displays current tournament, round and match numbers."""
        self.tournament_controller.update_tournament_in_progression()
        decorator = typer.style(" - - ", )
        separator = typer.style(" - ", )
        tournament_number = typer.style(f"Tournoi {self.tournament_controller.tournament.id_number}", )
        round_number = typer.style(f"Round {self.tournament_controller.current_round_number}", )
        match_number = typer.style(f"Match {self.tournament_controller.current_match_number}", )
        typer.echo(
            "\n" + decorator + tournament_number + separator + round_number + separator + match_number + decorator)

    def introduce_match(self, match: Match):
        """Displays current match's players names and ELO ranking.
        Args:
            match (Match): Match to be played.
        """
        player_1_title = typer.style(
            "Joueur 1: ")
        player_1_name = typer.style(
            "{f_name_1} {l_name_1} ".format(
                f_name_1=match.player_1.first_name,
                l_name_1=match.player_1.last_name,
            ),
        )
        player_1_rating = typer.style(
            f"({match.player_1.rating})",
        )
        player_1_full_presentation = player_1_title + player_1_name + player_1_rating
        versus = typer.style(" vs ", )
        player_2_title = typer.style("Joueur 2: ", )
        player_2_name = typer.style("{f_name_2} {l_name_2} ".format(f_name_2=match.player_2.first_name,
                                                                    l_name_2=match.player_2.last_name,
                                                                    ),)
        player_2_rating = typer.style(
            f"({match.player_2.rating})",)
        player_2_full_presentation = player_2_title + player_2_name + player_2_rating
        typer.echo(player_1_full_presentation + versus + player_2_full_presentation)

    def ask_for_winner(self):
        """Prompts the user to enter a player_winner.
        Returns:
            str: Winner of the match. ("1" for Player 1, "2" for Player 2, "nul" for a draw.)
        """
        winner = ""
        while winner.lower() not in ["1", "2", "nul"]:
            winner = typer.prompt("Entrez le gagnant (1, 2, ou nul)")
        return winner.lower()

    def ending_splash(self):
        """Displays final rating_table."""
        typer.echo("\n")
        _HELPER.print_success("TOURNOI TERMINÉ")
        _HELPER.print_info("classement final:")
        rating_table = MainDatabase().util.get_formated_rating_table(
            rating_table=self.tournament_controller.tournament.rating_table
        )
        for i, player in enumerate(rating_table, start=1):
            rank = typer.style(f"{i} -")
            player_name = player[0]
            points = str(player[1])
            typer.echo(f"{rank} {player_name} ({points} points)")
        typer.echo("\n")

        sleep(5)
