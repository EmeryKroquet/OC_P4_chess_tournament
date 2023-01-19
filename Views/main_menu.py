import typer

from views.tournament_views import TournamentMenu
from views.player_view import PlayerMenu
from views.report_views import ReportMenu
import views.tools as _HELPER


class MainMenu:
    """First view displayed, main menu."""

    def __init__(self):
        """Constructor for MainMenu."""

        _HELPER.print_title("menu principal")

        self.print_menu()
        self.user_selection()

    @classmethod
    def print_menu(cls):
        """Displays the different menu options."""

        number = "1. "
        typer.echo(number + "Tournois")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Gérer les joueurs")

        number = typer.style("3. ", bold=True)
        typer.echo(number + "Générer un rapport")

        number = typer.style("\n0. ", bold=True)
        typer.echo(number + "Quitter")

    @classmethod
    def user_selection(cls):
        """Prompts the user to select an option."""

        selection = typer.prompt("\nEntrez votre sélection ")
        typer.echo("\n")

        if selection == "0":
            typer.Exit()
        elif selection == "1":
            TournamentMenu()
        elif selection == "2":
            PlayerMenu()
        elif selection == "3":
            ReportMenu()
        else:
            cls.user_selection()
