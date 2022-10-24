from models.tournament import Tournament
from models.database.database import Database


class MainDatabase:
    """Helper class encapsulating methods to manipulate and transform database objects.
    Attributes:
        database (Database): Instance of database handler database."""

    def __init__(self, database: Database):
        """Constructor de Database."""
        self.database = database

    def if_tournament_id_in_database(self, tournament_id: int):
        """Verifies if a given tournament id exists in database.
        Args:
            tournament_id (int): Tournament id to verify.
        Returns:
            bool: Tournament id exists in database.
        """
        if tournament_id in self.database.tournaments:
            return True
        else:
            return False

    def if_player_id_in_database(self, player_id: int):
        """Vérifie si un identifiant de joueur donné existe dans la base de données.
        Retourne bool : L'identifiant du joueur existe dans la base de données.
        """
        if player_id in self.database.players:
            if self.database.players[player_id].delete_player:
                return False
            else:
                return True
        else:
            return False

    def if_tournament_db_empty(self):
        """Vérifie s'il n'y a pas de tournoi dans la base de données.
        Retourne bool : Aucun tournoi dans la base de données.
        """

    def if_player_db_empty(self):
        """Vérifie s'il n'y a pas de joueur dans la base de données.
            Retourne bool : Aucun joueur dans la base de données.
        """
        if len(self.database.players) == 0:
            return True
        else:
            return False

    def get_all_matches(self, tournament: Tournament):
        """Listes de tous les matches dans un tournoi."""

        match_list = []

        for round_id in tournament.tours:
            for match_id in tournament.tours[round_id].matches:
                player_1 = tournament.tours[round_id].matches[match_id].player_1
                player_2 = tournament.tours[round_id].matches[match_id].player_2
                match_list.append((player_1.id_number, player_2.id_number))
        return match_list

    def get_players_by_name(self, players_name: dict = None):
        """Listes de tous les joueurs par nom.
        Retournes :
            listes : Liste de tous les joueurs par nom de classement.
        """
        if players_name is None:
            players_name = self.database.players
        print(players_name)
        players_ids = sorted(players_name, key=lambda x: players_name[x].last_name)

        players_list = []
        for id_number in players_ids:
            if self.database.players[id_number].delete_player:
                continue
            players_list.append(self.database.players[id_number])
        return players_list

    def get_players_by_rating(self, players_name: dict = None):
        """Lists de tous les joueurs par ordre de classement.
        Retournes :
            listes : Lists de tous les joueurs par ordre de classement.
        """
        if players_name is None:
            players_name = self.database.players
        players_ids = sorted(players_name, key=lambda x: players_name[x].rating, reverse=True)

        players_list = []
        for id_number in players_ids:
            if self.database.players[id_number].delete_player:
                continue
            players_list.append(self.database.players[id_number])

        return players_list

    def get_players_by_id(self):
        """Listes de tous les ID joueurs dans la base.
        Retournes :
            Listes : Liste de tous les joueurs par ordre d'ID.
        """
        players_ids = sorted(self.database.players, key=lambda x: x)

        players_list = []
        for id_number in players_ids:
            if self.database.players[id_number].delete_player:
                continue
            players_list.append(self.database.players[id_number])

        return players_list

    def get_tournaments_by_id(self):
        """Listes de tous les tournois par ordre ID dans la base.
        Retournes :
            Listes : Listes de tous les tournois par ordre de ID dans la base.
        """
        players_ids = sorted(self.database.tournaments, key=lambda x: x)

        tournament_list = []
        for id_number in players_ids:
            tournament_list.append(self.database.tournaments[id_number])

        return tournament_list

    def get_tournament_from_id_str(self, tournament_id: str):
        """Recherche dans tous les tournois pour trouver le tournoi demandé.
        Retournes :
            Tournament : Reponse objet du Tournoi.
        """
        for tournament in self.database.tournaments:
            if str(tournament) == tournament_id:
                return self.database.tournaments[tournament]

    def get_player_from_id_str(self, player_id: str):
        """Cherche parmi tous les joueurs pour trouver le joueur demandé."""
        for player in self.database.players:
            if str(player) == player_id:
                return self.database.players[player]

    def get_player_name_from_id(self, player_id: int):
        """Cherche parmi tous les joueurs pour trouver le nom du joueur demandé.
        Retourne :
            str : Le nom et le prénom du joueur.
        """
        for player in self.database.players:
            if self.database.players[player].id_number == player_id:
                name = f"{self.database.players[player].first_name} {self.database.players[player].last_name}"
                return name

    def get_all_tournaments_existing(self):
        """Génère une liste de tous les tournois existants dans la base de données.
        Retourne :
            liste [Tournoi] : Tous les tournois existants dans la base de données.
        """
        tournament_list = []

        for tournament_id in self.database.tournaments:
            tournament_list.append(self.database.tournaments[tournament_id])

        return tournament_list

    def get_tournaments_in_progress(self):
        """Recherche dans la base de données les tournois non terminés.
        Retourne :
            liste [Tournoi] : Les tournois non terminés.
        """
        tournament_list = []

        for tournament in self.database.tournaments:
            if not self.database.tournaments[tournament].is_round_ended:
                tournament_list.append(self.database.tournaments[tournament])

        return tournament_list

    def get_players_names(self, players_name: list):

        return [self.get_player_name_from_id(player_id=i) for i in players_name]

    def get_format_rating_table(self, rating_table: dict):
        """Formate un dict tableau de classement en une liste de noms de joueurs et de scores, triés par points.
        Arguments :
            RatingTable (dict) : Tableau de classement à formater.
        Retourne :
            liste : Liste des noms et des scores des joueurs.
        """
        rating_list = [(k, v) for k, v in sorted(rating_table.items(), key=lambda item: item[1], reverse=True)]
        format_rating_table = []

        for player in rating_list:
            format_rating_table.append((self.get_player_name_from_id(player_id=int(player[0])), player[1]))

        return format_rating_table
