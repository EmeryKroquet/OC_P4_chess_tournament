class Match:

    def __init__(self, players: tuple, tournament_id: int,
                 round_id: int, player_winner: int,
                 id_number: int):
        self.tournament_id = tournament_id
        self.round_id = round_id
        self.player_winner = player_winner
        self.id_number = id_number

        self.player_1 = players[0]
        self.player_2 = players[1]

    def __str__(self):
        show_info = (f"First Name: {self.player_1.first_name}",
                     f"Last Name: {self.player_1.last_name}",
                     f"Rating: {self.player_1.rating_1} vs"
                     f"First Name2 : {self.player_2.first_name}",
                     f"Last Name2 : {self.player_2.last_name}",
                     f"Rating 2: {self.player_2.rating_2}",
                     f"Winner : {self.player_winner}\n"
                     f"id : {self.id_number}\n"

                     )
        return show_info
