import typer

import tools.tool as _TOOLS
from controllers.report_controller import ReportController
from models.database.main_database import MainController
from models.tournament import Tournament


class ReportMenu:
    """Vue pour les opérations liées au rapport."""

    def __init__(self):
        """Constructeur pour TournamentMenu."""
        _TOOLS.print_title("menu des rapports")

        self.main_menu()
        self.select_user_input()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def main_menu(cls):
        """Affiche les différentes options du menu."""
        choice = typer.style("1. ", bold=True)
        typer.echo(choice + "Joueurs")

        choice = typer.style("2. ", bold=True)
        typer.echo(choice + "Tournois")

        choice = typer.style("\n0. ", bold=True)
        typer.echo(choice + "Retour")

    @classmethod
    def select_user_input(cls):
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = typer.prompt("Entrez votre choix ")

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
    """View for player related reports."""

    def __init__(self):
        """Constructeur pour PlayerReportMenu."""
        _TOOLS.print_title("rapport des joueurs")
        if MainController().util.if_player_db_empty():
            _TOOLS.error_message("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.report_controller = ReportController()
        self.main_menu()
        self.select_user_input()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def main_menu(cls):
        """Affiche les différentes options du menu."""
        choice = typer.style("1. ", bold=True)
        typer.echo(choice + "Par Nom")

        choice = typer.style("2. ", bold=True)
        typer.echo(choice + "Par Rating")

        choice = typer.style("\n0. ", bold=True)
        typer.echo(choice + "Retour")

    def select_user_input(self):
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = typer.prompt("Entrez votre choix ")

        if user_choice == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            typer.echo("\n\n")
            self.report_controller.show_all_players_by_name()
        elif user_choice == "2":
            typer.echo("\n\n")
            self.report_controller.show_all_players_by_rating()
        else:
            self.select_user_input()
            return


class TournamentReportMenu:
    """Voir les rapports relatifs aux tournois."""

    def __init__(self):
        """Constructor for TournamentReportMenu."""

        _TOOLS.print_title("rapport des tournois")

        if MainController().util.if_tournament_db_empty():
            _TOOLS.error_message("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.report_controller = ReportController()

        self.mian_menu()
        self.select_user_input()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def mian_menu(cls):
        """Affiche les différentes options du menu."""
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
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = typer.prompt("Entrez votre choix ")

        if user_choice == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        elif user_choice == "1":
            typer.echo("\n\n")
            self.report_controller.show_all_tournaments()
        elif user_choice == "2":
            self.tournament_players_sub_menu()
        elif user_choice == "3":
            tournament_choice = _TOOLS.tournament_choice()
            self.report_controller.tournament_rounds(tournament=tournament_choice)
            if len(tournament_choice.rounds) == 0:
                _TOOLS.error_message("le tournoi ne comporte aucun round.")
                _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
                return

        elif user_choice == "4":
            tournament_choice = _TOOLS.tournament_choice()
            self.report_controller.tournament_matches(tournament=tournament_choice)
            if len(tournament_choice.rounds) == 0:
                _TOOLS.error_message("le tournoi ne comporte aucun match.")
                _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
                return
        else:
            self.select_user_input()
            return

    def tournament_players_sub_menu(self):
        """Sous-menu pour le rapport des joueurs du tournoi."""
        tournament_choice = _TOOLS.tournament_choice()

        choice = typer.style("1. ", bold=True)
        typer.echo(choice + "Par Nom")
        choice = typer.style("2. ", bold=True)
        typer.echo(choice + "Par Classement")
        choice = typer.style("\n0. ", bold=True)
        typer.echo(choice + "Retour")
        self.tournament_players_sub_menu_choice(tournament_choice=tournament_choice)

    def tournament_players_sub_menu_choice(self, tournament_choice: Tournament):
        """Demande de l'utilisateur pour le sous-menu de rapport des joueurs du tournoi. """
        user_choice = typer.prompt("Entrez votre sélection ")

        if user_choice == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            typer.echo("\n\n")
            self.report_controller.show_tournament_players_by_name(tournament=tournament_choice)
        elif user_choice == "2":
            self.report_controller.show_tournament_players_by_rating(tournament=tournament_choice)
        else:
            self.select_user_input()
            return
