from copy import deepcopy

from click.exceptions import Exit

import tools.tools as _TOOLS
from Controllers.tournament_controller import PlayMenu
from Models.database.main_database import MainDatabase
from Views.player_view import EditPlayerMenu


class TournamentMenu:

    def __int__(self):
        _TOOLS.print_title("menu des tournois")

        self.main_menu()
        self.get_tournament_user_choice()

    def main_menu(self):
        user_choice = _TOOLS.print_message("1.")
        print(user_choice + "Rependre un tournoi")

        user_choice = _TOOLS.print_message("2.")
        print(user_choice + "Créer un nouveau tournoi")

        user_choice = _TOOLS.print_message("3.")
        print(user_choice + "Modifier un tournoi")

        user_choice = _TOOLS.print_message("4.")
        print(user_choice + "Supprimer un tournoi")

        user_choice = _TOOLS.print_message("5.")
        print(user_choice + "Afficher tous les tournois")

        user_choice = _TOOLS.print_message("\n0.")
        print(user_choice + "Retour au menu")
        self.get_tournament_user_choice()

    def get_tournament_user_choice(self):
        user_choice = input("Viellez entrer un choix: ")

        if user_choice == "0":
            print("\n\n")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            print("\n\n")
            LoadTournamentMenu()
        elif user_choice == "2":
            print("\n\n")
            NewTournamentMenu()
        elif user_choice == "3":
            print("\n\n")
            EditTournamentMenu()
        elif user_choice == "4":
            print("\n\n")
            DeleteTournamentMenu()
        elif user_choice == "5":
            print("\n\n")
            EditTournamentMenu().tournaments_all_list()
            print("\n")
            LoadTournamentMenu().tournament_user_choice()
        else:
            LoadTournamentMenu().tournament_user_choice()


class LoadTournamentMenu:

    def __init__(self, tournament_id: int = None):
        _TOOLS.print_title("Chargement d'un tournoi")
        self.tournaments = MainDatabase().util.get_tournament_in_progression()
        self.show_tournaments(tournament_id=tournament_id)
        self.display_tournaments_in_progression()

        if len(self.tournaments) == 0:
            _TOOLS.error_message("aucun tournoi en cours.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.tournament_user_choice()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def show_tournaments(self, tournament_id: int = None):
        """Gère l'éventuel identifiant de tournoi passé à l'instanciation."""
        tournament_valable = (
                MainDatabase().util.get_tournament_by_id_string(tournament_id=tournament_id)
                in self.tournaments
        )
        if tournament_id is not None and not tournament_valable:
            _TOOLS.error_message(
                f"le tournoi n°{tournament_id} n'est pas disponible.",
            )
        elif tournament_id is not None and tournament_valable:
            self.start_tournament(tournament_id=tournament_id)
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def display_tournaments_in_progression(self):
        """Utilise le gestionnaire de base de données pour trouver et
            afficher les tournois non terminés afin que l'utilisateur puisse
            faire son choix.
         """
        for tournament in self.tournaments:
            print(f" - Tournoi n°{tournament.id_number} -")
            parameter = _TOOLS.print_message("Nom: ")
            print(parameter + tournament.name)
            parameter = _TOOLS.print_message("Date: ")
            print(parameter + tournament.date + "\n")

    def tournament_user_choice(self):
        """Demande à l'utilisateur de sélectionner un tournoi à charger."""
        choice = input("Entrez un ID de tournoi")
        tournament_ids = [x.id_number for x in self.tournaments]

        while not choice.isnumeric() or int(choice) not in tournament_ids:
            _TOOLS.error_message(f"pas de tournoi avec l'ID' {choice}")
            TournamentMenu().get_tournament_user_choice()
            return self.start_tournament(int(choice))

    @staticmethod
    def start_tournament(tournament_id):
        """Ouvre le menu de jeu pour le tournoi sélectionné."""
        PlayMenu(tournament_id)


class NewTournamentMenu:

    def __init__(self):
        """Constructeur pour TournamentMenu."""

        _TOOLS.print_title("création d'un tournoi")

        self.tournament_name = ""
        self.place = ""
        self.date = ""
        self.numbers_of_tours = ""
        self.time_control = ""
        self.description = ""
        self.players = []
        self.create_tournament_id = None

        self.create_tournament()
        self.add_players()
        self.confirm_tournament_creation()
        self.save_tournament()
        self.start_tournament()

    def create_tournament(self):
        _TOOLS.print_title(" Viellez entrer les informations du tournoi:")
        while len(self.tournament_name) == 0:
            self.tournament_name = input("Entrez le nom du tournois: ")

        while len(self.place) == 0:
            self.place = input("Entrez le lieu: ")

        while not _TOOLS.date_valid(date=self.date):
            self.date = input("Entrez la Date au format DD-MM-YYYY: ")

        while not self.numbers_of_tours.isnumeric():
            self.numbers_of_tours = input(" Entrez le nombre de rounds: ")

        while not self.valid_time_control():
            self.time_control = input("Veillez Entrer un contrôle de "
                                      "temps:\n"
                                      "Bullet\n"
                                      "Blitz\n"
                                      "Coup Rapide\n : ")
        while len(self.description) == 0:
            self.description = input("Veillez entrer une description: ")

    def valid_time_control(self):
        if self.time_control.lower() == "bullet":
            self.time_control = "Bullet"
            return True
        elif self.time_control.lower() == "blitz":
            self.time_control = "Blitz"
            return True
        elif self.time_control.lower() == "coup rapide":
            self.time_control = "Coup Rapide"
            return True
        else:
            if len(self.time_control) > 0:
                _TOOLS.error_message("Choix invalide:\n"
                                     " Entrez :\n"
                                     " Bullet\n"
                                     " Blitz\n"
                                     " Coup Rapide\n")
            return False

    def add_players(self):
        print("\n Veillez entrer le numéro d'un joueur à ajouter\n", )
        EditPlayerMenu().players_all_list()
        while len(self.players) < 8:
            choice = input(f"Joueur ({str(len(self.players))}/8)")
            if EditPlayerMenu().player_exists(choose_id=choice, players_ids=self.players):
                self.players.append(int(choice))

    def confirm_tournament_creation(self):
        self.display_tournament()
        self.list_of_selection_players_by_name()

        confirm = _TOOLS.print_message("\nSouhaitez vous confirmer la création de ce tournoi ?")
        if not confirm:
            _TOOLS.error_message("annulation. Le tournoi n'a pas été créé.")
            raise Exit

    def display_tournament(self):
        _TOOLS.print_info("paramètres du tournoi:")

        parameter = _TOOLS.print_message("Nom: ")
        print(parameter + self.tournament_name)
        parameter = _TOOLS.print_message("Lieu: ")
        print(parameter + self.place)
        parameter = _TOOLS.print_message("Date: ")
        print(parameter + self.date)
        parameter = _TOOLS.print_message("Number of tours: ")
        print(parameter + self.numbers_of_tours)
        parameter = _TOOLS.print_message("Contrôle du temps: ")
        print(parameter + self.time_control)
        parameter = _TOOLS.print_message("Description: ")
        print(parameter + self.description)

    def list_of_selection_players_by_name(self):
        """Liste des joueurs pour sélectionner par leurs noms"""
        _TOOLS.print_info("liste des joueurs: ")

        players_name = MainDatabase().util.get_players_names(players_name=self.players)

        for name in players_name:
            print(f" - {name}")

    def save_tournament(self):
        """ Utiliser le MainDatabase pour sauvegarder le create tournament"""
        self.create_tournament_id = MainDatabase().create_tournament(
            name=self.tournament_name,
            place=self.place,
            date=self.date,
            numbers_of_tours=int(self.numbers_of_tours),
            time_control=self.time_control,
            description=self.description,
            players=self.players,
            rating_table={},
        )
        _TOOLS.message_success("Le tournoi à été crée.")

    def start_tournament(self):
        confirm = _TOOLS.print_message("\nSouhaitez-vous commencer le tournoi ?")

        if confirm:
            PlayMenu(tournament_id=self.create_tournament_id)
        else:
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)


