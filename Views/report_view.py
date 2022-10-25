import tools.tools as _TOOLS
from Controllers.report_controller import ReportController
from Models.database.main_database import MainDatabase
from Models.tournament import Tournament
from Views.tournament_view import EditTournamentMenu


class ReportMenu:
    """Vue pour les opérations liées au rapport."""

    def __init__(self):
        """Constructeur pour TournamentMenu."""
        _TOOLS.print_title("menu des rapports")

        self.main_menu()
        self.select_user_input()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @staticmethod
    def main_menu():
        """Affiche les différentes options du menu."""
        choice = _TOOLS.print_message("1. ")
        print(choice + "Joueurs")

        choice = _TOOLS.print_message("2. ")
        print(choice + "Tournois")

        choice = _TOOLS.print_message("\n0. ")
        print(choice + "Retour")

    def select_user_input(self):
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = input("Entrez votre choix ")

        if user_choice == "0":
            print("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            PlayerReportMenu()
        elif user_choice == "2":
            TournamentReportMenu()
        else:
            self.select_user_input()


class PlayerReportMenu:
    """View for player related reports."""

    def __init__(self):
        """Constructeur pour PlayerReportMenu."""
        _TOOLS.print_title("rapport des joueurs")
        if MainDatabase().util.if_player_in_database_empty():
            _TOOLS.error_message("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.report_controller = ReportController()
        self.main_menu()
        self.select_user_input()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @staticmethod
    def main_menu():
        """Affiche les différentes options du menu."""
        choice = _TOOLS.print_message("1. ")
        print(choice + "Par Nom")

        choice = _TOOLS.print_message("2. ")
        print(choice + "Par Rating")

        choice = _TOOLS.print_message("\n0. ")
        print(choice + "Retour")

    def select_user_input(self):
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = input("Entrez votre choix: ")

        if user_choice == "0":
            print("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            print("\n\n")
            ReportController().show_all_players_by_name()
        elif user_choice == "2":
            print("\n\n")
            ReportController().show_all_players_by_rating()
        else:
            self.select_user_input()
            return


class TournamentReportMenu:
    """Voir les rapports relatifs aux tournois."""

    def __init__(self):
        """Constructor for TournamentReportMenu."""

        _TOOLS.print_title("rapport des tournois")

        if MainDatabase().util.if_tournament_in_database_empty():
            _TOOLS.error_message("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.report_controller = ReportController()

        self.mian_menu()
        self.select_user_input()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @staticmethod
    def mian_menu():
        """Affiche les différentes options du menu."""
        choice = _TOOLS.print_message("1. ")
        print(choice + "Tous les tournois")

        choice = _TOOLS.print_message("2. ")
        print(choice + "Joueurs d'un tournoi")

        choice = _TOOLS.print_message("3. ")
        print(choice + "Rounds d'un tournoi")

        choice = _TOOLS.print_message("4. ")
        print(choice + "Matchs d'un tournoi")

        choice = _TOOLS.print_message("\n0. ")
        print(choice + "Retour")

    def select_user_input(self):
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = input("Entrez votre choix: ")

        if user_choice == "0":
            print("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        elif user_choice == "1":
            print("\n\n")
            ReportController().show_all_tournaments()
        elif user_choice == "2":
            self.tournament_players_sub_menu()
        elif user_choice == "3":
            tournament_choice = EditTournamentMenu().tournament_choice()
            self.report_controller.tournament_rounds(tournament=tournament_choice)
            if len(tournament_choice.rounds) == 0:
                _TOOLS.error_message("le tournoi ne comporte aucun round.")
                _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
                return

        elif user_choice == "4":
            tournament_choice = EditTournamentMenu().tournament_choice()
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

        tournament_choice = EditTournamentMenu().tournament_choice()

        choice = _TOOLS.print_message("1. ")
        print(choice + "Par Nom")
        choice = _TOOLS.print_message("2. ")
        print(choice + "Par Classement")
        choice = _TOOLS.print_message("\n0. ")
        print(choice + "Retour")
        self.tournament_players_sub_menu_choice(tournament_choice=tournament_choice)

    def tournament_players_sub_menu_choice(self, tournament_choice: Tournament):
        """Demande de l'utilisateur pour le sous-menu de rapport des joueurs du tournoi. """

        user_choice = input("Entrez votre sélection ")

        if user_choice == "0":
            print("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            print("\n\n")
            self.report_controller.show_tournament_players_by_name(tournament=tournament_choice)
        elif user_choice == "2":
            self.report_controller.show_tournament_players_by_rating(tournament=tournament_choice)
        else:
            self.select_user_input()
            return
