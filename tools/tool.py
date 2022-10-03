from datetime import datetime
import datetime
import typer

from controllers.main_controller import MainController
import views.main_view as _MAIN_MENU
import views.tournament_view as _TOURNAMENT_MENU
import views.player_view as _PLAYER_MENU
import views.report_view as _REPORT_MENU


def message_success(message: str):
    typer.secho(f"> {message.capitalize()}", fg=typer.colors.BRIGHT_GREEN, bg=typer.colors.BRIGHT_BLACK, bold=True)
    typer.echo("\n")


def date_valid(date: str):
    try:
        datetime.datetime.strptime(date, "%d/%m/%Y")
        return True
    except ValueError:
        if len(date) > 0:
            error_message("date invalide.")
        return False


def print_info(message: str):
    typer.secho(f"- {message.capitalize()}", fg=typer.colors.BRIGHT_MAGENTA, bg=typer.colors.BRIGHT_BLACK, bold=True)
    typer.echo("\n")


def print_warning(message: str):
    typer.secho(f"{message.upper()}", fg=typer.colors.RED, blink=True, bold=True)
    typer.echo("\n")


def print_title(message: str):
    typer.secho(f"- {message.upper()} -", fg=typer.colors.BRIGHT_CYAN, bg=typer.colors.BRIGHT_BLACK, bold=True)
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


def tournaments_all_lists():
    """Listes de tous les tournois existants."""
    if MainController().util.if_tournament_db_empty():
        typer.secho("Aucun tournoi créé.")
        return
    print_info("liste des tournois existants:")
    all_tournaments = MainController().util.get_tournaments_by_id()
    for tournament in all_tournaments:
        if tournament.round_ended:
            round_ended = typer.style(" -> Terminé")
        else:
            round_ended = ""
        typer.echo(f"{tournament.id_number}. {tournament.name} - {tournament.date}" + round_ended)


def player_choice():
    """Prompts the user to select a player in database."""

    if MainController().util.if_player_db_empty():
        return None

    list_of_all_players()

    choice = ""
    while not player_exists(choose_id=choice):
        choice = typer.prompt("Choisir un joueur")

    return MainController().util.get_player_from_id_str(player_id=choice)


def list_of_all_players():
    print_info("liste des joueurs existantes:")
    all_players = MainController().util.get_players_by_id()
    for player in all_players:
        if player.delete_player:
            continue
        player_id = typer.style(str(player.id_number))
        typer.echo(f"{player_id}. {player.first_name} {player.last_name}")


def player_exists(choose_id: str, players_ids=list):

    if len(choose_id) == 0:
        return False
    if not choose_id.isnumeric():
        error_message("entrez le numéro du joueur apparaissant devant son nom")
        return False
    if choose_id in players_ids:
        error_message(f"le joueur numéro {choose_id} a déjà été ajouté")
        return False
    if MainController().util.if_player_id_in_database(player_id=int(choose_id)):
        if MainController().util.get_player_from_id_str(player_id=choose_id).delete_player:
            return False
        return True
    error_message(f"pas de joueur avec le numéro {choose_id}")
    return False


def valid_rating(valid_rtg):
    if valid_rtg.isnumeric():
        return True
    else:
        return False


def tournament_choice():
    if MainController().util.if_tournament_db_empty():
        return None
    tournaments_all_lists()
    choice = ""
    while not tournament_exists(selected_id=choice):
        choice = typer.prompt("Sélectionnez un tournoi")
    return MainController().util.get_tournament_from_id_str(tournament_id=choice)


def tournament_exists(selected_id: str):
    if len(selected_id) == 0:
        return False
    if not selected_id.isnumeric():
        error_message("Entrez le numéro du tournoi apparaissant devant son nom")
        return False
    if MainController().util.is_tournament_id_in_database(tournament_id=int(selected_id)):
        return True
    error_message(f"Pas de tournoi avec le numéro {selected_id}")
    return False


def alert_message(message: str):
    typer.secho(f"{message.upper()}", fg=typer.colors.RED, blink=True, bold=True)
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
    elif "elo" in field_title.lower():
        while not value.isnumeric():
            value = enter_new_value(field_title=field_title)
    else:
        while len(value) == 0:
            value = enter_new_value(field_title=field_title)

    return value


def display_current_value(field_title: str, value: any):
    parameter = typer.style(f"\n{field_title}: ", bold=True)
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
    typer.secho(f"! {message.capitalize()}",
                fg=typer.colors.BRIGHT_RED,
                bg=typer.colors.BRIGHT_BLACK,
                bold=True)
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
