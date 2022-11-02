from time import sleep


from Controllers.player_controller import PlayerController
from Models.database.main_database import MainDatabase
from Models.match import Match
from Models.round import Round

import tools.tools as _TOOLS


class TournamentController:

    def __init__(self, tournament_id: int):
        """Constructeur pour PlayerController.
            Tournament_id (int) : Id unique du tournoi à reprendre.
        """
        # breakpoint()
        self.tournament = MainDatabase().database.tournaments[tournament_id]
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
            all_matches_list = MainDatabase().util.get_all_matches(tournament=self.tournament)
            matches = self.generator.generate_next_round(
                matches=all_matches_list, rating_table=self.tournament.rating_table)

        round_id = MainDatabase().create_round(
            round_number=len(self.tournament.tours) + 1, tournament_id=self.tournament.id_number)
        self.current_round_id = round_id
        for players in matches:
            MainDatabase().create_match(players=players, tournament_id=self.tournament.id_number, round_id=round_id,
                                        winner=None)

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

        MainDatabase().database.tournaments[self.tournament.id_number].is_round_ended = True
        MainDatabase().save_tournament(tournament=MainDatabase().database.tournaments[self.tournament.id_number])
        return True

    def save_player_winner(self, match: Match, winner: str):
        """Prend le gagnant saisi par l'utilisateur et le sauvegarde dans la base de données.
              Gagnant (str) : Entrée de l'utilisateur.
        """
        if winner == "1":
            winner = 1
            MainDatabase().update_rating(
                tournament_id=match.tournament_id, player_id=match.player_1.id_number, winner_point=1)
        elif winner == "2":
            winner = 2
            MainDatabase().update_rating(
                tournament_id=match.tournament_id, player_id=match.player_2.id_number, winner_point=1)
        elif winner == "nul":
            winner = 0
            MainDatabase().update_rating(
                tournament_id=match.tournament_id, player_id=match.player_1.id_number, winner_point=0.5)
            MainDatabase().update_rating(
                tournament_id=match.tournament_id, player_id=match.player_2.id_number, winner_point=0.5)
        self.tournament.tours[self.current_round_id].matches[match.id_number].winner = winner
        MainDatabase().save_match(self.tournament.tours[self.current_round_id].matches[match.id_number])


class PlayMenu:

    def __init__(self, tournament_id: int):
        self.tournament_controller = TournamentController(tournament_id=tournament_id)
        self.play_match()

        _TOOLS.go_back_to_menu(current_view=self.__class__.__name__)

    def play_match(self):
        """Utilise la méthode de génération de match du gestionnaire
        de tournoi pour afficher un match jusqu'à la fin du tournoi. """
        while self.tournament_controller.generate_match() is not None:
            self.display_next_match(self.tournament_controller.generate_match())
        self.show_final_rating()

    def display_next_match(self, match: Match):
        """Lance les affichages d'informations et les invites pertinentes pour un Match donné."""
        self.display_tournament_in_progression()
        self.introduce_match(match=match)
        winner = self.ask_for_winner()
        self.tournament_controller.save_player_winner(match=match, winner=winner)

    def display_tournament_in_progression(self):
        """Affiche les numéros du tournoi, du tour et du match en cours."""
        self.tournament_controller.update_tournament_in_progression()
        decorator = _TOOLS.print_message(
            " - - ",

        )
        separator = _TOOLS.print_message(
            " - ",

        )
        tournament_number = _TOOLS.print_message(
            f"Tournoi {self.tournament_controller.tournament.id_number}")
        round_number = _TOOLS.print_message(
            f"Round {self.tournament_controller.current_round_number}")
        match_number = _TOOLS.print_message(
            f"Match {self.tournament_controller.current_match_number}")

        print("\n" + decorator +
              tournament_number +
              separator + round_number +
              separator + match_number +
              decorator)

    @staticmethod
    def introduce_match(match: Match):
        """Affiche les noms et le classement des joueurs du match en cours."""
        player_1_title = _TOOLS.print_message(
            "Joueur 1: ",

        )
        player_1_name = _TOOLS.print_message(
            f"First Name 1: {match.player_1.first_name} "
            f"Last Name 1: {match.player_1.last_name} "
            )
        player_1_rating = _TOOLS.print_message(
            f"({match.player_1.rating})")

        player_1_presentation = player_1_title + player_1_name + player_1_rating

        versus = _TOOLS.print_message(
            " vs ",

        )
        player_2_title = _TOOLS.print_message(
            "Joueur 2: ",

        )
        player_2_name = _TOOLS.print_message(
            "{first_name_2} {last_name_2} ".format(
                first_name_2=match.player_2.first_name,
                last_name_2=match.player_2.last_name,
            ))
        player_2_rating = _TOOLS.print_message(
            f"({match.player_2.rating})")

        player_2_presentation = player_2_title + player_2_name + player_2_rating

        print(player_1_presentation + versus + player_2_presentation)

    @staticmethod
    def ask_for_winner():
        winner = ""
        while winner.lower() not in ["1", "2", "nul"]:
            winner = input("Entrez le gagnant (1, 2, ou nul)")
        return winner.lower()

    def show_final_rating(self):
        """Affiche le classement final."""
        print("\n")
        _TOOLS.message_success("TOURNOI TERMINÉ")
        _TOOLS.print_info("classement final:")
        rating_table = MainDatabase().util.get_format_rating_table(
            rating_table=self.tournament_controller.tournament.rating_table)
        i = 1
        for player in rating_table:
            rating = _TOOLS.print_message(f"{i} -")
            player_name = player[0]
            points = str(player[1])
            print(f"{rating} {player_name} ({points} points)")
            i += 1

            print("\n")
            sleep(5)
