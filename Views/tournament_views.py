import typer

from copy import deepcopy

import views.play_game as _GameMenu
from controller.main_database import MainDatabase
import views.tools as _TOOLS


class TournamentMenu:
    """Vue pour les opérations liées au tournoi."""

    def __init__(self):
        """Constructeur de TournamentMenu."""
        _TOOLS.print_title("menu des tournois")

        self.print_menu()
        self.user_selection()

    @classmethod
    def print_menu(cls):
        """Affiche les différentes options du menu."""
        choice = typer.style("1. ")
        typer.echo(f"{choice}Reprendre un tournoi")
        choice = typer.style("2. ")
        typer.echo(f"{choice}Créer un nouveau tournoi")
        choice = typer.style("3. ")
        typer.echo(f"{choice}Modifier un tournoi")
        choice = typer.style("4. ")
        typer.echo(f"{choice}Supprimer un tournoi")
        choice = typer.style("5. ")
        typer.echo(f"{choice}Afficher tous les tournois")
        choice = typer.style("\n0. ")
        typer.echo(f"{choice}Retour")

    @classmethod
    def user_selection(cls):
        """Invite l'utilisateur à sélectionner une option."""
        user_selection = typer.prompt("Entrez votre sélection ")
        if user_selection == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=cls.__class__.__name__)
        elif user_selection == "1":
            typer.echo("\n\n")
            LoadTournamentMenu()
        elif user_selection == "2":
            typer.echo("\n\n")
            NewTournamentMenu()
        elif user_selection == "3":
            typer.echo("\n\n")
            EditTournamentMenu()
        elif user_selection == "4":
            typer.echo("\n\n")
            DeleteTournamentMenu()
        elif user_selection == "5":
            typer.echo("\n\n")
            _TOOLS.tournaments_all_list()
            typer.echo("\n")
            cls.user_selection()
        else:
            cls.user_selection()


class LoadTournamentMenu:
    """Vue affichée pour le chargement des tournois
        available_tournaments (liste) :
         Tournois non terminés disponibles pour le chargement.
    """

    def __init__(self, tournament_id: int = None):
        """Constructeur pour LoadTournamentMenu.
            tournament_id (int, facultatif) : Identifiant facultatif du tournoi à charger.
             La valeur par défaut est None.
        """
        _TOOLS.print_title("chargement d'un tournoi")
        self.available_tournaments = MainDatabase().util.get_unfinished_tournaments()
        self.tournament_select_parameter(tournament_id=tournament_id)
        self.display_unfinished_tournaments()

        if len(self.available_tournaments) == 0:
            _TOOLS.print_error("aucun tournoi en cours.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.user_selection()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def tournament_select_parameter(self, tournament_id: int = None):
        """Gère l'éventuel identifiant de tournoi passé à l'instanciation.
            tournament_id (str) : Identifiant facultatif du tournoi à charger.
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
        """Utilise le gestionnaire de base de données pour trouver et
         afficher les tournois non terminés afin que l'utilisateur puisse faire son choix.
         """
        for tournament in self.available_tournaments:
            typer.secho(f" - Tournoi n°{tournament.id_number} -")
            parameter = typer.style("Nom: ")
            typer.echo(parameter + tournament.name)
            parameter = typer.style("Date: ")
            typer.echo(parameter + tournament.date + "\n")

    def user_selection(self):
        """Demande à l'utilisateur de sélectionner un tournoi à charger."""
        selection = typer.prompt("Entrez un numéro de tournoi")
        available_ids = [x.id_number for x in self.available_tournaments]
        while not selection.isnumeric() or int(selection) not in available_ids:
            _TOOLS.print_error(f"pas de tournoi avec le numéro {selection}")
            self.user_selection()
            return
        self.start_tournament(int(selection))

    @classmethod
    def start_tournament(cls, tournament_id):
        """Ouvre le menu des jeux pour le tournoi sélectionné.
            tournament_id (int) : Id unique du tournoi à charger.
        """
        _GameMenu.GameMenu(tournament_id)


class NewTournamentMenu:
    """Vue pour la création d'un nouveau tournoi."""

    def __init__(self):
        """Constructeur de NewTournamentMenu."""
        _TOOLS.print_title("création d'un tournoi")
        self.tournament_name = ""
        self.place = ""
        self.date = ""
        self.number_of_rounds = ""
        self.time_control = ""
        self.description = ""
        self.players = []
        self.created_tournament_id = None

        self.tournament_settings_prompt()
        self.add_players()
        self.confirm_tournament_settings()
        self.save_tournament()
        self.start_tournament()

    def tournament_settings_prompt(self):
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
        """Invite l'utilisateur à sélectionner les joueurs participants."""
        typer.secho("\nEntrez le numéro d'un joueur à ajouter\n")
        _TOOLS.players_all_list()
        while len(self.players) < 8:
            selection = typer.prompt(f"Joueur ({len(self.players)}/8)")
            if _TOOLS.player_exists(choose_id=selection, players_ids=self.players):
                self.players.append(int(selection))

    def valid_time_control(self):
        """Vérifie si le type de contrôle horaire saisi par l'utilisateur est valide.
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

    def confirm_tournament_settings(self):
        """Invite l'utilisateur à confirmer les paramètres précédemment saisis.
            typer.Exit : Quitte si l'utilisateur annule la création.
        """
        self.listing_tournament_settings()
        self.list_participating_players()
        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce tournoi ?")
        if not confirm:
            _TOOLS.print_error("annulation. Le tournoi n'a pas été créé.")
            raise SystemExit

    def listing_tournament_settings(self):
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
        """Affiche les joueurs participants sélectionnés par leur nom. """
        _TOOLS.print_info("liste des joueurs: ")
        players_name = MainDatabase().util.get_players_names(players_sample=self.players)
        for name in players_name:
            typer.echo(f" - {name}")

    def save_tournament(self):
        """Utilise le gestionnaire de base de données pour enregistrer le tournoi créé."""
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
        """Démarre le tournoi créé si l'utilisateur le sélectionne."""
        if confirm := typer.confirm("\nSouhaitez vous commencer le tournoi ?"):
            _GameMenu.GameMenu(tournament_id=self.created_tournament_id)
        else:
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)


