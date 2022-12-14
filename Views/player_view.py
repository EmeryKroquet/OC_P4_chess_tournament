from copy import deepcopy

import typer

import tools.tools as _TOOLS
from Controllers.main_database import MainDatabase


class PlayerMenu:
    """Vue pour les opérations liées au joueur."""

    def __init__(self):
        """Constructeur pour Player Menu."""

        _TOOLS.print_title("menu des joueurs")

        self.main_menu()
        self.player_user_choice()

    @staticmethod
    def main_menu():
        """Affiche les différentes options du menu."""
        user_choice = "1. "
        print(user_choice + "Créer un nouveau joueur")

        user_choice = "2. "
        print(user_choice + "Modifier un joueur")

        user_choice = "3. "
        print(user_choice + "Supprimer un joueur")

        user_choice = "4. "
        print(user_choice + "Afficher tous les joueurs")

        user_choice = "\n0. "
        print(user_choice + "Retour au menu")

    def player_user_choice(self):
        """Invite l'utilisateur à sélectionner une option."""
        choice = input("\nEntrez votre choix: ")

        if choice == "0":
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif choice == "1":
            print("\n\n")
            NewPlayerMenu()
        elif choice == "2":
            print("\n\n")
            EditPlayerMenu()
        elif choice == "3":
            print("\n\n")
            DeletePlayerMenu()
        elif choice == "4":
            print("\n\n")
            _TOOLS.players_all_list()
            print("\n")
            self.player_user_choice()
        else:
            self.player_user_choice()


class NewPlayerMenu:
    def __init__(self):
        """Constructeur pour le New Player Menu."""
        _TOOLS.print_title("création d'un joueur")

        self.first_name = ""
        self.last_name = ""
        self.date_of_birth = ""
        self.gender = ""
        self.rating = ""

        self.display_menu()
        self.confirm_player_creation()
        self.save_player()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def display_menu(self):  # creation de joueur
        while len(self.first_name) == 0:
            self.first_name = input("Prénom du joueur: ")

        while len(self.last_name) == 0:
            self.last_name = input("Nom de famille du joueur: ")

        while not _TOOLS.date_valid(date=self.date_of_birth):
            self.date_of_birth = input("Date de naissance (DD-MM-YYYY): ")

        while not _TOOLS.gender_is_valid(gender=self.gender):
            self.gender = input("Genre (H/F): ")

        while not self.rating.isnumeric():
            self.rating = input("Rating: ")

    def confirm_player_creation(self):

        self.show_player()

        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce joueur ?")
        if not confirm:
            _TOOLS.error_message("annulation. Le joueur n'a pas été créé.")
            raise SystemExit

    def show_player(self):
        _TOOLS.print_info("Informations du joueur:")

        parameter = "Prénom: "
        print(parameter + self.first_name)
        parameter = "Nom de famille: "
        print(parameter + self.last_name)
        parameter = "Date de naissance: "
        print(parameter + self.date_of_birth)
        parameter = "Genre: "
        print(parameter + self.gender)
        parameter = "Rating: "
        print(parameter + str(self.rating))

    def save_player(self):
        """Utilise le gestionnaire de données pour sauvegarder le joueur créé."""
        player_id = MainDatabase().create_player(
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth,
            gender=self.gender,
            rating=int(self.rating)
        )
        _TOOLS.message_success(f"le joueur a été créé avec le numéro {player_id}.")


