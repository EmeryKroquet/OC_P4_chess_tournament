from controller.main_database import MainDatabase
from models.tournament import Tournament


class ReportController:
    """Gère la génération des données du rapport et l'enregistrement local.
    Attributs :
        data (liste) : Liste des données sérialisées pour le rapport.
    """
    def __init__(self):
        """Constructeur pour ReportController."""
        self.data = []

    def all_players_by_name(self):
        """Extraire les données de tous les joueurs classés par nom."""
        players_list = MainDatabase().util.get_players_by_name()

        for player in players_list:
            self.data.append(
                {
                    "Nom": player.last_name,
                    "Prénom": player.first_name,
                    "Date de naissance": player.date_of_birth,
                    "Genre": player.gender,
                    "Rating": player.rating,
                    "id": player.id_number,
                }
            )

    def all_players_by_rating(self):
        """Extraire les données de tous les joueurs classés par classement."""
        players_list = MainDatabase().util.get_players_by_rating()

        for player in players_list:
            self.data.append(
                {
                    "Rating": player.rating,
                    "Nom": player.last_name,
                    "Prénom": player.first_name,
                    "Date de naissance": player.date_of_birth,
                    "Genre": player.gender,
                    "id": player.id_number,
                }
            )

    def tournament_players_by_name(self, tournament: Tournament):
        """Extrait les données de tous les joueurs d'un tournoi classés par nom.
        Arguments :
            tournament (Tournoi) : Tournoi à prendre en compte.
        """
        players_dict = {player.id_number: player for player in tournament.players}
        players_list = MainDatabase().util.get_players_by_name(players_sample=players_dict)

        for player in players_list:
            self.data.append(
                {
                    "Nom": player.last_name,
                    "Prénom": player.first_name,
                    "Date de naissance": player.date_of_birth,
                    "Genre": player.gender,
                    "Rating": player.rating,
                    "id": player.id_number,
                }
            )

    def tournament_players_by_rating(self, tournament: Tournament):
        """Extrait les données de tous les joueurs d'un tournoi classés par classement.
        Args :
            tournament (Tournoi) : Tournoi à prendre en compte.
        """
        players_dict = {player.id_number: player for player in tournament.players}
        players_list = MainDatabase().util.get_players_by_rating(players_sample=players_dict)

        for player in players_list:
            self.data.append(
                {
                    "Rating": player.rating,
                    "Nom": player.last_name,
                    "Prénom": player.first_name,
                    "Date de naissance": player.date_of_birth,
                    "Genre": player.gender,
                    "id": player.id_number,
                }
            )

    def all_tournaments(self):
        """Extraire les données pour tous les tournois."""
        tournaments_list = MainDatabase().util.get_tournaments_by_id()

        for tournament in tournaments_list:
            players_ids = [x.id_number for x in tournament.players]
            list_of_players_name = MainDatabase().util.get_players_names(players_sample=players_ids)

            is_finished = "Terminé" if tournament.is_round_ended else "En cours"
            self.data.append(
                {
                    "id": tournament.id_number,
                    "Nom": tournament.name,
                    "Lieu": tournament.place,
                    "Date": tournament.date,
                    "Nombre de tours": tournament.number_of_tours,
                    "Contrôle de temps": tournament.time_control,
                    "Description": tournament.description,
                    "Progression": is_finished,
                    "Joueurs": list_of_players_name,
                    "Classement": MainDatabase().util.get_formated_rating_table(
                        rating_table=tournament.rating_table
                    ),
                }
            )

    def tournament_rounds(self, tournament: Tournament):
        """Extrait les données de tous les tours d'un tournoi.
        Args :
            tournament (Tournoi) : Tournoi à prendre en compte.
        """
        self.load_tournament_data(tournament_id=tournament.id_number)

        for round_ in tournament.tours:
            matches = []

            for match in tournament.tours[round_].matches:
                match = tournament.tours[round_].matches[match]
                player_1 = MainDatabase().util.get_player_name_from_id(match.player_1.id_number)
                player_2 = MainDatabase().util.get_player_name_from_id(match.player_2.id_number)
                matches.append(f"{player_1} vs {player_2}")

            self.data.append(
                {
                    "Round n°": tournament.tours[round_].number_of_round,
                    "Matchs": matches,
                    "id": tournament.tours[round_].id_number,
                }
            )

    def tournament_matches(self, tournament: Tournament):
        """Extrait les données de tous les matchs d'un tournoi.
        Arguments :
            tournament (Tournoi) : Tournoi à prendre en compte.
        """
        self.load_tournament_data(tournament_id=tournament.id_number)

        for round_ in tournament.tours:
            matches = tournament.tours[round_].matches
            for match in matches:
                match = matches[match]
                player_1 = f"{match.player_1.first_name} {match.player_1.last_name}"
                player_2 = f"{match.player_2.first_name} {match.player_2.last_name}"

                if match.winner is None:
                    winner = "Pas encore joué"
                elif match.winner == 0:
                    winner = "Match nul"
                elif match.winner == 1:
                    winner = player_1
                elif match.winner == 2:
                    winner = player_2

                self.data.append(
                    {"id": match.id_number, "Joueur 1": player_1, "Joueur 2": player_2, "Vainqueur": winner})

    def load_tournament_data(self, tournament_id: int):
        """Utilise le gestionnaire de base de données pour charger les tournées et les matchs d'un tournoi.
        Arguments :
            tournament_id (int) : Identifiant unique du tournoi à charger.
        """
        MainDatabase().load_rounds(tournament_id=tournament_id)
        MainDatabase().load_matches(tournament_id=tournament_id)
