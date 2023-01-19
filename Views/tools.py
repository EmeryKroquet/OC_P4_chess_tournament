import typer

from typing import Any
from datetime import datetime

from controller.main_database import MainDatabase
import views.main_menu as _MAIN_MENU
import views.player_view as _PLAYER_VIEWS
import views.tournament_views as _TOURNAMENT_VIEWS
import views.report_views as _REPORT_VIEWS


def go_back_to_menu(current_view: str):
    """Go to previous menu based on current view.
    Args:
        current_view (str): Current view name based on class __name__.
    """
    if current_view in {"TournamentMenu", "PlayerMenu", "ReportMenu", "GameMenu"}:
        _MAIN_MENU.MainMenu()
    elif current_view in {"NewTournamentMenu", "LoadTournamentMenu", "EditTournamentMenu", "DeleteTournamentMenu"}:
        _TOURNAMENT_VIEWS.TournamentMenu()
    elif current_view in {"NewPlayerMenu", "EditPlayerMenu", "DeletePlayerMenu"}:
        _PLAYER_VIEWS.PlayerMenu()
    elif current_view in {"PlayerReportMenu", "TournamentReportMenu"}:
        _REPORT_VIEWS.ReportMenu()


def print_title(message: str):
    """Prints a formated title.
    Args:
        message (str): Message content.
    """
    typer.secho(f"- {message.upper()} -", fg=typer.colors.BRIGHT_CYAN, bg=typer.colors.BRIGHT_BLACK, bold=True)
    typer.echo("\n")


def print_success(message: str):
    """Prints a formated success message.
    Args:
        message (str): Message content.
    """
    typer.secho(f"> {message.capitalize()}", fg=typer.colors.BRIGHT_GREEN, bg=typer.colors.BRIGHT_BLACK, bold=True)
    typer.echo("\n")


def print_info(message: str):
    """Prints a formated info message.
    Args:
        message (str): Message content.
    """

    typer.secho(f"- {message.capitalize()}", fg=typer.colors.BRIGHT_MAGENTA, bg=typer.colors.BRIGHT_BLACK, bold=True)
    typer.echo("\n")


def print_error(message: str):
    """Prints a formated error message.
    Args:
        message (str): Message content.
    """
    typer.secho(f"! {message.capitalize()}", fg=typer.colors.BRIGHT_RED, bg=typer.colors.BRIGHT_BLACK, bold=True)
    typer.echo("\n")


def print_warning(message: str):
    """Prints a formated warning message.
    Args:
        message (str): Message content.
    """
    typer.secho(f"{message.upper()}", fg=typer.colors.RED, blink=True, bold=True)
    typer.echo("\n")


def player_choice():
    """Prompts the user to select a player in database."""
    if MainDatabase().util.is_player_db_empty():
        return None

    players_all_list()
    choice = ""
    while not player_exists(choose_id=choice):
        choice = typer.prompt("Sélectionnez un joueur")

    return MainDatabase().util.get_player_object_from_id_str(player_id=choice)


def tournament_choice():
    """Prompts the user to select a tournament in database."""
    if MainDatabase().util.is_tournament_db_empty():
        return None
    tournaments_all_list()

    choice = ""
    while not tournament_exists(choose_id=choice):
        choice = typer.prompt("Choisir un tournoi")

    return MainDatabase().util.get_tournament_object_from_id_str(tournament_id=choice)


def tournaments_all_list():
    """Lists all existing tournaments."""
    if MainDatabase().util.is_tournament_db_empty():
        typer.secho("Aucun tournoi créé.")
        return
    print_info("liste des tournois existants:")

    all_tournaments = MainDatabase().util.get_tournaments_by_id()
    for tournament in all_tournaments:
        if tournament.is_round_ended:
            is_round_ended = typer.style(" -> Terminé")
        else:
            is_round_ended = ""
        typer.echo(f"{tournament.id_number}. {tournament.name} - {tournament.date}{is_round_ended}")


def players_all_list():
    """Lists all existing players."""
    print_info("liste des joueurs existants:")

    all_players = MainDatabase().util.get_players_by_id()
    for player in all_players:
        if player.delete_player:
            continue
        player_id = typer.style(str(player.id_number), bold=True)
        typer.echo(f"{player_id}. {player.first_name} {player.last_name}")