class EditPlayerMenu:

    def __init__(self, player_id: int = None):
        """Constructeur pour EditPlayerMenu."""

        _TOOLS.print_title("modification d'un joueur")
        self.show_players_list(player_id=str(player_id))
        if self.player_choice is None:
            _TOOLS.error_message("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.original_player_copy = deepcopy(self.player_choice)
        self.select_player_to_edite()
        if self.is_player_edited():
            self.confirm_player_creation()
            self.save_player()
        else:
            _TOOLS.message_success("aucune modification effectuée.")

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def show_players_list(cls, player_id: str):
        """Gère l'éventuel identifiant du joueur passé à l'instanciation. """
        exists_player = MainDatabase().util.if_payer_id_in_database(player_id=player_id)

        if player_id is not None and not exists_player:
            _TOOLS.error_message(f"le joueur n°{player_id} n'est pas disponible.")

        if player_id is not None and exists_player:
            cls.player_choice = MainDatabase().util.get_player_by_id_string(player_id=str(player_id))
        else:
            cls.player_choice = _TOOLS.player_choice()

    def select_player_to_edite(self):
        """Enumèrer tous les paramètres du joueur et demande de les modifier."""
        _TOOLS.print_info("informations actuelles du joueur:")
        self.player_choice.first_name = _TOOLS.edit_prompt(
            field_title="Prénom", value=self.player_choice.first_name)

        self.player_choice.last_name = _TOOLS.edit_prompt(
            field_title="Nom de famille", value=self.player_choice.last_name)
        self.player_choice.date_of_birth = _TOOLS.edit_prompt(field_title="Date of Birth",
                                                              value=self.player_choice.date_of_birth)
        self.player_choice.gender = _TOOLS.edit_prompt(field_title="Genre",
                                                       value=self.player_choice.gender)
        self.player_choice.rating = _TOOLS.edit_prompt(field_title="Rating",
                                                       value=str(self.player_choice.rating))

    def is_player_edited(self):
        """Compare l'objet du joueur sélectionné et la copie originale
            du joueur pour voir la différence.
        """
        if self.player_choice.first_name != self.original_player_copy.first_name:
            return True
        elif self.player_choice.last_name != self.original_player_copy.last_name:
            return True
        elif self.player_choice.date_of_birth != self.original_player_copy.date_of_birth:
            return True
        elif self.player_choice.gender != self.original_player_copy.gender:
            return True
        elif int(self.player_choice.rating) != self.original_player_copy.rating:
            return True
        else:
            return False

    def confirm_player_creation(self):
        """Invite l'utilisateur à confirmer les paramètres précédemment saisis. """
        self.show_player()
        confirm = typer.confirm("\nSouhaitez vous confirmer la modification de ce joueur ?")
        if not confirm:
            _TOOLS.error_message("annulation. Le joueur n'a pas été modifié.")
            raise SystemExit

    def show_player(self):
        """Affiche tous les paramètres du lecteur précédemment saisis."""
        _TOOLS.print_info("nouvelles informations du joueur:")

        parameter = "Prénom: "
        print(parameter + self.player_choice.first_name)
        parameter = "Nom de famille: "
        print(parameter + self.player_choice.last_name)
        parameter = "Date de naissance: "
        print(parameter + self.player_choice.date_of_birth)
        parameter = "Genre: "
        print(parameter + self.player_choice.gender)
        parameter = "Rating: "
        print(parameter + str(self.player_choice.rating))

    def save_player(self):
        """Utilise le gestionnaire de base de données pour sauvegarder le lecteur édité."""
        MainDatabase().create_player(
            first_name=self.player_choice.first_name,
            last_name=self.player_choice.last_name,
            date_of_birth=self.player_choice.date_of_birth,
            gender=self.player_choice.gender,
            rating=self.player_choice.rating,
            id_number=self.player_choice.id_number,
        )
        _TOOLS.message_success(f"le joueur n°{str(self.player_choice.id_number)} a été modifié.")


class DeletePlayerMenu:
    """Vue pour la suppression du joueur"""

    def __init__(self, player_id: int = None):
        """Constructeur pour DeletePlayerMenu."""
        _TOOLS.print_title("suppression d'un joueur")
        self.show_payers_list(player_id=str(player_id))
        if self.choose_player is None:
            _TOOLS.error_message("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.confirm_player_selection_to_delete()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def show_payers_list(cls, player_id: str):
        """Gère l'éventuel identifiant du joueur passé à l'instanciation."""

        exists_players = MainDatabase().util.if_payer_id_in_database(player_id=player_id)
        if player_id is not None and not exists_players:
            _TOOLS.error_message(f"le joueur n°{player_id} n'est pas disponible.")

        if player_id is not None and exists_players:
            cls.choose_player = MainDatabase().util.get_player_by_id_string(player_id=str(player_id))
        else:
            cls.choose_player = _TOOLS.player_choice()

    def confirm_player_selection_to_delete(self):
        """Demande à l'utilisateur de confirmer la suppression de l'utilisateur."""
        _TOOLS.print_warning(
            f"vous allez supprimer définitivement first name: {self.choose_player.first_name}"
            f"last name: {self.choose_player.last_name}"
        )
        confirm = typer.confirm("Confirmer la suppression ?")
        if confirm:
            self.delete_player()
        else:
            _TOOLS.message_success("l'utilisateur n'a pas été supprimé.")

    def delete_player(self):
        """Utilise le gestionnaire de base de données pour supprimer le lecteur."""
        MainDatabase().delete_player(player=self.choose_player)
