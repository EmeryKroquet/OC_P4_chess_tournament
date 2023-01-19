import typer

from copy import deepcopy

import views.game as _GameMenu
from controller.main_database import MainDatabase
import views.tools as _TOOLS


class TournamentMenu:
    """View for tournament related operations."""

    def __init__(self):
        """Constructor for TournamentMenu."""
        _TOOLS.print_title("menu des tournois")

        self.print_menu()
        self.user_selection()

    @classmethod
    def print_menu(cls):
        """Displays the different menu options."""

        number = typer.style("1. ")
        typer.echo(f"{number}Reprendre un tournoi")

        number = typer.style("2. ")
        typer.echo(f"{number}Créer un nouveau tournoi")

        number = typer.style("3. ")
        typer.echo(f"{number}Modifier un tournoi")

        number = typer.style("4. ")
        typer.echo(f"{number}Supprimer un tournoi")

        number = typer.style("5. ")
        typer.echo(f"{number}Afficher tous les tournois")

        number = typer.style("\n0. ")
        typer.echo(f"{number}Retour")

    @classmethod
    def user_selection(cls):
        """Prompts the user to select an option."""
        selection = typer.prompt("Entrez votre sélection: ")

        if selection == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=cls.__class__.__name__)
        elif selection == "1":
            typer.echo("\n\n")
            LoadTournamentMenu()
        elif selection == "2":
            typer.echo("\n\n")
            NewTournamentMenu()
        elif selection == "3":
            typer.echo("\n\n")
            EditTournamentMenu()
        elif selection == "4":
            typer.echo("\n\n")
            DeleteTournamentMenu()
        elif selection == "5":
            typer.echo("\n\n")
            _TOOLS.tournaments_all_list()
            typer.echo("\n")
            cls.user_selection()
        else:
            cls.user_selection()


