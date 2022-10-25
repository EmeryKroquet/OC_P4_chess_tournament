"""Classe Tournament"""


class Tournament:

    def __init__(self, name: str, place: str,
                 date: str, numbers_of_tours: int,
                 time_control: str, description: str,
                 id_number: int, is_round_ended: bool,
                 players: list, rating_table: dict):
        self.name = name
        self.place = place
        self.date = date
        self.numbers_of_tours = numbers_of_tours
        self.players = players
        self.time_control = time_control
        self.description = description
        self.id_number = id_number
        self.is_round_ended = is_round_ended
        self.rating_table = rating_table

        self.tours = {}

    def __str__(self):
        show_info = (f" - Tournament name: {self.name}\n"
                     f"   - Round is ended ?: {self.is_round_ended}\n"
                     f"   - Place: {self.place}\n"
                     f"   - Date: {self.date}\n"
                     f"   - Numbers of tours: {self.numbers_of_tours}\n"
                     f"   - Time Control: {self.time_control}\n"
                     f"   - Description: {self.description}\n"
                     f"   - Players: {self.players}\n"
                     f"   - Rating_table: {self.rating_table}\n"

                     f" - - Started rounds - -\n")

        for started_round in self.tours:
            show_info += started_round.__str__()

        return show_info
