from tinydb import Query, table

from models.database import Database
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from controller.main_controller import MainController


class SingletonMeta(type):
    """Meta pour une application singleton.
    Comme le DataHandler sera utilisé par différents modules, il n'est pas
    modules, il n'est pas nécessaire de charger la base de données plusieurs fois.
    Singleton a été gardé simple et n'est pas actuellement thread safe.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MainDatabase(metaclass=SingletonMeta):
    """Gère toutes les opérations liées à la base de données,
     y compris le CRUD pour les différents éléments de la base de données.

    Attributs :
        database (Base de données) : Objet encapsulant la base de données au format TinyDB et
         utilisable par les objets liés au tournoi.
        util (MainController) : Objet contenant des méthodes d'aide pour manipuler et transformer
        les objets de la base de données.
        players_table (table.Table) : Instance de la table TinyDB "Players".
        tournaments_table (table.Table) : Instance de la table "Tournois" de TinyDB.
        rounds_table (table.Table) : Instance de la table TinyDB "Rounds".
        matches_table (table.Table) : Instance de la table TinyDB "Matches".
    """

    def __init__(self):
        """Constructeur pour la classe MainDatabase. Initie le chargement de la base de données."""

        self.database = Database("database")
        self.util = MainController(database=self.database)

        self.players_table = None
        self.tournaments_table = None
        self.rounds_table = None
        self.matches_table = None
        self.load_database()

    def load_database(self):
        """Instancie les différentes tables dans les attributs et charge leur contenu
        en créant les objets correspondants.
        """

        self.players_table = self.database.db.table("players")
        self.tournaments_table = self.database.db.table("tournaments")
        self.rounds_table = self.database.db.table("tours")
        self.matches_table = self.database.db.table("matches")

        self.load_players()
        self.load_tournaments()

    def load_players(self):
        """Utilise la table TinyDB "Players" pour créer des objets Player."""

        for player in self.players_table:
            self.create_player(
                first_name=player["First Name"],
                last_name=player["Last Name"],
                date_of_birth=player["DOB"],
                gender=player["Gender"],
                rating=player["Rating"],
                id_num=player["id"],
                is_deleted=player["Is Deleted"],
                no_db_save=True,
            )

    def create_player(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        gender: str,
        rating: int,
        id_num: int = 0,
        is_deleted: bool = False,
        no_db_save: bool = False,
    ):
        """Crée un objet Player et le sauvegarde dans les attributs de la base de données.

        Arguments :
            first_name (str) : Prénom du joueur.
            last_name (str) : Nom de famille du joueur.
            date_of_birth (str) : Date de naissance du joueur.
            gender (str) : Sexe du joueur.
            rating (int) : Classement ELO du joueur.
            id_num (int, facultatif) : L'identifiant du joueur. La valeur par défaut est 0.
            is_deleted (bool, facultatif) : Le joueur est-il supprimé ? La valeur par défaut est False.
            no_db_save (bool, optional) : Si l'objet doit seulement être sauvegardé en mémoire,
             et non dans la base de données. La valeur par défaut est False.

        Retourne :
            int : L'identifiant du joueur créé.
        """

        if id_num == 0:
            id_num = self.found_next_id(self.players_table)

        player = Player(first_name.capitalize(), last_name.capitalize(), date_of_birth, gender.upper(), rating, id_num, is_deleted)

        self.save_player(player=player, no_db_save=no_db_save)

        return id_num

    def save_player(self, player: Player, no_db_save: bool = False):
        """Sauvegarde un objet Player dans TinyDB.

        Arguments :
            joueur (Player) : Objet Player à sauvegarder.
            no_db_save (bool, optionnel) : Si l'objet doit seulement être sauvegardé en mémoire,
             et non dans la base de données. La valeur par défaut est False.
        """

        self.database.players[player.id_number] = player

        if no_db_save:
            return

        query = Query()

        self.players_table.upsert(
            {
                "First Name": player.first_name,
                "Last Name": player.last_name,
                "DOB": player.date_of_birth,
                "Gender": player.gender,
                "Rating": int(player.rating),
                "id": int(player.id_number),
                "Is Deleted": player.delete_player,
            },
            query.id == int(player.id_number),
        )

    def delete_player(self, player: Player):
        """Supprimer un joueur en mettant un drapeau.
         L'utilisateur doit persister dans la base de données pour l'historique du tournoi.

        Arguments :
            joueur (Player) : Joueur à supprimer.
        """

        player.delete_player = True

        self.save_player(player=player)

    def load_tournaments(self):
        """Utilise la table TinyDB "Tournois" pour créer des objets Joueur."""

        for tournament in self.tournaments_table:
            self.create_tournament(
                name=tournament["Name"],
                place=tournament["Place"],
                date=tournament["Date"],
                number_of_rounds=tournament["Number of tours"],
                time_control=tournament["Time Control"],
                description=tournament["Description"],
                id_number=tournament["id"],
                is_finished=tournament["Is Finished"],
                players=tournament["Players"],
                rating_table=tournament["Rating Table"],
                no_db_save=True,
            )

    def create_tournament(
        self,
        name: str,
        place: str,
        date: str,
        number_of_rounds: int,
        time_control: str,
        description: str,
        players: list[int],
        rating_table: dict,
        id_number: int = 0,
        is_finished: bool = False,
        no_db_save: bool = False,
    ):
        """Crée un objet Tournoi et l'enregistre dans les attributs de la base de données.

        Arguments :
            name (str) : Nom du tournoi.
            place (str) : Lieu physique du tournoi.
            date (str) : Date du tournoi.
            number_of_rounds (int) : Nombre de tours à jouer.
            time_control (str) : Type de contrôle du temps choisi.
            description (str) : Description du tournoi.
            joueurs (liste [int]) : Ids des joueurs participants.
            rating_table (dict) : Table d'évaluation du tournoi.
            id_number (int, facultatif) : L'identifiant du tournoi. La valeur par défaut est 0.
            is_finished (bool, facultatif) : Le tournoi est-il terminé ? La valeur par défaut est False.
            no_db_save (bool, optional) : Si l'objet doit seulement être sauvegardé en mémoire,
             pas dans la base de données. La valeur par défaut est False.

        Retourne :
            int : L'id du tournoi créé.
        """

        if id_number == 0:
            id_number = self.found_next_id(self.tournaments_table)

        # Créer la liste requise d'objets Player à partir des identifiants des joueurs.
        player_objects = [self.database.players[player] for player in players]

        # Créer une rating_table vide si elle n'existe pas encore.
        if not rating_table:
            for player in players:
                rating_table[str(player)] = 0

        tournament = Tournament(
            name=name,
            place=place,
            date=date,
            number_of_rounds=number_of_rounds,
            time_control=time_control,
            description=description,
            id_number=id_number,
            is_round_ended=is_finished,
            players=player_objects,
            rating_table=rating_table,
        )

        self.save_tournament(tournament=tournament, no_db_save=no_db_save)

        return id_number

    def save_tournament(self, tournament: Tournament, no_db_save: bool = False):
        """Sauvegarde un objet Tournoi en mémoire et dans TinyDB.

        Arguments :
            tournament (Tournoi) : Objet Tournoi à sauvegarder.
            no_db_save (bool, facultatif) : Si l'objet ne doit être sauvegardé qu'en mémoire,
             pas dans la db. La valeur par défaut est False.
        """

        self.database.tournaments[tournament.id_number] = tournament

        if no_db_save:
            return

        query = Query()

        players_id = [player.id_number for player in tournament.players]

        self.tournaments_table.upsert(
            {
                "Name": tournament.name,
                "Place": tournament.place,
                "Date": tournament.date,
                "Number of tours": int(tournament.number_of_tours),
                "Time Control": tournament.time_control,
                "Description": tournament.description,
                "Players": players_id,
                "Rating Table": tournament.rating_table,
                "Is Finished": tournament.is_round_ended,
                "id": int(tournament.id_number),
            },
            query.id == int(tournament.id_number),
        )

    def delete_tournament(self, tournament: Tournament):
        """Supprime un tournoi dans la base de données.

        Args :
            tournament (Tournoi) : Tournoi à supprimer
        """

        self.load_rounds(tournament_id=tournament.id_number)
        self.load_matches(tournament_id=tournament.id_number)

        for round_ in tournament.tours:
            self.delete_round(round_=tournament.tours[round_])

        query = Query()
        self.tournaments_table.remove(query.id == int(tournament.id_number))

        del self.database.tournaments[int(tournament.id_number)]

    def load_rounds(self, tournament_id: int):
        """Utilise la table TinyDB "Rounds" pour créer des objets Round pour un tournoi particulier.

        Arguments :
            tournament_id (int) : Tournoi à prendre en compte.
        """

        for round_ in self.rounds_table:
            if round_["Tournament id"] != tournament_id:
                continue

            self.create_round(
                number_of_round=round_["Number of tours"],
                tournament_id=round_["Tournament id"],
                id_num=round_["id"],
                no_db_save=True,
            )

    def create_round(self, number_of_round: int, tournament_id: int, id_num: int = 0, no_db_save: bool = False):
        """Crée un objet rond et l'enregistre dans les attributs de la base de données.

        Arguments :
            nombre_de_rondes (int) : Nombre ordonné de tours.
            Tournament_id (int) : L'id du tournoi de la ronde.
            id_num (int, optionnel) : ID du tour. La valeur par défaut est 0.
            no_db_save (bool, optional) : Si l'objet doit seulement être sauvegardé en mémoire
            , et non dans la base de données. La valeur par défaut est False.

        Retourne :
            int : Id du tour créé.
        """

        if id_num == 0:
            id_num = self.found_next_id(self.rounds_table)

        created_round = Round(number_of_round=number_of_round, tournament_id=tournament_id, id_number=id_num)

        self.save_round(round_=created_round, no_db_save=no_db_save)

        return id_num

    def save_round(self, round_: Round, no_db_save: bool = False):
        """Sauvegarde un objet Round en mémoire et dans TinyDB.

               Arguments :
                   round_ (Round) : Objet Round à sauvegarder.
                Le soulignement est ajouté à cause du mot-clé réservé.
                   no_db_save (bool, optionnel) : Si l'objet doit seulement être sauvegardé en mémoire,
                    et non dans la base de données. La valeur par défaut est False.
               """

        self.database.tournaments[round_.tournament_id].tours[round_.id_number] = round_

        if no_db_save:
            return

        query = Query()

        self.rounds_table.upsert(
            {
                "Number of tours": round_.number_of_round,
                "Tournament id": int(round_.tournament_id),
                "id": int(round_.id_number),
            },
            query.id == int(round_.id_number),
        )

    def delete_round(self, round_: Round):
        """Supprime une ronde dans la base de données.

        Arguments :
            round_ (Round) : Rond à supprimer.
        """

        for match in round_.matches:
            self.delete_match(match=round_.matches[match])

        query = Query()
        self.rounds_table.remove(query.id == int(round_.id_number))

    def load_matches(self, tournament_id: int):
        """Utilise la table TinyDB "Matches" pour créer des objets Match pour un tournoi particulier.

        Arguments :
            tournament_id (int) : Tournoi à prendre en compte.
        """

        for match in self.matches_table:
            if match["Tournament id"] != tournament_id:
                continue

            player_1 = self.database.players[match["Player 1"]]
            player_2 = self.database.players[match["Player 2"]]

            players = (player_1, player_2)

            self.create_match(
                players=players,
                tournament_id=match["Tournament id"],
                round_id=match["Round id"],
                winner=match["Winner"],
                id_num=match["id"],
                no_db_save=True,
            )

    def create_match(
        self, players: tuple, tournament_id: int, round_id: int, winner: int, id_num: int = 0, no_db_save: bool = False
    ):
        """Crée un objet Match et l'enregistre dans les attributs de la base de données.

        Arguments :
            joueurs (tuple) : Tuple des deux joueurs en face.
            tournament_id (int) : L'identifiant du tournoi du Match.
            round_id (int) : L'identifiant du tour du match.

            winner (int) : Le joueur_gagnant du match. Soit 1 (premier joueur),
            2 (deuxième joueur) ou 0 (match nul).
            id_num (int, facultatif) : L'identifiant du match. La valeur par défaut est 0.
            no_db_save (bool, optional) : Si l'objet doit être sauvegardé uniquement en mémoire,
             et non dans la base de données. La valeur par défaut est False.
        """

        if id_num == 0:
            id_num = self.found_next_id(self.matches_table)

        match = Match(
            players=players,
            tournament_id=tournament_id,
            round_id=round_id,
            player_winner=winner,
            id_number=id_num,
        )

        self.save_match(match=match, no_db_save=no_db_save)

    def save_match(self, match: Match, no_db_save: bool = False):
        """Sauvegarde un objet Match en mémoire et dans TinyDB.

        Arguments :
            match (Match) : Objet Match à sauvegarder.
            no_db_save (bool, optional) : Si l'objet ne doit être sauvegardé qu'en mémoire,
             pas dans la db. La valeur par défaut est False.
        """

        self.database.tournaments[match.tournament_id].tours[match.round_id].matches[match.id_number] = match

        if no_db_save:
            return

        query = Query()

        self.matches_table.upsert(
            {
                "Player 1": match.player_1.id_number,
                "Player 2": match.player_2.id_number,
                "Winner": match.winner,
                "Tournament id": int(match.tournament_id),
                "Round id": int(match.round_id),
                "id": int(match.id_number),
            },
            query.id == int(match.id_number),
        )

    def delete_match(self, match: Match):
        """Supprime une correspondance dans la base de données.

        Arguments :
            match (Match) : Correspondance à supprimer.
        """

        query = Query()
        self.matches_table.remove(query.id == int(match.id_number))

    @staticmethod
    def found_next_id(table: table.Table):
        """Recherche dans une table TinyDB le prochain plus grand numéro d'identification.
        Arguments :
            table (table.Table) : Table TinyDB dans laquelle effectuer la recherche.
        Retourne :
            int : Le prochain plus grand identifiant à utiliser.
        """

        if len(table) == 0:
            return 1

        query = Query()

        biggest = 1

        while len(table.search(query.id >= biggest)) > 0:
            biggest += 1

        return biggest

    def update_rating_table(self, tournament_id: int, player_id: int, points_earned: float):
        """Met à jour la table d'évaluation d'un tournoi en ajoutant des points à un joueur.
        Arguments :
            tournament_id (int) : L'identifiant du tournoi.
            Player_id (int) : L'identifiant du joueur.
            Points_earned (float) : Points gagnés par le joueur.
        """

        tournament = self.database.tournaments[tournament_id]
        tournament.rating_table[str(player_id)] += points_earned
        self.save_tournament(tournament=tournament)

    def find_unfinished_tournaments(self):
        """Recherche dans la table des tournois un tournoi non terminé.
        Retourne :
            liste[table.Document] : Les tournois non terminés.
        """

        query = Query()

        return self.tournaments_table.search(query["Is Finished"] is False)
