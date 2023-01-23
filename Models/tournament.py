class Tournament:
    """Modèle pour le tournoi. Tous les tournois ont des tournées qui leur sont associées,
    ces tournées sont associées à des matchs.

    Attributs :
        name (str) : Nom du tournoi.
        place (str) : Lieu physique du tournoi.
        date (str) : Date du tournoi.
        number_of_tours (int) : Nombre de tours à jouer.
        time_control (str) : Type de contrôle du temps choisi.
        description (str) : Description du tournoi.
        id_number (int) : L'identifiant unique du tournoi.
        is_round_ended (bool) : Le tournoi est-il terminé ?
        players (list [Player]) : Liste des joueurs participants.
        rating_table (dict) : Table de classement du tournoi.
        tours (dict) : Tous les tours associés à ce tournoi.
    """

    def __init__(
            self,
            name: str,
            place: str,
            date: str,
            number_of_rounds: int,
            time_control: str,
            description: str,
            id_number: int,
            is_round_ended: bool,
            players: list,
            rating_table: dict,
    ):
        """Constructeur de Tournament."""
        self.name = name
        self.place = place
        self.date = date
        self.number_of_tours = number_of_rounds
        self.time_control = time_control
        self.description = description
        self.id_number = id_number
        self.is_round_ended = is_round_ended
        self.players = players
        self.rating_table = rating_table

        self.tours = {}

    def __str__(self):
        show_info = " - Tournament name: {name}\n".format(name=self.name) + \
                    "   - Is finished ?: {is_round_ended}\n".format(is_round_ended=self.is_round_ended)

        show_info += "   - Place: {place}\n".format(place=self.place)
        show_info += "   - Date: {date}\n".format(date=self.date)
        show_info += "   - Number of tours: {num}\n".format(num=self.number_of_tours)
        show_info += "   - Time Control: {time}\n".format(time=self.time_control)
        show_info += "   - Description: {description}\n".format(description=self.description)
        show_info += "   - Players: {players}\n".format(players=self.players)
        show_info += "   - Rating Table: {rating_table}\n".format(rating_table=self.rating_table)

        show_info += " - - Started tours - -\n"

        for started_round in self.tours:
            show_info += started_round.__str__()

        return show_info

    def __repr__(self):
        show_info = " - Tournament name: {name}\n".format(name=self.name) + \
                    "   - Is finished ?: {is_round_ended}\n".format(is_round_ended=self.is_round_ended)

        show_info += "   - Place: {place}\n".format(place=self.place)
        show_info += "   - Date: {date}\n".format(date=self.date)
        show_info += "   - Number of tours: {num}\n".format(num=self.number_of_tours)
        show_info += "   - Time Control: {time}\n".format(time=self.time_control)
        show_info += "   - Description: {description}\n".format(description=self.description)
        show_info += "   - Players: {players}\n".format(players=self.players)
        show_info += "   - Rating Table: {rating_table}\n".format(rating_table=self.rating_table)

        show_info += " - - Started tours - -\n"

        for started_round in self.tours:
            show_info += started_round.__str__()
        return show_info
