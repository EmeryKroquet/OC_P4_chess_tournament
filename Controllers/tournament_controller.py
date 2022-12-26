from Controllers.main_controller import MainController
from Controllers.player_controller import PlayerController

from Controllers.main_database import MainDatabase
from Models.match import Match
from Models.round import Round

from tinydb import TinyDB, Query


class TournamentController:

    def __init__(self, tournament_id: int):
        """Constructeur pour TournamentController.
            Tournament_id (int) : Id unique du tournoi à reprendre.
        """
        # print(MainDatabase().database.get_database_info())
        # try:
        #     self.tournament = MainController(MainDatabase()).database.tournaments[tournament_id]
        #     print(self.tournament.__dict__)
        # except Exception as e:
        #     print(e)

        #     print("The key does not exist in the dictionary")
        # maint_database = MainDatabase()
        # print(maint_database)
        self.tournament = MainController(MainDatabase()).get_tournaments_info()
        # print(self.tournament)
        # self.tournament = self.get_tournament_by_id(tournament_id)
        # print(self.tournament.database.db)
        # print(self.tournament.players)
        # print(PlayerController(players=self.tournament.players))
        # try:
        self.generator = PlayerController(players=self.tournament.players)
        #     print(self.generator)
        # except Exception as i:
        #     print(i)
        # if hasattr(self.generator, 'values'):
        # print(self.generator.values())
        # else:
        # print('Attribute not present in object')

        self.current_round_number = 0
        self.current_round_id = 0
        self.current_match_number = 0
        self.current_match_id = 0

        self.resume_tournament()

    def get_tournament_by_id(self, tournament_id):
        """ Récupérer les infos du tournoi dans le dictionnaire avec la clé id"""
        db = TinyDB("db.json")
        query = Query()
        db.get(query.self.tournament)
        return db

    def load_rounds_and_matches(self):
        """Utilise le gestionnaire de base de données pour charger en mémoire
                les tours du tournoi et les objets de correspondance.
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
        """Renvoie un nouveau match jusqu'à la fin du tournoi."""

        self.update_tournament_in_progression()
        current_tour = self.tournament.tours[self.current_round_id]
        if self.is_round_ended(tour=current_tour):
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
            list_of_all_matches = MainController().get_all_matches(tournament=self.tournament)
            matches = self.generator.generate_next_round(
                matches=list_of_all_matches, rating_table=self.tournament.rating_table)

        round_id = MainDatabase().create_round(
            round_number=len(self.tournament.tours) + 1, tournament_id=self.tournament.id_number)
        self.current_round_id = round_id
        for players in matches:
            MainDatabase().create_match(
                players=players, tournament_id=self.tournament.id_number, round_id=round_id, winner=None)

    def update_tournament_in_progression(self):
        """Demande une mise à jour de la progression des tours et des matchs du tournoi."""
        self.update_current_round()
        self.update_current_match()

    def update_current_round(self):
        """Met à jour le numéro du tour actuel et l'identifiant unique en fonction
            de l'achèvement des tours du tournoi."""
        for round_id in self.tournament.tours:
            round_obj = self.tournament.tours[round_id]
            if not self.is_round_ended(tour=round_obj):
                self.current_round_id = round_obj.id_number
                self.current_round_number = round_obj.round_number
            elif round_obj.round_number > self.current_round_number:
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

    def is_round_ended(self, tour: Round):
        """Vérifie si un tour est terminé en parcourant les gagnants de ses matchs.
            Retourne bool : Le match est terminé."""
        matches = tour.matches

        for match_id in matches:
            match = self.tournament.tours[tour.id_number].matches[match_id]
            if match.winner is None:
                return False

        return True

    def tournament_ended(self):
        """Vérifie si un tournoi est terminé en itérant à travers ses tours.
            Retourne bool : Le tournoi est terminé."""
        if len(self.tournament.tours) < self.tournament.numbers_of_tours:
            return False

        for round_id in self.tournament.tours:
            round_ = self.tournament.tours[round_id]
            if not self.is_round_ended(tour=round_):
                return False

        MainDatabase().tournaments[self.tournament.id_number].is_round_ended = True
        MainDatabase().save_tournament(tournament=MainDatabase().tournaments[self.tournament.id_number])
        return True

    def save_player_winner(self, match: Match, winner: str):
        """Prend le gagnant saisi par l'utilisateur et le sauvegarde dans la base de données.
              Gagnant (str) : Entrée de l'utilisateur.
        """
        if winner == "1":
            winner = 1
            MainDatabase().update_table_rating(
                tournament_id=match.tournament_id, player_id=match.player_1.id_number, winner_point=1)
        elif winner == "2":
            winner = 2
            MainDatabase().update_table_rating(
                tournament_id=match.tournament_id, player_id=match.player_2.id_number, winner_point=1)
        elif winner == "nul":
            winner = 0
            MainDatabase().update_table_rating(
                tournament_id=match.tournament_id, player_id=match.player_1.id_number, winner_point=0.5)
            MainDatabase().update_table_rating(
                tournament_id=match.tournament_id, player_id=match.player_2.id_number, winner_point=0.5)
        self.tournament.tours[self.current_round_id].matches[match.id_number].winner = winner
        MainDatabase().save_match(self.tournament.tours[self.current_round_id].matches[match.id_number])
