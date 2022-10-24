from datetime import datetime
import datetime
import typer

from models.database.main_database import MainDatabase
import views.main_view as _MAIN_MENU
import views.tournament_view as _TOURNAMENT_MENU
import views.player_view as _PLAYER_MENU
import views.report_view as _REPORT_MENU


def message_success(message: str):
    typer.secho(f"> {message.capitalize()}")
    typer.echo("\n")


def date_valid(date: str):
    try:
        datetime.datetime.strptime(date, "%d-%m-%Y")
        return True
    except ValueError:
        if len(date) > 0:
            error_message("date invalide.")
        return False


def print_info(message: str):
    typer.secho(f"- {message.capitalize()}")
    typer.echo("\n")


def print_warning(message: str):
    typer.secho(f"{message.upper()}")
    typer.echo("\n")


def print_title(message: str):
    typer.secho(f"- {message.upper()} -")
    typer.echo("\n")


def go_back_to_menu(current_view: str):
    if current_view in ["TournamentMenu", "PlayerMenu", "ReportMenu", "PlayMenu"]:
        _MAIN_MENU.MainMenu()
    elif current_view in ["TournamentMenu", "LoadTournamentMenu", "EditTournamentMenu", "DeleteTournamentMenu"]:
        _TOURNAMENT_MENU.TournamentMenu()
    elif current_view in ["NewPlayerMenu", "EditPlayerMenu", "DeletePlayerMenu"]:
        _PLAYER_MENU.PlayerMenu()
    elif current_view in ["PlayerReportMenu", "TournamentReportMenu"]:
        _REPORT_MENU.ReportMenu()


def player_choice():
    """Prompts the user to select a player in database."""

    if MainDatabase().util.if_player_db_empty():
        return None

    players_all_list()

    choice = ""
    while not player_exists(choose_id=choice):
        choice = typer.prompt("Sélectionnez un joueur")

    return MainDatabase().util.get_player_from_id_str(player_id=choice)


def tournament_choice():
    """Prompts the user to select a tournament in database."""

    if MainDatabase().util.if_tournament_db_empty():
        return None

    tournaments_all_list()

    choice = ""
    while not tournament_exists(choose_id=choice):
        choice = typer.prompt("Choisir un tournoi")

    return MainDatabase().util.get_tournament_from_id_str(tournament_id=choice)


def tournaments_all_list():
    """Lists all existing tournaments."""

    if MainDatabase().util.if_tournament_db_empty():
        typer.secho("Aucun tournoi créé.")
        return

    print_info("liste des tournois existants:")

    all_tournaments = MainDatabase().util.get_tournaments_by_id()

    for tournament in all_tournaments:
        if tournament.is_round_ended:
            is_round_ended = typer.style(" -> Terminé")
        else:
            is_round_ended = ""
        typer.echo(f"{tournament.id_number}. {tournament.name} - {tournament.date}" + is_round_ended)


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

    if len(choose_id) == 0:
        return False

    if not choose_id.isnumeric():
        error_message("entrez le numéro du tournoi apparaissant devant son nom")
        return False

    if MainDatabase().util.if_tournament_id_in_database(tournament_id=int(choose_id)):
        return True

    error_message(f"pas de tournoi avec le numéro {choose_id}")

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
    if len(choose_id) == 0:
        return False
    if not choose_id.isnumeric():
        error_message("entrez le numéro du joueur apparaissant devant son nom")
        return False
    if int(choose_id) in players_ids:
        error_message(f"le joueur numéro {choose_id} a déjà été ajouté")
        return False
    if MainDatabase().util.if_player_id_in_database(player_id=int(choose_id)):
        if MainDatabase().util.get_player_from_id_str(player_id=choose_id).delete_player:
            return False
        return True
    error_message(f"pas de joueur avec le numéro {choose_id}")
    return False


def alert_message(message: str):
    typer.secho(f"{message.upper()}")
    typer.echo("\n")


def set_date():
    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y")
    return date


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


def display_current_value(field_title: str, value: any):
    parameter = typer.style(f"\n{field_title}: ")
    typer.echo(parameter + str(value))


def enter_new_value(field_title: str):
    new_value = typer.prompt(f"Entrez une nouvelle valeur pour '{field_title}'")

    return new_value


def ask_for_edit():
    confirm = typer.confirm("Modifier cette information?")

    return confirm


def gender_is_valid(gender: str):
    if len(gender) == 0:
        return False
    elif gender.lower() == "h" or "H":
        return True
    elif gender.lower() == "f" or "F":
        return True
    else:
        error_message("genre incorrect. Entrez H ou F.")
        return False


def error_message(message: str):
    typer.secho(f"! {message.capitalize()}")
    typer.echo("\n")


def view_score(score):
    print("Pas de résultat")
    if score == 1:
        result = "Gagnant joueur 1"
    elif score == 0:
        result = "Gagnant joueur 2"
    else:
        result = "Match nul"
    return result


def print_report(data: dict):
    for element in data:
        for key in element:
            field_name = key + ": "
            value = typer.style(str(element[key]), bold=True)
            typer.echo(field_name + value)
        typer.echo("\n")
