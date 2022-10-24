from copy import deepcopy

import typer

from models.database.main_database import MainDatabase
import tools.tool as _TOOLS
import views.menu_play as _MENU_PLAY
from views.menu_play import PlayMenu


class TournamentMenu:

    def __int__(self):
        _TOOLS.print_title("menu des tournois")

        self.main_menu()
        self.tournament_user_choice()

    @classmethod
    def main_menu(cls):
        user_choice = typer.style("1.", bold=True)
        typer.echo(user_choice + "Rependre un tournoi")

        user_choice = typer.style("2.", bold=True)
        typer.echo(user_choice + "Créer un nouveau tournoi")

        user_choice = typer.style("3.", bold=True)
        typer.echo(user_choice + "Modifier un tournoi")

        user_choice = typer.style("4.", bold=True)
        typer.echo(user_choice + "Supprimer un tournoi")

        user_choice = typer.style("5.", bold=True)
        typer.echo(user_choice + "Afficher tous les tournois")

        user_choice = typer.style("\n0.", bold=True)
        typer.echo(user_choice + "Retour au menu")
        cls.tournament_user_choice()

    @classmethod
    def tournament_user_choice(cls):
        user_choice = typer.prompt("Viellez entrer un choix ")

        if user_choice == "0":
            typer.echo("\n\n")
            _TOOLS.go_back_to_menu(current_view=cls.__class__.__name__)
        elif user_choice == "1":
            typer.echo("\n\n")
            LoadTournamentMenu()
        elif user_choice == "2":
            typer.echo("\n\n")
            NewTournamentMenu()
        elif user_choice == "3":
            typer.echo("\n\n")
            EditTournamentMenu()
        elif user_choice == "4":
            typer.echo("\n\n")
            DeleteTournamentMenu()
        elif user_choice == "5":
            typer.echo("\n\n")
            _TOOLS.tournaments_all_list()
            typer.echo("\n")
            cls.tournament_user_choice()
        else:
            cls.tournament_user_choice()


