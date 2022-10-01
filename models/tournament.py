"""Classe Tournament"""


class Tournament:

    def __init__(self, name: str, place: str,
                 date: str, numbers_of_tours: int,
                 time_control: str, description: str,
                 id_number: int, round_ended: bool,
                 players: list, rating_table: dict):

        self.name = name
        self.place = place
        self.date = date
        self.numbers_of_tours = numbers_of_tours
        self.players = players
        self.time_control = time_control
        self.description = description
        self.id_number = id_number
        self.round_ended = round_ended
        self.rating_table = rating_table

        self.tours = {}

    def __str__(self):
        stdout_content = " - Tournament name: {name}\n".format(name=self.name)
        stdout_content += "   - Round_ended ?: {round_ended}\n".format(round_ended=self.round_ended)
        stdout_content += "   - Place: {place}\n".format(place=self.place)
        stdout_content += "   - Date: {date}\n".format(date=self.date)
        stdout_content += "   - Numbers of tours: {number}\n".format(number=self.numbers_of_tours)
        stdout_content += "   - Time Control: {time}\n".format(time=self.time_control)
        stdout_content += "   - Description: {description}\n".format(description=self.description)
        stdout_content += "   - Players: {players}\n".format(players=self.players)
        stdout_content += "   - Rating_table: {rating_table}\n".format(rating_table=self.rating_table)

        stdout_content += " - - Started rounds - -\n"

        for started_round in self.tours:
            stdout_content += started_round.__str__()

        return stdout_content
