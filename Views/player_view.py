import typer

from copy import deepcopy

from controller.main_database import MainDatabase
import views.tools as _TOOLS


class PlayerMenu:
    """View for player related operations."""

    def __init__(self):
        """Constructor for PlayerMenu."""

        _TOOLS.print_title("menu des joueurs")

        self.print_menu()
        self.user_selection()

    @staticmethod
    def print_menu():
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Créer un nouveau joueur")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Modifier un joueur")

        number = typer.style("3. ", bold=True)
        typer.echo(number + "Supprimer un joueur")

        number = typer.style("4. ", bold=True)
        typer.echo(number + "Afficher tous les joueurs")

        number = typer.style("\n0. ", bold=True)
        typer.echo(number + "Retour")

    def user_selection(self):
        """Prompts the user to select an option."""

        selection = typer.prompt("\nEntrez votre sélection: ")

        if selection == "0":
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
        elif selection == "1":
            typer.echo("\n\n")
            NewPlayerMenu()
        elif selection == "2":
            typer.echo("\n\n")
            EditPlayerMenu()
        elif selection == "3":
            typer.echo("\n\n")
            DeletePlayerMenu()
        elif selection == "4":
            typer.echo("\n\n")
            _TOOLS.players_all_list()
            typer.echo("\n")
            self.user_selection()
        else:
            self.user_selection()


class NewPlayerMenu:
    """View for new player creation.

    Attributes:
        first_name (str): Players's first name.
        last_name (str): Player's last name.
        date_of_birth (str): Player's date of birth.
        gender (str): Player's gender.
        rating (str): Player's ELO ranking.
    """

    def __init__(self):
        """Constructor for NewPlayerMenu."""

        _TOOLS.print_title("création d'un joueur")

        self.first_name = ""
        self.last_name = ""
        self.date_of_birth = ""
        self.gender = ""
        self.rating = ""

        self.settings_prompt()
        self.confirm_settings()
        self.save_player()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def settings_prompt(self):
        """Prompts the user to input the different player settings."""

        _TOOLS.print_info("entrez les informations du joueur")

        while len(self.first_name) == 0:
            self.first_name = typer.prompt("Prénom du joueur")

        while len(self.last_name) == 0:
            self.last_name = typer.prompt("Nom de famille du joueur")

        while not _TOOLS.date_is_valid(date=self.date_of_birth):
            self.date_of_birth = typer.prompt("Date de naissance (JJ/MM/AAAA)")

        while not _TOOLS.gender_is_valid(gender=self.gender):
            self.gender = typer.prompt("Genre (H/F)")

        while not self.rating.isnumeric():
            self.rating = typer.prompt("Rating")

    def confirm_settings(self):
        """Prompts the user to confirm the settings previously entered.

        Raises:
            typer.Exit: Exits if the user cancels the creation.
        """

        self.list_settings()

        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce joueur ?")
        if not confirm:
            _TOOLS.print_error("annulation. Le joueur n'a pas été créé.")
            raise typer.Exit

    def list_settings(self):
        """Displays all previously entered player settings."""

        _TOOLS.print_info("informations du joueur:")

        parameter = typer.style("Prénom: ", bold=True)
        typer.echo(parameter + self.first_name)
        parameter = typer.style("Nom de famille: ", bold=True)
        typer.echo(parameter + self.last_name)
        parameter = typer.style("Date de naissance: ", bold=True)
        typer.echo(parameter + self.date_of_birth)
        parameter = typer.style("Genre: ", bold=True)
        typer.echo(parameter + self.gender)
        parameter = typer.style("Rating: ", bold=True)
        typer.echo(parameter + str(self.rating))

    def save_player(self):
        """Uses database handler to save created player."""

        created_player_id = MainDatabase().create_player(
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth,
            gender=self.gender,
            rating=int(self.rating),
        )

        _TOOLS.print_success(f"le joueur a été créé avec le numéro {created_player_id}.")