class LoadTournamentMenu:

    def __init__(self, tournament_id: int = None):
        _TOOLS.print_title("Chargement d'un tournoi")
        self.tournaments = MainDatabase().util.get_tournaments_in_progress()
        self.tournament_arg_handler(tournament_id=tournament_id)
        self.display_tournaments_in_progress()

        if len(self.tournaments) == 0:
            _TOOLS.error_message("aucun tournoi en cours.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.tournament_user_choice()
        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def tournament_arg_handler(self, tournament_id: int = None):
        """Gère l'éventuel identifiant de tournoi passé à l'instanciation.

                Arguments :
                    tournament_id (str) : Identifiant facultatif du tournoi à charger.
                """
        tournament_valable = (
                MainDatabase().util.get_tournament_from_id_str(tournament_id=tournament_id)
                in self.tournaments
        )
        if tournament_id is not None and not tournament_valable:
            _TOOLS.error_message(
                f"le tournoi n°{tournament_id} n'est pas disponible.",
            )
        elif tournament_id is not None and tournament_valable:
            self.start_tournament(tournament_id=tournament_id)
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def display_tournaments_in_progress(self):
        """Utilise le gestionnaire de base de données pour trouver et
            afficher les tournois non terminés afin que l'utilisateur puisse
            faire son choix.
         """
        for tournament in self.tournaments:
            typer.secho(f" - Tournoi n°{tournament.id_number} -", fg=typer.colors.CYAN)
            parameter = typer.style("Nom: ", bold=True)
            typer.echo(parameter + tournament.name)
            parameter = typer.style("Date: ", bold=True)
            typer.echo(parameter + tournament.date + "\n")

    def tournament_user_choice(self):
        """Demande à l'utilisateur de sélectionner un tournoi à charger."""
        choice = typer.prompt("Entrez un ID de tournoi")
        tournament_ids = [x.id_number for x in self.tournaments]

        while not choice.isnumeric() or int(choice) not in tournament_ids:
            _TOOLS.error_message(f"pas de tournoi avec l'ID' {choice}")
            TournamentMenu().tournament_user_choice()
            return self.start_tournament(int(choice))

    @staticmethod
    def start_tournament(tournament_id):
        """Ouvre le menu de jeu pour le tournoi sélectionné.
                Arguments :
                    tournament_id (int) : Id unique du tournoi à charger.
        """
        _MENU_PLAY.PlayMenu(tournament_id)


class NewTournamentMenu:
    """Vue pour la création de nouveaux tournois.

        Attributs :
            nom_du_tournoi (str) : Nom du tournoi.
            Lieu (str) : Lieu du tournoi.
            date (str) : Date du tournoi.
            Nombre_de_tours (str) : Nombre de tours à jouer.
            Time_control (str) : Type de contrôle du temps.
            description (str) : Description du tournoi.
            Created_tournament_id (int) : Identifiant unique du tournoi créé.
        """

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

        self.create_tournament_prompt()
        self.add_players()
        self.confirm_tournament_parameters()
        self.save_tournament()
        self.start_tournament()

    def create_tournament_prompt(self):
        _TOOLS.print_title(" Viellez entrer les informations du tournoi:")
        while len(self.tournament_name) == 0:
            self.tournament_name = typer.prompt("Entrez le nom du tournois ")

        while len(self.place) == 0:
            self.place = typer.prompt("Entrez le lieu: ")

        while not _TOOLS.date_valid(date=self.date):
            self.date = typer.prompt("Entrez la Date au format DD/MM/YYYY")

        while not self.numbers_of_tours.isnumeric():
            self.numbers_of_tours = typer.prompt(" Entrez le nombre de rounds ")

        while not self.valid_time_control():
            self.time_control = typer.prompt("Veillez Entrer un contrôle de "
                                             "temps:\n"
                                             "Bullet\n"
                                             "Blitz\n"
                                             "Coup Rapide\n")

        while len(self.description) == 0:
            self.description = typer.prompt("Veillez entrer une description ")

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
        typer.secho("\n Veillez entrer le numéro d'un joueur à ajouter\n",)
        _TOOLS.players_all_list()
        while len(self.players) < 8:
            choice = typer.prompt(f"Joueur ({str(len(self.players))}/8)")
            if _TOOLS.player_exists(choose_id=choice, players_ids=self.players):
                self.players.append(int(choice))

    def confirm_tournament_parameters(self):
        self.list_of_parameters_of_tournament()
        self.list_of_selection_players_by_name()

        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce tournoi ?")
        if not confirm:
            _TOOLS.error_message("annulation. Le tournoi n'a pas été créé.")
            raise typer.Exit

    def list_of_parameters_of_tournament(self):
        _TOOLS.print_info("paramètres du tournoi:")

        parameter = typer.style("Nom: ")
        typer.echo(parameter + self.tournament_name)
        parameter = typer.style("Lieu: ")
        typer.echo(parameter + self.place)
        parameter = typer.style("Date: ")
        typer.echo(parameter + self.date)
        parameter = typer.style("Number of tours: ")
        typer.echo(parameter + self.numbers_of_tours)
        parameter = typer.style("Contrôle du temps: ")
        typer.echo(parameter + self.time_control)
        parameter = typer.style("Description: ")
        typer.echo(parameter + self.description)

    def list_of_selection_players_by_name(self):
        """Liste des joueurs pour sélectionner par leurs noms"""
        _TOOLS.print_info("liste des joueurs: ")

        players_name = MainDatabase().util.get_players_names(players_name=self.players)

        for name in players_name:
            typer.echo(f" - {name}")

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
        confirm = typer.confirm("\nSouhaitez-vous commencer le tournoi ?")

        if confirm:
            PlayMenu(tournament_id=self.create_tournament_id)
        else:
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)