class LoadTournamentMenu:
    """View displayed for tournament loading.
    Attributes:
        available_tournaments (list): Unfinished tournaments available for loading.
    """

    def __init__(self, tournament_id: int = None):
        """Constructor for LoadTournamentMenu.
        Args:
            tournament_id (int, optional): Optional tournament id to be loaded. Defaults to None.
        """

        _TOOLS.print_title("chargement d'un tournoi")

        self.available_tournaments = MainDatabase().util.get_unfinished_tournaments()

        self.cli_argument_handler(tournament_id=tournament_id)

        self.display_unfinished_tournaments()

        if len(self.available_tournaments) == 0:
            _TOOLS.print_error("aucun tournoi en cours.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.user_selection()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def cli_argument_handler(self, tournament_id: int = None):
        """Handles eventual tournament id passed at instantiation.
        Args:
            tournament_id (str): Optional tournament id to be loaded.
        """
        if tournament_id is not None:
            tournament_is_available = (
                    MainDatabase().util.get_tournament_object_from_id_str(tournament_id=tournament_id)
                    in self.available_tournaments
            )

            if not tournament_is_available:
                _TOOLS.print_error(
                    f"le tournoi n°{tournament_id} n'est pas disponible.",
                )
            else:
                self.start_tournament(tournament_id=tournament_id)
                _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def display_unfinished_tournaments(self):
        """Uses database handler to find and display unfinished tournament for the user to choose from."""
        for tournament in self.available_tournaments:
            typer.secho(f" - Tournoi n°{tournament.id_number} -", fg=typer.colors.CYAN)
            parameter = typer.style("Nom: ", bold=True)
            typer.echo(parameter + tournament.name)
            parameter = typer.style("Date: ", bold=True)
            typer.echo(parameter + tournament.date + "\n")

    def user_selection(self):
        """Prompts the user to select a tournament to be loaded."""
        selection = typer.prompt("Entrez un numéro de tournoi")

        available_ids = [x.id_number for x in self.available_tournaments]
        while not selection.isnumeric() or int(selection) not in available_ids:
            _TOOLS.print_error(f"pas de tournoi avec le numéro {selection}")
            self.user_selection()
            return
        self.start_tournament(int(selection))

    @classmethod
    def start_tournament(cls, tournament_id):
        """Opens the Game Menu for selected tournament.
        Args:
            tournament_id (int): Unique id of the tournament to be loaded.
        """
        _GameMenu.GameMenu(tournament_id)


class NewTournamentMenu:
    """View for new tournament creation.

    Attributes:
        tournament_name (str): Name of the tournament.
        place (str): Location of the tournament.
        date (str): Date of the tournament.
        number_of_rounds (str): Number of tours to be played.
        time_control (str): Type of time control.
        description (str): Description of the tournament.
        created_tournament_id (int): Unique id of the created tournament.
    """

    def __init__(self):
        """Constructor for NewTournamentMenu."""

        _TOOLS.print_title("création d'un tournoi")

        self.tournament_name = ""
        self.place = ""
        self.date = ""
        self.number_of_rounds = ""
        self.time_control = ""
        self.description = ""
        self.players = []
        self.created_tournament_id = None

        self.settings_prompt()
        self.add_players()
        self.confirm_settings()
        self.save_tournament()
        self.start_tournament()

    def settings_prompt(self):
        """Prompts the user to input the different tournament settings."""

        _TOOLS.print_info("entrez les informations du tournoi.")
        while len(self.tournament_name) == 0:
            self.tournament_name = typer.prompt("Nom du tournoi")
        while len(self.place) == 0:
            self.place = typer.prompt("Lieu")
        while not _TOOLS.date_is_valid(date=self.date):
            self.date = typer.prompt("Date (JJ-MM-AAAA)")
        while not self.number_of_rounds.isnumeric():
            self.number_of_rounds = typer.prompt("Nombre de round")
        while not self.valid_time_control():
            self.time_control = typer.prompt("Contrôle du temps")
        while len(self.description) == 0:
            self.description = typer.prompt("Description")

    def add_players(self):
        """Prompts the user to select the participating players."""
        typer.secho("\nEntrez le numéro d'un joueur à ajouter\n")
        _TOOLS.players_all_list()
        while len(self.players) < 8:
            selection = typer.prompt(f"Joueur ({len(self.players)}/8)")
            if _TOOLS.player_exists(choose_id=selection, players_ids=self.players):
                self.players.append(int(selection))

    def valid_time_control(self):
        """Vérifie si le type de contrôle horaire saisi par l'utilisateur est valide.
        Retourne :
            bool : Le contrôle horaire est valide.
        """
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
                _TOOLS.print_error("entrée incorrect. Entrez Bullet, Blitz ou Coup Rapide.")
            return False

    def confirm_settings(self):
        """Prompts the user to confirm the settings previously entered.
        Raises:
            typer.Exit: Exits if the user cancels the creation.
        """
        self.list_settings()
        self.list_participating_players()

        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce tournoi ?")
        if not confirm:
            _TOOLS.print_error("annulation. Le tournoi n'a pas été créé.")
            raise SystemExit

    def list_settings(self):
        """Displays all previously entered tournament settings."""
        _TOOLS.print_info("paramètres du tournoi:")
        parameter = typer.style("Nom: ")
        typer.echo(parameter + self.tournament_name)
        parameter = typer.style("Lieu: ")
        typer.echo(parameter + self.place)
        parameter = typer.style("Date: ")
        typer.echo(parameter + self.date)
        parameter = typer.style("Nombre de tours: ")
        typer.echo(parameter + self.number_of_rounds)
        parameter = typer.style("Contrôle du temps: ")
        typer.echo(parameter + self.time_control)
        parameter = typer.style("Description: ")
        typer.echo(parameter + self.description)

    def list_participating_players(self):
        """Displays selected participating players by their name."""
        _TOOLS.print_info("liste des joueurs: ")
        players_name = MainDatabase().util.get_players_names(players_sample=self.players)
        for name in players_name:
            typer.echo(f" - {name}")

    def save_tournament(self):
        """Uses database handler to save created tournament."""

        self.created_tournament_id = MainDatabase().create_tournament(
            name=self.tournament_name,
            place=self.place,
            date=self.date,
            number_of_rounds=int(self.number_of_rounds),
            time_control=self.time_control,
            description=self.description,
            players=self.players,
            rating_table={},
        )
        _TOOLS.print_success("le tournoi a été créé.")

    def start_tournament(self):
        """Starts created tournament if the user select so."""
        if confirm := typer.confirm("\nSouhaitez vous commencer le tournoi ?"):
            _GameMenu.GameMenu(tournament_id=self.created_tournament_id)
        else:
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)


