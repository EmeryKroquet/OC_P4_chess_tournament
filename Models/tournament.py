class Tournament:
    """Model for tournament. All tournaments have tours associated with them,
    these tours have matches associated with them.

    Attributes:
        name (str): Tournament's name.
        place (str): Tournament's physical place.
        date (str): Tournament's date.
        number_of_tours (int): Number of tours to be played.
        time_control (str): Type of time control chosen.
        description (str): Tournament's description.
        id_number (int): Tournament's unique id.
        is_round_ended (bool): Is the tournament finished ?
        players (list[Player]): List of participating players.
        rating_table (dict): Tournament's rating_table.
        tours (dict): All tours associated with this tournament.
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
        """Constructor for Tournament.

        Args:
            name (str): Tournament's name.
            place (str): Tournament's physical place.
            date (str): Tournament's date.
            number_of_rounds (int): Number of tours to be played.
            time_control (str): Type of time control chosen.
            description (str): Tournament's description.
            id_number (int): Tournament's unique id.
            is_round_ended (bool): Is the tournament finished ?
            players (list[Player]): List of participating players.
            rating_table (dict): Tournament's rating_table.
        """

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
        show_info = " - Tournament name: {name}\n".format(name=self.name)
        show_info += "   - Is finished ?: {is_round_ended}\n".format(is_round_ended=self.is_round_ended)
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
