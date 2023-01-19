from models.round import Round
from models.match import Match

from controller.player_controller import PlayerController
from controller.main_database import MainDatabase


class TournamentController:
    """Gère la génération et la progression d'un tournoi.
    Attributes:
        tournament (Tournament): Corresponding tournament object.
        generator (PlayerController): Object to generate matchmaking.
        current_round_number (int): Number of the round currently played.
        current_round_id (int): Unique id of the round currently played.
        current_match_number (int): Number of the match currently played.
        current_match_id (int): Unique id of the match currently played.
    """
    def __init__(self, tournament_id: int):
        """Constructeur pour TournamentController.
            Tournament_id (int) : Id unique du tournoi à reprendre.
        """
        # print(MainDatabase().database.tournaments)
        self.tournament = MainDatabase().database.tournaments[tournament_id]
        # print(self.tournament)
        self.generator = PlayerController(players=self.tournament.players)

        self.current_round_number = 0
        self.current_round_id = 0
        self.current_match_number = 0
        self.current_match_id = 0

        self.resume_tournament()

    def load_rounds_and_matches(self):
        """Utilise le gestionnaire de base de données pour charger en mémoire
         les manches et les objets de matchs du tournoi.
         """
        MainDatabase().load_rounds(tournament_id=self.tournament.id_number)
        MainDatabase().load_matches(tournament_id=self.tournament.id_number)

    def resume_tournament(self):
        """Crée le premier tour si nécessaire et demande une mise à jour de la première progression."""
        self.load_rounds_and_matches()
        if len(self.tournament.tours) == 0:
            self.create_round()
        self.update_tournament_in_progression()

    def generate_match(self):
        """Renvoie un nouveau match jusqu'à la fin du tournoi.
        Retourne :
            Match : Le prochain match à jouer.
        """
        self.update_tournament_in_progression()
        current_round = self.tournament.tours[self.current_round_id]
        if self.is_round_finished(round_=current_round):
            if self.is_tournament_finished():
                return None
            self.create_round()
            self.update_tournament_in_progression()
            current_round = self.tournament.tours[self.current_round_id]
        return current_round.matches[self.current_match_id]

    def create_round(self):
        """Crée un nouveau tour et ses matchs en se basant sur la progression actuelle du tournoi."""
        if len(self.tournament.tours) == 0:
            matches = self.generator.generate_first_round()
        else:
            MainDatabase().util.get_all_matches(tournament=self.tournament)
            matches = self.generator.generate_next_round(
                rating_table=self.tournament.rating_table)
        round_id = MainDatabase().create_round(
            number_of_round=len(self.tournament.tours) + 1, tournament_id=self.tournament.id_number)
        self.current_round_id = round_id
        for players in matches:
            MainDatabase().create_match(
                players=players, tournament_id=self.tournament.id_number, round_id=round_id, winner=None)

    def update_tournament_in_progression(self):
        """Demande une mise à jour de la progression des tours et des matchs du tournoi."""
        self.update_current_round()
        self.update_current_match()

    def update_current_round(self):
        """Met à jour le numéro du tour actuel et l'identifiant unique
        en fonction de l'achèvement des tours du tournoi.
        """
        for round_id in self.tournament.tours:
            round_object = self.tournament.tours[round_id]
            if not self.is_round_finished(round_=round_object):
                self.current_round_id = round_object.id_number
                self.current_round_number = round_object.number_of_round
            elif round_object.number_of_round > self.current_round_number:
                self.current_round_number = round_object.number_of_round
                self.current_round_id = round_object.id_number

    def update_current_match(self):
        """Met à jour le numéro de match actuel et l'identifiant unique
            en fonction de l'achèvement des matchs du tour.
        """
        self.current_match_number = 0
        current_round = self.tournament.tours[self.current_round_id]
        # Rechercher si une correspondance n'est pas encore terminée
        for match in current_round.matches:
            self.current_match_number += 1
            if current_round.matches[match].winner is None:
                self.current_match_id = current_round.matches[match].id_number
                return
        # Si tous les matchs du tour sont terminés, on prend arbitrairement le premier match
        # car aucun d'entre eux ne sera joué.
        first_match_id = list(current_round.matches.keys())[0]
        self.current_match_id = first_match_id

    def is_round_finished(self, round_: Round):
        """Verifies if a round is finished by iterating through its matches' winners.
        Args:
            round_ (Round): Round object to be verified.
        Returns:
            bool: Match is finished.
        """
        matches = round_.matches
        for match_id in matches:
            match_object = self.tournament.tours[round_.id_number].matches[match_id]
            if match_object.winner is None:
                return False
        return True

    def is_tournament_finished(self):
        """Verifies if a tournament is finished by iterating through its tours.
        Returns:
            bool: Tournament is finished.
        """
        if len(self.tournament.tours) < self.tournament.number_of_tours:
            return False
        for round_id in self.tournament.tours:
            round_object = self.tournament.tours[round_id]
            if not self.is_round_finished(round_=round_object):
                return False
        MainDatabase().database.tournaments[self.tournament.id_number].is_round_ended = True
        MainDatabase().save_tournament(tournament=MainDatabase().database.tournaments[self.tournament.id_number])
        return True

    def save_winner(self, match: Match, winner: str):
        """Prend le gagnant saisi par l'utilisateur et l'enregistre dans la base de données.
        Arguments :
            match (Match) : Match à prendre en compte.
            Gagnant (str) : Entrée de l'utilisateur.
        """
        if winner == "1":
            winner = 1
            MainDatabase().update_rating_table(
                tournament_id=match.tournament_id, player_id=match.player_1.id_number, points_earned=1)
        elif winner == "2":
            winner = 2
            MainDatabase().update_rating_table(
                tournament_id=match.tournament_id, player_id=match.player_2.id_number, points_earned=1)
        elif winner == "nul":
            winner = 0
            MainDatabase().update_rating_table(
                tournament_id=match.tournament_id, player_id=match.player_1.id_number, points_earned=0.5)
            MainDatabase().update_rating_table(
                tournament_id=match.tournament_id, player_id=match.player_2.id_number, points_earned=0.5)
        self.tournament.tours[self.current_round_id].matches[match.id_number].winner = winner
        MainDatabase().save_match(self.tournament.tours[self.current_round_id].matches[match.id_number])
