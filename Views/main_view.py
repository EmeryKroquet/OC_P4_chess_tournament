import typer

import tools.tools as _TOOLS
from Views.player_view import PlayerMenu
from Views.report_view import ReportMenu
from Views.tournament_view import TournamentMenu


class MainMenu:

    def __int__(self):
        self.main_menu()
        self.get_user_choice()

    def main_menu(self):
        _TOOLS.print_title(" Menu principal")

        user_choice = typer.style("1. ")
        typer.echo(user_choice + "Gérer les Tournois")

        user_choice = typer.style("2. ")
        typer.echo(user_choice + "Gérer les joueurs")

        user_choice = typer.style("3. ")
        typer.echo(user_choice + "Générer des rapports")

        user_choice = typer.style("\n0. ")
        typer.echo(user_choice + "Quitter")
        self.get_user_choice()

    def get_user_choice(self):
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
            self.get_user_choice()