def tournament_exists(choose_id: str):
    """Verifies if the tournament selected by the user exists.
    Args:
        choose_id (str): Tournament chosen by the user.
    Returns:
        bool: The tournament is selectable.
    """
    if not choose_id:
        return False
    if not choose_id.isnumeric():
        print_error("entrez le numéro du tournoi apparaissant devant son nom")
        return False
    if MainDatabase().util.is_tournament_id_in_database(tournament_id=int(choose_id)):
        return True

    print_error(f"pas de tournoi avec le numéro {choose_id}")

    return False


def player_exists(choose_id: str, players_ids=None):
    """Verifies if the player selected by the user exists.
    Args:
        choose_id (str): Player chosen by the user.
        players_ids (list, optional): List of ids the user cannot choose from. Defaults to [].

    Returns:
        bool: The user is selectable.
    """
    if players_ids is None:
        players_ids = []
    if not choose_id:
        return False
    if not choose_id.isnumeric():
        print_error("entrez le numéro du joueur apparaissant devant son nom")
        return False
    if int(choose_id) in players_ids:
        print_error(f"le joueur numéro {choose_id} a déjà été ajouté")
        return False
    if MainDatabase().util.is_player_id_in_database(player_id=int(choose_id)):
        return not MainDatabase().util.get_player_object_from_id_str(player_id=choose_id).delete_player
    print_error(f"pas de joueur avec le numéro {choose_id}")
    return False


def edit_prompt(field_title: str, value: Any):
    display_current_value(field_title=field_title, value=value)

    if not ask_for_edit():
        return value

    value = ""

    if "date" in field_title.lower():
        while not date_is_valid(date=value):
            value = enter_new_value(field_title=field_title)
    elif "genre" in field_title.lower():
        while not gender_is_valid(gender=value):
            value = enter_new_value(field_title=field_title)
    elif "rating" in field_title.lower():
        while not value.isnumeric():
            value = enter_new_value(field_title=field_title)
    else:
        while len(value) == 0:
            value = enter_new_value(field_title=field_title)
    return value


def display_current_value(field_title: str, value: Any):
    """Displays the current value of a field.
    Args:
        field_title (str): Title to display.
        value (Any): Value to display.
    """
    parameter = typer.style(f"\n{field_title}: ", bold=True)
    typer.echo(parameter + str(value))


def ask_for_edit():
    """Asks the user for information edit.
    Returns:
        bool: User want to edit this field.
    """
    confirm = typer.confirm("Modifier cette information?")
    return confirm


def enter_new_value(field_title: str):
    """Displays a prompt for a new value.
    Args:
        field_title (str): Title to display.
    Returns:
        str: New value given by the user.
    """
    return typer.prompt(f"Entrez une nouvelle valeur pour '{field_title}'")


def date_is_valid(date: str):
    """Verifies if the date entered by the user is valid using datetime library.
    Returns:
        bool: The date exists.
    """
    try:
        datetime.strptime(date, "%d-%m-%Y")
        return True
    except ValueError:
        if date != "":
            print_error("date incorrecte.")
        return False


def gender_is_valid(gender: str):
    """Verifies if the gender entered by the user is valid.
    Returns:
        bool: The gender is valid.
    """

    if not gender:
        return False
    elif gender.lower() == "h":
        gender = "H"
        return True
    elif gender.lower() == "f":
        gender = "F"
        return True
    else:
        print_error("genre incorrect. Entrez H ou F.")
        return False


def print_report(data: dict):
    """Prints a generated report in console.
    Args:
        data (dict): Report data dict.
    """
    for element in data:
        for key in element:
            field_name = f"{key}: "
            value = typer.style(str(element[key]), bold=True)
            typer.echo(field_name + value)
        typer.echo("\n")


def ask_for_report_export():
    """Prompts the user to select export settings.
    Returns:
        bool: User wants to export the report.
    """
    print_info("souhaitez vous exporter ce rapport ?")

    number = typer.style("1. ", bold=True)
    typer.echo(f"{number}Oui")
    number = typer.style("2. ", bold=True)
    typer.echo(f"{number}Non")

    selection = ""
    while selection not in ["1", "2"]:
        selection = typer.prompt("Entrez votre sélection: ")
    if selection == "1":
        return True
    elif selection == "2":
        return False
