from controllers.player_controller import PlayerController
from controllers.main_controller import MainController
from models.match import Match
from models.round import Round


class TournamentController:
    """Gère la génération et la progression d'un tournoi.

    Attributes :
        tournament (Tournoi) : Objet de tournoi correspondant.
        Generator (TournamentController Objet permettant de générer le tournoi correspondant.
        Current_round_number (int) : Numéro du round actuellement joué.
        current_round_id (int) : Identifiant unique du tour en cours de jeu.
        Current_match_number (int) : Numéro du match en cours.
        Current_match_id (int) : Identifiant unique du match en cours.
    """

    def __init__(self, tournament_id: int):
        """Constructeur pour PlayerController.
            Tournament_id (int) : Id unique du tournoi à reprendre.
        """
        self.tournament = MainController().database.tournaments[tournament_id]
        self.generator = PlayerController(players=self.tournament.players)

        self.current_round_number = 0
        self.current_round_id = 0
        self.current_match_number = 0
        self.current_match_id = 0

        self.resume_tournament()

    def load_rounds_and_matches(self):
        """Utilise le gestionnaire de base de données pour charger en mémoire
            les tours du tournoi et les objets de correspondance.
        """
        MainController().load_rounds(tournament_id=self.tournament.id_number)
        MainController().load_matches(tournament_id=self.tournament.id_number)

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
        current_tour = self.tournament.tours[self.current_round_id]
        if self.round_ended(tour=current_tour):
            if self.tournament_ended():
                return None
            self.create_round()
            self.update_tournament_in_progression()
            current_tour = self.tournament.tours[self.current_round_id]
        return current_tour.matches[self.current_match_id]

    def create_round(self):
        """Crée un nouveau tour et ses matchs en se basant sur la progression actuelle du tournoi."""
        if len(self.tournament.tours) == 0:
            matches = self.generator.generate_first_round()
        else:
            all_matches_list = MainController().util.get_all_matches(tournament=self.tournament)
            matches = self.generator.generate_next_round(
                matches=all_matches_list, rating_table=self.tournament.rating_table)

        round_id = MainController().create_round(
            round_number=len(self.tournament.tours) + 1, tournament_id=self.tournament.id_number)
        self.current_round_id = round_id
        for players in matches:
            MainController().create_match(players=players, tournament_id=self.tournament.id_number, round_id=round_id, winner=None)

    def update_tournament_in_progression(self):
        """Demande une mise à jour de la progression des tours et des matchs du tournoi."""
        self.update_current_round()
        self.update_current_match()

    def update_current_round(self):
        """Met à jour le numéro du tour actuel et l'identifiant unique en fonction
            de l'achèvement des tours du tournoi.
        """
        for round_id in self.tournament.tours:
            round_obj = self.tournament.tours[round_id]
            if not self.round_ended(tour=round_obj):
                self.current_round_id = round_obj.id_number
                self.current_round_number = round_obj.round_number
            else:
                if round_obj.round_number > self.current_round_number:
                    self.current_round_number = round_obj.round_number
                    self.current_round_id = round_obj.id_number

    def update_current_match(self):
        """Met à jour le numéro de match actuel et l'identifiant unique en fonction
            de l'achèvement des matchs du tour.
        """
        self.current_match_number = 0
        current_tour = self.tournament.tours[self.current_round_id]
        # Rechercher si une correspondance n'est pas encore terminée
        for match in current_tour.matches:
            self.current_match_number += 1
            if current_tour.matches[match].winner is None:
                self.current_match_id = current_tour.matches[match].id_number
                return
            # Si tous les matchs du tour sont terminés, on prend arbitrairement le premier match,
            # car aucun d'entre eux ne sera joué.
            first_match_id = list(current_tour.matches.keys())[0]
            self.current_match_id = first_match_id

    def round_ended(self, tour: Round):
        """Vérifie si un tour est terminé en parcourant les gagnants de ses matchs.
        Arguments :
            tour (Round) : Objet de ronde à vérifier.
        Retourne :
            bool : Le match est terminé.
        """
        matches = tour.matches

        for match_id in matches:
            match_obj = self.tournament.tours[tour.id_number].matches[match_id]
            if match_obj.winner is None:
                return False

        return True

    def tournament_ended(self):
        """Vérifie si un tournoi est terminé en itérant à travers ses tours.
        Retourne :
            bool : Le tournoi est terminé.
        """
        if len(self.tournament.tours) < self.tournament.numbers_of_tours:
            return False

        for round_id in self.tournament.tours:
            round_obj = self.tournament.tours[round_id]
            if not self.round_ended(tour=round_obj):
                return False

        MainController().database.tournaments[self.tournament.id_number].round_ended = True
        MainController().save_tournament(tournament=MainController().database.tournaments[self.tournament.id_number])
        return True

    def save_player_winner(self, match: Match, winner: str):
        """Prend le gagnant saisi par l'utilisateur et le sauvegarde dans la base de données.
               Arguments :
                   match (Match) : Match à prendre en compte.
                   Gagnant (str) : Entrée de l'utilisateur.
               """
        if winner == "1":
            winner = 1
            MainController().update_rating(
                tournament_id=match.tournament_id, player_id=match.player_1.id_number, points_earned=1)
        elif winner == "2":
            winner = 2
            MainController().update_rating(
                tournament_id=match.tournament_id, player_id=match.player_2.id_number, points_earned=1)
        elif winner == "nul":
            winner = 0
            MainController().update_rating(
                tournament_id=match.tournament_id, player_id=match.player_1.id_number, points_earned=0.5)
            MainController().update_rating(
                tournament_id=match.tournament_id, player_id=match.player_2.id_number, points_earned=0.5)
        self.tournament.tours[self.current_round_id].matches[match.id_number].winner = winner
        MainController().save_match(self.tournament.tours[self.current_round_id].matches[match.id_number])

