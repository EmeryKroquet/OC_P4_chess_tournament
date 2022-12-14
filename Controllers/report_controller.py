from Controllers.main_database import MainDatabase
from Models.tournament import Tournament


class ReportController:

    def __init__(self):
        """Constructeur de ReportController."""

        self.data = []

    def show_all_players_by_name(self):
        """Extraire les données de tous les joueurs triés par nom. """
        players_list = MainDatabase().util.get_payer_by_name()

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

    def show_all_players_by_rating(self):
        """Extraire les données de tous les joueurs classés par ordre de classement dans la table."""

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

    def show_tournament_players_by_name(self, tournament: Tournament):
        players_dict = {}
        for player in tournament.players:
            players_dict[player.id_number] = player

        players_list = MainDatabase().util.get_players_names(players_name=players_dict)

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

    def show_tournament_players_by_rating(self, tournament: Tournament):

        players_dict = {}
        for player in tournament.players:
            players_dict[player.id_number] = player

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

    def show_all_tournaments(self):
        """Extraire les données pour tous les tournois."""

        tournaments_list = MainDatabase().util.get_tournaments_by_id()

        for tournament in tournaments_list:

            players_ids = [x.id_number for x in tournament.players]
            list_of_players_name = MainDatabase().util.get_players_names(players_names=players_ids)

            if tournament.is_round_ended:
                is_round_ended = "Terminé"
            else:
                is_round_ended = "En cours"

            self.data.append(
                {
                    "id": tournament.id_number,
                    "Nom": tournament.name,
                    "Lieu": tournament.place,
                    "date": tournament.date,
                    "Nombre de rounds": tournament.numbers_of_tours,
                    "Contrôle de temps": tournament.time_control,
                    "description": tournament.description,
                    "Progression": is_round_ended,
                    "Joueurs": list_of_players_name,
                    "Classement": MainDatabase().util.get_format_rating_table(
                        rating_table=tournament.rating_table
                    ),
                }
            )

    def tournament_rounds(self, tournament: Tournament):
        self.load_tournament_data(tournament_id=tournament.id_number)

        for tour in tournament.tours:
            matches = []

            for match in tournament.tours[tour].matches:
                match = tournament.tours[tour].matches[match]
                player_1 = MainDatabase().util.get_player_name_from_id(match.player_1.id_number)
                player_2 = MainDatabase().util.get_player_name_from_id(match.player_2.id_number)
                matches.append(f"{player_1} vs {player_2}")

            self.data.append(
                {
                    "Round n°": tournament.tours[tour].number_of_tours,
                    "Matchs": matches,
                    "id": tournament.tours[tour].id_number,
                }
            )

    def tournament_matches(self, tournament: Tournament):
        self.load_tournament_data(tournament_id=tournament.id_number)

        for tour in tournament.tours:
            matches = tournament.tours[tour].matches
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

    @staticmethod
    def load_tournament_data(tournament_id: int):
        MainDatabase().load_rounds(tournament_id=tournament_id)
        MainDatabase().load_matches(tournament_id=tournament_id)