class EditTournamentMenu:
    """View for tournament editing.
        selected_tournament (Tournament): Tournament selected by user for edit.
        original_tournament_copy (Tournament): Deep copy of initial Tournament state for modification check.
    """
    def __init__(self, tournament_id: int = None):
        """Constructeur pour EditTournamentMenu.
            tournament_id (int, facultatif) : Identifiant facultatif du tournoi à charger.
             La valeur par défaut est None.
        """
        _TOOLS.print_title("modification d'un tournoi")
        self.select_tournament_parameter(tournament_id=tournament_id)
        if self.selected_tournament is None:
            _TOOLS.print_error("aucun tournoi créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.original_tournament_copy = deepcopy(self.selected_tournament)
        self.edit_tournament_selection()
        if self.is_tournament_edited():
            self.confirm_tournament_settings()
            self.save_tournament()
        else:
            _TOOLS.print_success("aucune modification effectuée.")
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def select_tournament_parameter(cls, tournament_id: int = None):
        """Gère l'éventuel identifiant de tournoi passé à l'instanciation.
            tournament_id (str) : Identifiant facultatif du tournoi à charger.
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

    def edit_tournament_selection(self):
        """Enumère tous les paramètres du tournoi et demande de les modifier."""

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
        """Compare l'objet du tournoi sélectionné et la copie originale du tournoi pour déterminer la différence.
            bool : Les attributs du tournoi ont été modifiés.
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

    def confirm_tournament_settings(self):
        """Invite l'utilisateur à confirmer les paramètres précédemment saisis.
            typer.Exit : Quitte si l'utilisateur annule la création.
        """
        self.listing_tournament_settings()
        confirm = typer.confirm("\nSouhaitez vous confirmer la modification de ce tournoi ?")
        if not confirm:
            _TOOLS.print_error("annulation. Le tournoi n'a pas été modifié.")
            raise SystemExit

    def listing_tournament_settings(self):
        """Affiche tous les paramètres du tournoi précédemment saisis."""
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
        # Transformer la liste des objets Player en liste d'identifiants de joueurs.
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
    """Vue pour la suppression du tournoi
           selected_tournament (Tournoi) : Tournoi sélectionné par l'utilisateur pour être supprimé.
       """

    def __init__(self, tournament_id: int = None):
        """Constructeur pour DeleteTournamentMenu.
            tournament_id (int, facultatif) : Identifiant facultatif du tournoi à charger.
             La valeur par défaut est None.
        """
        _TOOLS.print_title("suppression d'un tournoi")
        self.tournament_select_parameter(tournament_id=tournament_id)
        if self.selected_tournament is None:
            _TOOLS.print_error("aucun tournoi créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.confirm_tournament_selection()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def tournament_select_parameter(cls, tournament_id: str = None):
        """Gère l'éventuel identifiant de tournoi passé à l'instanciation.
            tournament_id (str) : Identifiant facultatif du tournoi à charger.
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

    def confirm_tournament_selection(self):
        """Demande à l'utilisateur de confirmer la suppression du tournoi."""
        _TOOLS.print_warning(f"Vous allez supprimer définitivement le tournoi '{self.selected_tournament.name}'")
        if confirm := typer.confirm("Confirmer la suppression ?"):
            self.delete_tournament()
        else:
            typer.secho("\n Le tournoi n'a pas été supprimé")

    def delete_tournament(self):
        """Utilise le gestionnaire de base de données pour supprimer le tournoi."""
        MainDatabase().delete_tournament(tournament=self.selected_tournament)
