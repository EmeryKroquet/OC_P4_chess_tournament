import typer

import tools.tool as _TOOLS
from views import tournament_view, player_view, report_view
from views.player_view import PlayerMenu
from views.report_view import ReportMenu
from views.tournament_view import TournamentMenu


class MainMenu:

    def __init__(self):

        self.main_menu()
        self.select_user_input()

    @classmethod
    def main_menu(cls):
        _TOOLS.print_title("menu principal")

        user_choice = typer.style("1. ", bold=True)
        typer.echo(user_choice + "Gérer les Tournois")

        user_choice = typer.style("2. ", bold=True)
        typer.echo(user_choice + "Gérer les joueurs")

        user_choice = typer.style("3. ", bold=True)
        typer.echo(user_choice + "Générer des rapports")

        user_choice = typer.style("\n0. ", bold=True)
        typer.echo(user_choice + "Quitter")
        cls.select_user_input()

    @classmethod
    def select_user_input(cls):
        choice = typer.prompt("\nEntrez un choix ")
        typer.echo("\n")

        if choice == "0":
            typer.Exit()
        elif choice == "1":
            TournamentMenu()
            TournamentMenu().main_menu()
        elif choice == "2":
            PlayerMenu()
        elif choice == "3":
            ReportMenu()
        else:
            cls.select_user_input()
