import datetime

import typer

import Views.player_view as _PLAYER_MENU
import Views.main_view as _MAIN_MENU
import Views.tournament_view as _TOURNAMENT_MENU
import Views.report_view as _REPORT_MENU
from Controllers.main_controller import MainController
from Controllers.main_database import MainDatabase


def print_message(message):
    print(message)


def print_title(message: str):
    print(f"- {message.upper()} -")
    print("\n")


def print_info(message: str):
    print(f"- {message.capitalize()}")
    print("\n")


def print_warning(message: str):
    print(f"{message.upper()}")
    print("\n")


def error_message(message: str):
    print(f"! {message.capitalize()}")
    print("\n")


def message_success(message: str):
    print(f"> {message.capitalize()}")
    print("\n")


def alert_message(message: str):
    print(f"{message.upper()}")
    print("\n")


def display_current_value(field_title: str, value: any):

    print(f"\n{field_title}: {str(value)}")


def enter_new_value(field_title: str):
    return input(f"Entrez une nouvelle valeur pour '{field_title}'")


def ask_for_edit():
    print_message("Modifiez-vous cette information?")


def edit_prompt(field_title: str, value: any):
    display_current_value(field_title=field_title, value=value)

    if not ask_for_edit():
        return value

    value = ""

    if "date" in field_title.lower():
        while not date_valid(date=value):
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


def date_valid(date: str):
    try:
        datetime.datetime.strptime(date, "%d-%m-%Y")
        return True
    except ValueError:
        if date != "":
            error_message("date invalide.")
        return False


def gender_is_valid(gender: str):
    return gender != ""


def go_back_to_menu(current_view: str):
    if current_view in {"TournamentMenu", "PlayerMenu", "ReportMenu", "PlayGameMenu"}:
        _MAIN_MENU.MainMenu()
    elif current_view in {"TournamentMenu", "LoadTournamentMenu", "EditTournamentMenu", "DeleteTournamentMenu"}:
        _TOURNAMENT_MENU.TournamentMenu()
    elif current_view in {"NewPlayerMenu", "EditPlayerMenu", "DeletePlayerMenu"}:
        _PLAYER_MENU.PlayerMenu()
    elif current_view in {"PlayerReportMenu", "TournamentReportMenu"}:
        _REPORT_MENU.ReportMenu()


def player_choice():
    if MainController(MainDatabase()).if_player_in_database_empty():
        return None

    players_all_list()

    choice = ""
    while not player_exists(choose_id=choice):
        choice = input("\n Sélectionnez un joueur: ")

    return MainController(MainDatabase()).get_player_by_id_string(player_id=choice)


def players_all_list():
    """Listes de tous les joueurs existants."""

    print_info("liste des joueurs existants: ")

    all_players = MainController(MainDatabase()).get_players_by_id()

    for player in all_players:
        if player.delete_player:
            continue
        player_id = typer.style(str(player.id_number))
        print(f"{player_id}. {player.first_name} - {player.last_name}")


def tournaments_all_list():
    """Listes de tous les tournois existants."""
    if MainController(MainDatabase()).if_tournament_in_database_empty():
        print("Aucun tournoi créé.")
        return
    print_info("\nliste des tournois existants: ")

    all_tournaments = MainController(MainDatabase()).get_tournament_by_id()
    for tournament in all_tournaments:
        is_round_ended = " -> Terminé" if tournament.is_round_ended else ""
        print(f"{tournament.id_number}. {tournament.name} - {tournament.date}{is_round_ended}")


def player_exists(choose_id: str, players_ids=None):
    if players_ids is None:
        players_ids = []
    if not choose_id:
        return False
    if not choose_id.isnumeric():
        error_message("entrez le numéro du joueur devant son nom")
        return False
    if int(choose_id) in players_ids:
        error_message(f"le joueur numéro {choose_id} a déjà été ajouté")
        return False
    if MainController(MainDatabase()).if_payer_id_in_database(player_id=int(choose_id)):
        return not MainController(MainDatabase()).get_player_by_id_string(player_id=choose_id).delete_player

    error_message(f"pas de joueur avec le numéro {choose_id}")
    return False