class EditTournamentMenu:
    """View for tournament editing.
    Attributes:
        selected_tournament (Tournament): Tournament selected by user for edit.
        original_tournament_copy (Tournament): Deep copy of initial Tournament state for modification check.
    """
    def __init__(self, tournament_id: int = None):
        """Constructor for EditTournamentMenu.
        Args:
            tournament_id (int, optional): Optional tournament id to be loaded. Defaults to None.
        """
        _TOOLS.print_title("modification d'un tournoi")
        self.cli_argument_handler(tournament_id=tournament_id)
        if self.selected_tournament is None:
            _TOOLS.print_error("aucun tournoi créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.original_tournament_copy = deepcopy(self.selected_tournament)
        self.select_edit()
        if self.is_tournament_edited():
            self.confirm_settings()
            self.save_tournament()
        else:
            _TOOLS.print_success("aucune modification effectuée.")
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def cli_argument_handler(cls, tournament_id: int = None):
        """Handles eventual tournament id passed at instantiation.
        Args:
            tournament_id (str): Optional tournament id to be loaded.
        """
        tournament_exists = MainDatabase().util.is_tournament_id_in_database(tournament_id=tournament_id)
        if tournament_id is not None and not tournament_exists:
            _TOOLS.print_error(f"le tournoi n°{tournament_id} n'est pas disponible.")
        if tournament_id is not None and tournament_exists:
            cls.selected_tournament = MainDatabase().util.get_tournament_object_from_id_str(
                tournament_id=tournament_id
            )
        else:
            cls.selected_tournament = _TOOLS.tournament_choice()

    def select_edit(self):
        """Enumerates all tournament's settings and asks for edit."""

        _TOOLS.print_info("informations actuelles du tournoi:")

        self.selected_tournament.name = _TOOLS.edit_prompt(field_title="Nom", value=self.selected_tournament.name)
        self.selected_tournament.place = _TOOLS.edit_prompt(
            field_title="Lieu", value=self.selected_tournament.place
        )
        self.selected_tournament.date = _TOOLS.edit_prompt(field_title="Date", value=self.selected_tournament.date)
        self.selected_tournament.description = _TOOLS.edit_prompt(
            field_title="Description", value=self.selected_tournament.description
        )

    def is_tournament_edited(self):
        """Compares selected tournament object and original tournament copy for difference.

        Returns:
            bool: The Tournament attributes were modified.
        """

        if self.selected_tournament.name != self.original_tournament_copy.name:
            return True
        elif self.selected_tournament.place != self.original_tournament_copy.place:
            return True
        elif self.selected_tournament.date != self.original_tournament_copy.date:
            return True
        elif self.selected_tournament.description != self.original_tournament_copy.description:
            return True
        else:
            return False

    def confirm_settings(self):
        """Prompts the user to confirm the settings previously entered.

        Raises:
            typer.Exit: Exits if the user cancels the creation.
        """

        self.list_settings()

        confirm = typer.confirm("\nSouhaitez vous confirmer la modification de ce tournoi ?")
        if not confirm:
            _TOOLS.print_error("annulation. Le tournoi n'a pas été modifié.")
            raise SystemExit

    def list_settings(self):
        """Displays all previously entered tournament settings."""

        _TOOLS.print_info("nouvelles informations du tournoi:")
        parameter = typer.style("Nom: ")
        typer.echo(parameter + self.selected_tournament.name)
        parameter = typer.style("Lieu: ")
        typer.echo(parameter + self.selected_tournament.place)
        parameter = typer.style("Date: ")
        typer.echo(parameter + self.selected_tournament.date)
        parameter = typer.style("Description: ")
        typer.echo(parameter + self.selected_tournament.description)

    def save_tournament(self):
        """Uses database handler to save edited tournament."""
        # Transform list of Player objects to list of player ids
        self.selected_tournament.players = [x.id_number for x in self.selected_tournament.players]

        MainDatabase().create_tournament(
            name=self.selected_tournament.name,
            place=self.selected_tournament.place,
            date=self.selected_tournament.date,
            number_of_rounds=int(self.selected_tournament.number_of_tours),
            time_control=self.selected_tournament.time_control,
            description=self.selected_tournament.description,
            players=self.selected_tournament.players,
            rating_table=self.selected_tournament.rating_table,
            is_finished=self.selected_tournament.is_round_ended,
            id_number=self.selected_tournament.id_number,
        )

        _TOOLS.print_success(f"le tournoi n°{str(self.selected_tournament.id_number)} a été modifié.")


class DeleteTournamentMenu:
    """View for tournament deletion

    Attributes:
        selected_tournament (Tournament): Tournament selected by user for deletion.
    """

    def __init__(self, tournament_id: int = None):
        """Constructor for DeleteTournamentMenu.
        Args:
            tournament_id (int, optional): Optional tournament id to be loaded. Defaults to None.
        """
        _TOOLS.print_title("suppression d'un tournoi")

        self.cli_argument_handler(tournament_id=tournament_id)
        if self.selected_tournament is None:
            _TOOLS.print_error("aucun tournoi créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.confirm_selection()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def cli_argument_handler(cls, tournament_id: str = None):
        """Handles eventual tournament id passed at instantiation.
        Args:
            tournament_id (str): Optional tournament id to be loaded.
        """
        tournament_exists = MainDatabase().util.is_tournament_id_in_database(tournament_id=tournament_id)
        if tournament_id is not None and not tournament_exists:
            _TOOLS.print_error(f"le tournoi n°{tournament_id} n'est pas disponible.")

        if tournament_id is not None and tournament_exists:
            cls.selected_tournament = MainDatabase().util.get_tournament_object_from_id_str(
                tournament_id=tournament_id
            )
        else:
            cls.selected_tournament = _TOOLS.tournament_choice()

    def confirm_selection(self):
        """Prompts the user to confirm tournament deletion."""
        _TOOLS.print_warning(f"Vous allez supprimer définitivement le tournoi '{self.selected_tournament.name}'")

        if confirm := typer.confirm("Confirmer la suppression ?"):
            self.delete_tournament()
        else:
            typer.secho("\n Le tournoi n'a pas été supprimé")

    def delete_tournament(self):
        """Uses database handler to delete tournament."""
        MainDatabase().delete_tournament(tournament=self.selected_tournament)