class EditTournamentMenu:

    def __int__(self, tournament_id: int = None):
        _TOOLS.print_title("Modification d'un tournoi")
        self.tournament_arg_handler(tournament_id=tournament_id)

        if self.tournament_choice is None:
            _TOOLS.error_message("Aucun tournoi crée.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return
        self.original_tournament_copy = deepcopy(self.tournament_choice)

        if self.edited_tournament():
            self.confirm_parameters()
            self.save_tournament()
        else:
            _TOOLS.message_success("aucune modification effectuée.")

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

        self.select_tournament_to_edit()

    @classmethod
    def tournament_arg_handler(cls, tournament_id: int = None):
        """Gère l'éventuel identifiant de tournoi passé à l'instanciation.
                Arguments :
                    tournament_id (str) : Identifiant facultatif du tournoi à charger.
        """
        tournament_exists = MainDatabase().util.if_tournament_id_in_database(tournament_id=tournament_id)

        if tournament_id is not None and not tournament_exists:
            _TOOLS.error_message(f"le tournoi n°{tournament_id} n'est pas disponible.")

        if tournament_id is not None and tournament_exists:
            cls.tournament_choice = MainDatabase().util.get_tournament_from_id_str(
                tournament_id=int(tournament_id)
            )
        else:
            cls.tournament_choice = _TOOLS.tournament_choice()

    def select_tournament_to_edit(self):
        """Enumerate tous les paramètres du tournoi et demande de les modifier."""

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
        """Compare l'objet du tournoi sélectionné et la copie originale du tournoi pour déterminer la différence.
                Retourne :
                    bool : Les attributs du tournoi ont été modifiés.
    """
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

    def confirm_parameters(self):
        self.list_of_parameters_of_tournament()

        confirm = typer.confirm("\nSouhaitez vous confirmer la modification de ce tournoi ?")
        if not confirm:
            _TOOLS.error_message("annulation. Le tournoi n'a pas été modifié.")
            raise typer.Exit

    def list_of_parameters_of_tournament(self):
        _TOOLS.print_info("nouvelle information du tournoi")
        parameter = typer.style("Nom: ")
        typer.echo(parameter + self.tournament_choice.name)
        parameter = typer.style("Lieu: ")
        typer.echo(parameter + self.tournament_choice.place)
        parameter = typer.style("Date: ")
        typer.echo(parameter + self.tournament_choice.date)
        parameter = typer.style("Description: ")
        typer.echo(parameter + self.tournament_choice.description)

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


class DeleteTournamentMenu:

    def __int__(self, tournament_id: int = None):
        _TOOLS.print_title("suppression d'un tournoi")

        self.tournament_arg_handler(tournament_id=tournament_id)

        if self.tournament_choice is None:
            _TOOLS.error_message("aucun tournoi créé.")
            _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)
            return

        self.confirm_tournament_choice()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    @classmethod
    def tournament_arg_handler(cls, tournament_id: int = None):
        tournament_exists = MainDatabase().util.is_tournament_id_in_database(tournament_id=tournament_id)

        if tournament_id is not None and not tournament_exists:
            _TOOLS.error_message(f"le tournoi n°{tournament_id} n'est pas disponible.")

        if tournament_id is not None and tournament_exists:
            cls.tournament_choice = MainDatabase().util.get_tournament_from_id_str(
                tournament_id=tournament_id
            )
        else:
            cls.tournament_choice = _TOOLS.tournament_choice()

    def confirm_tournament_choice(self):
        _TOOLS.alert_message(f"Vous allez supprimer définitivement le tournoi '{self.tournament_choice.name}'")

        confirm = typer.confirm("Confirmez-vous la suppression ?")

        if confirm:
            self.delete_tournament()
        else:
            typer.secho("\n Le tournoi n'a pas été supprimé", fg=typer.colors.GREEN)

    def delete_tournament(self):
        MainDatabase().delete_tournament(tournament=self.tournament_choice)
