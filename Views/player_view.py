import typer

from copy import deepcopy

from controller.main_database import MainDatabase
import views.tools as _TOOLS


class PlayerMenu:
    """Vue pour les opérations liées au joueur."""

    def __init__(self):
        """Constructeur pour PlayerMenu."""
        _TOOLS.print_title("menu des joueurs")
        self.print_menu()
        self.user_choice_selection()

    @staticmethod
    def print_menu():
        """Affiche les différentes options du menu."""
        choice = typer.style("1. ")
        typer.echo(f"{choice}Créer un nouveau joueur")
        choice = typer.style("2. ")
        typer.echo(f"{choice}Modifier un joueur")
        choice = typer.style("3. ")
        typer.echo(f"{choice}Supprimer un joueur")
        choice = typer.style("4. ")
        typer.echo(f"{choice}Afficher tous les joueurs")
        choice = typer.style("\n0. ")
        typer.echo(f"{choice}Retour")

    def user_choice_selection(self):
        """Invite l'utilisateur à sélectionner une option."""
        user_choice = typer.prompt("\nEntrez votre sélection ")
        if user_choice == "0":
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif user_choice == "1":
            typer.echo("\n\n")
            NewPlayerMenu()
        elif user_choice == "2":
            typer.echo("\n\n")
            EditPlayerMenu()
        elif user_choice == "3":
            typer.echo("\n\n")
            DeletePlayerMenu()
        elif user_choice == "4":
            typer.echo("\n\n")
            _TOOLS.players_all_list()
            typer.echo("\n")
            self.user_choice_selection()
        else:
            self.user_choice_selection()


class NewPlayerMenu:
    """Vue pour la création d'un nouveau joueur."""

    def __init__(self):
        """Constructeur pour le NewPlayerMenu."""
        _TOOLS.print_title("création d'un joueur")
        self.first_name = ""
        self.last_name = ""
        self.date_of_birth = ""
        self.gender = ""
        self.rating = ""

        self.user_settings_prompt()
        self.confirm_player_settings()
        self.save_player()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def user_settings_prompt(self):
        """Invite l'utilisateur à saisir les différents paramètres du lecteur."""
        _TOOLS.print_info("entrez les informations du joueur")
        while len(self.first_name) == 0:
            self.first_name = typer.prompt("Prénom du joueur")
        while len(self.last_name) == 0:
            self.last_name = typer.prompt("Nom de famille du joueur")
        while not _TOOLS.date_is_valid(date=self.date_of_birth):
            self.date_of_birth = typer.prompt("Date de naissance (JJ-MM-AAAA)")
        while not _TOOLS.gender_is_valid(gender=self.gender):
            self.gender = typer.prompt("Genre (H/F)")
        while not self.rating.isnumeric():
            self.rating = typer.prompt("Rating")

    def confirm_player_settings(self):
        """Invite l'utilisateur à confirmer les paramètres précédemment saisis.
            typer.Exit : Quitte si l'utilisateur annule la création.
        """
        self.listing_player_settings()
        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce joueur ?")
        if not confirm:
            _TOOLS.print_error("annulation. Le joueur n'a pas été créé.")
            raise typer.Exit

    def listing_player_settings(self):
        """Affiche tous les paramètres du lecteur précédemment saisis."""
        _TOOLS.print_info("informations du joueur:")
        parameter = typer.style("Prénom: ")
        typer.echo(parameter + self.first_name)
        parameter = typer.style("Nom de famille: ")
        typer.echo(parameter + self.last_name)
        parameter = typer.style("Date de naissance: ")
        typer.echo(parameter + self.date_of_birth)
        parameter = typer.style("Genre: ")
        typer.echo(parameter + self.gender)
        parameter = typer.style("Rating: ")
        typer.echo(parameter + str(self.rating))

    def save_player(self):
        """Utilise le gestionnaire de base de données pour enregistrer le lecteur créé."""
        created_player_id = MainDatabase().create_player(
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth,
            gender=self.gender,
            rating=int(self.rating),
        )
        _TOOLS.print_success(f"le joueur a été créé avec le numéro {created_player_id}.")


