import typer

# from controller.config_loader import _CONFIG
from controller.main_database import MainDatabase
from controller.report_controller import ReportController
import views.tools as _HELPER

from models.tournament import Tournament


class ReportMenu:
    """View for report related operations."""

    def __init__(self):
        """Constructor for TournamentMenu."""

        _HELPER.print_title("menu des rapports")

        self.main_menu()
        self.select_user_input()

        _HELPER.go_back_to_menu(current_view=self.__class__.__name__)

    @staticmethod
    def main_menu():
        """Displays the different menu options."""

        choice = typer.style("1. ", bold=True)
        typer.echo(choice + "Joueurs")

        choice = typer.style("2. ", bold=True)
        typer.echo(choice + "Tournois")

        choice = typer.style("\n0. ", bold=True)
        typer.echo(choice + "Retour")

    @classmethod
    def select_user_input(cls):
        """Prompts the user to select an option."""

        user_choice = typer.prompt("Entrez choix ")

        if user_choice == "0":
            typer.echo("\n\n")
            _HELPER.go_back_to_menu(current_view=cls.__class__.__name__)
        elif user_choice == "1":
            PlayerReportMenu()
        elif user_choice == "2":
            TournamentReportMenu()
        else:
            cls.select_user_input()


class PlayerReportMenu:
    """View for player related reports."""

    def __init__(self):
        """Constructor for PlayerReportMenu."""

        _HELPER.print_title("rapport des joueurs")

        if MainDatabase().util.is_player_db_empty():
            _HELPER.print_error("aucun joueur créé.")
            _HELPER.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.report_controller = ReportController()

        self.main_menu()
        self.select_user_input()

        _HELPER.go_back_to_menu(current_view=self.__class__.__name__)

    @staticmethod
    def main_menu():
        """Displays the different menu options."""

        choice = typer.style("1. ", bold=True)
        typer.echo(choice + "Par Nom")

        choice = typer.style("2. ", bold=True)
        typer.echo(choice + "Par Rating")

        choice = typer.style("\n0. ", bold=True)
        typer.echo(choice + "Retour")

    def select_user_input(self):
        """Prompts the user to select an option."""

        user_choice = typer.prompt("Entrez votre sélection: ")

        if user_choice == "0":
            typer.echo("\n\n")
            _HELPER.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            typer.echo("\n\n")
            self.report_controller.all_players_by_name()
        elif user_choice == "2":
            typer.echo("\n\n")
            self.report_controller.all_players_by_rating()
        else:
            self.select_user_input()
            return
        #
        # _TOOLS.print_report(self.report_controller.data)
        # export_format = _TOOLS.report_export_prompt()
        #
        # if export_format is not None:
        #     save_path = self.report_controller.init_export(export_format)
        # else:
        #     return
        #
        # _TOOLS.print_success(f"rapport enregistré sous: {save_path}")


class TournamentReportMenu:
    """View for tournament related reports."""

    def __init__(self):
        """Constructor for TournamentReportMenu."""

        _HELPER.print_title("rapport des tournois")

        if MainDatabase().util.is_tournament_db_empty():
            _HELPER.print_error("aucun joueur créé.")
            _HELPER.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.report_handler = ReportController()

        self.main_menu()
        self.select_user_input()

        _HELPER.go_back_to_menu(current_view=self.__class__.__name__)

    @staticmethod
    def main_menu():
        """Displays the different menu options."""

        choice = typer.style("1. ", bold=True)
        typer.echo(choice + "Tous les tournois")

        choice = typer.style("2. ", bold=True)
        typer.echo(choice + "Joueurs d'un tournoi")

        choice = typer.style("3. ", bold=True)
        typer.echo(choice + "Rounds d'un tournoi")

        choice = typer.style("4. ", bold=True)
        typer.echo(choice + "Matchs d'un tournoi")

        choice = typer.style("\n0. ", bold=True)
        typer.echo(choice + "Retour")

    def select_user_input(self):
        """Prompts the user to select an option."""

        user_choice = typer.prompt("Entrez votre sélection: ")

        if user_choice == "0":
            typer.echo("\n\n")
            _HELPER.go_back_to_menu(current_view=self.__class__.__name__)
            return

        elif user_choice == "1":
            typer.echo("\n\n")
            self.report_handler.all_tournaments()

        elif user_choice == "2":
            self.tournament_players_sub_menu()

        elif user_choice == "3":
            selected_tournament = _HELPER.tournament_choice()
            self.report_handler.tournament_rounds(tournament=selected_tournament)
            if len(selected_tournament.tours) == 0:
                _HELPER.print_error("le tournoi ne comporte aucun round.")
                _HELPER.go_back_to_menu(current_view=self.__class__.__name__)
                return

        elif user_choice == "4":
            selected_tournament = _HELPER.tournament_choice()
            self.report_handler.tournament_matches(tournament=selected_tournament)
            if len(selected_tournament.tours) == 0:
                _HELPER.print_error("le tournoi ne comporte aucun match.")
                _HELPER.go_back_to_menu(current_view=self.__class__.__name__)
                return

        else:
            self.select_user_input()
            return
        #
        # _TOOLS.print_report(self.report_handler.data)
        # export_format = _TOOLS.report_export_prompt()
        #
        # if export_format is not None:
        #     save_path = self.report_handler.init_export(export_format)
        # else:
        #     return
        #
        # _TOOLS.print_success(f"rapport enregistré sous: {save_path}")

    def tournament_players_sub_menu(self):
        """Sub-menu for tournament's players report."""

        tournament_choice = _HELPER.tournament_choice()

        choice = typer.style("1. ", bold=True)
        typer.echo(choice + "Par Nom")

        choice = typer.style("2. ", bold=True)
        typer.echo(choice + "Par Rating")

        choice = typer.style("\n0. ", bold=True)
        typer.echo(choice + "Retour")

        self.tournament_players_sub_menu_selection(selected_tournament=tournament_choice)

    def tournament_players_sub_menu_selection(self, selected_tournament: Tournament):
        """User prompt for tournament's players report sub-menu.

        Args:
            selected_tournament (Tournament): Tournament previously selected.
        """

        user_choice = typer.prompt("Entrez votre sélection ")

        if user_choice == "0":
            typer.echo("\n\n")
            _HELPER.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            typer.echo("\n\n")
            self.report_handler.tournament_players_by_name(tournament=selected_tournament)
        elif user_choice == "2":
            self.report_handler.tournament_players_by_rating(tournament=selected_tournament)
        else:
            self.select_user_input()
            return
