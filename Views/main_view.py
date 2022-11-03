import tools.tools as _TOOLS
from Views.player_view import PlayerMenu
from Views.report_view import ReportMenu
from Views.tournament_view import TournamentMenu


class MainMenu:

    def __int__(self):
        self.menu_principal()
        self.get_user_choice()

    @classmethod
    def menu_principal(cls):
        _TOOLS.print_title(" Menu principal")

        user_choice = "1. "
        print(user_choice + "Gérer les Tournois")

        user_choice = "2. "
        print(user_choice + "Gérer les joueurs")

        user_choice = "3. "
        print(user_choice + "Générer des rapports")

        user_choice = "\n0. "
        print(user_choice + "Quitter")
        cls.get_user_choice()

    @classmethod
    def get_user_choice(cls):
        choice = input("\nEntrez un choix: ")
        print("\n")

        if choice == "0":
            raise SystemExit
        elif choice == "1":
            TournamentMenu().main_menu()
        elif choice == "2":
            PlayerMenu()
        elif choice == "3":
            ReportMenu()
        else:
            cls.get_user_choice()