class EditPlayerMenu:
    """Vue pour l'édition du joueur.
        selected_player (Joueur) : Le joueur sélectionné par l'utilisateur pour être édité.
        original_player_copy (Joueur) :
         Copie profonde de l'état initial du lecteur pour vérification de la modification.
    """

    def __init__(self, player_id: int = None):
        """Constructeur pour EditPlayerMenu.
                   player_id (int, facultatif) : Identifiant facultatif du lecteur à charger.
                    La valeur par défaut est None.
               """
        _TOOLS.print_title("modification d'un joueur")
        self.user_select_parameter(player_id=str(player_id))
        if self.selected_player is None:
            _TOOLS.print_error("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.original_player_copy = deepcopy(self.selected_player)
        self.edit_player_selection()
        if self.is_player_edited():
            self.confirm_player_settings()
            self.save_player()
        else:
            _TOOLS.print_success("aucune modification effectuée.")
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def user_select_parameter(cls, player_id: str):
        """Gère l'éventuel identifiant du joueur passé à l'instanciation.
            player_id (str) : Identifiant facultatif du joueur à charger.
        """
        player_exists = MainDatabase().util.is_player_id_in_database(player_id=player_id)
        if player_id is not None and not player_exists:
            _TOOLS.print_error(f"le joueur n°{player_id} n'est pas disponible.")
        if player_id is not None and player_exists:
            cls.selected_player = MainDatabase().util.get_player_object_from_id_str(player_id=player_id)
        else:
            cls.selected_player = _TOOLS.player_choice()

    def edit_player_selection(self):
        """Enumère tous les paramètres du joueur et demande de les modifier."""
        _TOOLS.print_info("informations actuelles du joueur:")
        self.selected_player.first_name = _TOOLS.edit_prompt(
            field_title="Prénom", value=self.selected_player.first_name)
        self.selected_player.last_name = _TOOLS.edit_prompt(
            field_title="Nom de famille", value=self.selected_player.last_name)
        self.selected_player.date_of_birth = _TOOLS.edit_prompt(field_title="Date de naissance",
                                                                value=self.selected_player.date_of_birth)
        self.selected_player.gender = _TOOLS.edit_prompt(field_title="Genre", value=self.selected_player.gender)
        self.selected_player.rating = _TOOLS.edit_prompt(field_title="Rating", value=str(self.selected_player.rating))

    def is_player_edited(self):
        """Compare l'objet du joueur sélectionné et la copie originale du joueur pour déterminer la différence.
            bool : Les attributs du joueur ont été modifiés.
        """
        if self.selected_player.first_name != self.original_player_copy.first_name:
            return True
        elif self.selected_player.last_name != self.original_player_copy.last_name:
            return True
        elif self.selected_player.date_of_birth != self.original_player_copy.date_of_birth:
            return True
        elif self.selected_player.gender != self.original_player_copy.gender:
            return True
        elif int(self.selected_player.rating) != self.original_player_copy.rating:
            return True
        else:
            return False

    def confirm_player_settings(self):
        """Invite l'utilisateur à confirmer les paramètres précédemment saisis.
                   typer.Exit : Quitte si l'utilisateur annule la création.
               """
        self.listing_player_settings()
        confirm = typer.confirm("\nSouhaitez vous confirmer la modification de ce joueur ?")
        if not confirm:
            _TOOLS.print_error("annulation. Le joueur n'a pas été modifié.")
            raise typer.Exit

    def listing_player_settings(self):
        """Displays all previously entered player settings."""
        _TOOLS.print_info("nouvelles informations du joueur:")
        parameter = typer.style("Prénom: ")
        typer.echo(parameter + self.selected_player.first_name)
        parameter = typer.style("Nom de famille: ")
        typer.echo(parameter + self.selected_player.last_name)
        parameter = typer.style("Date de naissance: ")
        typer.echo(parameter + self.selected_player.date_of_birth)
        parameter = typer.style("Genre: ")
        typer.echo(parameter + self.selected_player.gender)
        parameter = typer.style("Rating: ")
        typer.echo(parameter + str(self.selected_player.rating))

    def save_player(self):
        """Utilise le gestionnaire de base de données pour sauvegarder le lecteur édité."""
        MainDatabase().create_player(
            first_name=self.selected_player.first_name,
            last_name=self.selected_player.last_name,
            date_of_birth=self.selected_player.date_of_birth,
            gender=self.selected_player.gender,
            rating=self.selected_player.rating,
            id_num=self.selected_player.id_number,
        )
        _TOOLS.print_success(f"le joueur n°{str(self.selected_player.id_number)} a été modifié.")


class DeletePlayerMenu:
    """Vue pour la suppression d'un joueur
        selected_player (Joueur) : Joueur sélectionné par l'utilisateur pour être supprimé.
    """

    def __init__(self, player_id: int = None):
        """Constructeur pour DeletePlayerMenu.
            player_id (int, facultatif) : Identifiant facultatif du joueur à charger. La valeur par défaut est None.
        """
        _TOOLS.print_title("suppression d'un joueur")
        self.user_select_parameter(player_id=str(player_id))
        if self.selected_player is None:
            _TOOLS.print_error("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.confirm_user_selection()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def user_select_parameter(cls, player_id: str):
        """Gère l'éventuel identifiant du joueur passé à l'instanciation.
            player_id (str) : Identifiant facultatif du joueur à charger.
        """
        player_exists = MainDatabase().util.is_player_id_in_database(player_id=player_id)
        if player_id is not None and not player_exists:
            _TOOLS.print_error(f"le joueur n°{player_id} n'est pas disponible.")
        if player_id is not None and player_exists:
            cls.selected_player = MainDatabase().util.get_player_object_from_id_str(player_id=player_id)
        else:
            cls.selected_player = _TOOLS.player_choice()

    def confirm_user_selection(self):
        """Prompts the user to confirm user deletion."""
        _TOOLS.print_warning(
            "vous allez supprimer définitivement '{first_name} {last_name}'".format(
                first_name=self.selected_player.first_name, last_name=self.selected_player.last_name
            )

        )

        if confirm := typer.confirm("Confirmer la suppression ?"):
            self.delete_player()
        else:
            _TOOLS.print_success("l'utilisateur n'a pas été supprimé.")

    def delete_player(self):
        """Uses database handler to delete player."""
        MainDatabase().delete_player(player=self.selected_player)