class EditTournamentMenu:

    def __int__(self, tournament_id: int = None):
        _TOOLS.print_title("Modification d'un tournoi")
        self.show_tournaments(tournament_id=tournament_id)

        if self.tournament_choice is None:
            _TOOLS.error_message("Aucun tournoi crée.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.original_tournament_copy = deepcopy(self.tournament_choice)

        if self.edited_tournament():
            self.confirm_modification()
            self.save_tournament()
        else:
            _TOOLS.message_success("aucune modification effectuée.")

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

        self.select_tournament_to_edit()

    @classmethod
    def show_tournaments(cls, tournament_id: int = None):
        """Gère l'éventuel identifiant de tournoi passé à l'instanciation."""
        tournament_exists = MainDatabase().util.if_tournament_id_in_database(tournament_id=tournament_id)

        if tournament_id is not None and not tournament_exists:
            _TOOLS.error_message(f"le tournoi n°{tournament_id} n'est pas disponible.")

        if tournament_id is not None and tournament_exists:
            cls.tournament_choice = MainDatabase().util.get_tournament_from_id_str(
                tournament_id=int(tournament_id)
            )
        else:
            cls.tournament_choice = cls.tournament_choice()

    def select_tournament_to_edit(self):
        """Enumerate tous les paramètres du tournoi et demande à les modifier."""

        _TOOLS.print_info("les informations actuelles du tournoi")

        self.tournament_choice.name = _TOOLS.edit_prompt(field_title="Nom", value=self.tournament_choice.name)
        self.tournament_choice.place = _TOOLS.edit_prompt(
            field_title="Lieu", value=self.tournament_choice.place
        )
        self.tournament_choice.date = _TOOLS.edit_prompt(field_title="Date", value=self.tournament_choice.date)
        self.tournament_choice.description = _TOOLS.edit_prompt(
            field_title="Description", value=self.tournament_choice.description
        )

    def edited_tournament(self):
        """Compare l'objet du tournoi sélectionné et la copie originale du tournoi pour déterminer la différence."""
        if self.tournament_choice.name != self.original_tournament_copy.name:
            return True
        elif self.tournament_choice.place != self.original_tournament_copy.place:
            return True
        elif self.tournament_choice.date != self.original_tournament_copy.date:
            return True
        elif self.tournament_choice.description != self.original_tournament_copy.description:
            return True
        else:
            return False

    def confirm_modification(self):
        self.show_tournament()

        confirm = _TOOLS.print_message("\nSouhaitez vous confirmer la modification de ce tournoi ?")
        if not confirm:
            _TOOLS.error_message("annulation. Le tournoi n'a pas été modifié.")
            raise Exit

    def show_tournament(self):
        _TOOLS.print_info("nouvelle information du tournoi")
        parameter = _TOOLS.print_message("Nom: ")
        print(parameter + self.tournament_choice.name)
        parameter = _TOOLS.print_message("Lieu: ")
        print(parameter + self.tournament_choice.place)
        parameter = _TOOLS.print_message("Date: ")
        print(parameter + self.tournament_choice.date)
        parameter = _TOOLS.print_message("Description: ")
        print(parameter + self.tournament_choice.description)

    def save_tournament(self):
        """ Utiliser la classe MainDatabase pour modifier le tournoi"""
        self.tournament_choice.players = [x.id_number for x in self.tournament_choice.players]

        MainDatabase().create_tournament(
            name=self.tournament_choice.name,
            place=self.tournament_choice.place,
            date=self.tournament_choice.date,
            numbers_of_tours=int(self.tournament_choice.numbers_of_tours),
            time_control=self.tournament_choice.time_control,
            description=self.tournament_choice.description,
            players=self.tournament_choice.players,
            rating_table=self.tournament_choice.rating_table,
            is_round_ended=self.tournament_choice.is_round_ended,
            id_number=self.tournament_choice.id_number
        )

        _TOOLS.message_success(f"le tournoi n°{str(self.tournament_choice.id_number)} a été modifié.")

    @classmethod
    def tournament_choice(cls):
        """Prompts the user to select a tournament in database."""
        if MainDatabase().util.if_player_in_database_empty():
            return None
        cls.tournaments_all_list()

        choice = ""
        while not cls.tournament_exists(choose_id=choice):
            choice = _TOOLS.print_message("Choisir un tournoi")
        return MainDatabase().util.get_tournament_by_id_string(tournament_id=choice)

    @staticmethod
    def tournaments_all_list():
        """Listes de tous les tournois existants."""
        if MainDatabase().util.if_tournament_in_database_empty():
            print("Aucun tournoi créé.")
            return
        _TOOLS.print_info("liste des tournois existants:")

        all_tournaments = MainDatabase().util.get_tournaments_by_id()
        for tournament in all_tournaments:
            if tournament.is_round_ended:
                is_round_ended = _TOOLS.print_message(" -> Terminé")
            else:
                is_round_ended = ""
            print(f"{tournament.id_number}. {tournament.name} - {tournament.date}" + is_round_ended)

    @staticmethod
    def tournament_exists(choose_id: str):
        """Verifies if the tournament selected by the user exists."""

        if len(choose_id) == 0:
            return False
        if not choose_id.isnumeric():
            _TOOLS.error_message("entrez le numéro du tournoi devant son nom")
            return False
        if MainDatabase().util.if_tournament_id_in_database(tournament_id=int(choose_id)):
            return True
        _TOOLS.error_message(f"pas de tournoi avec le numéro {choose_id}")
        return False


class DeleteTournamentMenu:

    def __int__(self, tournament_id: int = None):
        _TOOLS.print_title("suppression d'un tournoi")

        self.show_tournaments(tournament_id=tournament_id)

        if self.tournament_choose is None:
            _TOOLS.error_message("aucun tournoi créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.confirm_tournament_creation()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def show_tournaments(cls, tournament_id: int = None):
        tournament_exists = MainDatabase().util.if_tournament_id_in_database(tournament_id=tournament_id)

        if tournament_id is not None and not tournament_exists:
            _TOOLS.error_message(f"le tournoi n°{tournament_id} n'est pas disponible.")

        if tournament_id is not None and tournament_exists:
            cls.tournament_choose = MainDatabase().util.get_tournament_by_id_string(
                tournament_id=tournament_id
            )
        else:
            cls.tournament_choose = EditTournamentMenu().tournament_choice()

    def confirm_tournament_creation(self):
        _TOOLS.alert_message(f"Vous allez supprimer définitivement le tournoi '{self.tournament_choose.name}'")
        confirm = _TOOLS.print_message("Confirmez-vous la suppression ?")
        if confirm:
            self.delete_tournament()
        else:
            print("\n Le tournoi n'a pas été supprimé")

    def delete_tournament(self):
        MainDatabase().delete_tournament(tournament=self.tournament_choose)
