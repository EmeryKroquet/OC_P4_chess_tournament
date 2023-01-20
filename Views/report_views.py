import typer

from controller.main_database import MainDatabase
from controller.report_controller import ReportController
import views.tools as _TOOLS

from models.tournament import Tournament


class ReportMenu:
    """Vue pour les opérations liées au rapport."""

    def __init__(self):
        """Constructeur pour le TournamentMenu."""
        _TOOLS.print_title("menu des rapports")
        self.main_menu()
        self.select_user_input()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @staticmethod
    def main_menu():
        """Affiche les différentes options du menu."""
        choice = typer.style("1. ")
        typer.echo(f"{choice}Joueurs")
        choice = typer.style("2. ")
        typer.echo(f"{choice}Tournois")
        choice = typer.style("\n0. ")
        typer.echo(f"{choice}Retour")

    @classmethod
    def select_user_input(cls):
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = typer.prompt("Entrez choix ")
        if user_choice == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=cls.__class__.__name__)
        elif user_choice == "1":
            PlayerReportMenu()
        elif user_choice == "2":
            TournamentReportMenu()
        else:
            cls.select_user_input()


class PlayerReportMenu:
    """Voir les rapports relatifs aux joueurs."""

    def __init__(self):
        """Constructeur pour PlayerReportMenu."""
        _TOOLS.print_title("rapport des joueurs")
        if MainDatabase().util.is_player_db_empty():
            _TOOLS.print_error("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.report_controller = ReportController()
        self.main_menu()
        self.select_user_input()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @staticmethod
    def main_menu():
        """Affiche les différentes options du menu."""
        choice = typer.style("1. ", bold=True)
        typer.echo(f"{choice}Par Nom")
        choice = typer.style("2. ", bold=True)
        typer.echo(f"{choice}Par Rating")
        choice = typer.style("\n0. ", bold=True)
        typer.echo(f"{choice}Retour")

    def select_user_input(self):
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = typer.prompt("Entrez votre sélection ")
        if user_choice == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            typer.echo("\n\n")
            self.report_controller.all_players_by_name()
        elif user_choice == "2":
            typer.echo("\n\n")
            self.report_controller.all_players_by_rating()
        else:
            self.select_user_input()
            return


class TournamentReportMenu:
    """Voir les rapports relatifs aux tournois."""

    def __init__(self):
        """Constructeur pour TournamentReportMenu."""
        _TOOLS.print_title("rapport des tournois")
        if MainDatabase().util.is_tournament_db_empty():
            _TOOLS.print_error("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.report_view = ReportController()
        self.main_menu()
        self.select_user_input()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @staticmethod
    def main_menu():
        """Affiche les différentes options du menu."""
        choice = typer.style("1. ", bold=True)
        typer.echo(f"{choice}Tous les tournois")
        choice = typer.style("2. ", bold=True)
        typer.echo(choice + "Joueurs d'un tournoi")
        choice = typer.style("3. ", bold=True)
        typer.echo(choice + "Rounds d'un tournoi")
        choice = typer.style("4. ", bold=True)
        typer.echo(choice + "Matchs d'un tournoi")
        choice = typer.style("\n0. ", bold=True)
        typer.echo(f"{choice}Retour")

    def select_user_input(self):
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = typer.prompt("Entrez votre sélection: ")
        if user_choice == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        elif user_choice == "1":
            typer.echo("\n\n")
            self.report_view.all_tournaments()
        elif user_choice == "2":
            self.tournament_players_sub_menu()
        elif user_choice == "3":
            selected_tournament = _TOOLS.tournament_choice()
            self.report_view.tournament_rounds(tournament=selected_tournament)
            if len(selected_tournament.tours) == 0:
                _TOOLS.print_error("le tournoi ne comporte aucun round.")
                _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
                return
        elif user_choice == "4":
            selected_tournament = _TOOLS.tournament_choice()
            self.report_view.tournament_matches(tournament=selected_tournament)
            if len(selected_tournament.tours) == 0:
                _TOOLS.print_error("le tournoi ne comporte aucun match.")
                _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
                return
        else:
            self.select_user_input()
            return

    def tournament_players_sub_menu(self):
        """Sub-menu for tournament's players report."""
        tournament_choice = _TOOLS.tournament_choice()
        choice = typer.style("1. ", bold=True)
        typer.echo(f"{choice}Par Nom")
        choice = typer.style("2. ", bold=True)
        typer.echo(f"{choice}Par Rating")
        choice = typer.style("\n0. ", bold=True)
        typer.echo(f"{choice}Retour")
        self.tournament_players_sub_menu_selection(selected_tournament=tournament_choice)

    def tournament_players_sub_menu_selection(self, selected_tournament: Tournament):
        """Demande de l'utilisateur pour le sous-menu de rapport des joueurs du tournoi.
            selected_tournament (Tournoi) : Tournoi précédemment sélectionné.
        """
        user_choice = typer.prompt("Entrez votre sélection ")
        if user_choice == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            typer.echo("\n\n")
            self.report_view.tournament_players_by_name(tournament=selected_tournament)
        elif user_choice == "2":
            self.report_view.tournament_players_by_rating(tournament=selected_tournament)
        else:
            self.select_user_input()
            return