class EditPlayerMenu:
    """View for player editing.

    Attributes:
        selected_player (Player): Player selected by user for edit.
        original_player_copy (Player): Deep copy of initial Player state for modification check.
    """

    def __init__(self, player_id: int = None):
        """Constructor for EditPlayerMenu.

        Args:
            player_id (int, optional): Optional player id to be loaded. Defaults to None.
        """

        _TOOLS.print_title("modification d'un joueur")

        self.cli_argument_handler(player_id=str(player_id))

        if self.selected_player is None:
            _TOOLS.print_error("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.original_player_copy = deepcopy(self.selected_player)

        self.select_edit()

        if self.is_player_edited():
            self.confirm_settings()
            self.save_player()
        else:
            _TOOLS.print_success("aucune modification effectuée.")

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def cli_argument_handler(cls, player_id: str):
        """Handles eventual player id passed at instantiation.

        Args:
            player_id (str): Optional player id to be loaded.
        """

        player_exists = MainDatabase().util.is_player_id_in_database(player_id=player_id)

        if player_id is not None and not player_exists:
            _TOOLS.print_error(f"le joueur n°{player_id} n'est pas disponible.")

        if player_id is not None and player_exists:
            cls.selected_player = MainDatabase().util.get_player_object_from_id_str(player_id=str(player_id))
        else:
            cls.selected_player = _TOOLS.player_choice()

    def select_edit(self):
        """Enumerates all player's settings and asks for edit."""

        _TOOLS.print_info("informations actuelles du joueur:")

        self.selected_player.first_name = _TOOLS.edit_prompt(
            field_title="Prénom", value=self.selected_player.first_name
        )
        self.selected_player.last_name = _TOOLS.edit_prompt(
            field_title="Nom de famille", value=self.selected_player.last_name
        )
        self.selected_player.date_of_birth = _TOOLS.edit_prompt(field_title="Date de naissance", value=self.selected_player.date_of_birth)
        self.selected_player.gender = _TOOLS.edit_prompt(field_title="Genre", value=self.selected_player.gender)
        self.selected_player.rating = _TOOLS.edit_prompt(field_title="Rating", value=str(self.selected_player.rating))

    def is_player_edited(self):
        """Compares selected player object and original player copy for difference.

        Returns:
            bool: The Player attributes were modified.
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

    def confirm_settings(self):
        """Prompts the user to confirm the settings previously entered.

        Raises:
            typer.Exit: Exits if the user cancels the creation.
        """

        self.list_settings()

        confirm = typer.confirm("\nSouhaitez vous confirmer la modification de ce joueur ?")
        if not confirm:
            _TOOLS.print_error("annulation. Le joueur n'a pas été modifié.")
            raise typer.Exit

    def list_settings(self):
        """Displays all previously entered player settings."""

        _TOOLS.print_info("nouvelles informations du joueur:")

        parameter = typer.style("Prénom: ", bold=True)
        typer.echo(parameter + self.selected_player.first_name)
        parameter = typer.style("Nom de famille: ", bold=True)
        typer.echo(parameter + self.selected_player.last_name)
        parameter = typer.style("Date de naissance: ", bold=True)
        typer.echo(parameter + self.selected_player.date_of_birth)
        parameter = typer.style("Genre: ", bold=True)
        typer.echo(parameter + self.selected_player.gender)
        parameter = typer.style("Rating: ", bold=True)
        typer.echo(parameter + str(self.selected_player.rating))

    def save_player(self):
        """Uses database handler to save edited player."""

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
    """View for player deletion

    Attributes:
        selected_player (Player): Player selected by user for deletion.
    """

    def __init__(self, player_id: int = None):
        """Constructor for DeletePlayerMenu.

        Args:
            player_id (int, optional): Optional player id to be loaded. Defaults to None.
        """

        _TOOLS.print_title("suppression d'un joueur")

        self.cli_argument_handler(player_id=str(player_id))

        if self.selected_player is None:
            _TOOLS.print_error("aucun joueur créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.confirm_selection()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def cli_argument_handler(cls, player_id: str):
        """Handles eventual player id passed at instantiation.

        Args:
            player_id (str): Optional player id to be loaded.
        """

        player_exists = MainDatabase().util.is_player_id_in_database(player_id=str(player_id))

        if player_id is not None and not player_exists:
            _TOOLS.print_error(f"le joueur n°{player_id} n'est pas disponible.")

        if player_id is not None and player_exists:
            cls.selected_player = MainDatabase().util.get_player_object_from_id_str(player_id=str(player_id))
        else:
            cls.selected_player = _TOOLS.player_choice()

    def confirm_selection(self):
        """Prompts the user to confirm user deletion."""

        _TOOLS.print_warning(
            "vous allez supprimer définitivement '{first_name} {last_name}'".format(
                first_name=self.selected_player.first_name, last_name=self.selected_player.last_name
            )

        )

        confirm = typer.confirm("Confirmer la suppression ?")

        if confirm:
            self.delete_player()
        else:
            _TOOLS.print_success("l'utilisateur n'a pas été supprimé.")

    def delete_player(self):
        """Uses database handler to delete player."""

        MainDatabase().delete_player(player=self.selected_player)
