from click.exceptions import Exit

import tools.tools as _TOOLS
from Views.player_view import PlayerMenu
from Views.report_view import ReportMenu
from Views.tournament_view import TournamentMenu


class MainMenu:

    def __int__(self):
        self.menu_principal()
        self.get_user_choice()

    def menu_principal(self):
        _TOOLS.print_title(" Menu principal")

        user_choice = "1. "
        print(user_choice + "Gérer les Tournois")

        user_choice = "2. "
        print(user_choice + "Gérer les joueurs")

        user_choice = "3. "
        print(user_choice + "Générer des rapports")

        user_choice = "\n0. "
        print(user_choice + "Quitter")
        self.get_user_choice()

    def get_user_choice(self):
        choice = input("\nEntrez un choix: ")
        print("\n")

        if choice == "0":
            Exit()
        elif choice == "1":
            TournamentMenu()
            TournamentMenu().main_menu()
        elif choice == "2":
            PlayerMenu()
        elif choice == "3":
            ReportMenu()
        else:
            self.get_user_choice()
